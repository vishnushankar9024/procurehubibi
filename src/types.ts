export type AIProviderName = "openai" | "gemini" | "mock";

export type ScalarValue = string | number | boolean;
export type ExtractedValue = ScalarValue | "Not Provided";

export interface CollectionConfig {
  boq: string;
  templates: string;
  scoringMatrices: string;
  vendorEvaluations: string;
  vendorScores: string;
  vendorComparisons: string;
  reports: string;
}

export interface DocumentChunk {
  chunkId: string;
  sourceDocument: string;
  text: string;
}

export interface TraceEvidence {
  chunkId: string;
  sourceDocument: string;
  quote?: string;
}

export interface BoqItem {
  itemCode?: string;
  description: string;
  unit: string;
  quantity: number;
  rate?: number;
  sourceChunkId: string;
  confidence: number;
}

export interface BoqRecord {
  _id: string;
  projectId: string;
  standard: "POMI";
  fileName: string;
  mimeType: string;
  items: BoqItem[];
  missingFields: Array<{
    rowRef: string;
    missing: Array<"description" | "unit" | "quantity">;
  }>;
  trace: {
    model: string;
    extractedAt: string;
    chunkCount: number;
  };
}

export interface TemplateCriterion {
  key: string;
  label: string;
  description: string;
  dataType: "text" | "number" | "boolean";
  mandatory: boolean;
  unit?: string;
  minValue?: number;
  maxValue?: number;
}

export interface PrequalificationTemplate {
  _id: string;
  projectId: string;
  projectType: string;
  qualitative: TemplateCriterion[];
  quantitative: TemplateCriterion[];
  requirements: Record<string, unknown>;
  createdAt: string;
  trace: {
    model: string;
    rationale: string;
  };
}

export interface ScoringCriterion {
  key: string;
  label: string;
  category: "qualitative" | "quantitative";
  weight: number;
  method: "boolean" | "scaled";
  maxScore: number;
  threshold: number;
  mandatory: boolean;
}

export interface ScoringMatrix {
  _id: string;
  projectId: string;
  templateId: string;
  criteria: ScoringCriterion[];
  totalWeight: number;
  globalThresholdPercent: number;
  deterministic: true;
  createdAt: string;
}

export interface RiskSignal {
  type: string;
  detail: string;
  confidence: number;
}

export interface AnalyzedParameter {
  key: string;
  label: string;
  category: "qualitative" | "quantitative";
  value: ExtractedValue;
  normalizedScoreHint: number;
  confidence: number;
  evidence: TraceEvidence[];
  compliance: "Compliant" | "Non-Compliant" | "Not Provided";
  notes: string[];
}

export interface VendorEvaluation {
  _id: string;
  projectId: string;
  vendorId: string;
  templateId: string;
  complianceStatus: "compliant" | "partial" | "non_compliant";
  missingInformation: string[];
  parameters: AnalyzedParameter[];
  riskSignals: RiskSignal[];
  confidenceScore: number;
  explainability: {
    model: string;
    chunkCount: number;
    evaluatedAt: string;
    logs: string[];
  };
}

export interface ScoredParameter {
  key: string;
  label: string;
  rawScore: number;
  maxScore: number;
  weight: number;
  weightedScore: number;
  passedThreshold: boolean;
  mandatoryPassed: boolean;
  rationale: string;
}

export interface VendorScore {
  _id: string;
  projectId: string;
  vendorId: string;
  evaluationId: string;
  scoringMatrixId: string;
  scoredParameters: ScoredParameter[];
  totalWeightedScore: number;
  maxWeightedScore: number;
  percentage: number;
  qualificationStatus: "qualified" | "disqualified";
  qualificationReason: string;
  deterministic: true;
  scoredAt: string;
  explainability: {
    matrixId: string;
    evaluationId: string;
    logs: string[];
  };
}

export interface VendorComparison {
  _id: string;
  projectId: string;
  ranking: Array<{
    vendorId: string;
    rank: number;
    scoreId: string;
    percentage: number;
    qualificationStatus: "qualified" | "disqualified";
  }>;
  comparisonMatrix: Array<{
    vendorId: string;
    scoreId: string;
    percentage: number;
    strengths: string[];
    weaknesses: string[];
    complianceSummary: string;
  }>;
  generatedAt: string;
}

export interface ProcurementReport {
  _id: string;
  projectId: string;
  json: {
    projectId: string;
    generatedAt: string;
    vendorEvaluations: VendorEvaluation[];
    vendorScores: VendorScore[];
    comparison?: VendorComparison;
    recommendationSummary: string;
    explainability: string[];
  };
  html: string;
  generatedAt: string;
}

export interface TemplateCreateInput {
  projectId: string;
  projectType: string;
  requirements: Record<string, unknown>;
}

export interface ScoringCreateInput {
  projectId: string;
  templateId: string;
  globalThresholdPercent: number;
  criteria: ScoringCriterion[];
}

export interface VendorAnalyzeInput {
  projectId: string;
  vendorId: string;
  templateId: string;
  documents: Array<{
    fileName: string;
    mimeType: string;
    content: string;
  }>;
  structuredInput: Record<string, unknown>;
}

export interface VendorScoreInput {
  projectId: string;
  vendorId: string;
  scoringMatrixId: string;
  vendorEvaluationId: string;
}

export interface VendorCompareInput {
  projectId: string;
  vendorScoreIds: string[];
}
