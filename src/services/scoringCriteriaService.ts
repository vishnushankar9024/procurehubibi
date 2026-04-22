import { randomUUID } from "node:crypto";

import { ValidationError } from "../lib/errors";
import type { ProcurementRepository } from "../lib/db/repository";
import type { ScoringCreateInput, ScoringMatrix } from "../types";

function validateScoringInput(input: ScoringCreateInput): number {
  if (!input.criteria.length) {
    throw new ValidationError("At least one scoring criterion is required.");
  }

  const totalWeight = input.criteria.reduce((sum, criterion) => sum + criterion.weight, 0);
  if (totalWeight <= 0 || totalWeight > 100) {
    throw new ValidationError("Total criteria weight must be in range (0, 100].");
  }

  if (input.globalThresholdPercent < 0 || input.globalThresholdPercent > 100) {
    throw new ValidationError("Global threshold percent must be between 0 and 100.");
  }

  for (const criterion of input.criteria) {
    if (criterion.maxScore <= 0) {
      throw new ValidationError(`Criterion '${criterion.key}' must have maxScore > 0.`);
    }
    if (criterion.threshold < 0 || criterion.threshold > criterion.maxScore) {
      throw new ValidationError(
        `Criterion '${criterion.key}' threshold must be between 0 and maxScore.`,
      );
    }
  }

  return totalWeight;
}

export class ScoringCriteriaService {
  constructor(private readonly repository: ProcurementRepository) {}

  async createScoring(input: ScoringCreateInput): Promise<ScoringMatrix> {
    const totalWeight = validateScoringInput(input);

    const matrix: ScoringMatrix = {
      _id: randomUUID(),
      projectId: input.projectId,
      templateId: input.templateId,
      criteria: input.criteria.map((criterion) => ({
        ...criterion,
        mandatory: Boolean(criterion.mandatory),
      })),
      totalWeight,
      globalThresholdPercent: input.globalThresholdPercent,
      deterministic: true,
      createdAt: new Date().toISOString(),
    };

    await this.repository.saveScoringMatrix(matrix);
    return matrix;
  }
}
