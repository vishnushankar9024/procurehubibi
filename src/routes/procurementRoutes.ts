import { Router } from "express";
import multer from "multer";
import { ZodError } from "zod";

import {
  boqUploadSchema,
  compareVendorsSchema,
  createScoringSchema,
  createTemplateSchema,
  scoreVendorSchema,
  vendorAnalyzeSchema,
} from "../validation/schemas";
import { BoqService } from "../services/boqService";
import { TemplateService } from "../services/templateService";
import { ScoringCriteriaService } from "../services/scoringCriteriaService";
import { VendorAnalyzerService } from "../services/vendorAnalyzerService";
import { VendorScoringService } from "../services/vendorScoringService";
import { VendorComparisonService } from "../services/vendorComparisonService";
import { ReportingService } from "../services/reportingService";
import { ValidationError } from "../lib/errors";

interface ProcurementDeps {
  boqService: BoqService;
  templateService: TemplateService;
  scoringCriteriaService: ScoringCriteriaService;
  vendorAnalyzerService: VendorAnalyzerService;
  vendorScoringService: VendorScoringService;
  vendorComparisonService: VendorComparisonService;
  reportingService: ReportingService;
}

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 20 * 1024 * 1024 },
});

function parseJsonField<T>(value: unknown, fallback: T): T {
  if (typeof value !== "string") {
    return (value as T) ?? fallback;
  }

  try {
    return JSON.parse(value) as T;
  } catch {
    return fallback;
  }
}

function parseRequest<T>(schema: { parse: (value: unknown) => T }, value: unknown): T {
  try {
    return schema.parse(value);
  } catch (error) {
    if (error instanceof ZodError) {
      throw new ValidationError("Request validation failed.", error.flatten());
    }
    throw error;
  }
}

export function createProcurementRouter({
  boqService,
  templateService,
  scoringCriteriaService,
  vendorAnalyzerService,
  vendorScoringService,
  vendorComparisonService,
  reportingService,
}: ProcurementDeps): Router {
  const router = Router();

  router.post("/boq/upload", upload.single("file"), async (req, res, next) => {
    try {
      const parsedBody = parseRequest(boqUploadSchema, req.body);
      if (!req.file) {
        throw new ValidationError("BOQ file is required");
      }
      const result = await boqService.uploadBoq({
        projectId: parsedBody.projectId,
        fileName: req.file.originalname,
        mimeType: req.file.mimetype,
        content: req.file.buffer.toString("utf8"),
      });
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.post("/template/create", async (req, res, next) => {
    try {
      const payload = parseRequest(createTemplateSchema, req.body);
      const result = await templateService.createTemplate(payload);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.post("/scoring/create", async (req, res, next) => {
    try {
      const payload = parseRequest(createScoringSchema, req.body);
      const result = await scoringCriteriaService.createScoring(payload);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.post("/vendor/analyze", upload.array("documents"), async (req, res, next) => {
    try {
      const payload = parseRequest(vendorAnalyzeSchema, {
        ...req.body,
        structuredInput: parseJsonField(req.body.structuredInput, {}),
      });
      const files = (req.files as Express.Multer.File[] | undefined) ?? [];
      const result = await vendorAnalyzerService.analyzeVendorSubmission({
        ...payload,
        documents: files.map((file) => ({
          fileName: file.originalname,
          mimeType: file.mimetype,
          content: file.buffer.toString("utf8"),
        })),
      });
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.post("/vendor/score", async (req, res, next) => {
    try {
      const payload = parseRequest(scoreVendorSchema, req.body);
      const result = await vendorScoringService.scoreVendor(payload);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.post("/vendor/compare", async (req, res, next) => {
    try {
      const payload = parseRequest(compareVendorsSchema, req.body);
      const result = await vendorComparisonService.compareVendors(payload);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.get("/report/:projectId", async (req, res, next) => {
    try {
      const { projectId } = req.params;
      const report = await reportingService.generateProjectReport(projectId);
      res.status(200).json(report);
    } catch (error) {
      next(error);
    }
  });

  return router;
}
