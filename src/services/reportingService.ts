import { randomUUID } from "node:crypto";

import type { AiProvider } from "../lib/ai/aiProvider";
import type { ProcurementRepository } from "../lib/db/repository";
import type { ProcurementReport } from "../types";

export class ReportingService {
  constructor(
    private readonly repository: ProcurementRepository,
    private readonly aiProvider: AiProvider,
  ) {}

  async generateProjectReport(projectId: string): Promise<ProcurementReport> {
    const [vendorEvaluations, vendorScores, comparison] = await Promise.all([
      this.repository.listVendorEvaluationsByProject(projectId),
      this.repository.listVendorScoresByProject(projectId),
      this.repository.getLatestVendorComparison(projectId),
    ]);

    const summarySource = {
      projectId,
      vendorCount: vendorScores.length,
      ranking: comparison?.ranking ?? [],
      riskSignals: vendorEvaluations.map((evaluation) => ({
        vendorId: evaluation.vendorId,
        riskSignals: evaluation.riskSignals,
      })),
      qualification: vendorScores.map((score) => ({
        vendorId: score.vendorId,
        percentage: score.percentage,
        qualificationStatus: score.qualificationStatus,
        qualificationReason: score.qualificationReason,
      })),
    };

    const aiResult = await this.aiProvider.generate({
      task: "report_summary",
      messages: [
        {
          role: "system",
          content:
            "Write factual procurement recommendations strictly from provided JSON evidence.",
        },
        {
          role: "user",
          content: `Generate concise recommendation summary for this report data:\n${JSON.stringify(
            summarySource,
          )}`,
        },
      ],
      maxTokens: 700,
    });

    const generatedAt = new Date().toISOString();
    const report: ProcurementReport = {
      _id: randomUUID(),
      projectId,
      generatedAt,
      json: {
        projectId,
        generatedAt,
        vendorEvaluations,
        vendorScores,
        comparison: comparison ?? undefined,
        recommendationSummary: aiResult.content,
        explainability: [
          "Deterministic scoring and ranking were used for qualification and comparison.",
          "AI was only used to synthesize recommendation narrative from structured outputs.",
          ...aiResult.traces,
        ],
      },
      html: this.buildHtml(projectId, generatedAt, aiResult.content, vendorScores, comparison),
    };

    await this.repository.saveReport(report);
    return report;
  }

  private buildHtml(
    projectId: string,
    generatedAt: string,
    recommendationSummary: string,
    vendorScores: Array<{
      vendorId: string;
      percentage: number;
      qualificationStatus: string;
      qualificationReason: string;
    }>,
    comparison:
      | {
          ranking: Array<{
            vendorId: string;
            rank: number;
            percentage: number;
          }>;
        }
      | null,
  ): string {
    const scoreRows = vendorScores
      .map(
        (score) =>
          `<tr><td>${score.vendorId}</td><td>${score.percentage.toFixed(
            2,
          )}%</td><td>${score.qualificationStatus}</td><td>${score.qualificationReason}</td></tr>`,
      )
      .join("");

    const rankingRows = (comparison?.ranking ?? [])
      .map(
        (ranked) =>
          `<tr><td>${ranked.rank}</td><td>${ranked.vendorId}</td><td>${ranked.percentage.toFixed(
            2,
          )}%</td></tr>`,
      )
      .join("");

    return `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Procurement Report - ${projectId}</title>
  </head>
  <body>
    <h1>Procurement Report: ${projectId}</h1>
    <p><strong>Generated at:</strong> ${generatedAt}</p>
    <h2>Recommendation Summary</h2>
    <p>${recommendationSummary}</p>
    <h2>Vendor Evaluation Summary</h2>
    <table border="1" cellspacing="0" cellpadding="6">
      <thead>
        <tr><th>Vendor</th><th>Score</th><th>Status</th><th>Reason</th></tr>
      </thead>
      <tbody>${scoreRows}</tbody>
    </table>
    <h2>Vendor Ranking</h2>
    <table border="1" cellspacing="0" cellpadding="6">
      <thead>
        <tr><th>Rank</th><th>Vendor</th><th>Score</th></tr>
      </thead>
      <tbody>${rankingRows}</tbody>
    </table>
  </body>
</html>`;
  }
}
