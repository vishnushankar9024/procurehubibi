import express, { type NextFunction, type Request, type Response } from "express";
import { getConfig } from "./config";
import { appLogger } from "./lib/logger";
import { AppError } from "./lib/errors";
import { createProcurementServices } from "./app";
import { createProcurementRouter } from "./routes/procurementRoutes";

export async function createApp() {
  const config = getConfig();
  const services = await createProcurementServices(config);

  const app = express();
  app.use(express.json({ limit: "10mb" }));

  app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  app.use(
    "/",
    createProcurementRouter({
      boqService: services.boqService,
      templateService: services.templateService,
      scoringCriteriaService: services.scoringCriteriaService,
      vendorAnalyzerService: services.vendorAnalyzerService,
      vendorScoringService: services.vendorScoringService,
      vendorComparisonService: services.vendorComparisonService,
      reportingService: services.reportingService,
    }),
  );

  app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
    if (err instanceof AppError) {
      appLogger.warn({ err }, "handled application error");
      return res.status(err.statusCode).json({
        error: err.message,
        details: err.details,
      });
    }

    appLogger.error({ err }, "unhandled error");
    return res.status(500).json({ error: "Internal server error" });
  });

  return app;
}

async function start() {
  const config = getConfig();
  const app = await createApp();
  app.listen(config.port, () => {
    appLogger.info({ port: config.port }, "AI Procurement Manager started");
  });
}

if (require.main === module) {
  start().catch((error: unknown) => {
    appLogger.error({ err: error }, "failed to start server");
    process.exit(1);
  });
}
