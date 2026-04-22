import { describe, expect, it } from "vitest";

import { VendorScoringService } from "../src/services/vendorScoringService";
import type { ScoringMatrix, VendorEvaluation } from "../src/types";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("VendorScoringService", () => {
  it("scores vendor deterministically and marks disqualified on mandatory failure", async () => {
    const repository = new InMemoryRepository();
    const matrix: ScoringMatrix = {
      _id: "score-1",
      projectId: "project-1",
      templateId: "template-1",
      criteria: [
        {
          key: "experience_years",
          label: "Experience",
          category: "qualitative",
          weight: 40,
          method: "scaled",
          maxScore: 5,
          threshold: 3,
          mandatory: true,
        },
      ],
      totalWeight: 40,
      globalThresholdPercent: 60,
      deterministic: true,
      createdAt: new Date().toISOString(),
    };
    await repository.saveScoringMatrix(matrix);

    const evaluation: VendorEvaluation = {
      _id: "eval-1",
      projectId: "project-1",
      vendorId: "vendor-1",
      templateId: "template-1",
      complianceStatus: "partial",
      missingInformation: [],
      parameters: [
        {
          key: "experience_years",
          label: "Experience",
          category: "qualitative",
          value: "2 years",
          normalizedScoreHint: 2,
          confidence: 0.8,
          evidence: [],
          compliance: "Compliant",
          notes: ["Short experience profile."],
        },
      ],
      riskSignals: [],
      confidenceScore: 0.8,
      explainability: {
        model: "mock",
        chunkCount: 1,
        evaluatedAt: new Date().toISOString(),
        logs: [],
      },
    };
    await repository.saveVendorEvaluation(evaluation);

    const service = new VendorScoringService(repository);
    const score = await service.scoreVendor({
      projectId: "project-1",
      vendorId: "vendor-1",
      scoringMatrixId: "score-1",
      vendorEvaluationId: "eval-1",
    });

    expect(score.qualificationStatus).toBe("disqualified");
    expect(score.totalWeightedScore).toBeLessThan(score.maxWeightedScore);
    expect(score.explainability.logs.length).toBeGreaterThan(0);
  });
});
