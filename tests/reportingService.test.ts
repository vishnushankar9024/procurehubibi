import { describe, expect, it } from "vitest";

import { MockProvider } from "../src/lib/ai/mockProvider";
import { ReportingService } from "../src/services/reportingService";
import type { VendorComparison, VendorEvaluation, VendorScore } from "../src/types";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("ReportingService", () => {
  it("generates a JSON + HTML report from stored evaluation artifacts", async () => {
    const repository = new InMemoryRepository();
    const aiProvider = new MockProvider();
    const service = new ReportingService(repository, aiProvider);

    const evaluation: VendorEvaluation = {
      _id: "eval-1",
      projectId: "project-1",
      vendorId: "vendor-a",
      templateId: "template-1",
      complianceStatus: "compliant",
      missingInformation: [],
      parameters: [],
      riskSignals: [],
      confidenceScore: 0.9,
      explainability: {
        model: "mock",
        chunkCount: 1,
        evaluatedAt: new Date().toISOString(),
        logs: [],
      },
    };
    await repository.saveVendorEvaluation(evaluation);

    const score: VendorScore = {
      _id: "score-1",
      projectId: "project-1",
      vendorId: "vendor-a",
      evaluationId: "eval-1",
      scoringMatrixId: "matrix-1",
      scoredParameters: [],
      totalWeightedScore: 80,
      maxWeightedScore: 100,
      percentage: 80,
      qualificationStatus: "qualified",
      qualificationReason: "All checks passed",
      deterministic: true,
      scoredAt: new Date().toISOString(),
      explainability: {
        matrixId: "matrix-1",
        evaluationId: "eval-1",
        logs: [],
      },
    };
    await repository.saveVendorScore(score);

    const comparison: VendorComparison = {
      _id: "cmp-1",
      projectId: "project-1",
      ranking: [
        {
          vendorId: "vendor-a",
          rank: 1,
          scoreId: "score-1",
          percentage: 80,
          qualificationStatus: "qualified",
        },
      ],
      comparisonMatrix: [
        {
          vendorId: "vendor-a",
          scoreId: "score-1",
          percentage: 80,
          strengths: ["Strong history"],
          weaknesses: [],
          complianceSummary: "All compliant",
        },
      ],
      generatedAt: new Date().toISOString(),
    };
    await repository.saveVendorComparison(comparison);

    const report = await service.generateProjectReport("project-1");
    expect(report.projectId).toBe("project-1");
    expect(report.json.vendorScores).toHaveLength(1);
    expect(report.html).toContain("Procurement Report");
  });
});
