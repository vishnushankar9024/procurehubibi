import { randomUUID } from "node:crypto";

import type { AiProvider } from "../lib/ai/aiProvider";
import type { ProcurementRepository } from "../lib/db/repository";
import type { PrequalificationTemplate, TemplateCreateInput, TemplateCriterion } from "../types";

type TemplateSuggestionOutput = {
  rationale?: string;
  qualitative?: TemplateCriterion[];
  quantitative?: TemplateCriterion[];
};

function safeJsonParse(input: string): TemplateSuggestionOutput {
  try {
    return JSON.parse(input) as TemplateSuggestionOutput;
  } catch {
    return {};
  }
}

function fallbackTemplate(projectType: string): Pick<PrequalificationTemplate, "qualitative" | "quantitative"> {
  return {
    qualitative: [
      {
        key: "experience",
        label: "Relevant Experience",
        description: `Experience delivering ${projectType} projects.`,
        dataType: "text",
        mandatory: true,
      },
      {
        key: "technical_capability",
        label: "Technical Capability",
        description: "Depth of engineering and execution capabilities.",
        dataType: "text",
        mandatory: true,
      },
      {
        key: "certifications",
        label: "Certifications",
        description: "Quality and safety certifications relevant to project delivery.",
        dataType: "text",
        mandatory: false,
      },
    ],
    quantitative: [
      {
        key: "financial_turnover",
        label: "Financial Turnover",
        description: "Average annual turnover over the last 3 financial years.",
        dataType: "number",
        unit: "USD",
        minValue: 1,
        mandatory: true,
      },
      {
        key: "project_size_handled",
        label: "Project Size Handled",
        description: "Largest project value delivered in the last 5 years.",
        dataType: "number",
        unit: "USD",
        minValue: 1,
        mandatory: true,
      },
      {
        key: "resource_strength",
        label: "Resource Strength",
        description: "Available skilled workforce for this procurement package.",
        dataType: "number",
        unit: "persons",
        minValue: 1,
        mandatory: false,
      },
    ],
  };
}

export class TemplateService {
  constructor(
    private readonly repository: ProcurementRepository,
    private readonly aiProvider: AiProvider,
  ) {}

  async createTemplate(input: TemplateCreateInput): Promise<PrequalificationTemplate> {
    const prompt = [
      "Suggest a prequalification template for construction procurement.",
      "Output strict JSON with keys: rationale, qualitative[], quantitative[].",
      "Each criterion supports: key, label, description, dataType(text|number|boolean), mandatory, unit?, minValue?, maxValue?.",
      "Prioritize experience, past projects, technical capability, certifications, financial turnover, project size handled, resource strength.",
      `PROJECT TYPE: ${input.projectType}`,
      `PROJECT REQUIREMENTS: ${JSON.stringify(input.requirements)}`,
    ].join("\n");

    const aiResult = await this.aiProvider.generate({
      task: "template_suggest",
      messages: [
        {
          role: "system",
          content:
            "You are an assistant generating procurement template suggestions. Never include unsupported fields.",
        },
        { role: "user", content: prompt },
      ],
      responseSchemaHint: "JSON with rationale, qualitative[], quantitative[]",
    });

    const suggested = safeJsonParse(aiResult.content);
    const fallback = fallbackTemplate(input.projectType);

    const template: PrequalificationTemplate = {
      _id: randomUUID(),
      projectId: input.projectId,
      projectType: input.projectType,
      qualitative: (suggested.qualitative?.length ? suggested.qualitative : fallback.qualitative).map(
        (criterion) => ({ ...criterion, mandatory: Boolean(criterion.mandatory) }),
      ),
      quantitative: (suggested.quantitative?.length ? suggested.quantitative : fallback.quantitative).map(
        (criterion) => ({ ...criterion, mandatory: Boolean(criterion.mandatory) }),
      ),
      requirements: input.requirements,
      createdAt: new Date().toISOString(),
      trace: {
        model: aiResult.model,
        rationale:
          suggested.rationale ??
          "Template generated with default fallback criteria due to limited AI signal.",
      },
    };

    await this.repository.saveTemplate(template);
    return template;
  }
}
