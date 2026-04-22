import { z } from "zod";

import type { AIProviderName, CollectionConfig } from "./types";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().default(3000),
  AI_PROVIDER: z.enum(["openai", "gemini", "mock"]).default("mock"),
  OPENAI_API_KEY: z.string().optional(),
  OPENAI_MODEL: z.string().default("gpt-4.1-mini"),
  GEMINI_API_KEY: z.string().optional(),
  GEMINI_MODEL: z.string().default("gemini-2.0-flash"),
  MONGODB_URI: z.string().optional(),
  MONGODB_DB_NAME: z.string().default("procurement"),
  GOOGLE_CLOUD_PROJECT: z.string().optional(),
  MONGODB_URI_SECRET_NAME: z.string().default("mongodb-uri"),
  MONGODB_URI_SECRET_VERSION: z.string().default("latest"),
  MONGODB_URI_SECRET_RESOURCE: z.string().optional(),
  BOQ_COLLECTION: z.string().default("boq_documents"),
  TEMPLATE_COLLECTION: z.string().default("prequalification_templates"),
  SCORING_COLLECTION: z.string().default("scoring_matrices"),
  VENDOR_EVALUATION_COLLECTION: z.string().default("vendor_evaluations"),
  VENDOR_SCORE_COLLECTION: z.string().default("vendor_scores"),
  VENDOR_COMPARISON_COLLECTION: z.string().default("vendor_comparisons"),
  REPORT_COLLECTION: z.string().default("procurement_reports"),
  MAX_CHUNK_CHARS: z.coerce.number().default(3500),
  MAX_AI_TOKENS: z.coerce.number().default(1200),
  USE_IN_MEMORY_DB: z
    .string()
    .optional()
    .transform((value) => value === "true"),
});

export type RuntimeConfig = {
  nodeEnv: "development" | "test" | "production";
  port: number;
  aiProvider: AIProviderName;
  openAiApiKey?: string;
  openAiModel: string;
  geminiApiKey?: string;
  geminiModel: string;
  mongoUri?: string;
  mongoDbName: string;
  gcpProject?: string;
  mongoSecretName: string;
  mongoSecretVersion: string;
  mongoSecretResource?: string;
  mongoCollections: CollectionConfig;
  chunkSize: number;
  maxAiTokens: number;
  useInMemoryDb: boolean;
};

let cachedConfig: RuntimeConfig | null = null;

export function getConfig(): RuntimeConfig {
  if (cachedConfig) {
    return cachedConfig;
  }

  const env = envSchema.parse(process.env);
  cachedConfig = {
    nodeEnv: env.NODE_ENV,
    port: env.PORT,
    aiProvider: env.AI_PROVIDER as AIProviderName,
    openAiApiKey: env.OPENAI_API_KEY,
    openAiModel: env.OPENAI_MODEL,
    geminiApiKey: env.GEMINI_API_KEY,
    geminiModel: env.GEMINI_MODEL,
    mongoUri: env.MONGODB_URI,
    mongoDbName: env.MONGODB_DB_NAME,
    gcpProject: env.GOOGLE_CLOUD_PROJECT,
    mongoSecretName: env.MONGODB_URI_SECRET_NAME,
    mongoSecretVersion: env.MONGODB_URI_SECRET_VERSION,
    mongoSecretResource: env.MONGODB_URI_SECRET_RESOURCE,
    mongoCollections: {
      boq: env.BOQ_COLLECTION,
      templates: env.TEMPLATE_COLLECTION,
      scoringMatrices: env.SCORING_COLLECTION,
      vendorEvaluations: env.VENDOR_EVALUATION_COLLECTION,
      vendorScores: env.VENDOR_SCORE_COLLECTION,
      vendorComparisons: env.VENDOR_COMPARISON_COLLECTION,
      reports: env.REPORT_COLLECTION,
    },
    chunkSize: env.MAX_CHUNK_CHARS,
    maxAiTokens: env.MAX_AI_TOKENS,
    useInMemoryDb: env.USE_IN_MEMORY_DB ?? false,
  };

  return cachedConfig;
}

export function resetConfigForTests() {
  cachedConfig = null;
}
