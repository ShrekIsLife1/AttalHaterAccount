# Sprint 1 — AI Use

**Student:** Clément Dominique Delrieu — 69540460016 — GitHub: @ClemDelGh  

## LLM used
Google Antigravity Agent (Claude 3.7 Sonnet & Gemini), used as specification authoring, TDD implementer, and QA verification agent.

## Selected key prompts (6–10)
| # | Prompt (summarised) | What I did with the result |
|---|---------------------|----------------------------|
| 1 | From the Sprint 1 requirements, help me clean up the repository baseline and create the initial project skeleton with PR template and living PDF draft. | Reviewed directory structure, validated removal of obsolete comments, and verified the PDF draft skeleton before branching. |
| 2 | Draft the complete Software Requirements Specification (SRS) for the UniMerch campus merchandise store with 13 Functional Requirements, 8 Business Rules in minor units (satang), and 6 NFRs. | Reviewed the draft, clarified the integer satang calculation rules, and ensured explicit exclusions for payment gateways and delivery tracking in Sprint 1. |
| 3 | Create the 3-tier architecture diagram, PostgreSQL entity-relationship model with Prisma, role permission matrix, and GCP deployment architecture for the System-Level SDS. | Verified data model relations between User, Session, Product, Order, and OrderItem with non-null foreign keys and minor unit pricing constraints. |
| 4 | Write the Prisma schema, migration, and idempotent seed script with bcrypt password hashing, plus persistence integration tests. | Verified seed idempotency by executing consecutive runs without unique key collisions and confirmed database persistence across server reloads. |
| 5 | Implement session authentication with SHA-256 tokens, HttpOnly cookies, and RBAC middleware using TDD (failing tests first). | Verified failing test commit `cdc98d8` before passing implementation commit `fec3f9b`, enforcing generic 401 on bad credentials. |
| 6 | Develop the product catalog API (GET /api/products) filtering active items with integer minor units, and verify public catalog access. | Verified active-only filter, integer priceMinor values, and ensured stockQuantity=0 items remain visible as out-of-stock. |
| 7 | Conçois les composants React du panier, du passage de commande et de l'historique des achats avec gestion du panier local. | Validated formatted THB prices (฿), line total recalculations, and updated Vitest component mocks in Checkout.test.tsx. |
| 8 | Implement cross-cutting authorization hardening tests and customer order isolation returning 404 without data or existence leaks. | Verified 18 security tests across anonymous, customer, and operator roles to enforce strict ownership boundaries. |
| 9 | Compile the final deliverable ODT report embedding 20 evidence screenshots, test suite outputs, and GitHub review record links. | Verified that all 20 screenshots and diagrams were properly rendered, framed, and verified against the Lab 3/4 submission standard. |

## My Reflection
Throughout Sprint 1, AI assistance proved exceptionally valuable in maintaining strict traceability across the multi-issue workflow:
1. **Contract-Driven Development:** Defining the exact data structures, status transitions, and minor unit pricing rules in Issue #1 and #3 ensured zero drift between backend and frontend implementations.
2. **TDD Discipline & Concurrency:** Committing failing integration tests before implementation confirmed that security boundaries (401, 403, 404, 409) were genuinely enforced by the backend rather than merely hidden in the UI.
3. **Traceability & Test Verification:** Automating all planned STS tests across unit, API, UI, and E2E suites caught edge cases such as stockout rollbacks and non-leaking 404 responses for cross-customer order lookups.
In future iterations, generating database reset hooks between parallel test runners earlier in the pipeline would further streamline testing cycles.
