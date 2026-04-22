import { describe, expect, it } from "vitest";

import { ScoringCriteriaService } from "../src/services/scoringCriteriaService";
import { ValidationError } from "../src/lib/errors";
import { InMemoryRepository } from "./helpers/inMemoryRepository";

describe("ScoringCriteriaService", () => {
  it("creates deterministic scoring matrix", async () => {
    const repository = new InMemoryRepository();
    const service = new ScoringCriteriaService(repository);

    const matrix = await service.createScoring({
      projectId: "project-1",
      templateId: "template-1",
      globalThresholdPercent: 65,
      criteria: [
        {
          key: "experience",
          label: "Experience",
          category: "qualitative",
          weight: 40,
          method: "scaled",
          maxScore: 5,
          threshold: 3,
          mandatory: true,
        },
        {
          key: "turnover",
          label: "Turnover",
          category: "quantitative",
          weight: 60,
          method: "scaled",
          maxScore: 5,
          threshold: 2,
          mandatory: false,
        },
      ],
    });

    expect(matrix.deterministic).toBe(true);
    expect(matrix.totalWeight).toBe(100);
  });

  it("rejects invalid threshold range", async () => {
    const repository = new InMemoryRepository();
    const service = new ScoringCriteriaService(repository);

    await expect(
      service.createScoring({
        projectId: "project-1",
        templateId: "template-1",
        globalThresholdPercent: 65,
        criteria: [
          {
            key: "experience",
            label: "Experience",
            category: "qualitative",
            weight: 100,
            method: "scaled",
            maxScore: 5,
            threshold: 9,
            mandatory: true,
          },
        ],
      }),
    ).rejects.toBeInstanceOf(ValidationError);
  });
});
