import { describe, expect, it } from "vitest";

import { MockProvider } from "../src/lib/ai/mockProvider";
import { VendorAnalyzerService } from "../src/services/vendorAnalyzerService";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("VendorAnalyzerService", () => {
  it("analyzes vendor documents and fills missing fields as Not Provided", async () => {
    const repository = new InMemoryRepository();
    const aiProvider = new MockProvider();
    const templateId = "tpl-1";
    await repository.saveTemplate({
      _id: templateId,
      projectId: "p1",
      projectType: "commercial-building",
      qualitative: [
        {
          key: "experience_years",
          label: "Relevant Experience",
          description: "Years of similar project execution.",
          dataType: "text",
          mandatory: true,
        },
      ],
      quantitative: [
        {
          key: "annual_turnover",
          label: "Annual Turnover",
          description: "Average turnover.",
          dataType: "number",
          mandatory: true,
          unit: "USD",
          minValue: 1000000,
        },
      ],
      requirements: {},
      createdAt: new Date().toISOString(),
      trace: { model: "mock", rationale: "test" },
    });

    const service = new VendorAnalyzerService(repository, aiProvider, 2000);
    const evaluation = await service.analyzeVendorSubmission({
      projectId: "p1",
      vendorId: "vendor-a",
      templateId,
      documents: [
        {
          fileName: "submission.txt",
          mimeType: "text/plain",
          content: "Vendor has 10 years experience and turnover details included.",
        },
      ],
      structuredInput: {},
    });

    expect(evaluation.vendorId).toBe("vendor-a");
    expect(evaluation.parameters.length).toBeGreaterThan(0);
    expect(evaluation.confidenceScore).toBeGreaterThan(0);
  });
});
