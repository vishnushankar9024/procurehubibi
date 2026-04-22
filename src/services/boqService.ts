import { randomUUID } from "node:crypto";

import type { AiProvider } from "../lib/ai/aiProvider";
import { ValidationError } from "../lib/errors";
import type { ProcurementRepository } from "../lib/db/repository";
import type { BoqItem, BoqRecord, DocumentChunk } from "../types";

type BoqUploadInput = {
  projectId: string;
  fileName: string;
  mimeType: string;
  content: string;
};

type RawBoqParseOutput = {
  items?: Array<{
    itemCode?: string;
    description?: string;
    unit?: string;
    quantity?: number | string;
    rate?: number | string;
    confidence?: number;
  }>;
  missingFields?: Array<{
    rowRef?: string;
    missing?: Array<"description" | "unit" | "quantity">;
  }>;
};

function chunkText(sourceDocument: string, text: string, chunkSize: number): DocumentChunk[] {
  if (!text.trim()) {
    return [];
  }

  const chunks: DocumentChunk[] = [];
  let start = 0;
  let index = 0;
  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length);
    chunks.push({
      chunkId: `${sourceDocument}-chunk-${index + 1}`,
      sourceDocument,
      text: text.slice(start, end),
    });
    start = end;
    index += 1;
  }
  return chunks;
}

function safeJsonParse(value: string): RawBoqParseOutput {
  try {
    const parsed = JSON.parse(value) as RawBoqParseOutput;
    return parsed;
  } catch {
    return {};
  }
}

export class BoqService {
  constructor(
    private readonly repository: ProcurementRepository,
    private readonly aiProvider: AiProvider,
    private readonly chunkSize: number,
  ) {}

  async uploadBoq(input: BoqUploadInput): Promise<BoqRecord> {
    const chunks = chunkText(input.fileName, input.content, this.chunkSize);
    if (chunks.length === 0) {
      throw new ValidationError("BOQ document content is empty.");
    }

    const chunkItems: BoqItem[] = [];
    const missingFields: BoqRecord["missingFields"] = [];
    const traces: string[] = [];

    for (const chunk of chunks) {
      const prompt = [
        "Extract BOQ items from the text and normalize to POMI fields.",
        "Return strict JSON with keys: items[], missingFields[].",
        "Each item supports: itemCode?, description, unit, quantity, rate?, confidence.",
        "For missing data do not guess. Keep missing entries in missingFields list.",
        `TEXT:\n${chunk.text}`,
      ].join("\n");

      const aiResult = await this.aiProvider.generate({
        task: "boq_parse",
        messages: [
          {
            role: "system",
            content:
              "You are a construction procurement parser. Never hallucinate unavailable values.",
          },
          { role: "user", content: prompt },
        ],
        responseSchemaHint: "JSON with { items: [], missingFields: [] }",
      });

      traces.push(...aiResult.traces);

      const parsed = safeJsonParse(aiResult.content);
      const normalizedItems = this.normalizeItems(parsed.items ?? [], chunk.chunkId);
      chunkItems.push(...normalizedItems);

      for (const missing of parsed.missingFields ?? []) {
        missingFields.push({
          rowRef: missing.rowRef ?? chunk.chunkId,
          missing: missing.missing ?? [],
        });
      }
    }

    if (chunkItems.length === 0) {
      throw new ValidationError("No BOQ items could be extracted from the uploaded content.");
    }

    const record: BoqRecord = {
      _id: randomUUID(),
      projectId: input.projectId,
      standard: "POMI",
      fileName: input.fileName,
      mimeType: input.mimeType,
      items: chunkItems,
      missingFields,
      trace: {
        model: this.aiProvider.name,
        extractedAt: new Date().toISOString(),
        chunkCount: chunks.length,
      },
    };

    await this.repository.saveBoq(record);
    return record;
  }

  private normalizeItems(rawItems: RawBoqParseOutput["items"], sourceChunkId: string): BoqItem[] {
    const normalized: BoqItem[] = [];
    for (const rawItem of rawItems ?? []) {
      const description = (rawItem.description ?? "").trim();
      const unit = (rawItem.unit ?? "").trim();
      const quantity = Number(rawItem.quantity ?? 0);
      if (!description || !unit || Number.isNaN(quantity)) {
        continue;
      }

      const rate =
        rawItem.rate === undefined || rawItem.rate === null
          ? undefined
          : Number(rawItem.rate);

      normalized.push({
        itemCode: rawItem.itemCode,
        description,
        unit,
        quantity,
        rate: Number.isNaN(rate ?? NaN) ? undefined : rate,
        sourceChunkId,
        confidence: Math.max(0, Math.min(1, Number(rawItem.confidence ?? 0.5))),
      });
    }

    return normalized;
  }
}
