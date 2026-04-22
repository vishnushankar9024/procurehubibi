import { randomUUID } from "node:crypto";

import { ValidationError } from "../lib/errors";
import type { ProcurementRepository } from "../lib/db/repository";
import type { VendorCompareInput, VendorComparison, VendorScore } from "../types";

function rankScores(scores: VendorScore[]) {
  return [...scores].sort((a, b) => {
    if (b.percentage !== a.percentage) {
      return b.percentage - a.percentage;
    }
    return b.totalWeightedScore - a.totalWeightedScore;
  });
}

function getStrengths(score: VendorScore): string[] {
  return score.scoredParameters
    .filter((parameter) => parameter.weightedScore >= parameter.weight * 0.8)
    .map((parameter) => `${parameter.label}: high performance`);
}

function getWeaknesses(score: VendorScore): string[] {
  return score.scoredParameters
    .filter((parameter) => !parameter.passedThreshold)
    .map((parameter) => `${parameter.label}: below threshold`);
}

function complianceSummary(score: VendorScore): string {
  const passed = score.scoredParameters.filter((parameter) => parameter.passedThreshold).length;
  const total = score.scoredParameters.length;
  return `${passed}/${total} criteria passed thresholds`;
}

export class VendorComparisonService {
  constructor(private readonly repository: ProcurementRepository) {}

  async compareVendors(input: VendorCompareInput): Promise<VendorComparison> {
    if (input.vendorScoreIds.length < 2) {
      throw new ValidationError("At least two vendor score ids are required for comparison.");
    }

    const scores = await Promise.all(
      input.vendorScoreIds.map((scoreId) => this.repository.getVendorScoreById(scoreId)),
    );

    const resolvedScores: VendorScore[] = [];
    for (const score of scores) {
      if (!score || score.projectId !== input.projectId) {
        throw new ValidationError("One or more vendor scores not found for project.");
      }
      resolvedScores.push(score);
    }

    const ranked = rankScores(resolvedScores);
    const ranking = ranked.map((score, index) => ({
      vendorId: score.vendorId,
      rank: index + 1,
      scoreId: score._id,
      percentage: score.percentage,
      qualificationStatus: score.qualificationStatus,
    }));

    const comparisonMatrix = ranked.map((score) => ({
      vendorId: score.vendorId,
      scoreId: score._id,
      percentage: score.percentage,
      strengths: getStrengths(score),
      weaknesses: getWeaknesses(score),
      complianceSummary: complianceSummary(score),
    }));

    const comparison: VendorComparison = {
      _id: randomUUID(),
      projectId: input.projectId,
      ranking,
      comparisonMatrix,
      generatedAt: new Date().toISOString(),
    };

    await this.repository.saveVendorComparison(comparison);
    return comparison;
  }
}
