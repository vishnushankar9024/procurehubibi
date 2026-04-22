import { z } from "zod";

export const boqUploadSchema = z.object({
  projectId: z.string().min(1),
});

export const createTemplateSchema = z.object({
  projectId: z.string().min(1),
  projectType: z.string().min(1),
  requirements: z.record(z.string(), z.unknown()).default({}),
});

const scoringCriterionSchema = z.object({
  key: z.string().min(1),
  label: z.string().min(1),
  category: z.enum(["qualitative", "quantitative"]),
  weight: z.number().gt(0).max(100),
  method: z.enum(["boolean", "scaled"]),
  maxScore: z.number().gt(0),
  threshold: z.number().min(0),
  mandatory: z.boolean().default(false),
});

export const createScoringSchema = z.object({
  projectId: z.string().min(1),
  templateId: z.string().min(1),
  globalThresholdPercent: z.number().min(0).max(100).default(60),
  criteria: z.array(scoringCriterionSchema).min(1),
});

export const vendorAnalyzeSchema = z.object({
  projectId: z.string().min(1),
  vendorId: z.string().min(1),
  templateId: z.string().min(1),
  structuredInput: z.record(z.string(), z.unknown()).default({}),
});

export const scoreVendorSchema = z.object({
  projectId: z.string().min(1),
  vendorId: z.string().min(1),
  scoringMatrixId: z.string().min(1),
  vendorEvaluationId: z.string().min(1),
});

export const compareVendorsSchema = z.object({
  projectId: z.string().min(1),
  vendorScoreIds: z.array(z.string().min(1)).min(2),
});
