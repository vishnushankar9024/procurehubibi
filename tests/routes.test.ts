import express from "express";
import request from "supertest";
import { describe, expect, it } from "vitest";

import { createProcurementRouter } from "../src/routes/procurementRoutes";
import { createAiProvider } from "../src/lib/ai";
import { BoqService } from "../src/services/boqService";
import { TemplateService } from "../src/services/templateService";
import { ScoringCriteriaService } from "../src/services/scoringCriteriaService";
import { VendorAnalyzerService } from "../src/services/vendorAnalyzerService";
import { VendorScoringService } from "../src/services/vendorScoringService";
import { VendorComparisonService } from "../src/services/vendorComparisonService";
import { ReportingService } from "../src/services/reportingService";
import { InMemoryRepository } from "./helpers/inMemoryRepository";
import { AppError } from "../src/lib/errors";

function createTestApp() {
  const repository = new InMemoryRepository();
  const aiProvider = createAiProvider("mock");
  const boqService = new BoqService(repository, aiProvider, 2000);
  const templateService = new TemplateService(repository, aiProvider);
  const scoringCriteriaService = new ScoringCriteriaService(repository);
  const vendorAnalyzerService = new VendorAnalyzerService(repository, aiProvider, 2000);
  const vendorScoringService = new VendorScoringService(repository);
  const vendorComparisonService = new VendorComparisonService(repository);
  const reportingService = new ReportingService(repository, aiProvider);

  const app = express();
  app.use(express.json());
  app.use(
    "/",
    createProcurementRouter({
      boqService,
      templateService,
      scoringCriteriaService,
      vendorAnalyzerService,
      vendorScoringService,
      vendorComparisonService,
      reportingService,
    }),
  );
  app.use(
    (
      err: unknown,
      _req: express.Request,
      res: express.Response,
      _next: express.NextFunction,
    ) => {
      if (err instanceof AppError) {
        return res.status(err.statusCode).json({ error: err.message, details: err.details });
      }
      return res.status(500).json({ error: "Internal server error" });
    },
  );
  return app;
}

describe("Procurement routes", () => {
  it("runs end-to-end happy path", async () => {
    const app = createTestApp();

    const templateResponse = await request(app).post("/template/create").send({
      projectId: "p1",
      projectType: "commercial_building",
      requirements: { deadlineMonths: 18 },
    });
    expect(templateResponse.status).toBe(201);
    const templateId = templateResponse.body._id;

    const scoringResponse = await request(app).post("/scoring/create").send({
      projectId: "p1",
      templateId,
      globalThresholdPercent: 60,
      criteria: [
        {
          key: "experience_years",
          label: "Relevant Experience",
          category: "qualitative",
          weight: 40,
          method: "scaled",
          maxScore: 5,
          threshold: 3,
          mandatory: true,
        },
        {
          key: "annual_turnover",
          label: "Annual Turnover",
          category: "quantitative",
          weight: 60,
          method: "scaled",
          maxScore: 5,
          threshold: 2,
          mandatory: true,
        },
      ],
    });
    expect(scoringResponse.status).toBe(201);
    const matrixId = scoringResponse.body._id;

    const analyzeResponse = await request(app)
      .post("/vendor/analyze")
      .field("projectId", "p1")
      .field("vendorId", "vendor-a")
      .field("templateId", templateId)
      .field("structuredInput", JSON.stringify({ vendorTier: "A" }))
      .attach("documents", Buffer.from("Vendor profile and audited statements"), "vendor-a.txt");
    expect(analyzeResponse.status).toBe(201);
    const evaluationId = analyzeResponse.body._id;

    const scoreResponse = await request(app).post("/vendor/score").send({
      projectId: "p1",
      vendorId: "vendor-a",
      scoringMatrixId: matrixId,
      vendorEvaluationId: evaluationId,
    });
    expect(scoreResponse.status).toBe(201);

    const compareResponse = await request(app).post("/vendor/compare").send({
      projectId: "p1",
      vendorScoreIds: [scoreResponse.body._id, scoreResponse.body._id],
    });
    expect(compareResponse.status).toBe(201);

    const reportResponse = await request(app).get("/report/p1");
    expect(reportResponse.status).toBe(200);
    expect(reportResponse.body.projectId).toBe("p1");
    expect(typeof reportResponse.body.html).toBe("string");
  });
});
