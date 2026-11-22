# Traceability Matrix and Coverage Analysis

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Authors:** Student Ba (Author, Issue #2) & Student Cl (Reviewer)  
**Status:** Approved Baseline  

> **Active Sprint Scope Note:**  
> In accordance with the Deliverable 1 requirements, **only Sprint 1 is currently being implemented and verified**. The full 3-sprint matrix below demonstrates comprehensive forward and backward traceability across the entire product vision, but all executable contracts, database migrations, and verification suites for this delivery are strictly confined to Sprint 1 (AC-01 through AC-18).  

---

## 1. Acceptance Criteria Inventory (Sprint 1 Baseline)

| AC ID | Target Feature | Acceptance Criterion Statement | Verification Level |
|---|---|---|---|
| **AC-01** | F-01 | Given valid credentials (email and password), when `POST /api/auth/login` is called, the server responds with HTTP 200, sets an `HttpOnly` session cookie, and returns the user's id, email, and role. | Integration / API |
| **AC-02** | F-01 | Given non-existent email or incorrect password, when `POST /api/auth/login` is called, the server responds with generic HTTP 401 and an error payload without user enumeration. | Integration / API |
| **AC-03** | F-01 | Given an unauthenticated request or expired session cookie, when any protected endpoint is called, the server responds with HTTP 401. | Integration / API |
| **AC-04** | F-01 | Given an authenticated session, when `POST /api/auth/logout` is called, the server destroys the session in the database, clears the cookie, and responds with HTTP 200. | Integration / API |
| **AC-05** | F-02 | Given an active catalog, when `GET /api/products` is called, the server responds with HTTP 200 and a list of active products with authoritative prices in minor units (`priceMinor`) and accurate stock availability badges. Inactive items are excluded. | Integration / API |
| **AC-06** | F-03 | Given an authenticated customer and valid multi-item payload with sufficient stock, when `POST /api/orders` is called, the server atomically creates the order with status `PLACED`, snapshots item prices (`unitPriceAtOrder`), decrements product inventory, and responds with HTTP 201 and order details. | Integration / API + DB |
| **AC-07** | F-03 | Given an empty order lines array (`items: []`) or missing items, when `POST /api/orders` is called, the server rejects the request with HTTP 400 and creates no records. | Integration / API |
| **AC-08** | F-03 | Given an order request where at least one item's requested quantity exceeds available `stockQuantity`, when `POST /api/orders` is called, the server aborts the transaction with HTTP 400 and leaves inventory completely unchanged. | Integration / API + DB |
| **AC-09** | F-03 | Given an order request containing an inactive product (`isActive = false`), when `POST /api/orders` is called, the server aborts the transaction with HTTP 400. | Integration / API |
| **AC-10** | F-03 | Given a placed order, when the application server process is stopped and restarted, all order records, line items, and updated stock quantities remain strictly persistent and verifiable in the database. | Integration / Persistence |
| **AC-11** | F-04 | Given an authenticated customer, when `GET /api/orders` is called, the server responds with HTTP 200 and lists only orders belonging to that customer, sorted newest first with complete line totals. | Integration / API |
| **AC-12** | F-04 | Given an authenticated customer A, when `GET /api/orders/:id` is called for an order belonging to customer B, the server responds with HTTP 404 and leaks no order metadata. | Integration / API |
| **AC-13** | F-01, F-05 | Given an authenticated user with role `CUSTOMER`, when calling operator-only endpoints (`GET /api/operator/orders` or `PATCH /api/operator/orders/:id/accept`), the server rejects the request with HTTP 403 Forbidden. | Integration / API |
| **AC-14** | F-05 | Given an authenticated operator, when `GET /api/operator/orders` is called, the server responds with HTTP 200 and lists all incoming orders with status `PLACED` sorted chronologically (oldest first). | Integration / API |
| **AC-15** | F-05 | Given an authenticated operator and an order in `PLACED` status, when `PATCH /api/operator/orders/:id/accept` is called, the server transitions the order status to `ACCEPTED`, records `operatorId` and `acceptedAt` timestamp, and responds with HTTP 200. | Integration / API + DB |
| **AC-16** | F-05 | Given an order already in `ACCEPTED` status, when `PATCH /api/operator/orders/:id/accept` is called again, the server rejects the invalid state transition with HTTP 409 Conflict. | Integration / API |
| **AC-17** | F-01, F-03 | Given an authenticated operator, when attempting to call customer-only order creation (`POST /api/orders`), the server rejects the request with HTTP 403 Forbidden. | Integration / API |
| **AC-18** | F-01, F-02 | Given an unseeded or existing database, running the database seed script idempotently populates the required test accounts ($\ge 3$ customers, $\ge 2$ operators) and products ($\ge 8$ products) without duplicate key errors or data corruption. | Integration / Seed Script |

---

## 2. Requirements Traceability Matrix (RTM)

### 2.1 Functional Requirements (FR) Traceability

| Req ID | Requirement Statement | Implementing Feature | Target Sprint | Acceptance Criteria | Test Specification / Verification Method | Status |
|---|---|---|---|---|---|---|
| **FR-01** | User Authentication (email + password, secure session) | F-01 | Sprint 1 | AC-01, AC-02, AC-18 | `auth.api.test.ts` (Valid/invalid credentials, cookie verification) | Complete (Drafted) |
| **FR-02** | Session Invalidation / Logout | F-01 | Sprint 1 | AC-04 | `auth.api.test.ts` (Server session deletion, cookie cleared) | Complete (Drafted) |
| **FR-03** | Role-Based Route Protection (RBAC) | F-01 | Sprint 1 | AC-03, AC-13, AC-17 | `rbac.api.test.ts` (401 unauth, 403 role violation) | Complete (Drafted) |
| **FR-04** | Browse Active Catalog & Live Stock | F-02 | Sprint 1 | AC-05, AC-18 | `catalog.api.test.ts` (Stock badges, integer satang price) | Complete (Drafted) |
| **FR-05** | Multi-Line Order Placement & Atomic Decrement | F-03 | Sprint 1 | AC-06, AC-07, AC-08, AC-09 | `orders.api.test.ts` (Atomic placement, stock decrement) | Complete (Drafted) |
| **FR-06** | Snapshot Historical Item Price | F-03 | Sprint 1 | AC-06, AC-10 | `orders.api.test.ts` (`unitPriceAtOrder` immutability) | Complete (Drafted) |
| **FR-07** | Customer Order History & Detail View | F-04 | Sprint 1 | AC-11 | `orders-customer.api.test.ts` (List own orders, detail breakdown) | Complete (Drafted) |
| **FR-08** | Customer Data Isolation | F-04 | Sprint 1 | AC-12 | `orders-isolation.api.test.ts` (HTTP 404 cross-customer query) | Complete (Drafted) |
| **FR-09** | Operator Incoming Order Queue | F-05 | Sprint 1 | AC-14 | `operator-orders.api.test.ts` (List `PLACED` queue chronologically) | Complete (Drafted) |
| **FR-10** | Operator Order Acceptance | F-05 | Sprint 1 | AC-15, AC-16 | `operator-orders.api.test.ts` (Transition `PLACED->ACCEPTED`, 409 conflict) | Complete (Drafted) |
| **FR-11** | Operator Catalog Management | F-06 | Sprint 2 | — | Sprint 2 planned contract tests | Planned (S2) |
| **FR-12** | Extended Fulfillment & Cancellation | F-07, F-08, F-09 | Sprint 2 | — | Sprint 2 planned contract tests | Planned (S2) |
| **FR-13** | Reporting Dashboard & Analytics | F-10, F-11 | Sprint 3 | — | Sprint 3 planned benchmark tests | Planned (S3) |

---

### 2.2 Business Rules (BR) Traceability

| Rule ID | Rule Statement | Implementing Feature | Target Sprint | Enforcing AC | Verification Mechanism | Status |
|---|---|---|---|---|---|---|
| **BR-01** | Monetary Representation (minor units, THB satang, no floats) | F-02, F-03 | Sprint 1 | AC-05, AC-06 | Schema integer type + validation logic in `orders.api.test.ts` | Complete |
| **BR-02** | Atomic Placement & Stock Decrement (transactional rollback) | F-03 | Sprint 1 | AC-06, AC-08, AC-10 | Prisma `$transaction` integration tests with concurrency simulation | Complete |
| **BR-03** | Authoritative Server Pricing (ignore client price/total) | F-03 | Sprint 1 | AC-06 | API test sending forged low prices, verifying server ignores them | Complete |
| **BR-04** | Order Status Lifecycle (`PLACED -> ACCEPTED` in S1; 409 on invalid) | F-05 | Sprint 1 | AC-15, AC-16 | State machine guard in order service; negative tests in `operator-orders.api.test.ts` | Complete |
| **BR-05** | Customer Order Ownership (access scoped to `session.userId`) | F-04 | Sprint 1 | AC-12 | Route query filter scoped by `userId`; verified by `orders-isolation.api.test.ts` | Complete |
| **BR-06** | Order Line Constraints ($1 \le \text{qty} \le 10$, no duplicates) | F-03 | Sprint 1 | AC-07, AC-08 | Zod payload schema validation and API rejection test | Complete |
| **BR-07** | Secure Credential Storage (bcrypt salt $\ge 10$) | F-01 | Sprint 1 | AC-01, AC-18 | DB seed & auth service inspection; no plaintext passwords | Complete |
| **BR-08** | Operator Scope Restrictions (`OPERATOR` only, 403 on forbidden) | F-01, F-05 | Sprint 1 | AC-13, AC-17 | Role middleware check; tested by `rbac.api.test.ts` | Complete |

---

### 2.3 Non-Functional Requirements (NFR) Traceability

| NFR ID | Requirement Statement | Target Metric | Implementing Feature | Enforcing AC | Verification Method | Status |
|---|---|---|---|---|---|---|
| **NFR-01** | Auth & RBAC Enforcement | 100% routes protected; 401 unauth; 403 forbidden; 404 isolated | F-01, F-04, F-05 | AC-01, AC-02, AC-03, AC-12, AC-13, AC-17 | Automated API integration test suite covering all routes | Complete |
| **NFR-02** | Relational Data Persistence | Data persists across process restart | F-02, F-03, F-04 | AC-10 | Persistence test script (stop server, query Postgres, verify state) | Complete |
| **NFR-03** | Seed Reproducibility & Idempotence | Consecutive seed executions succeed without duplicate errors | F-01, F-02 | AC-18 | Double-run seed test script asserting identical row counts | Complete |
| **NFR-04** | Fresh Clone Reproducibility | Install, migrate, seed, test in $< 5\text{ min}$ | F-12 | — | Fresh clone execution verification in isolated environment | Complete |
| **NFR-05** | Order Placement Latency | 10-line order response in $< 1000\text{ ms}$ | F-03, F-12 | AC-06 | Latency benchmark test measuring round-trip response time | Complete |
| **NFR-06** | Responsive UI Layout | Adapt cleanly from 375px to 1920px | F-12 | — | Playwright responsive viewport assertions (Sprint 3) | Planned (S3) |

---

## 3. Forward and Backward Traceability Analysis

### 3.1 Forward Traceability (Requirements $\rightarrow$ Design $\rightarrow$ Tests)
- Every requirement in the SRS (`FR-01` through `FR-13`, `BR-01` through `BR-08`, and `NFR-01` through `NFR-06`) is mapped directly to at least one Feature (`F-01` to `F-12`).
- Every Sprint 1 requirement is mapped to one or more rigorous Acceptance Criteria (`AC-01` to `AC-18`).
- Every Acceptance Criterion is mapped to a concrete, executable integration or contract test suite.
- **Forward Orphan Check:** 0 orphaned requirements.

### 3.2 Backward Traceability (Code & Tests $\rightarrow$ Features $\rightarrow$ Requirements)
- Every Acceptance Criterion (`AC-01` to `AC-18`) traces back to an explicit requirement in the approved SRS.
- No "gold-plating" or ungrounded features are introduced outside the scope of Theme 4.
- Every test in Sprint 1 directly validates an identified Acceptance Criterion and Business Rule.
- **Backward Orphan Check:** 0 ungrounded features or acceptance criteria.

---

## 4. Coverage Summary Table

| Requirement Category | Total Identified | Covered in Sprint 1 Baseline | Covered in Sprint 2 Expansion | Covered in Sprint 3 Hardening | Overall Coverage |
|---|---|---|---|---|---|
| **Functional Requirements (FR)** | 13 | 10 (77%) | 2 (15%) | 1 (8%) | **100%** |
| **Business Rules (BR)** | 8 | 8 (100%) | — | — | **100%** |
| **Non-Functional Requirements (NFR)** | 6 | 4 (67%) | — | 2 (33%) | **100%** |
| **Acceptance Criteria (AC)** | 18 | 18 (100%) | — | — | **100%** |
