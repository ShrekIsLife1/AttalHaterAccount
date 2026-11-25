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

---

## 3. Docker Containerization & Local Stack Verification (Issue #18)

### Container Architecture & Multi-Stage Build
The unified production container is specified in the root `Dockerfile` and builds both frontend and backend into a single lightweight runtime image:
1. **Stage 1 (`client-builder`)**: Compiles React Vite SPA to static assets in `/app/client/dist`.
2. **Stage 2 (`server-builder`)**: Compiles TypeScript backend and generates Prisma Client.
3. **Stage 3 (`production`)**: Alpine-based minimal Node.js runtime (`node:24-alpine`):
   - Runs as non-root user `USER node` (UID 1000).
   - Injects `GIT_SHA` via build argument `ARG GIT_SHA="dev"` / `ENV GIT_SHA=${GIT_SHA}`.
   - Listens on port `3000` (configurable via `PORT` environment variable for Cloud Run).
   - Serves API routes on `/api/*` and falls back to static SPA `index.html` for client routes.
   - Entrypoint uses `exec "$@"` to pass signals (SIGTERM) directly to PID 1 for graceful Cloud Run termination.

### Local Docker Compose Stack (`docker-compose.yml`)
The local development and testing environment orchestrates four container services:
- `unimerch-db`: PostgreSQL 16 Alpine with persistent named volume `postgres_data` and healthcheck via `pg_isready`.
- `unimerch-migrate`: Transient service running `npx prisma migrate deploy && npm run prisma:seed`.
- `unimerch-server`: Express backend serving the application and probes on port 3000.
- `unimerch-client`: Nginx preview proxy for client development on port 5173.

### Check C-03 Verification Evidence

| Test ID | Command | Verified Behavior / Expected Output | Result |
|---|---|---|:---:|
| **TEST-L5-10** | `docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t unimerch:test .` | Multi-stage build succeeds from clean tree without local node_modules or .env | Pass |
| **TEST-L5-11** | `docker compose up -d --build` | DB becomes healthy, migration & seed exits 0, server responds to `/api/ready` | Pass |
| **TEST-L5-12** | `docker run --rm unimerch:test id -u` | Returns `1000` (non-root `node` user); zero `.env` or `.git` files in container | Pass |
| **TEST-L5-13** | `curl -s localhost:3000/` & `curl -s localhost:3000/api/products` | UI served (`<html...`) and API returns seeded catalog JSON | Pass |
| **TEST-L5-14** | `curl -s localhost:3000/api/version` | Returns `{ "commit": "<GIT_SHA>" }` matching `git rev-parse HEAD` | Pass |

Automated verification script: `scripts/test-container.sh`.

---

## 4. First Cloud Deployment & Live Domain Verification (Issue #20)

### Cloud Architecture & Provisioned Infrastructure
- **GCP Project:** `cpe-se-course-2026` (Region: `asia-southeast1`)
- **Team Resource Prefix:** `s3c35c9bd`
- **Cloud Run Runtime Service:** `s3c35c9bd`
  - Live Public URL: `https://s3c35c9bd-4d7hbszvwq-as.a.run.app`
  - Port: `3000`
  - Memory: `512Mi`, CPU: `1`
  - Scaling: Min instances `0` (scales to zero when idle), Max instances `3`
  - Service Account: `s3c35c9bd-runner@cpe-se-course-2026.iam.gserviceaccount.com`
- **Cloud Run Migration Job:** `s3c35c9bd-migrate`
  - Executes: `sh -c "npx prisma migrate deploy && npm run prisma:seed"`
  - Cloud SQL Connection: Attached via Unix socket `/cloudsql/cpe-se-course-2026:asia-southeast1:s3c35c9bd-pg`
- **Cloud SQL PostgreSQL Instance:** `s3c35c9bd-pg`
  - Database: `s3c35c9bd`
  - User: `s3c35c9bd`
  - Tier: Smallest `db-f1-micro`, storage auto-increase disabled (fixed 10GB SSD)
- **Secret Manager Secrets:**
  - `s3c35c9bd-database-url`: Sourced by Cloud Run service and migration job
  - `s3c35c9bd-admin-password`: Bootstrap operator credentials
  - `s3c35c9bd-demo-password`: Seed password for initial demo customer and operator accounts

### Deployment Execution via Cloud Shell
```bash
# 1. Inspect dry-run commands
DRY_RUN=1 PROJECT_ID="cpe-se-course-2026" REGION="asia-southeast1" bash deploy/deploy.sh

# 2. Execute idempotent deployment
PROJECT_ID="cpe-se-course-2026" REGION="asia-southeast1" bash deploy/deploy.sh --demo
```

### Check C-04 Live Domain Verification Matrix

| Test ID | Level | Verification Criterion | Verification Method / Command | Result |
|---|---|---|---|:---:|
| **TEST-L5-20** | Live | Public endpoint health & readiness | `curl -fsS https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/ready` returns `{"status":"ready","db":"connected"}` | Pass |
| **TEST-L5-21** | Live | Customer order journey (F-01..04) | Sign in as `customer1@example.com` -> browse products -> place order -> verify order detail and server-computed total | Pass |
| **TEST-L5-22** | Live | Business rule rejection (BR-04) | Ordering quantity 0 or out-of-stock product rejected with 400/409, inventory unaffected | Pass |
| **TEST-L5-23** | Live | RBAC boundary security (BR-08) | Customer accessing operator routes (`/api/test/operator-only` or operator screens) receives 403 Forbidden | Pass |
| **TEST-L5-24** | Live | Database persistence across reload | Created order appears in "My Orders" (`/api/orders/my-orders`) and persists across page reloads | Pass |
| **TEST-L5-25** | Config | Resource quotas and secret safety | Cloud Run `min=0`, `max=3`, Cloud SQL `db-f1-micro`, zero secrets in revision environment | Pass |
