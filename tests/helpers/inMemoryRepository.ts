import type { ProcurementRepository } from "../../src/lib/db/repository";
import type {
  BoqRecord,
  PrequalificationTemplate,
  ProcurementReport,
  ScoringMatrix,
  VendorComparison,
  VendorEvaluation,
  VendorScore,
} from "../../src/types";

export class InMemoryRepository implements ProcurementRepository {
  public boqRecords = new Map<string, BoqRecord>();
  public templates = new Map<string, PrequalificationTemplate>();
  public scoringMatrices = new Map<string, ScoringMatrix>();
  public vendorEvaluations = new Map<string, VendorEvaluation>();
  public vendorScores = new Map<string, VendorScore>();
  public vendorComparisons = new Map<string, VendorComparison>();
  public reports = new Map<string, ProcurementReport>();

  async saveBoq(record: BoqRecord): Promise<void> {
    this.boqRecords.set(record._id, record);
  }

  async saveTemplate(record: PrequalificationTemplate): Promise<void> {
    this.templates.set(record._id, record);
  }

  async getTemplateById(templateId: string): Promise<PrequalificationTemplate | null> {
    return this.templates.get(templateId) ?? null;
  }

  async saveScoringMatrix(record: ScoringMatrix): Promise<void> {
    this.scoringMatrices.set(record._id, record);
  }

  async getScoringMatrixById(scoringMatrixId: string): Promise<ScoringMatrix | null> {
    return this.scoringMatrices.get(scoringMatrixId) ?? null;
  }

  async saveVendorEvaluation(record: VendorEvaluation): Promise<void> {
    this.vendorEvaluations.set(record._id, record);
  }

  async getVendorEvaluationById(vendorEvaluationId: string): Promise<VendorEvaluation | null> {
    return this.vendorEvaluations.get(vendorEvaluationId) ?? null;
  }

  async listVendorEvaluationsByProject(projectId: string): Promise<VendorEvaluation[]> {
    return [...this.vendorEvaluations.values()].filter((record) => record.projectId === projectId);
  }

  async saveVendorScore(record: VendorScore): Promise<void> {
    this.vendorScores.set(record._id, record);
  }

  async getVendorScoreById(vendorScoreId: string): Promise<VendorScore | null> {
    return this.vendorScores.get(vendorScoreId) ?? null;
  }

  async listVendorScoresByProject(projectId: string): Promise<VendorScore[]> {
    return [...this.vendorScores.values()].filter((record) => record.projectId === projectId);
  }

  async saveVendorComparison(record: VendorComparison): Promise<void> {
    this.vendorComparisons.set(record._id, record);
  }

  async getLatestVendorComparison(projectId: string): Promise<VendorComparison | null> {
    const matches = [...this.vendorComparisons.values()]
      .filter((record) => record.projectId === projectId)
      .sort((a, b) => b.generatedAt.localeCompare(a.generatedAt));
    return matches[0] ?? null;
  }

  async saveReport(record: ProcurementReport): Promise<void> {
    this.reports.set(record._id, record);
  }

  async getLatestReport(projectId: string): Promise<ProcurementReport | null> {
    const matches = [...this.reports.values()]
      .filter((record) => record.projectId === projectId)
      .sort((a, b) => b.generatedAt.localeCompare(a.generatedAt));
    return matches[0] ?? null;
  }
}
