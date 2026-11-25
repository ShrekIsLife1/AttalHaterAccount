# Lab 5 Deliverable — Living Document (Evidence Index & Answers)

**Status Legend:** ✅ Complete · 🟡 In Progress · 🔲 Planned · 📸 Screenshot Attached / Captured  
**Target Submission:** `lab5_sec1_AttalHaterAccount.pdf`  
**Public Repository:** [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount)  
**Base Release (Sprint 1):** Commit `c029872` / Tag `v0.1.0-sprint1`  

---

## Answer Part 0: Team and Evidence Index

### 0.1 Team Metadata & Public Infrastructure

| Item | Details |
|---|---|
| **Course & Term** | CPE 334 Software Engineering — Lab 5: Cloud Deployment & CI/CD on GCP |
| **Team / Group Name** | `AttalHaterAccount` (Theme 4 — UniMerch Campus Store) |
| **Student 1 (Ba)** | Baptiste Carré (Student ID: `69540460014`, GitHub: `@ShrekIsLife1`) |
| **Student 2 (Cl)** | Clément Dominique Delrieu (Student ID: `69540460016`, GitHub: `@ClemDelGh`) |
| **Public GitHub Repo** | [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount) (Verified accessible in incognito mode) |
| **Course GCP Project ID** | `cpe-se-course-2026` |
| **GCP Region** | `asia-southeast1` |
| **Team Resource Prefix** | `s3c35c9bd` |
| **Artifact Registry** | `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd` |
| **Cloud Run Service** | `s3c35c9bd` (Planned live URL provisioned in #16 / #20) |
| **Cloud Run Migration Job**| `s3c35c9bd-migrate` |

---

### 0.2 Lab 5 Contribution Table (Pair Work Breakdown)

| Issue | Title | Author | Reviewer | PR Link | Status |
|---|---|:---:|:---:|---|:---:|
| **#16** | GCP account, project, budget alert & baseline | **Ba** | Cl | [PR #44](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/44) | ✅ Merged |
| **#17** | Cloud-ready configuration, probes, `.env.example` | **Cl** | Ba | [PR #45](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/45) | ✅ Merged |
| **#18** | Dockerize application & container verification | **Ba** | Cl | [PR #46](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/46) | ✅ Merged |
| **#19** | CI on Pull Requests (`test-and-docker`, C-01) | **Cl** | Ba | [PR #47](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/47) | ✅ Merged |
| **#20** | First deployment to GCP & domain journey (C-04) | **Ba** | Cl | [PR #48](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/48) | ✅ Merged |
| **#21** | GitHub ↔ GCP (WIF) & failing PR gate (C-02) | **Cl** | Ba | [PR #50](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/50) | ✅ Merged |
| **#22** | Repeatable deploy pipeline & release commit (C-06) | **Ba** | Cl | [PR #51](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/51) | ✅ Merged |
| **#23** | Cloud persistence & rollback verification (C-05) | **Cl** | Ba | [PR #52](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/52) | ✅ Merged |
| **#24** | Cost control: pause/resume Cloud SQL & quota audit | **Ba** | Cl | [PR #49](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/49) | ✅ Merged |
| **#25** | Final deployment documentation & deliverable PDF | **Cl** | Ba | *Pending #24* | 🔲 Planned |

---

### 0.3 Consolidated Evidence Index (Traceability Matrix)

| Rubric Part | Required Evidence | Check / ID | Artifact / Link / Reference | Verification Result |
|---|---|:---:|---|---|
| **Part 0: Team & Index** | Public repo & contribution records | R-10, R-11, R-12 | [GitHub Repository](https://github.com/ShrekIsLife1/AttalHaterAccount) | Incognito verified; alternating roles respected |
| **Part 1: CI & Quality Gate** | CI workflow & passing PR | C-01, R-05 | `.github/workflows/ci-docker.yml`, [PR #47](https://github.com/ShrekIsLife1/AttalHaterAccount/pull/47) | `test-and-docker` passes on every PR (TEST-L5-15..19) |
| **Part 1: CI & Quality Gate** | Branch protection & blocked failing PR | C-02, R-06 | Branch `test/intentionally-failing-ci-gate` PR; `deployment.md` Sec 5 | Merge gate verified — blocked PR + passing PR (TEST-L5-26..31) |
| **Part 2: Docker & Config** | Unified multi-stage Dockerfile & clean build | C-03, R-01 | [Dockerfile](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/Dockerfile), `TEST-L5-10` | Builds cleanly from clean tree with GIT_SHA |
| **Part 2: Docker & Config** | Local compose stack runs with `.env.example` | C-03, R-01 | [docker-compose.yml](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/docker-compose.yml), `TEST-L5-11` | DB healthy, migrations pass, `/api/ready` 200 |
| **Part 2: Docker & Config** | Non-root user & zero secrets baked in | R-01, R-02 | `TEST-L5-12` (`node` UID 1000) | No `.env` or `.git` in image |
| **Part 2: Docker & Config** | Environment table & no secrets committed | R-02 | [deployment.md](file:///home/lapulga/Documents/cours/Thailande/SWE/lab%20duo/AttalHaterAccount/docs/labs/lab05/deployment.md) Sec 2 | 8 variables documented; Secret Scanning active |
| **Part 3: GCP & Persistence** | Live domain customer ordering journey | C-04, R-03 | Public Cloud Run URL, `deployment.md` Sec 4 | Verified live customer ordering journey, RBAC, persistence (TEST-L5-20..25) |
| **Part 3: GCP & Persistence** | Data persistence across service restart | C-05, R-04 | `deployment.md` Sec 8; Prisma migrations additive; scale-to-zero + redeploy + rollback verified | TEST-L5-43..47 all Pass |
| **Part 4: Release Pipeline** | Continuous deployment on merge to main | C-06, R-07 | `.github/workflows/deploy.yml`, `deployment.md` Sec 6 | Automated release pipeline on merge to main gated by CI (TEST-L5-32..40) |
| **Part 4: Release Pipeline** | Release revision equals commit SHA | R-08 | `GET /api/version` matches release commit, `deploy/release.sh` | Immutable digest resolution and commit SHA verification (TEST-L5-41..42) |

---

## Answer Part 1: CI and Quality Gate (Issues #19 & #21)

### 1.1 CI Workflow Specification (`.github/workflows/ci-docker.yml`)
- **Workflow Name:** `CI & Docker Build`
- **Job Identifier:** `test-and-docker` (Mandatory name, required by grading rubric and branch protection gate)
- **Triggers:**
  - `workflow_call`: Enables reusable invocation by `deploy.yml`.
  - `pull_request`: Evaluates all pull requests targeting `lab5-staging` or `main`.
  - `workflow_dispatch`: Allows manual test runs from GitHub Actions console.
- **Service Container:** Ephemeral `postgres:16-alpine` database service with automated readiness healthchecks (`pg_isready`).
- **Pipeline Pipeline Stages:**
  1. **Source Checkout:** `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`.
  2. **Runtimes Setup:** Node.js 20 with npm caching, Python 3.12 for offline deploy scripts.
  3. **Script Syntax & Stub Verification:** Syntax check (`bash -n`) and mocked execution of `deploy.sh`, `release.sh`, `smoke_test.py` (`TEST-L5-19`).
  4. **Backend Validation:** Clean dependency installation (`npm ci`), Prisma migration (`npx prisma migrate deploy`), idempotency seed verification (`npm run seed`), and Vitest test suite (`npm test`).
  5. **Frontend Validation:** Client Vitest suite (`npm test`) and React production bundle compilation (`npm run build`).
  6. **Container Verification:** Builds production multi-stage Docker image (`docker build --build-arg GIT_SHA=...`).

### 1.2 Check C-01: Passing Pull Request Verification
- Every PR into `lab5-staging` triggers `test-and-docker`.
- Zero bypasses (`continue-on-error: false`); all test assertions must pass for the check to succeed.
- Comprehensive test results and counts are reported across backend, frontend, deploy stubs, and container build.

### 1.3 Check C-02: Branch Protection & Failing PR Merge Gate (Issue #21)

**Workload Identity Federation (R-06, R-09):**
- GitHub Actions authenticates to GCP using short-lived OIDC tokens via `google-github-actions/auth@v3` — no long-lived service-account JSON key is stored in GitHub.
- WIF provider and service account are stored as repository variables (`WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`) in `Settings → Environments → demo`.
- The `deploy.yml` job authenticates without `credentials_json`; the token expires after 1 hour.

**Branch Protection Ruleset (R-09):**
- Both `lab5-staging` and `main` branches have branch protection rules requiring `test-and-docker` to pass before any PR can be merged.
- GitHub blocks the "Merge pull request" button for any PR where `test-and-docker` has not completed successfully.

**Failing PR Demonstration (C-02):**
- Branch `test/intentionally-failing-ci-gate` was created from `lab5-staging` with a deliberately broken assertion (`expect(true).toBe(false)` in the health test).
- A PR was opened targeting `lab5-staging`; `test-and-docker` failed; GitHub displayed **"Required status checks must pass before merging"** and disabled the merge button.
- The temporary branch was closed without merging after capturing the evidence.

| Test ID | Criterion | Result |
|---|---|:---:|
| **TEST-L5-26** | WIF: no JSON key; OIDC exchange via `google-github-actions/auth` | Pass |
| **TEST-L5-27** | WIF variables in `Settings → Environments → demo` | Pass |
| **TEST-L5-28** | `lab5-staging` requires `test-and-docker` as required status check | Pass |
| **TEST-L5-29** | `main` requires `test-and-docker` as required status check | Pass |
| **TEST-L5-30** | Failing PR blocked: merge button disabled, "Required status checks must pass" shown | Pass |
| **TEST-L5-31** | Passing PR (this PR #50) unblocked: all checks pass, merge enabled | Pass |

---

## Answer Part 2: Docker and Reproducible Configuration (Issues #17 & #18)

### 2.1 Unified Production Container (`Dockerfile`)
- **Multi-Stage Architecture:**
  - Stage 1 (`client-builder`): Compiles React TypeScript Vite SPA (`npm run build`) to static assets in `/app/client/dist`.
  - Stage 2 (`server-builder`): Generates Prisma Client (`npx prisma generate`) and compiles TypeScript Express backend (`npm run build`).
  - Stage 3 (`production`): Minimal Alpine runtime (`node:24-alpine`) running as unprivileged user `USER node` (UID 1000). Serves both the REST API and the React SPA on port 3000.
- **Traceability (`GIT_SHA`):** Injected as build argument (`ARG GIT_SHA="dev"`), exposed via `ENV GIT_SHA=${GIT_SHA}`, and queried by `GET /api/version` (TEST-L5-14).
- **Graceful Shutdown:** `ENTRYPOINT ["./docker-entrypoint.sh"]` with `exec "$@"` ensures PID 1 receives SIGTERM signals from Cloud Run.

### 2.2 Local Container Stack (`docker-compose.yml`)
- Orchestrates:
  - `unimerch-db`: PostgreSQL 16 Alpine with persistent volume `postgres_data` and healthcheck via `pg_isready`.
  - `unimerch-migrate`: Transient container executing `npx prisma migrate deploy && npm run prisma:seed`.
  - `unimerch-server`: Express backend serving the application on port 3000.
  - `unimerch-client`: Preview reverse-proxy on port 5173.
- Starts out of the box using only default values from `.env.example`.

### 2.3 Check C-03 & Container Test Suite (`TEST-L5-10` to `TEST-L5-14`)

Automated script: `scripts/test-container.sh`.

```bash
# Execution Command
bash scripts/test-container.sh
```

| Test ID | Verified Criteria | Evidence / Result |
|---|---|:---:|
| **TEST-L5-10** | `docker build .` succeeds from clean tree with `GIT_SHA` build arg | Pass (Built `unimerch:test`) |
| **TEST-L5-11** | `docker compose up --build` with `.env.example`: DB healthy, migration/seed exits 0, `/api/ready` 200 | Pass (`{"status":"ready","db":"connected"}`) |
| **TEST-L5-12** | Container runs as non-root (`id -u` = 1000) and contains zero `.env` or `.git` files | Pass (UID 1000, zero secrets found) |
| **TEST-L5-13** | UI served (`GET /` returns HTML) and API reachable (`GET /api/products`) | Pass (HTML returned & catalog JSON received) |
| **TEST-L5-14** | `GET /api/version` matches `GIT_SHA` passed at build time | Pass (`{"commit":"<GIT_SHA>"}`) |

### 2.4 Cloud-Ready Environment Configuration (Issue #17)
- All runtime configurations read strictly from environment variables via Zod schema validation in `server/src/config.ts`.
- `.env.example` contains only harmless placeholders (`DATABASE_URL`, `SESSION_SECRET`, `PORT`, `CORS_ORIGIN`, `NODE_ENV`, `MAX_QTY_PER_LINE`, `GIT_SHA`, `SEED_PASSWORD`).
- Zero passwords, tokens, or connection strings committed to Git. GitHub Push Protection and Secret Scanning active.

---

## Answer Part 3: GCP Deployment and Persistence (Issues #16, #20, #23, #24)

### 3.1 Course GCP Infrastructure Setup (Issue #16)
- Course Project ID: `cpe-se-course-2026` (Region: `asia-southeast1`)
- Team Prefix: `s3c35c9bd`
- Dedicated Smallest-Tier Cloud SQL PostgreSQL Instance provisioned: `s3c35c9bd-pg`.
- Cloud Run Service (`s3c35c9bd`) and Migration Job (`s3c35c9bd-migrate`) created.
- Budget alert configured with thresholds (50%, 90%, 100%) and notification to team.

### 3.2 First Cloud Deployment & Live Domain Journey (Issue #20 / Check C-04)
- **Live Public URL:** `https://s3c35c9bd-4d7hbszvwq-as.a.run.app`
- **Cloud Run Service Configuration:**
  - Runtime image: `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd/s3c35c9bd:latest`
  - Port: `3000` (non-root `USER node`)
  - Resource limits: `512Mi` RAM, `1` vCPU, `min-instances=0`, `max-instances=3`
  - Dedicated IAM Service Account: `s3c35c9bd-runner@cpe-se-course-2026.iam.gserviceaccount.com`
  - Secrets injected via Secret Manager: `DATABASE_URL=s3c35c9bd-database-url:latest`
- **Migration & Idempotent Seed:**
  - Executed via Cloud Run Job `s3c35c9bd-migrate` using `npx prisma migrate deploy && npm run prisma:seed`.
  - Cloud SQL connectivity verified via Unix socket proxy.

#### Check C-04 Live Verification Summary

| Test ID | Criterion Proved | Verification Result & Evidence |
|---|---|:---:|
| **TEST-L5-20** | Live health & ready probes | `GET /api/ready` returns 200 `{ "status": "ready", "db": "connected" }` |
| **TEST-L5-21** | Customer ordering journey | Customer signs in -> adds products to cart -> checkout places order -> order detail displays server-calculated total |
| **TEST-L5-22** | Business rule rejection | Ordering zero quantity or unavailable product rejected with 400/409; stock preserved |
| **TEST-L5-23** | RBAC boundary security | Customer prevented from accessing operator routes (`/api/test/operator-only` returns 403 Forbidden) |
| **TEST-L5-24** | Database persistence | Created customer order visible in "My Orders" (`/api/orders/my-orders`) across page reload |
| **TEST-L5-25** | Quotas & secret protection | Cloud Run min=0 / max=3; Cloud SQL db-f1-micro; zero plain-text secrets in revision config |

### 3.3 Cost Control, Pause/Resume & Teardown Procedures (Issue #24)

#### Inactivity Billing Architecture
- **Cloud Run Compute:** Employs dynamic serverless autoscaling with `min-instances=0`. In the absence of incoming HTTP requests, active instances drop to 0 within minutes, resulting in zero idle CPU/RAM billing.
- **Cloud SQL Compute:** Running `db-f1-micro` instance incurs fixed hourly compute charges (~$10–13/month). Storage (10 GB SSD) incurs ~$1.70/month.
- **Inactivity Pause Procedure:** Pausing the database stops compute charges while retaining persistent storage data. Revoking `allUsers` invoker prevents accidental external invocation.

#### CLI Inactivity Commands
```bash
# PAUSE
gcloud run services remove-iam-policy-binding s3c35c9bd --member=allUsers --role=roles/run.invoker --region=asia-southeast1 --project=cpe-se-course-2026
gcloud sql instances patch s3c35c9bd-pg --activation-policy=NEVER --project=cpe-se-course-2026

# RESUME
gcloud sql instances patch s3c35c9bd-pg --activation-policy=ALWAYS --project=cpe-se-course-2026
# Wait until state is RUNNABLE, then re-open public traffic:
gcloud run services add-iam-policy-binding s3c35c9bd --member=allUsers --role=roles/run.invoker --region=asia-southeast1 --project=cpe-se-course-2026
```

#### Verification Matrix (TEST-L5-48 to TEST-L5-51)
| Test ID | Verified Behavior | Evidence / Result |
|---|---|:---:|
| **TEST-L5-48** | Service resume procedure | Cloud SQL patched `--activation-policy=ALWAYS`; `GET /api/ready` returns 200 `{"status":"ready","db":"connected"}` |
| **TEST-L5-49** | Database persistence after resume | Previously placed orders remain visible via `/api/orders/my-orders`; schema and products intact |
| **TEST-L5-50** | Graceful 503 handling while paused | When DB is paused, `GET /api/ready` returns 503 `{"status":"not_ready","db":"disconnected"}`; zero crashes, zero secret leaks |
| **TEST-L5-51** | Idle scale-to-zero & quota audit | Cloud Run `min-instances=0`, `max-instances=3`, `memory=512Mi`; GCP Budget alert configured with 50%, 90%, 100% notification thresholds |

#### End-of-Term Teardown Safety (`deploy/teardown.sh`)
- Strictly scheduled for end of academic term after grading confirmation.
- Contains interactive prompts (`DRY_RUN=1` support), systematically deleting Cloud Run services, migration jobs, Artifact Registry images, and Cloud SQL instances.

### 3.4 Cloud Persistence & Rollback Verification (Issue #23 / Check C-05)

**Core guarantee:** All user data lives in Cloud SQL, not in the container. The Cloud Run instance is fully stateless — it can be replaced, restarted, or rolled back without any data loss.

**Persistence across lifecycle events:**
- **Scale-to-zero restart:** Container shuts down after idle timeout, starts fresh on next request. Orders created before the restart are retrieved unchanged from Cloud SQL.
- **Redeployment:** `release.sh` runs additive Prisma migrations then swaps the Cloud Run image. Existing records (users, orders, sessions) persist throughout.
- **Pause/resume cycle (Issue #24):** Cloud SQL paused (`--activation-policy=NEVER`) then resumed (`--activation-policy=ALWAYS`). All pre-pause data intact after resume.
- **Fast rollback:** `workflow_dispatch` with `image_tag` = prior SHA points Cloud Run to a previous revision. Cloud SQL is not touched — no downgrade migration. `GET /api/version` reflects the rolled-back SHA; orders accessible immediately.

**Migration safety:** `grep -rn "DROP TABLE\|DROP COLUMN" prisma/migrations/` returns zero results — migrations are strictly additive (R-04 compliant).

| Test ID | Criterion | Evidence / Result |
|---|---|:---:|
| **TEST-L5-43** | Data survives Cloud Run scale-to-zero/restart | Orders from #20 retrieved after idle restart via `GET /api/orders/my-orders` |
| **TEST-L5-44** | Data survives redeployment via `release.sh` | Orders unchanged after `workflow_dispatch` redeployment; order IDs identical |
| **TEST-L5-45** | Prisma migrations are additive (no DROP statements) | Zero `DROP TABLE` or `DROP COLUMN` in `prisma/migrations/` |
| **TEST-L5-46** | Data survives Cloud SQL pause/resume cycle | Orders intact after resume (see Issue #24 TEST-L5-49) |
| **TEST-L5-47** | Fast rollback via `image_tag` leaves Cloud SQL unchanged | `GET /api/version` returns prior SHA; orders accessible post-rollback |

---

## Answer Part 4: Repeatable Release Pipeline (Issue #22 / Check C-06)

### 4.1 Continuous Deployment Pipeline Specification (`.github/workflows/deploy.yml`)

The repository implements an automated, keyless continuous deployment pipeline to Google Cloud Run:
- **Triggers:**
  - `push` to `main`: Automatically triggered when a release Pull Request from `lab5-staging` is merged.
  - `workflow_dispatch`: Manual trigger with optional input `image_tag` for zero-migration instant rollbacks.
- **Sequential Job Execution:**
  1. `test`: Calls reusable workflow `ci-docker.yml` (running job `test-and-docker`). Validates offline stubs, PostgreSQL migrations/seeds, backend Vitest suite, frontend build, and Docker multi-stage build.
  2. `deploy`: Depends on `needs: test`. Only runs if `needs.test.result == 'success'`.

### 4.2 Security, Traceability and Deployment Flow
- **Keyless Authentication (WIF):** Authenticates via Workload Identity Federation using `google-github-actions/auth` and repository variables `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` from `environment: demo`. No long-lived service account JSON key exists in GitHub.
- **Traceable Container Build:** Image is built with `--build-arg GIT_SHA=$IMAGE_TAG` and published as `asia-southeast1-docker.pkg.dev/cpe-se-course-2026/s3c35c9bd/s3c35c9bd:<commit-sha>`.
- **Immutable Digest Resolution:** `deploy/release.sh` resolves the tag to its immutable `@sha256:...` digest so that the migration job and Cloud Run service run the exact same binary.
- **Automated Migration Gate:** Cloud Run Job `s3c35c9bd-migrate` is updated to the image digest and executed with `--wait`. If database migrations fail, the pipeline halts immediately, leaving the production service untouched.
- **Zero-Downtime Traffic Migration:** Cloud Run Service `s3c35c9bd` is updated with the new digest, and traffic is cut over to 100% on latest revision.
- **Automated Smoke Test:** `deploy/smoke_test.py` validates `/api/health`, `/api/ready`, `/`, and `/api/products` on the live URL with retry handling.
- **Verification of R-08:** `curl https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/version` returns `{ "commit": "<GIT_SHA>" }` matching the release commit.

### 4.3 Instant Rollback Capability
Running the workflow via `workflow_dispatch` with `image_tag=<PREVIOUS_40_CHAR_SHA>` activates rollback mode:
- Tests, build, and migration are bypassed (`ROLLBACK=true`).
- Cloud Run service traffic is pointed directly to the pre-existing container digest in under 15 seconds.

### 4.4 Check C-06 Verification Matrix

| Test ID | Criterion Proved | Verification Evidence | Result |
|---|---|---|:---:|
| **TEST-L5-32** | CD Workflow Triggers | `push` to `main` + `workflow_dispatch` rollback trigger | Pass |
| **TEST-L5-33** | Quality Gate Enforcement | `deploy` requires `test-and-docker` passing (`needs: test`) | Pass |
| **TEST-L5-34** | Broken Build Prevention | Failing CI step blocks `deploy` job from starting | Pass |
| **TEST-L5-35** | Keyless WIF Auth | Token exchange via `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` | Pass |
| **TEST-L5-36** | Tagged Container Build | Published image tagged with full commit SHA and `GIT_SHA` arg | Pass |
| **TEST-L5-37** | Immutable Digest Pinning | Resolved to `@sha256:` digest before execution | Pass |
| **TEST-L5-38** | Migration Pre-Deployment | `s3c35c9bd-migrate` executes `--wait` before service update | Pass |
| **TEST-L5-39** | Traffic Cutover | Service updated and traffic directed 100% to latest revision | Pass |
| **TEST-L5-40** | Automated Smoke Testing | `deploy/smoke_test.py` confirms health, DB ready, HTML, products | Pass |
| **TEST-L5-41** | Traceability R-08 | Live `/api/version` commit matches release commit SHA | Pass |
| **TEST-L5-42** | Fast Rollback | Rollback restores prior revision without running migrations | Pass |
