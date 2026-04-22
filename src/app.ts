import type { RuntimeConfig } from "./config";
import { createAiProvider } from "./lib/ai";
import { connectMongo } from "./lib/db/mongoClient";
import { MongoRepository } from "./lib/db/repository";
import { InMemoryRepository } from "./lib/db/inMemoryRepository";
import {
  BoqService,
  ReportingService,
  ScoringCriteriaService,
  TemplateService,
  VendorAnalyzerService,
  VendorComparisonService,
  VendorScoringService,
} from "./services";

export type ProcurementServices = {
  boqService: BoqService;
  templateService: TemplateService;
  scoringCriteriaService: ScoringCriteriaService;
  vendorAnalyzerService: VendorAnalyzerService;
  vendorScoringService: VendorScoringService;
  vendorComparisonService: VendorComparisonService;
  reportingService: ReportingService;
};

export async function createProcurementServices(
  config: RuntimeConfig,
): Promise<ProcurementServices> {
  const repository = config.useInMemoryDb
    ? new InMemoryRepository()
    : new MongoRepository(await connectMongo(config), config.mongoCollections);
  const aiProvider = createAiProvider(config.aiProvider);

  return {
    boqService: new BoqService(repository, aiProvider, config.chunkSize),
    templateService: new TemplateService(repository, aiProvider),
    scoringCriteriaService: new ScoringCriteriaService(repository),
    vendorAnalyzerService: new VendorAnalyzerService(
      repository,
      aiProvider,
      config.chunkSize,
    ),
    vendorScoringService: new VendorScoringService(repository),
    vendorComparisonService: new VendorComparisonService(repository),
    reportingService: new ReportingService(repository, aiProvider),
  };
}
