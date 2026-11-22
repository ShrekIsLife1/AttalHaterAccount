# Sprint 1 — AI Use

**Student:** Baptiste Carré — 69540460014 — GitHub: @ShrekIsLife1  

## LLM used
Google Antigravity Agent (Claude 3.7 Sonnet & Gemini), used as specification authoring, TDD implementer, and QA verification agent.

## Selected key prompts (6–10)
| # | Prompt (summarised) | What I did with the result |
|---|---------------------|----------------------------|
| 1 | Establish the comprehensive feature inventory (F-01..F-12) and bidirectional Requirements Traceability Matrix (RTM) linking FRs/BRs/NFRs to Sprint 1 features and acceptance criteria. | Verified 1-to-1 requirement mappings, checked that 0 forward or backward orphans existed, and confirmed Sprint 1 containment. |
| 2 | Construct the three-sprint implementation plan (Sprint 1/2/3) with technical dependencies and feasibility justification for the core ordering workflow. | Validated that the minimal end-to-end purchasing path (auth, catalog, cart, placement, operator accept) is fully delivered in Sprint 1. |
| 3 | Draft the Sprint 1 engineering contracts for F-01 to F-05, acceptance criteria (AC-01..AC-20), Software Test Specification (TEST-01..TEST-26), and Product Definition of Done. | Verified test IDs mapped to every acceptance criterion and standardized all API error payloads to `{ "error": string }`. |
| 4 | Build the React Login component with AuthContext, busy indicator, generic error feedback, and role-conditional navigation redirecting to Customer vs Operator shells. | Tested role redirect logic, verified no user enumeration on failed login, and wrote 6 Vitest component tests. |
| 5 | Implement the authoritative order pricing logic and POST /api/orders endpoint with atomic transaction and stock decrement using TDD. | Verified failing test commit `8ade73a` before passing implementation, enforcing boundary checks ($1 \le qty \le 10$) and stockout rollback. |
| 6 | Implement the operator order queue API (GET /api/operator/orders) and single-step accept action with 409 conflict protection against double acceptance. | Verified failing test commit `339cbde` before passing implementation, checked chronological sorting (createdAt ASC), and verified 409 guard. |
| 7 | Develop the end-to-end integration and workflow verification tests across server and client suites for complete customer and operator domain journeys. | Verified TEST-24, TEST-25, and TEST-26 across both Supertest API flows and React workflow suites, confirming all 103 tests pass cleanly. |

## My Reflection
Throughout Sprint 1, AI assistance proved exceptionally valuable in maintaining strict traceability across the multi-issue workflow:
1. **Contract-Driven Development:** Defining the exact data structures, status transitions, and minor unit pricing rules in Issue #5 ensured zero drift between backend and frontend implementations.
2. **TDD Discipline & Concurrency:** Committing failing integration tests before implementation confirmed that security boundaries (401, 403, 404, 409) were genuinely enforced by the backend rather than merely hidden in the UI.
3. **Traceability & Test Verification:** Automating all planned STS tests across unit, API, UI, and E2E suites caught edge cases such as stockout rollbacks and non-leaking 404 responses for cross-customer order lookups.
In future iterations, generating database reset hooks between parallel test runners earlier in the pipeline would further streamline testing cycles.
