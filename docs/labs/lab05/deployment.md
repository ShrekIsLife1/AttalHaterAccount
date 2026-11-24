# Lab 5 — Cloud Deployment & CI/CD on Google Cloud

## 1. GCP Project & Team Infrastructure Baseline (Issue #16)

- **Course GCP Project ID:** `cpe-se-course-2026`
- **Region:** `asia-southeast1`
- **Team Resource Prefix:** `s3c35c9bd`
- **Cloud Run Service:** `s3c35c9bd`
- **Cloud Run Migration Job:** `s3c35c9bd-migrate`
- **Artifact Registry Repository:** `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd`
- **Public GitHub Repository:** `https://github.com/ShrekIsLife1/AttalHaterAccount` (branch `main`)

### Issue #16 Verification Checklist
- [x] Course GCP Portal accessed via registered student Google account (`https://cpe334-student-cloud-4d7hbszvwq-as.a.run.app`).
- [x] Public repository verified in incognito mode (R-12 compliant).
- [x] GitHub Secret Scanning and Push Protection enabled on repository.
- [x] Course Cloud Resources activated and provisioned for team prefix `s3c35c9bd`:
  - Artifact Registry repository initialized.
  - Dedicated smallest-tier Cloud SQL PostgreSQL instance provisioned.
  - Dedicated Cloud Run runtime service and migration job created.
  - Secret Manager credentials and service account bindings configured.
- [x] Budget and shared course quota controls established.
- [x] Zero credentials or database passwords committed to Git.

---

## 2. Environment Variables & Cloud-Ready Configuration (Issue #17)

Every setting required by the application is sourced exclusively from the process environment. Missing required variables halt startup with a clear error without leaking secret values.

| Variable | Purpose | Secret? | Default / Source |
|---|---|:---:|---|
| `DATABASE_URL` | PostgreSQL connection URL with credentials & schema | **Yes** | Cloud SQL Secret Manager / `.env` in dev |
| `PORT` | HTTP port for the Express backend server | No | `3000` (Cloud Run injects `PORT=8080`) |
| `SESSION_SECRET` | Secret key for cryptographic session validation | **Yes** | Secret Manager / `.env` (min 32 chars in prod) |
| `CORS_ORIGIN` | Allowed client origin for CORS headers | No | `http://localhost:5173` |
| `NODE_ENV` | Runtime environment (`development`, `test`, `production`) | No | `development` |
| `MAX_QTY_PER_LINE` | Domain boundary constraint for maximum line items | No | `10` |
| `GIT_SHA` | Full git commit SHA passed at container build time | No | `unknown` (injected via Docker build arg) |
| `SEED_PASSWORD` | Password for initial seeded accounts | **Yes** | Secret Manager / `.env` (insecure fallback rejected in prod) |

### Probes and Endpoints

- `GET /api/health` — Lightweight probe; returns `200 { "status": "ok", "service": "TokTickIT API" }` without accessing the database.
- `GET /api/ready` — Readiness probe; queries database via `SELECT 1`. Returns `200 { "status": "ready", "db": "connected" }` when healthy, or `503 { "status": "not_ready", "db": "disconnected" }` if unreachable.
- `GET /api/version` — Version endpoint; returns `200 { "commit": "<GIT_SHA>" }` without exposing internal environment dumps or stack traces.
