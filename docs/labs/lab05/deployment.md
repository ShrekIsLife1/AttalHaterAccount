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

## 5. GitHub ↔ GCP Integration: Workload Identity Federation & Merge Gate (Issue #21)

### Workload Identity Federation (R-06, R-09)

GitHub Actions authenticates to Google Cloud **without any long-lived service-account JSON key**. Instead, the runner exchanges a short-lived GitHub OIDC token for a GCP access token using Workload Identity Federation (WIF).

**How it works (keyless flow):**
1. GitHub Actions generates a short-lived OIDC token signed by `token.actions.githubusercontent.com`.
2. The `google-github-actions/auth` action sends that token to the GCP STS API.
3. GCP validates the token against the WIF pool binding (repo/branch conditions) and returns a scoped access token.
4. The runner uses that token for all subsequent `gcloud`/Docker registry operations — the token expires after 1 hour with no rotation needed.

**Repository / Environment Variables (not secrets):**

| Variable | Value (GitHub `Settings → Environments → demo`) |
|---|---|
| `WIF_PROVIDER` | `projects/670075229477/locations/global/workloadIdentityPools/s3c35c9bd-pool/providers/s3c35c9bd-provider` |
| `WIF_SERVICE_ACCOUNT` | `s3c35c9bd-deployer@cpe-se-course-2026.iam.gserviceaccount.com` |
| `GCP_PROJECT_ID` | `cpe-se-course-2026` |
| `GCP_REGION` | `asia-southeast1` |

No `credentials_json` secret is present in the repository. Zero long-lived credentials are stored in GitHub.

**Relevant `deploy.yml` step:**
```yaml
- name: Authenticate to Google Cloud without a key
  uses: google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093 # v3
  with:
    workload_identity_provider: ${{ vars.WIF_PROVIDER }}
    service_account: ${{ vars.WIF_SERVICE_ACCOUNT }}
```

### Branch Protection Ruleset (R-09, C-02)

Both `lab5-staging` and `main` branches require the `test-and-docker` status check to pass before any pull request can be merged.

**Configuration (`Settings → Branches`):**
- **Protected branches:** `lab5-staging`, `main`
- **Required status check:** `test-and-docker` (job id defined in `.github/workflows/ci-docker.yml`)
- **Effect:** GitHub disables the "Merge pull request" button for any PR where `test-and-docker` has not completed with status `success`.

### Check C-02: Failing PR Blocked by Merge Gate

To demonstrate the merge gate in action, a temporary branch `test/intentionally-failing-ci-gate` was created from `lab5-staging` with a deliberately failing assertion:

```typescript
// server/tests/lab5/health.api.test.ts — intentional failure for C-02 demo
it("INTENTIONAL FAILURE — merge gate demo", () => {
  expect(true).toBe(false); // This always fails
});
```

This branch was opened as a PR into `lab5-staging`. The `test-and-docker` job failed, and GitHub blocked the merge with the message **"Required status checks must pass before merging"**. The merge button remained disabled until the failing branch was closed without merging.

### Check C-02 Verification Matrix

| Test ID | Level | Verification Criterion | Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-26** | WIF | No JSON key stored in GitHub; auth uses OIDC token exchange | `deploy.yml` uses `google-github-actions/auth` with `WIF_PROVIDER`/`WIF_SERVICE_ACCOUNT` variables; zero `credentials_json` present | Pass |
| **TEST-L5-27** | WIF | WIF variables set in `environment: demo` | `Settings → Environments → demo` Variables shows `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` configured | Pass |
| **TEST-L5-28** | Branch Protection | `lab5-staging` requires `test-and-docker` to pass | `Settings → Branches` protection rule for `lab5-staging` lists `test-and-docker` as required check | Pass |
| **TEST-L5-29** | Branch Protection | `main` requires `test-and-docker` to pass | `Settings → Branches` protection rule for `main` lists `test-and-docker` as required check | Pass |
| **TEST-L5-30** | Merge Gate (C-02) | Failing PR is blocked from merging | Branch `test/intentionally-failing-ci-gate` → PR into `lab5-staging`; merge button disabled; "Required status checks must pass" shown | Pass |
| **TEST-L5-31** | Merge Gate (C-02) | Passing PR is unblocked and merged | PR #21 (`issue/21-github-gcp-merge-gate` → `lab5-staging`); all checks pass; merge enabled | Pass |

---

## 6. Continuous Deployment Pipeline & Release Workflow (Issue #22 / Check C-06)

### Architecture of Continuous Deployment (`.github/workflows/deploy.yml`)

The production continuous deployment pipeline is triggered automatically whenever code is merged into the `main` branch, or manually via `workflow_dispatch` (used for rollbacks).

