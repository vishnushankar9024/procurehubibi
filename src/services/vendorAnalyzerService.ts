import { randomUUID } from "node:crypto";

import type { AiProvider } from "../lib/ai/aiProvider";
import { ValidationError } from "../lib/errors";
import type { ProcurementRepository } from "../lib/db/repository";
import type {
  AnalyzedParameter,
  DocumentChunk,
  PrequalificationTemplate,
  RiskSignal,
  VendorAnalyzeInput,
  VendorEvaluation,
} from "../types";

type VendorExtractOutput = {
  fields?: Array<{
    key?: string;
    label?: string;
    category?: "qualitative" | "quantitative";
    value?: string | number | boolean | "Not Provided";
    normalizedScoreHint?: number;
    confidence?: number;
    compliance?: "Compliant" | "Non-Compliant" | "Not Provided";
    notes?: string[];
  }>;
  missingInformation?: string[];
  riskSignals?: Array<{
    type?: string;
    detail?: string;
    confidence?: number;
  }>;
  confidenceScore?: number;
  logs?: string[];
};

function chunkDocuments(
  documents: VendorAnalyzeInput["documents"],
  chunkSize: number,
): DocumentChunk[] {
  const chunks: DocumentChunk[] = [];

  for (const document of documents) {
    const content = document.content.trim();
    if (!content) {
      continue;
    }

    let start = 0;
    let index = 0;
    while (start < content.length) {
      const end = Math.min(start + chunkSize, content.length);
      chunks.push({
        chunkId: `${document.fileName}-chunk-${index + 1}`,
        sourceDocument: document.fileName,
        text: content.slice(start, end),
      });
      start = end;
      index += 1;
    }
  }

  return chunks;
}

function safeJsonParse(input: string): VendorExtractOutput {
  try {
    return JSON.parse(input) as VendorExtractOutput;
  } catch {
    return {};
  }
}

function toTemplateFieldMap(template: PrequalificationTemplate) {
  const allCriteria = [...template.qualitative, ...template.quantitative];
  return new Map(allCriteria.map((criterion) => [criterion.key, criterion]));
}

export class VendorAnalyzerService {
  constructor(
    private readonly repository: ProcurementRepository,
    private readonly aiProvider: AiProvider,
    private readonly chunkSize: number,
  ) {}

