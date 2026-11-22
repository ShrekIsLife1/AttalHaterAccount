# Sprint 1 — AI Use

**Team:** Clément Dominique Delrieu (`69540460016`, @ClemDelGh) & Baptiste Carré (`69540460014`, @ShrekIsLife1)  
**Repository:** [https://github.com/ShrekIsLife1/AttalHaterAccount](https://github.com/ShrekIsLife1/AttalHaterAccount)  
**Release Tag:** `v0.1.0-sprint1` | **Release Commit:** `b011f66`  

## LLM used
Google Antigravity Agent (Claude 3.7 Sonnet & Gemini), used as specification authoring, TDD implementer, and QA verification agent.

## Selected key prompts (6–10)
| # | Prompt (summarised) | What I did with the result |
|---|---------------------|----------------------------|
| 1 | From the Sprint 1 requirements, help me clean up the repository baseline and create the initial project skeleton with PR template and living PDF draft. | Reviewed directory structure, validated removal of obsolete comments, and verified the PDF draft skeleton before branching. |
| 2 | Draft the complete Software Requirements Specification (SRS) for the UniMerch campus merchandise store with 13 Functional Requirements, 8 Business Rules in minor units (satang), and 6 NFRs. | Reviewed the draft, clarified the integer satang calculation rules, and ensured explicit exclusions for payment gateways and delivery tracking in Sprint 1. |
| 3 | Establish the comprehensive feature inventory (F-01..F-12) and bidirectional Requirements Traceability Matrix (RTM) linking FRs/BRs/NFRs to Sprint 1 features and acceptance criteria. | Verified 1-to-1 requirement mappings, checked that 0 forward or backward orphans existed, and confirmed Sprint 1 containment. |
| 4 | Create the 3-tier architecture diagram, PostgreSQL entity-relationship model with Prisma, role permission matrix, and GCP deployment architecture for the System-Level SDS. | Verified data model relations between User, Session, Product, Order, and OrderItem with non-null foreign keys and minor unit pricing constraints. |
| 5 | Draft the Sprint 1 engineering contracts for F-01 to F-05, acceptance criteria (AC-01..AC-20), Software Test Specification (TEST-01..TEST-26), and Product Definition of Done. | Verified test IDs mapped to every acceptance criterion and standardized error payloads to `{ "error": string }`. |
| 6 | Write the Prisma schema, migration, and idempotent seed script with bcrypt password hashing, plus persistence integration tests. | Verified seed idempotency by executing consecutive runs without unique key collisions and confirmed database persistence across server reloads. |
| 7 | Implement session authentication with SHA-256 tokens, HttpOnly cookies, and RBAC middleware using TDD (failing tests first). | Verified failing test commit `cdc98d8` before passing implementation commit `fec3f9b`, enforcing generic 401 on bad credentials. |
| 8 | Implement the product catalog API (GET /api/products) filtering active items with integer minor units, and build the React Login and Customer Ordering UI. | Verified public access and out-of-stock badge rendering, and updated Vitest component mocks for cart checkout and order history. |
| 9 | Implement authoritative order creation with atomic stock decrement and operator order acceptance with 409 conflict protection using TDD. | Verified rollback on stock exhaustion, enforced line quantity limits ($1 \le qty \le 10$), and verified 409 guard on double acceptance. |
| 10 | Implement authorization hardening, non-enumerating 404 isolation for cross-customer orders, and complete E2E workflow integration verification. | Verified 18 cross-cutting security tests, customer/operator journey suites, and generated the final deliverable report with 20 evidence screenshots. |

## My Reflection
Throughout Sprint 1, AI assistance proved exceptionally valuable in maintaining strict traceability across the multi-issue workflow:
1. **Contract-Driven Development:** Defining the exact data structures, status transitions, and minor unit pricing rules in Issue #5 ensured zero drift between backend and frontend implementations.
2. **TDD Discipline & Concurrency:** Committing failing integration tests before implementation confirmed that security boundaries (401, 403, 404, 409) were genuinely enforced by the backend rather than merely hidden in the UI.
3. **Traceability & Test Verification:** Automating all 26 planned STS tests across unit, API, UI, and E2E suites caught edge cases such as stockout rollbacks and non-leaking 404 responses for cross-customer order lookups.
In future iterations, generating automated database reset hooks between parallel test runners earlier in the pipeline would further streamline testing cycles.

## Individual Records
- Clément Dominique Delrieu (69540460016): [docs/deliverable-1/69540460016/ai_use.md](69540460016/ai_use.md)
- Baptiste Carré (69540460014): [docs/deliverable-1/69540460014/ai_use.md](69540460014/ai_use.md)