```
[ Push / Merge to main ]
          │
          ▼
   ┌──────────────┐
   │   Job 1:     │ ──(uses ci-docker.yml: test-and-docker)
   │    test      │ ──[ Deploy stubs -> Server tests -> Client tests -> Docker build ]
   └──────┬───────┘
          │ (Only on success; blocks release on any test failure)
          ▼
   ┌──────────────┐
   │   Job 2:     │ ──(Environment: demo)
   │    deploy    │
   └──────┬───────┘
          ├─► 1. Validate inputs (IMAGE_TAG must be 40-char SHA)
          ├─► 2. Authenticate to GCP keyless via Workload Identity Federation (WIF)
          ├─► 3. Build & push image tagged with commit SHA:
          │      asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd/s3c35c9bd:<SHA>
          ├─► 4. Run deploy/release.sh:
          │      ├─ Pin image to immutable @sha256 digest
          │      ├─ Run migration job s3c35c9bd-migrate (--wait)
          │      └─ Update Cloud Run service s3c35c9bd & traffic --to-latest
          ├─► 5. Execute automated smoke test (deploy/smoke_test.py):
          │      [ /api/health 200, /api/ready db:connected, / HTML, /api/products catalog ]
          └─► 6. Write GitHub step summary with commit SHA, digest, and URL
```

### Key Security & Integrity Controls

1. **Gate before Deploy (`needs: test`):**
   The `deploy` job never executes if the `test` job (`test-and-docker`) fails or is cancelled. Broken code never triggers image building, database migration, or Cloud Run deployment.
2. **Workload Identity Federation (Keyless Auth):**
   The runner requests a short-lived OIDC federated token from GCP using `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT`. No static JSON key exists in GitHub Secrets.
3. **Immutable Digest Pinning (`@sha256:...`):**
   `deploy/release.sh` resolves the tag to an immutable container digest before executing the migration job and updating the service. This guarantees that the exact same tested binary runs the database migrations and serves user requests.
4. **Automated Migration Gate (`--wait`):**
   `s3c35c9bd-migrate` runs before the service is updated. If the database migration fails, `deploy/release.sh` exits immediately with code 1 (`set -e`), leaving the running Cloud Run service completely untouched.
5. **Traceability via `GIT_SHA` (R-08):**
   Docker is built with `--build-arg GIT_SHA=$IMAGE_TAG`. Querying `GET /api/version` on the live Cloud Run URL returns `{ "commit": "<GIT_SHA>" }` exactly matching the released Git commit SHA.
6. **Zero-Migration Rollback Mechanism:**
   When triggering `deploy.yml` via `workflow_dispatch` with an existing commit SHA in `image_tag`:
   - `test` job is skipped (`!inputs.image_tag`).
   - Image build is skipped (`env.ROLLBACK == 'true'`).
   - Migration job is skipped (`ROLLBACK == true` in `release.sh`).
   - Cloud Run service is instantly pointed to the previous `@sha256` digest and receives 100% traffic in seconds.

---

### Check C-06 Verification Matrix

| Test ID | Level | Verification Criterion | Evidence / Command | Result |
|---|---|---|---|:---:|
| **TEST-L5-32** | CD Workflow | Trigger on push to `main` and `workflow_dispatch` | `.github/workflows/deploy.yml` triggers configuration | Pass |
| **TEST-L5-33** | CD Workflow | `test-and-docker` CI gate runs before `deploy` | `deploy` job has `needs: test` and condition `needs.test.result == 'success'` | Pass |
| **TEST-L5-34** | CD Workflow | Broken test halts release pipeline before GCP call | CI test failure skips `deploy` job completely | Pass |
| **TEST-L5-35** | WIF | Keyless deployment authentication via WIF | `google-github-actions/auth` exchanges GitHub token for GCP STS token | Pass |
| **TEST-L5-36** | Container | Release image built with `GIT_SHA` build arg and pushed to Artifact Registry | Image tagged `.../s3c35c9bd/s3c35c9bd:$IMAGE_TAG` | Pass |
| **TEST-L5-37** | Release Script | Tag resolved to immutable `@sha256` digest | `gcloud artifacts docker images describe` in `deploy/release.sh` | Pass |
| **TEST-L5-38** | Release Script | Database migration job executes with `--wait` | `s3c35c9bd-migrate` runs and gates service update | Pass |
| **TEST-L5-39** | Cloud Run | Service updated with digest and traffic set `--to-latest` | `gcloud run services update-traffic s3c35c9bd --to-latest` | Pass |
| **TEST-L5-40** | Smoke Test | Automated post-deploy smoke test validates endpoints | `python3 deploy/smoke_test.py "$SERVICE_URL"` passes all probes | Pass |
| **TEST-L5-41** | Traceability | Live `/api/version` matches release commit SHA | `curl -fsS https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/version` | Pass |
| **TEST-L5-42** | Rollback | Rollback bypasses build and migration | `deploy/release.sh` with `ROLLBACK=true` restores prior digest | Pass |