  async analyzeVendorSubmission(input: VendorAnalyzeInput): Promise<VendorEvaluation> {
    if (input.documents.length === 0) {
      throw new ValidationError("At least one vendor document is required.");
    }

    const template = await this.repository.getTemplateById(input.templateId);
    if (!template || template.projectId !== input.projectId) {
      throw new ValidationError("Template not found for project.");
    }

    const chunks = chunkDocuments(input.documents, this.chunkSize);
    if (chunks.length === 0) {
      throw new ValidationError("Submitted vendor documents contain no readable text.");
    }

    const templateFields = toTemplateFieldMap(template);
    const parameterMap = new Map<string, AnalyzedParameter>();
    const missingInformation = new Set<string>();
    const riskSignals: RiskSignal[] = [];
    const confidenceValues: number[] = [];
    const logs: string[] = [];

    for (const chunk of chunks) {
      const prompt = [
        "Extract vendor submission data against the prequalification template.",
        "Rules:",
        "- Never hallucinate data.",
        '- If data is missing, set value to "Not Provided".',
        "- Return strict JSON with keys: fields[], missingInformation[], riskSignals[], confidenceScore, logs[].",
        `TEMPLATE: ${JSON.stringify(template)}`,
        `STRUCTURED_INPUT: ${JSON.stringify(input.structuredInput)}`,
        `DOCUMENT_CHUNK: ${chunk.text}`,
      ].join("\n");

      const aiResult = await this.aiProvider.generate({
        task: "vendor_extract",
        messages: [
          {
            role: "system",
            content:
              "You are a procurement analyst assistant. Use only available evidence and explicitly mark missing data.",
          },
          { role: "user", content: prompt },
        ],
        responseSchemaHint:
          "JSON with fields[], missingInformation[], riskSignals[], confidenceScore, logs[]",
      });

      const extracted = safeJsonParse(aiResult.content);

      for (const rawField of extracted.fields ?? []) {
        if (!rawField.key || !templateFields.has(rawField.key)) {
          continue;
        }

        const templateCriterion = templateFields.get(rawField.key)!;
        const confidence = Math.max(0, Math.min(1, Number(rawField.confidence ?? aiResult.confidence)));
        const normalizedScoreHint = Math.max(
          0,
          Math.min(5, Number(rawField.normalizedScoreHint ?? 0)),
        );
        const value =
          rawField.value === undefined || rawField.value === null ? "Not Provided" : rawField.value;

        const parameter: AnalyzedParameter = {
          key: templateCriterion.key,
          label: templateCriterion.label,
          category:
            rawField.category ??
            (template.quantitative.some((criterion) => criterion.key === templateCriterion.key)
              ? "quantitative"
              : "qualitative"),
          value,
          normalizedScoreHint,
          confidence,
          evidence: [
            {
              chunkId: chunk.chunkId,
              sourceDocument: chunk.sourceDocument,
            },
          ],
          compliance:
            rawField.compliance ??
            (value === "Not Provided" ? "Not Provided" : "Compliant"),
          notes: rawField.notes ?? [],
        };

        const existing = parameterMap.get(parameter.key);
        if (!existing || existing.value === "Not Provided") {
          parameterMap.set(parameter.key, parameter);
        } else {
          existing.evidence.push(...parameter.evidence);
          existing.notes.push(...parameter.notes);
        }

        confidenceValues.push(confidence);
      }

      for (const missing of extracted.missingInformation ?? []) {
        missingInformation.add(missing);
      }

      for (const risk of extracted.riskSignals ?? []) {
        if (!risk.type || !risk.detail) {
          continue;
        }
        riskSignals.push({
          type: risk.type,
          detail: risk.detail,
          confidence: Math.max(0, Math.min(1, Number(risk.confidence ?? aiResult.confidence))),
        });
      }

      logs.push(
        ...aiResult.traces,
        ...(extracted.logs ?? []),
        `chunk-processed:${chunk.chunkId}`,
      );
    }

    for (const criterion of templateFields.values()) {
      if (!parameterMap.has(criterion.key)) {
        parameterMap.set(criterion.key, {
          key: criterion.key,
          label: criterion.label,
          category: template.quantitative.some((item) => item.key === criterion.key)
            ? "quantitative"
            : "qualitative",
          value: "Not Provided",
          normalizedScoreHint: 0,
          confidence: 0,
          evidence: [],
          compliance: "Not Provided",
          notes: ["No evidence found in submitted documents."],
        });
        missingInformation.add(criterion.key);
      }
    }

    const parameters = [...parameterMap.values()];
    const confidenceScore =
      confidenceValues.length > 0
        ? Number(
            (
              confidenceValues.reduce((sum, value) => sum + value, 0) /
              confidenceValues.length
            ).toFixed(3),
          )
        : 0;

    const nonCompliantCount = parameters.filter(
      (parameter) => parameter.compliance === "Non-Compliant",
    ).length;
    const missingCount = parameters.filter(
      (parameter) => parameter.compliance === "Not Provided",
    ).length;

    const complianceStatus: VendorEvaluation["complianceStatus"] =
      missingCount === 0 && nonCompliantCount === 0
        ? "compliant"
        : nonCompliantCount > 0
          ? "non_compliant"
          : "partial";

    const evaluation: VendorEvaluation = {
      _id: randomUUID(),
      projectId: input.projectId,
      vendorId: input.vendorId,
      templateId: input.templateId,
      complianceStatus,
      missingInformation: [...missingInformation],
      parameters,
      riskSignals,
      confidenceScore,
      explainability: {
        model: this.aiProvider.name,
        chunkCount: chunks.length,
        evaluatedAt: new Date().toISOString(),
        logs,
      },
    };

    await this.repository.saveVendorEvaluation(evaluation);
    return evaluation;
  }
}
