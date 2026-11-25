# Lab 5 Software Test Specifications & Traceability Matrix

## Consolidated Lab 5 Test Map

| Requirement / Check | Issue | Planned TEST IDs | Level | Description | Status |
|---|---|---|---|---|:---:|
| **R-12, Cost Control** | #16 | — | Cloud Setup | GCP portal activation, team resources, budget controls, public repo & push protection | ✅ Done |
| **R-02, R-04** | #17 | TEST-L5-01..04, L5-08..09 | Unit / API | Config loader, `.env.example`, session DB persistence, safe production seed | ✅ Done |
| **R-01, C-03** | #18 | TEST-L5-10..14 | Container | Docker multi-stage build from fresh clone, docker-compose local stack, non-root user | ✅ Done |
| **R-05, C-01** | #19 | TEST-L5-15..19 | CI Workflow | GitHub Actions `test-and-docker` job on PRs into `lab5-staging` and `main` | ✅ Done |
| **R-03, R-04, C-04** | #20 | TEST-L5-20..25 | Live / Smoke | First deployment on Cloud Run, live domain customer order journey, failure rejections | ✅ Done |
| **R-06, R-09, C-02** | #21 | TEST-L5-26..31 | Merge Gate | Workload Identity Federation, branch protection ruleset, failing PR blocked | ✅ Done |
| **R-07, R-08, C-06** | #22 | TEST-L5-32..42 | Release Pipeline | `deploy.yml`, automated smoke test, release by commit SHA digest | ✅ Done |
| **R-04, C-05** | #23 | TEST-L5-43..47 | Persistence / Rollback | Data persistence across service restart and redeploy, additive migrations, rollback | 🔲 Planned |
| **Cost Control** | #24 | TEST-L5-48..51 | Operations | Pause/resume Cloud SQL procedure, Cloud Run min=0 instances, spend tracking | ✅ Done |
| **R-08, R-11, DoD** | #25 | TEST-L5-52..58 | Documentation | Final release verification, `deployment.md`, secret scan, and LEB2 deliverable PDF | 🔲 Planned |

---

## Detailed Test Specifications: Issue #17 (Cloud-Ready Configuration)

| TEST ID | Level | Test Description | Target File | Result |
|---|---|---|---|:---:|
| **TEST-L5-01** | Unit | Config loader returns typed values when all variables are set | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-02** | Unit | Missing required variable (`DATABASE_URL`, `SESSION_SECRET`) throws error naming variable without leaking value | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-03** | Unit | Invalid types (`MAX_QTY_PER_LINE=abc`) rejected; production rejects insecure/missing secrets | `server/tests/lab5/config.unit.test.ts` | Pass |
| **TEST-L5-04** | Script | Every `process.env.X` read in `server/src` appears in `.env.example`; contains only placeholders | `server/tests/lab5/env-example.test.ts` | Pass |
| **TEST-L5-05** | API | `GET /api/health` returns 200 `{ status: "ok" }` without database dependency | `server/tests/lab5/health.api.test.ts` | Pass |
| **TEST-L5-06** | API | `GET /api/ready` returns 200 when DB connected, 503 when unreachable | `server/tests/lab5/health.api.test.ts` | Pass |
| **TEST-L5-07** | API | `GET /api/version` returns `GIT_SHA` from environment without leaking sensitive variables | `server/tests/lab5/version.api.test.ts` | Pass |
| **TEST-L5-08** | API | Session persists across requests and survives app restart via PostgreSQL `Session` table | `server/tests/lab5/session-persistence.api.test.ts` | Pass |
| **TEST-L5-09** | Unit/API | Seed in production rejects missing or default `SEED_PASSWORD`; seed is strictly idempotent | `server/tests/lab5/seed-config.test.ts` | Pass |

---

## Detailed Test Specifications: Issue #18 (Dockerize Application)

| TEST ID | Level | Test Description | Verification Method | Result |
|---|---|---|---|:---:|
| **TEST-L5-10** | Container | Unified multi-stage `Dockerfile` builds cleanly from fresh tree with `GIT_SHA` build arg | `docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t unimerch:test .` | Pass |
| **TEST-L5-11** | Container | `docker compose up --build` with `.env.example` starts DB, executes migration/seed, answers `/api/ready` | `docker compose up -d --build && curl -fsS localhost:3000/api/ready` | Pass |
| **TEST-L5-12** | Container | Non-root runtime user (`USER node`, UID ≠ 0); zero `.env` or `.git` files inside container | `docker run --rm unimerch:test id -u` & `find /app -name '.env*'` | Pass |
| **TEST-L5-13** | Container | Unified container serves client SPA at `GET /` and API endpoints at `GET /api/products` | `curl -s localhost:3000/ \| grep -i "<html"` & `curl -s localhost:3000/api/products` | Pass |
| **TEST-L5-14** | Container | `GET /api/version` returns commit SHA exactly matching `GIT_SHA` passed at build time | `curl -s localhost:3000/api/version` matches `git rev-parse HEAD` | Pass |

