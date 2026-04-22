import type { Db } from "mongodb";

import type {
  BoqRecord,
  CollectionConfig,
  PrequalificationTemplate,
  ProcurementReport,
  ScoringMatrix,
  VendorComparison,
  VendorEvaluation,
  VendorScore,
} from "../../types";

export interface ProcurementRepository {
  saveBoq(record: BoqRecord): Promise<void>;
  saveTemplate(record: PrequalificationTemplate): Promise<void>;
  getTemplateById(templateId: string): Promise<PrequalificationTemplate | null>;
  saveScoringMatrix(record: ScoringMatrix): Promise<void>;
  getScoringMatrixById(scoringMatrixId: string): Promise<ScoringMatrix | null>;
  saveVendorEvaluation(record: VendorEvaluation): Promise<void>;
  getVendorEvaluationById(vendorEvaluationId: string): Promise<VendorEvaluation | null>;
  listVendorEvaluationsByProject(projectId: string): Promise<VendorEvaluation[]>;
  saveVendorScore(record: VendorScore): Promise<void>;
  getVendorScoreById(vendorScoreId: string): Promise<VendorScore | null>;
  listVendorScoresByProject(projectId: string): Promise<VendorScore[]>;
  saveVendorComparison(record: VendorComparison): Promise<void>;
  getLatestVendorComparison(projectId: string): Promise<VendorComparison | null>;
  saveReport(record: ProcurementReport): Promise<void>;
  getLatestReport(projectId: string): Promise<ProcurementReport | null>;
}

export class MongoRepository implements ProcurementRepository {
  constructor(
    private readonly db: Db,
    private readonly collections: CollectionConfig,
  ) {}

  async saveBoq(record: BoqRecord): Promise<void> {
    await this.db.collection<BoqRecord>(this.collections.boq).insertOne(record);
  }

  async saveTemplate(record: PrequalificationTemplate): Promise<void> {
    await this.db
      .collection<PrequalificationTemplate>(this.collections.templates)
      .insertOne(record);
  }

  async getTemplateById(templateId: string): Promise<PrequalificationTemplate | null> {
    return this.db
      .collection<PrequalificationTemplate>(this.collections.templates)
      .findOne({ _id: templateId });
  }

  async saveScoringMatrix(record: ScoringMatrix): Promise<void> {
    await this.db
      .collection<ScoringMatrix>(this.collections.scoringMatrices)
      .replaceOne({ _id: record._id }, record, { upsert: true });
  }

  async getScoringMatrixById(scoringMatrixId: string): Promise<ScoringMatrix | null> {
    return this.db
      .collection<ScoringMatrix>(this.collections.scoringMatrices)
      .findOne({ _id: scoringMatrixId });
  }

  async saveVendorEvaluation(record: VendorEvaluation): Promise<void> {
    await this.db
      .collection<VendorEvaluation>(this.collections.vendorEvaluations)
      .insertOne(record);
  }

  async getVendorEvaluationById(
    vendorEvaluationId: string,
  ): Promise<VendorEvaluation | null> {
    return this.db
      .collection<VendorEvaluation>(this.collections.vendorEvaluations)
      .findOne({ _id: vendorEvaluationId });
  }

  async listVendorEvaluationsByProject(projectId: string): Promise<VendorEvaluation[]> {
    return this.db
      .collection<VendorEvaluation>(this.collections.vendorEvaluations)
      .find({ projectId })
      .toArray();
  }

  async saveVendorScore(record: VendorScore): Promise<void> {
    await this.db
      .collection<VendorScore>(this.collections.vendorScores)
      .replaceOne({ _id: record._id }, record, { upsert: true });
  }

  async getVendorScoreById(vendorScoreId: string): Promise<VendorScore | null> {
    return this.db
      .collection<VendorScore>(this.collections.vendorScores)
      .findOne({ _id: vendorScoreId });
  }

  async listVendorScoresByProject(projectId: string): Promise<VendorScore[]> {
    return this.db
      .collection<VendorScore>(this.collections.vendorScores)
      .find({ projectId })
      .toArray();
  }

  async saveVendorComparison(record: VendorComparison): Promise<void> {
    await this.db
      .collection<VendorComparison>(this.collections.vendorComparisons)
      .insertOne(record);
  }

  async getLatestVendorComparison(projectId: string): Promise<VendorComparison | null> {
    return this.db
      .collection<VendorComparison>(this.collections.vendorComparisons)
      .find({ projectId })
      .sort({ generatedAt: -1 })
      .limit(1)
      .next();
  }

  async saveReport(record: ProcurementReport): Promise<void> {
    await this.db.collection<ProcurementReport>(this.collections.reports).insertOne(record);
  }

  async getLatestReport(projectId: string): Promise<ProcurementReport | null> {
    return this.db
      .collection<ProcurementReport>(this.collections.reports)
      .find({ projectId })
      .sort({ generatedAt: -1 })
      .limit(1)
      .next();
  }
}
