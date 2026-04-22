import type { AiGenerateInput, AiGenerateOutput, AiProvider } from "./aiProvider";

function defaultEvaluationPayload(): string {
  const payload = {
    fields: [
      {
        key: "experience_years",
        label: "Relevant Experience",
        category: "qualitative",
        value: "10 years in commercial projects",
        normalizedScoreHint: 4,
        confidence: 0.82,
        compliance: "Compliant",
        notes: ["Validated against project references."],
      },
      {
        key: "annual_turnover",
        label: "Annual Turnover",
        category: "quantitative",
        value: 12000000,
        normalizedScoreHint: 5,
        confidence: 0.91,
        compliance: "Compliant",
        notes: ["Audited financial statement found."],
      },
    ],
    missingInformation: [],
    riskSignals: [
      {
        type: "commercial_risk",
        detail: "No fixed-price clause evidence in the submitted draft contract.",
        confidence: 0.62,
      },
    ],
    confidenceScore: 0.865,
    logs: ["Mock extraction generated for development mode."],
  };

  return JSON.stringify(payload);
}

function defaultBoqPayload(): string {
  return JSON.stringify({
    items: [
      {
        itemCode: "POMI-01",
        description: "Excavation in foundation trenches",
        unit: "m3",
        quantity: 120.5,
        rate: 18.2,
        confidence: 0.89,
      },
      {
        itemCode: "POMI-02",
        description: "Reinforced concrete grade C25",
        unit: "m3",
        quantity: 65,
        rate: 140,
        confidence: 0.92,
      },
    ],
    missingFields: [],
  });
}

function defaultTemplatePayload(): string {
  return JSON.stringify({
    rationale:
      "Template emphasizes delivery capability, proven project history, and financial stability.",
    qualitative: [
      {
        key: "experience_years",
        label: "Relevant Experience",
        description: "Years of experience in similar construction procurements.",
        dataType: "text",
        mandatory: true,
      },
      {
        key: "technical_capability",
        label: "Technical Capability",
        description: "Breadth of technical teams and execution process maturity.",
        dataType: "text",
        mandatory: true,
      },
    ],
    quantitative: [
      {
        key: "annual_turnover",
        label: "Annual Turnover",
        description: "Average annual turnover over the last 3 years.",
        dataType: "number",
        mandatory: true,
        unit: "USD",
        minValue: 5000000,
      },
      {
        key: "resource_strength",
        label: "Resource Strength",
        description: "Number of skilled resources available for project deployment.",
        dataType: "number",
        mandatory: false,
        unit: "persons",
        minValue: 50,
      },
    ],
  });
}

export class MockProvider implements AiProvider {
  readonly name = "mock";

  async generate(input: AiGenerateInput): Promise<AiGenerateOutput> {
    const promptText = input.messages.map((message) => message.content).join("\n");

    let content = "{}";
    if (input.task === "boq_parse") {
      content = defaultBoqPayload();
    } else if (input.task === "template_suggest") {
      content = defaultTemplatePayload();
    } else if (input.task === "vendor_extract") {
      content = defaultEvaluationPayload();
    } else if (input.task === "report_summary") {
      content =
        "Top-ranked vendors meet mandatory criteria, while disqualified vendors fail threshold checks. Review commercial risk signals before final award.";
    } else if (promptText.includes("boq") || promptText.includes("POMI")) {
      content = defaultBoqPayload();
    } else if (promptText.includes("template")) {
      content = defaultTemplatePayload();
    } else if (promptText.includes("vendor")) {
      content = defaultEvaluationPayload();
    }

    const traces: string[] = [
      `mock-task:${input.task}`,
      `message-count:${input.messages.length}`,
      `schema-hint:${input.responseSchemaHint ?? "none"}`,
    ];
    return {
      content,
      confidence: 0.84,
      model: "mock-model-v1",
      traces,
    };
  }
}
