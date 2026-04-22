# AI Procurement Manager Agent (Construction Procurement)

Production-ready TypeScript backend implementing a hybrid AI + deterministic procurement lifecycle.

## Features Implemented

- **BOQ Processor (POMI):** AI-assisted parsing of BOQ uploads with structured output and missing-field traceability.
- **Prequalification Template Builder:** AI-assisted qualitative + quantitative template suggestion stored in MongoDB.
- **Scoring Criteria Engine:** deterministic weighted scoring matrix with thresholds + mandatory criteria.
- **Vendor Submission Analyzer:** AI-based extraction with chunking, compliance checks, risk signals, confidence score, and strict `"Not Provided"` fallback.
- **Vendor Scoring Engine:** deterministic scoring only (no AI math).
- **Vendor Comparison Engine:** deterministic ranking, strengths/weaknesses, compliance summaries.
- **Report Generator:** JSON + PDF-ready HTML output with AI-authored recommendation summary from structured evidence.
- **MongoDB + Secret Manager:** runtime Mongo URI retrieval from Secret Manager, schema-preserving collection usage.
- **Cloud Run Ready:** Dockerfile + cloudbuild config included.

## Tech Stack

- Node.js + TypeScript
- Express
- MongoDB
- Google Secret Manager
- OpenAI / Gemini / Mock AI provider abstraction

## Folder Structure

- `src/server.ts` - HTTP server entrypoint
- `src/app.ts` - service composition and dependency wiring
- `src/routes/` - REST endpoints
- `src/services/` - module agents (BOQ, template, scoring, analysis, comparison, reporting)
- `src/lib/ai/` - AI provider abstraction + implementations
- `src/lib/db/` - Mongo client, secret manager, repository
- `src/validation/` - request schemas
- `src/types.ts` - shared domain models
- `tests/` - unit + route tests
- `samples/` - sample requests and mock vendor docs

## API Endpoints (Mandatory)

- `POST /boq/upload`
- `POST /template/create`
- `POST /scoring/create`
- `POST /vendor/analyze`
- `POST /vendor/score`
- `POST /vendor/compare`
- `GET /report/:projectId`

## Environment Variables

Set these in local `.env` or deployment environment:

- `PORT` (default: `3000`)
- `AI_PROVIDER` = `openai` | `gemini` | `mock`
- `OPENAI_API_KEY` (required for `openai`)
- `OPENAI_MODEL` (default: `gpt-4.1-mini`)
- `GEMINI_API_KEY` (required for `gemini`)
- `GEMINI_MODEL` (default: `gemini-2.0-flash`)
- `MONGODB_URI` (optional if secret manager is used)
- `MONGODB_DB_NAME` (default: `procurement`)
- `GOOGLE_CLOUD_PROJECT` (required for secret manager path derivation if `MONGODB_URI` absent)
- `MONGODB_URI_SECRET_NAME` (default: `mongodb-uri`)
- `MONGODB_URI_SECRET_VERSION` (default: `latest`)
- `MONGODB_URI_SECRET_RESOURCE` (optional full resource override)
- collection names (optional):
  - `BOQ_COLLECTION`
  - `TEMPLATE_COLLECTION`
  - `SCORING_COLLECTION`
  - `VENDOR_EVALUATION_COLLECTION`
  - `VENDOR_SCORE_COLLECTION`
  - `VENDOR_COMPARISON_COLLECTION`
  - `REPORT_COLLECTION`

## Local Setup

1. Install dependencies:
   - `npm install`
2. Run tests:
   - `npm test`
3. Run development server:
   - `npm run dev`

Health check:
- `GET http://localhost:3000/health`

## Sample API Requests

See:
- `samples/requests.http`
- `samples/vendor_documents/vendor_a_profile.txt`
- `samples/vendor_documents/vendor_b_profile.txt`

## Deterministic vs AI Boundaries

AI is used **only** for:
- document understanding
- text extraction
- semantic summary/risk insights

Deterministic logic handles:
- all score computations
- qualification thresholds
- ranking and comparison
- workflow state transitions

## Hallucination Safety & Traceability

- Extraction prompts require strict JSON and explicit `"Not Provided"` for missing data.
- Evidence traces track chunk/document origins.
- Reports include explainability logs indicating deterministic vs AI-generated segments.

## Testing

Included test coverage:
- BOQ service
- Template service
- Scoring criteria service
- Vendor analyzer service
- Vendor scoring service
- Vendor comparison service
- Reporting service
- Route-level end-to-end workflow test

Run:
- `npm test`

## Deployment (Cloud Run)

Build and deploy using included `Dockerfile` and `cloudbuild.yaml`.

Example:
- `gcloud builds submit --config cloudbuild.yaml`
- `gcloud run deploy procurehub-ai-agent --image gcr.io/$PROJECT_ID/procurehub-ai-agent --platform managed --region us-central1`