---

## 7. Cost Control, Pause/Resume & Teardown Procedures (Issue #24)

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


---

## 8. Cloud Persistence & Rollback Verification (Issue #23 / Check C-05)

### Why Persistence Matters

Cloud Run is a stateless serverless platform: the container can be stopped, restarted, or replaced at any moment. All user data must survive these events because it lives exclusively in Cloud SQL — not in the container's filesystem. Issue #23 verifies that this promise holds across every lifecycle event.

### Persistence Guarantees

**1. Stateless Container + Persistent Database**
- The Cloud Run container carries zero user state; every restart begins from a clean image.
- All mutable data (users, orders, sessions) is stored in Cloud SQL PostgreSQL (`s3c35c9bd-pg`).
- Session tokens are stored in the `Session` table (not in-memory), so active sessions survive container replacement.

**2. Additive-Only Prisma Migrations**
- Every migration in `prisma/migrations/` is a forward-only DDL change.
- Verified: `grep -rn "DROP TABLE\|DROP COLUMN" prisma/migrations/` returns zero results.
- The migration job (`s3c35c9bd-migrate`) runs `prisma migrate deploy` — idempotent and safe to replay.

**3. Scale-to-Zero Cycle**
- Cloud Run `min-instances=0` means the container shuts down after ~15 minutes of inactivity.
- On the next request, a new instance starts and immediately reads from Cloud SQL — user data intact.

**4. Pause/Resume Persistence (see Section 7 / Issue #24)**
- Cloud SQL was paused (`--activation-policy=NEVER`) and resumed (`--activation-policy=ALWAYS`).
- All orders placed before the pause remained fully intact after resume — no data loss, no restore needed.

### Redeployment Persistence

When `deploy/release.sh` runs a new release:
1. `s3c35c9bd-migrate` executes `prisma migrate deploy` — only applies new migrations, existing data untouched.
2. Cloud Run traffic is atomically cut over to the new digest via `update-traffic --to-latest`.
3. Old revision is drained gracefully (SIGTERM → 10 s drain window).
4. Existing orders, users, and sessions remain accessible throughout.

### Fast Rollback Without Data Loss

Triggered by `workflow_dispatch` with `image_tag` = previous commit SHA:
- Tests, build, and migration steps are skipped (image already exists in Artifact Registry).
- Cloud Run service is pointed directly to the prior digest.
- **Cloud SQL is not touched** — no downgrade migration, no data loss.
- After rollback, `GET /api/version` reflects the rolled-back SHA; `GET /api/orders/my-orders` returns unchanged orders.

### Check C-05 Verification Matrix

| Test ID | Level | Verification Criterion | Evidence |
|---|---|---|---|
| **TEST-L5-43** | Persistence | Data survives Cloud Run scale-to-zero/restart | Orders created in #20 retrieved after idle restart; `GET /api/orders/my-orders` returns same records |
| **TEST-L5-44** | Persistence | Data survives a full redeployment via `release.sh` | Orders retrieved after `workflow_dispatch` redeployment; order IDs unchanged |
| **TEST-L5-45** | Persistence | Prisma migrations are strictly additive (no DROP) | `grep -rn "DROP TABLE\|DROP COLUMN" prisma/migrations/` returns zero matches |
| **TEST-L5-46** | Persistence | Data survives Cloud SQL pause/resume cycle | Orders intact after `--activation-policy=ALWAYS` resume (see Issue #24 evidence) |
| **TEST-L5-47** | Rollback | Fast rollback via `image_tag` leaves Cloud SQL unchanged | `GET /api/version` returns prior SHA; orders accessible post-rollback |

---

## 9. Final Release & Documentation Sign-Off (Issue #25)

### Final Checklist
- [x] **Public Repository (R-12):** `https://github.com/ShrekIsLife1/AttalHaterAccount` accessible without authentication.
- [x] **Secret Scan:** Zero `.env`, `.key`, `.pem`, or credential files tracked in Git (`git ls-files` verified); GitHub Secret Scanning & Push Protection active.
- [x] **All Tests Passing (TEST-L5-01..58):** Backend, frontend, deploy stubs, container, CI/CD, live Cloud Run, persistence, and cost-control checks documented in `docs/labs/lab05/tests.md`.
- [x] **Minimalist Deliverable Report:** `docs/deliverable-2/PDF_DRAFT.md` and `docs/deliverable-2/lab5_sec1_AttalHaterAccount.pdf` prepared for LEB2 submission.
- [x] **Inactivity Safety:** Pause/resume procedure documented in Section 7 so Cloud SQL compute charges remain controlled after grading.
