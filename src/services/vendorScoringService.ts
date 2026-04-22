import { randomUUID } from "node:crypto";

import { AppError } from "../lib/errors";
import type { ProcurementRepository } from "../lib/db/repository";
import type { ScoringCriterion, VendorScore, VendorScoreInput } from "../types";

function normalizeToCriterionScale(rawHint: number, criterion: ScoringCriterion): number {
  const boundedHint = Math.max(0, Math.min(5, rawHint));
  return (boundedHint / 5) * criterion.maxScore;
}

export class VendorScoringService {
  constructor(private readonly repository: ProcurementRepository) {}

  async scoreVendor(input: VendorScoreInput): Promise<VendorScore> {
    const [matrix, evaluation] = await Promise.all([
      this.repository.getScoringMatrixById(input.scoringMatrixId),
      this.repository.getVendorEvaluationById(input.vendorEvaluationId),
    ]);

    if (!matrix || matrix.projectId !== input.projectId) {
      throw new AppError("Scoring matrix not found for project.", 404);
    }

    if (!evaluation || evaluation.projectId !== input.projectId || evaluation.vendorId !== input.vendorId) {
      throw new AppError("Vendor evaluation not found for project/vendor.", 404);
    }

    const parametersByKey = new Map(evaluation.parameters.map((parameter) => [parameter.key, parameter]));
    let totalWeightedScore = 0;
    let maxWeightedScore = 0;
    let qualificationStatus: VendorScore["qualificationStatus"] = "qualified";
    let qualificationReason = "All mandatory and threshold checks passed.";
    const logs: string[] = [];

    const scoredParameters = matrix.criteria.map((criterion) => {
      const parameter = parametersByKey.get(criterion.key);
      const rawScore = parameter
        ? normalizeToCriterionScale(parameter.normalizedScoreHint, criterion)
        : 0;
      const boundedRawScore = Math.max(0, Math.min(criterion.maxScore, rawScore));

      const weightedScore = (boundedRawScore / criterion.maxScore) * criterion.weight;
      const criterionMaxWeighted = criterion.weight;
      totalWeightedScore += weightedScore;
      maxWeightedScore += criterionMaxWeighted;

      const passedThreshold = boundedRawScore >= criterion.threshold;
      const mandatoryPassed = !criterion.mandatory || passedThreshold;

      if (criterion.mandatory && !mandatoryPassed && qualificationStatus !== "disqualified") {
        qualificationStatus = "disqualified";
        qualificationReason = `Mandatory criterion '${criterion.label}' failed.`;
      } else if (!passedThreshold && qualificationStatus !== "disqualified") {
        qualificationStatus = "disqualified";
        qualificationReason = `Threshold not met for '${criterion.label}'.`;
      }

      logs.push(
        `criterion:${criterion.key};raw:${boundedRawScore.toFixed(3)};weighted:${weightedScore.toFixed(3)};mandatory:${criterion.mandatory};passed:${passedThreshold}`,
      );

      return {
        key: criterion.key,
        label: criterion.label,
        rawScore: Number(boundedRawScore.toFixed(3)),
        maxScore: criterion.maxScore,
        weight: criterion.weight,
        weightedScore: Number(weightedScore.toFixed(3)),
        passedThreshold,
        mandatoryPassed,
        rationale: parameter ? parameter.notes.join(" | ") : "Not Provided",
      };
    });

    const percentage =
      maxWeightedScore > 0
        ? Number(((totalWeightedScore / maxWeightedScore) * 100).toFixed(3))
        : 0;

    if (qualificationStatus === "qualified" && percentage < matrix.globalThresholdPercent) {
      qualificationStatus = "disqualified";
      qualificationReason = `Global threshold of ${matrix.globalThresholdPercent}% not reached.`;
    }

    const score: VendorScore = {
      _id: randomUUID(),
      projectId: input.projectId,
      vendorId: input.vendorId,
      evaluationId: evaluation._id,
      scoringMatrixId: matrix._id,
      scoredParameters,
      totalWeightedScore: Number(totalWeightedScore.toFixed(3)),
      maxWeightedScore: Number(maxWeightedScore.toFixed(3)),
      percentage,
      qualificationStatus,
      qualificationReason,
      deterministic: true,
      scoredAt: new Date().toISOString(),
      explainability: {
        matrixId: matrix._id,
        evaluationId: evaluation._id,
        logs,
      },
    };

    await this.repository.saveVendorScore(score);
    return score;
  }
}
