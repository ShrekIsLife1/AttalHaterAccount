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

---

## 5. Cost Control, Pause/Resume & Teardown Procedures (Issue #24)

### Cost Model & Inactivity Strategy
In the provisioned GCP architecture for team `s3c35c9bd`, resources incur costs according to two distinct billing models:
1. **Cloud Run (`s3c35c9bd`)**: Pay-per-request serverless compute. Configured with `--min-instances=0`, Cloud Run automatically scales to zero instances when no HTTP requests are arriving, incurring **$0.00** compute charges during idle periods.
2. **Cloud SQL PostgreSQL (`s3c35c9bd-pg`)**: Continuous instance pricing. A running `db-f1-micro` instance incurs compute charges 24/7 (~$10–13/month) regardless of whether requests arrive. Storage (10 GB SSD) incurs ~$1.70/month regardless of instance state.

To prevent quota exhaustion and unnecessary cloud spend during idle periods (weekends, breaks, between sprints), the team applies a **Pause Procedure** that stops the Cloud SQL instance and revokes public traffic to Cloud Run.

---

### Step-by-Step Pause Procedure

When leaving the environment idle, run the following commands (or perform the Console equivalent):

#### 1. CLI Commands to Pause
```bash
# Set environment variables
export PROJECT_ID="cpe-se-course-2026"
export REGION="asia-southeast1"
export SERVICE_NAME="s3c35c9bd"
export SQL_INSTANCE="s3c35c9bd-pg"

# Step 1: Revoke unauthenticated public access to Cloud Run (prevents unwanted traffic)
gcloud run services remove-iam-policy-binding "${SERVICE_NAME}" \
  --region="${REGION}" \
  --project="${PROJECT_ID}" \
  --member="allUsers" \
  --role="roles/run.invoker"

# Step 2: Stop Cloud SQL compute instance (halts hourly compute billing)
gcloud sql instances patch "${SQL_INSTANCE}" \
  --project="${PROJECT_ID}" \
  --activation-policy="NEVER"
```

#### 2. GCP Web Console Walkthrough to Pause
1. **Stop Cloud SQL:**
   - In GCP Console, navigate to **SQL** -> Click instance **`s3c35c9bd-pg`**.
   - In the top action bar, click **Stop**.
   - Confirm stop. The instance status changes to *Stopped* (`activationPolicy=NEVER`). Data on SSD storage remains completely preserved.
2. **Revoke Public Ingress:**
   - Navigate to **Cloud Run** -> Click service **`s3c35c9bd`**.
   - Click the **Security** tab -> under **Authentication**, verify ingress is restricted, or under **Permissions**, remove `allUsers` with role `Cloud Run Invoker`.

#### 3. Verified System Behavior While Paused (`TEST-L5-50`)
- **Public HTTP Requests:** External visitors receive `403 Forbidden` from Google Cloud's frontend before hitting any container compute.
- **Service Invocation with DB Paused:** If invoked via internal service account or authenticated token while Cloud SQL is paused, the backend readiness probe (`GET /api/ready`) gracefully catches connection timeouts and returns:
  ```json
  HTTP/1.1 503 Service Unavailable
  {
    "status": "not_ready",
    "db": "disconnected"
  }
  ```
  The process does not crash (PID 1 survives) and leaks zero internal connection strings or stack traces.

---

### Step-by-Step Resume Procedure

When resuming active development, testing, or grading evaluation:

#### 1. CLI Commands to Resume
```bash
export PROJECT_ID="cpe-se-course-2026"
export REGION="asia-southeast1"
export SERVICE_NAME="s3c35c9bd"
export SQL_INSTANCE="s3c35c9bd-pg"

# Step 1: Start Cloud SQL instance
gcloud sql instances patch "${SQL_INSTANCE}" \
  --project="${PROJECT_ID}" \
  --activation-policy="ALWAYS"

# Step 2: Poll instance status until RUNNABLE
echo "Waiting for Cloud SQL instance ${SQL_INSTANCE} to become RUNNABLE..."
while true; do
  STATUS=$(gcloud sql instances describe "${SQL_INSTANCE}" --project="${PROJECT_ID}" --format="value(state)")
  echo "Current state: ${STATUS}"
  if [ "${STATUS}" = "RUNNABLE" ]; then
    break
  fi
  sleep 5
done

# Step 3: Re-grant public unauthenticated access to Cloud Run
gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --region="${REGION}" \
  --project="${PROJECT_ID}" \
  --member="allUsers" \
  --role="roles/run.invoker"

# Step 4: Verify live service readiness
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(status.url)")
curl -fsS "${SERVICE_URL}/api/ready"
```

#### 2. GCP Web Console Walkthrough to Resume
1. Navigate to **SQL** -> Click **`s3c35c9bd-pg`** -> Click **Start**. Wait ~60–90 seconds for status to show a green checkmark (*Runnable*).
2. Navigate to **Cloud Run** -> Click **`s3c35c9bd`** -> **Security** -> **Permissions** -> Click **Add Principal** -> Principal: `allUsers`, Role: `Cloud Run Invoker` -> Save.
3. Access the Cloud Run public URL in browser to verify that UniMerch loads immediately.

#### 3. Verified System Behavior After Resume (`TEST-L5-48` & `TEST-L5-49`)
- `GET /api/ready` returns `200 {"status":"ready","db":"connected"}`.
- All database state (seed users, catalog products, customer order history created in Issue #20) persists intact without data corruption.

---

### Teardown Procedure (`deploy/teardown.sh`)

> [!CAUTION]
> **DO NOT execute teardown during the active semester or while grading is pending.**  
> Teardown permanently deletes cloud resources and is strictly reserved for the end-of-term cleanup after final course grade confirmation.

The automated cleanup script `deploy/teardown.sh` safely deprovisions resources with safety checks:
1. **Interactive Confirmation:** Prompts for explicit confirmation before proceeding (`DRY_RUN=1` can be passed to preview actions).
2. **Cloud Run Service & Job Cleanup:** Deletes service `s3c35c9bd` and migration job `s3c35c9bd-migrate`.
3. **Artifact Registry Images:** Removes published container digests from repository `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd/s3c35c9bd`.
4. **Cloud SQL Termination:** Deletes PostgreSQL instance `s3c35c9bd-pg` after prompting for double confirmation.

```bash
# Preview teardown actions without deleting
DRY_RUN=1 bash deploy/teardown.sh

# Live teardown (End-of-term ONLY)
PROJECT_ID="cpe-se-course-2026" REGION="asia-southeast1" bash deploy/teardown.sh
```

---

### Check Cost Control Verification Matrix

| Test ID | Criterion Proved | Verification Command / Evidence | Result |
|---|---|---|:---:|
| **TEST-L5-48** | Service resume procedure | Cloud SQL patched `--activation-policy=ALWAYS`; `GET /api/ready` returns 200 `{"status":"ready","db":"connected"}` | Pass |
| **TEST-L5-49** | Database persistence after resume | Previously placed orders remain visible via `/api/orders/my-orders`; schema and products intact | Pass |
| **TEST-L5-50** | Graceful 503 handling while paused | When DB is paused, `GET /api/ready` returns 503 `{"status":"not_ready","db":"disconnected"}`; zero crashes, zero secret leaks | Pass |
| **TEST-L5-51** | Idle scale-to-zero & quota audit | Cloud Run `min-instances=0`, `max-instances=3`, `memory=512Mi`; GCP Budget alert configured with 50%, 90%, 100% notification thresholds | Pass |

