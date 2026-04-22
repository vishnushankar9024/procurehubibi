import { describe, expect, it } from "vitest";

import { VendorComparisonService } from "../src/services/vendorComparisonService";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("VendorComparisonService", () => {
  it("compares vendors and generates ranking", async () => {
    const repository = new InMemoryRepository();
    const service = new VendorComparisonService(repository);

    repository.vendorScores.set("score-1", {
      _id: "score-1",
      projectId: "project-1",
      vendorId: "vendor-a",
      evaluationId: "eval-1",
      scoringMatrixId: "matrix-1",
      scoredParameters: [
        {
          key: "experience",
          label: "Experience",
          rawScore: 4,
          maxScore: 5,
          weight: 60,
          weightedScore: 48,
          passedThreshold: true,
          mandatoryPassed: true,
          rationale: "Good",
        },
      ],
      totalWeightedScore: 48,
      maxWeightedScore: 60,
      percentage: 80,
      qualificationStatus: "qualified",
      qualificationReason: "Pass",
      deterministic: true,
      scoredAt: new Date().toISOString(),
      explainability: {
        matrixId: "matrix-1",
        evaluationId: "eval-1",
        logs: [],
      },
    });

    repository.vendorScores.set("score-2", {
      _id: "score-2",
      projectId: "project-1",
      vendorId: "vendor-b",
      evaluationId: "eval-2",
      scoringMatrixId: "matrix-1",
      scoredParameters: [
        {
          key: "experience",
          label: "Experience",
          rawScore: 2,
          maxScore: 5,
          weight: 60,
          weightedScore: 24,
          passedThreshold: false,
          mandatoryPassed: false,
          rationale: "Weak",
        },
      ],
      totalWeightedScore: 24,
      maxWeightedScore: 60,
      percentage: 40,
      qualificationStatus: "disqualified",
      qualificationReason: "Fail",
      deterministic: true,
      scoredAt: new Date().toISOString(),
      explainability: {
        matrixId: "matrix-1",
        evaluationId: "eval-2",
        logs: [],
      },
    });

    const comparison = await service.compareVendors({
      projectId: "project-1",
      vendorScoreIds: ["score-1", "score-2"],
    });

    expect(comparison.ranking[0].vendorId).toBe("vendor-a");
    expect(comparison.comparisonMatrix[1].weaknesses.length).toBe(1);
  });
});
