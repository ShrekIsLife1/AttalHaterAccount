# Lab 5 Software Test Specifications & Traceability Matrix

## Consolidated Lab 5 Test Map

| Requirement / Check | Issue | Planned TEST IDs | Level | Description |
|---|---|---|---|---|
| **R-12, Cost Control** | #16 | — | Cloud Setup | GCP portal activation, team resources, budget controls, public repo & push protection |
| **R-02, R-04** | #17 | TEST-L5-01..04, L5-08..09 | Unit / API | Config loader, `.env.example`, session DB persistence, safe production seed |
| **R-01, C-03** | #18 | TEST-L5-10..14 | Container | Docker multi-stage build from fresh clone, docker-compose local stack, non-root user |
| **R-05, C-01** | #19 | TEST-L5-15..19 | CI Workflow | GitHub Actions `test-and-docker` job on PRs into `sprint1-staging` and `main` |
| **R-03, R-04, C-04** | #20 | TEST-L5-20..25 | Live / Smoke | First deployment on Cloud Run, live domain customer order journey, failure rejections |
| **R-06, R-09, C-02** | #21 | TEST-L5-26..31 | Merge Gate | Workload Identity Federation, branch protection ruleset, failing PR blocked |
| **R-07, R-08, C-06** | #22 | TEST-L5-32..42 | Release Pipeline | `deploy.yml`, automated smoke test, release by commit SHA digest |
| **R-04, C-05** | #23 | TEST-L5-43..47 | Persistence / Rollback | Data persistence across service restart and redeploy, additive migrations, rollback |
| **Cost Control** | #24 | TEST-L5-48..51 | Operations | Pause/resume Cloud SQL procedure, Cloud Run min=0 instances, spend tracking |
| **R-08, R-11, DoD** | #25 | TEST-L5-52..58 | Documentation | Final release verification, `deployment.md`, secret scan, and LEB2 deliverable PDF |