---

## Detailed Test Specifications: Issue #19 (CI on Pull Requests)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-15** | CI | A PR targeting `lab5-staging` or `main` triggers job `test-and-docker` running all stages (deploy script stubs, server tests, client tests, Docker build) | GitHub Actions workflow trigger & run status | Pass |
| **TEST-L5-16** | CI | Run log captures full test summaries with counts (passed/failed/skipped) for all suites including Lab 5 | GitHub Actions step execution logs | Pass |
| **TEST-L5-17** | CI | Workflow fails when any test step fails; zero `continue-on-error` or `\|\| true` bypasses | Workflow review of `.github/workflows/ci-docker.yml` | Pass |
| **TEST-L5-18** | CI | CI triggers consistently on PRs into both `lab5-staging` and `main`, as well as on `workflow_dispatch` | Workflow triggers `pull_request` branches config | Pass |
| **TEST-L5-19** | CI | Offline deploy script stubs (`test_deploy_stub.sh`, `test_release_stub.sh`, `test_smoke.py`) execute in CI before backend tests | CI step 3 execution | Pass |

---

## Detailed Test Specifications: Issue #20 (First Deployment to GCP)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-20** | Live | Public endpoint health & readiness: `/api/health` 200, `/api/ready` `db:connected`, `/` serves HTML, `/api/products` returns catalog | `curl -fsS https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/ready` | Pass |
| **TEST-L5-21** | Live (C-04) | Full Customer purchasing domain journey: customer logs in -> adds products to cart -> submits order -> receives order detail with server-calculated price | Manual / E2E journey on live Cloud Run URL | Pass |
| **TEST-L5-22** | Live (C-04) | Business rule validation: placing order with invalid quantity or out-of-stock item is rejected with 400/409, inventory unchanged | API / UI rejection check on live service | Pass |
| **TEST-L5-23** | Live (C-04) | Role-Based Access Control: customer is forbidden from accessing operator endpoints (`/api/test/operator-only` -> 403 Forbidden) | RBAC boundary verification on live service | Pass |
| **TEST-L5-24** | Live | End-to-end database persistence: created order is retrieved from Cloud SQL via `/api/orders/my-orders` across page reloads | UI session & order persistence verification | Pass |
| **TEST-L5-25** | Config | Cloud Run & Cloud SQL configuration constraints: min instances 0, max instances ≤ 3, smallest tier Cloud SQL, secrets stored exclusively in Secret Manager | `gcloud run services describe s3c35c9bd` inspection | Pass |

---

## Detailed Test Specifications: Issue #24 (Cost Control: Pause & Resume)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-48** | Operations | Cloud SQL resume procedure: patching instance with `--activation-policy=ALWAYS` transitions state to `RUNNABLE`, Cloud Run service ready probe `/api/ready` recovers to 200 `{ "status": "ready", "db": "connected" }` | CLI patch execution and curl `/api/ready` | Pass |
| **TEST-L5-49** | Operations | Database persistence after pause/resume cycle: existing database records (users, products, customer orders placed in Issue #20) remain fully intact without data loss or corruption | Verify `GET /api/orders/my-orders` and catalog after resume | Pass |
| **TEST-L5-50** | Operations | Graceful failure during paused state: when Cloud SQL is stopped (`--activation-policy=NEVER`) and public ingress revoked, public callers receive 403 Forbidden; authenticated probe requests return clean 503 `{ "status": "not_ready", "db": "disconnected" }` without container crash or secret leakage | `curl -i` verification against paused service | Pass |
| **TEST-L5-51** | Config | Serverless scale-to-zero and quota compliance: Cloud Run service is configured with `min-instances=0` (scales to zero when idle, $0 compute charge), `max-instances=3`, memory `512Mi`; GCP budget alert configured with 50%, 90%, 100% notification thresholds | `gcloud run services describe s3c35c9bd` inspection & budget alert check | Pass |

## Detailed Test Specifications: Issue #21 (GitHub ↔ GCP Merge Gate)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-26** | WIF | GitHub Actions authenticates to GCP using Workload Identity Federation (no long-lived service-account JSON key stored in GitHub Secrets) | `deploy.yml` step "Authenticate to Google Cloud without a key" uses `google-github-actions/auth` with `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` variables from `environment: demo`; zero `credentials_json` present in workflow | Pass |
| **TEST-L5-27** | WIF | WIF provider and service account are stored as repository/environment variables (not secrets) in `Settings → Environments → demo` | GitHub `Settings → Environments → demo` Variables section shows `WIF_PROVIDER` (projects/.../workloadIdentityPools/...) and `WIF_SERVICE_ACCOUNT` (`s3c35c9bd-runner@cpe-se-course-2026.iam.gserviceaccount.com`) | Pass |
| **TEST-L5-28** | Branch Protection | `lab5-staging` branch requires the `test-and-docker` status check to pass before any PR can be merged | GitHub `Settings → Branches → lab5-staging` protection rule lists `test-and-docker` as required status check | Pass |
| **TEST-L5-29** | Branch Protection | `main` branch requires the `test-and-docker` status check to pass before any PR can be merged | GitHub `Settings → Branches → main` protection rule lists `test-and-docker` as required status check | Pass |
| **TEST-L5-30** | Merge Gate (C-02) | A PR with a deliberately broken test is blocked from merging: GitHub disables the "Merge pull request" button and shows "Required status checks must pass before merging" | Branch `test/intentionally-failing-ci-gate` opened as PR into `lab5-staging`; `test-and-docker` fails (intentional assertion error in `health.api.test.ts`); screenshot shows merge button disabled | Pass |
| **TEST-L5-31** | Merge Gate (C-02) | A PR with all tests passing is unblocked and can be merged normally | PR #21 (`issue/21-github-gcp-merge-gate` → `lab5-staging`) triggers `test-and-docker`; all checks pass; merge button is enabled | Pass |

---

## Detailed Test Specifications: Issue #22 (Repeatable Release Pipeline)

| TEST ID | Level | Test Description | Verification Method / Evidence | Result |
|---|---|---|---|:---:|
| **TEST-L5-32** | CD Workflow | CD trigger specification: `deploy.yml` triggers automatically on push to `main` branch and manually via `workflow_dispatch` with optional `image_tag` input | `.github/workflows/deploy.yml` triggers configuration | Pass |
| **TEST-L5-33** | CD Workflow | CI quality gate enforcement: `test` job calls reusable workflow `ci-docker.yml` (`test-and-docker`); `deploy` job declares `needs: test` and only runs on success | `deploy.yml` job dependency graph and conditional execution | Pass |
| **TEST-L5-34** | CD Workflow | Broken build gate: if any CI step fails in `test-and-docker`, the `deploy` job is skipped; zero broken revisions reach GCP | Simulated CI failure halts pipeline before GCP authentication | Pass |
| **TEST-L5-35** | WIF | Keyless deployment authentication: runner authenticates via WIF using `google-github-actions/auth` and repository variables `WIF_PROVIDER` / `WIF_SERVICE_ACCOUNT` | GitHub Actions deploy job execution log | Pass |
| **TEST-L5-36** | Container | Release image is built with `--build-arg GIT_SHA=$IMAGE_TAG`, tagged with the full 40-character commit SHA, and pushed to Artifact Registry | Docker build and push step in GitHub Actions log | Pass |
| **TEST-L5-37** | Release Script | Immutable digest pinning: `deploy/release.sh` resolves `$IMAGE_TAG` to `@sha256:` digest before updating any Cloud Run resource | `gcloud artifacts docker images describe` verification in `release.sh` | Pass |
| **TEST-L5-38** | Release Script | Automated database migration gate: `s3c35c9bd-migrate` job runs with `--wait`; release halts before service update if migration fails | `test_release_stub.sh` ("migration failure blocks service update") and live run | Pass |
| **TEST-L5-39** | Cloud Run | Atomic traffic cutover: Cloud Run service `s3c35c9bd` updated to new digest and `update-traffic --to-latest` routes 100% of traffic | `gcloud run services describe s3c35c9bd` traffic configuration | Pass |
| **TEST-L5-40** | Smoke Test | Automated post-deploy verification: `deploy/smoke_test.py` validates `/api/health`, `/api/ready`, `/`, and `/api/products` with retry logic | Smoke test step log with all checks returning PASS | Pass |
| **TEST-L5-41** | Traceability | Commit digest verification (R-08): `GET /api/version` on the live Cloud Run URL returns `{ "commit": "<GIT_SHA>" }` matching the release commit | `curl -s https://s3c35c9bd-4d7hbszvwq-as.a.run.app/api/version` | Pass |
| **TEST-L5-42** | Rollback | Zero-migration fast rollback: `workflow_dispatch` with `image_tag` skips tests, build, and migration, pointing service directly to prior digest | `test_release_stub.sh` ("rollback reuses image without touching migration") and workflow condition check | Pass |

