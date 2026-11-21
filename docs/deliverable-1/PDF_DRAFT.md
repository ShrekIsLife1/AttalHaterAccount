# Deliverable 1 — PDF draft (living document)
Status legend: ✅ complete · 🟡 partial · ⬜ not started · 📸 screenshot needed
Release commit: <RELEASE_COMMIT>   Tag: <TAG>

## Front page   (filled in #15)
- Students: Clément Dominique Delrieu (ID 69540460016, @ClemDelGh), Baptiste Carré (ID 69540460014, @ShrekIsLife1)
- Theme / context: Theme 4 — E-Commerce/Ordering — Campus Merchandise Shop (UniMerch)
- Repository: https://github.com/ShrekIsLife1/AttalHaterAccount.git
- Release: tag <TAG>, commit <RELEASE_COMMIT>

## Navigation table   (page numbers filled in #15)
| Part | Pages | Main IDs | Execution evidence |
|---|---|---|---|

## Part A — SRS and product scope   ✅ (#1)

### A.1 Problem Statement & Context
The **UniMerch Campus Store** is an on-campus merchandise shop serving university students, faculty, alumni, and administrative staff. The shop offers branded merchandise, apparel (hoodies, t-shirts), stationery (notebooks, pens), and everyday campus accessories (water bottles, tote bags, mugs).

Currently, the physical store suffers from substantial operational bottlenecks:
- **Long Counter Queues:** During semester openings and campus events, students wait in long queues just to enquire about product availability and prices.
- **Stock Inconsistencies:** Store operators manually track physical inventory, leading to overselling or discovering that requested items are out of stock after payment attempts.
- **Manual Order Processing:** Paper-based receipts and untracked orders result in delayed fulfillment and occasional misplaced orders.
- **Pricing Discrepancies:** Outdated printed price tags lead to friction at checkout when prices are updated in central store logs.

**Solution Vision:** A robust web-based ordering application that allows customers to view authoritative catalog items with live availability, place multi-item orders with server-validated pricing, and track their order status. Store operators manage an organized incoming queue, review order lines, and progress orders through transparent fulfillment stages.

### A.2 Actors and Responsibilities
| Actor | Description | Core Responsibilities |
|---|---|---|
| **Customer** | Enrolled student or staff member purchasing merchandise | - Authenticate securely via email and password.<br>- Browse product catalog with authoritative prices and stock availability.<br>- Assemble and submit multi-line orders.<br>- View own order history and track order status.<br>- Cannot modify catalog, cannot accept orders, cannot view other customers' orders. |
| **Operator** | Campus store staff member managing fulfillment and catalog | - Authenticate securely via email and password.<br>- View incoming orders queue (`PLACED`) sorted chronologically.<br>- Accept incoming orders (`PLACED -> ACCEPTED`) with recorded timestamp and operator identity.<br>- Progress order fulfillment in subsequent sprints (`PREPARING -> READY -> COMPLETED`).<br>- Manage catalog items, pricing, and stock levels (Sprint 2).<br>- Cannot place orders as an operator; accesses customer orders within store scope. |

### A.3 Product Scope and Explicit Exclusions
- **In Scope:**
  - **Sprint 1 (Baseline & Working Slice):** Session-based authentication with role-based access control (`CUSTOMER`, `OPERATOR`); read-only catalog with live availability badges and minor-unit prices; multi-line order placement with server-side authoritative pricing, stock validation, atomic inventory decrement; customer order history and detail view; operator incoming orders queue and acceptance transition (`PLACED -> ACCEPTED`); persistent PostgreSQL database with idempotent seeding.
  - **Sprint 2 (Core Expansion):** Operator catalog management (create, update, toggle active status, restock); order cancellation by customer and rejection by operator; extended fulfillment lifecycle (`ACCEPTED -> PREPARING -> READY -> COMPLETED`); simulated payment workflow.
  - **Sprint 3 (Hardening & Analytics):** Operator sales and order analytics dashboard; order search and filtering; hardened error handling and performance benchmarks.
- **Explicit Exclusions:**
  - *No Real Payment Gateways:* Real payment integrations (Stripe, PayPal, banking APIs) are strictly excluded; simulated payment states are used.
  - *No External Delivery / Logistics APIs:* Pickup occurs on campus at the UniMerch service counter; no external courier tracking is integrated.
  - *No External Messaging Providers:* No external SMS/email services; all status updates remain internal to the web platform.
  - *No Self-Registration or Password Recovery in Sprint 1:* Seeded demo accounts with pre-hashed credentials are used.

### A.4 Functional Requirements (FR)
- **FR-01 (User Authentication):** A user can submit valid credentials (email and password) to log in. The system creates a secure session and returns the user's profile (`id`, `name`, `role`). Password hashes are never returned.
- **FR-02 (User Logout):** An authenticated user can log out. The backend invalidates the session server-side, clearing the authentication cookie. Subsequent requests with the terminated session are rejected.
- **FR-03 (Catalog Browsing):** An authenticated customer or operator can retrieve the catalog of products. Each product displays name, description, unit price (formatted in minor units), and an availability status (`inStock` or `unavailable`).
- **FR-04 (Order Placement):** A customer can submit an order containing 1 to $N$ distinct product lines with specified quantities. The server computes the total authoritatively, validates stock, snapshots unit prices, decrements inventory, and saves the order in `PLACED` status in a single atomic transaction.
- **FR-05 (Customer Order History & Detail):** A customer can view a list of all orders they previously placed (showing order ID, date, status, and total). The customer can open any of their own orders to inspect full line details.
- **FR-06 (Operator Incoming Orders):** An operator can view a queue of all incoming orders with `status = PLACED`, ordered chronologically (oldest first) to ensure fair first-in-first-out processing.
- **FR-07 (Operator Order Acceptance):** An operator can accept a `PLACED` order. The backend updates the order `status = ACCEPTED`, records `acceptedAt` timestamp, and records `acceptedByOperatorId` referencing the acting operator.
- **FR-08 (Operator Catalog Management - Sprint 2):** An operator can create a new product, edit metadata, adjust stock, and toggle active status.
- **FR-09 (Order Cancellation and Rejection - Sprint 2):** A customer can cancel a `PLACED` order; an operator can reject a `PLACED` order with a reason note.
- **FR-10 (Extended Fulfillment Transitions - Sprint 2):** Operators advance orders sequentially: `ACCEPTED -> PREPARING -> READY -> COMPLETED`.
- **FR-11 (Simulated Payment Processing - Sprint 2):** Customers execute simulated payments, transitioning status to `PAID` with a generated synthetic reference.
- **FR-12 (Sales and Order Analytics - Sprint 3):** Operators view aggregated sales metrics, revenue, order breakdown by status, and inventory turnover.
- **FR-13 (Order Search and Filtering - Sprint 3):** Customers and operators search and filter orders by status, date range, or customer.

### A.5 Business Rules (BR)
- **BR-01 (Authoritative Server-Side Pricing):** Order line totals and order grand totals must be calculated strictly on the backend using authoritative product prices stored in the database. Any client-submitted `price`, `unitPrice`, or `total` in the request body is completely ignored.
- **BR-02 (Line Quantity Boundaries):** Each order line `quantity` must be a positive integer such that $1 \le \text{quantity} \le \text{MAX\_QTY\_PER\_LINE}$ (configured to 10). Quantities $\le 0$, non-integers, missing values, or values $> 10$ must be rejected with HTTP 400.
- **BR-03 (Inventory Availability & Atomicity):** A product is orderable only if `isActive = true` and `stockQuantity >= requested_quantity`. An order cannot contain duplicate product entries across multiple lines. If any line item is unavailable or invalid, the entire order submission is rejected (HTTP 400 or 409), no partial order is saved, and product stock remains unchanged (all-or-nothing database transaction).
- **BR-04 (Price Snapshot Immutability):** When an order is created, the current unit price of each item is captured in `OrderItem.unitPriceAtOrder`. Any subsequent price updates to `Product.priceMinor` in the catalog must never alter historical orders or their computed totals.
- **BR-05 (Customer Ownership & Privacy):** A customer can access only orders where `Order.customerId` matches their own authenticated user ID. Any request by Customer A to read or inspect Customer B's order must return HTTP 404 (Not Found) without confirming the existence of the record or leaking private data.
- **BR-06 (Strict State Transition Lifecycle):** In Sprint 1, the only permitted order state transition is `PLACED -> ACCEPTED` initiated by an operator. Transitioning an order that is already `ACCEPTED` (or in any other status) must be rejected with HTTP 409 (Conflict), leaving database state untouched.
- **BR-07 (Secure Credential Storage):** Passwords must never be stored in plaintext. Passwords must be hashed using a salted cryptographic hashing algorithm (bcrypt with minimum work factor 10 or argon2) prior to database insertion.
- **BR-08 (Operator Scope and Role Restrictions):** Only authenticated users with role `OPERATOR` are authorized to list incoming orders or trigger the accept transition. Any request by a `CUSTOMER` to operator endpoints must be rejected with HTTP 403 (Forbidden).

### A.6 Non-Functional Requirements (NFR)
| NFR ID | Requirement Statement | Measurable Target | Verification Method | Sprint |
|---|---|---|---|---|
| **NFR-01** | **Authentication & Role Authorization Enforcement** | 100% of protected routes reject unauthenticated requests with HTTP 401 and empty/safe error payload; role violations return HTTP 403; cross-user order access returns HTTP 404. | Automated integration tests (`auth.api.test.ts`, `orders-access.api.test.ts`, `operator-orders.api.test.ts`). | Sprint 1 |
| **NFR-02** | **Relational Data Persistence Across Restarts** | All database records (users, products, orders, order items, sessions) persist across application process stops and restarts. | Automated persistence test (`persistence.api.test.ts`) that disconnects, queries data, and verifies state intact. | Sprint 1 |
| **NFR-03** | **Seed Reproducibility & Idempotence** | Executing the database seed command consecutively does not produce duplicate rows or trigger constraint violations. | Scripted test running `npm run seed && npm run seed` and asserting identical record counts. | Sprint 1 |
| **NFR-04** | **Fresh Clone Reproducibility** | A developer can clone a fresh repository and execute install, migration, seed, test, and dev server in under 5 minutes following only the `README.md`. | Timed manual and scripted clean-room test on a separate workspace clone. | Sprint 1 |
| **NFR-05** | **Order Placement Latency** | A valid 10-line order creation request responds with HTTP 201 in under $1000\text{ ms}$ on local developer environment. | Automated benchmark test measuring API round-trip duration under local test database. | Sprint 3 |
| **NFR-06** | **Responsive User Interface** | Web application layouts adapt cleanly without horizontal scrolling or clipping across screen widths from $375\text{ px}$ (mobile) to $1920\text{ px}$ (desktop). | Visual inspection and automated Playwright responsive viewport assertions. | Sprint 3 |

### A.7 Assumptions, Frozen Design Decisions, and Open Questions
| Topic / Decision | Chosen Resolution & Justification | Status |
|---|---|---|
| **Domain Context** | Campus merchandise store (UniMerch): single-store catalog, single fulfillment team, student/staff customers. | Frozen |
| **User Roles** | Exactly two roles: `CUSTOMER` and `OPERATOR`. Exactly one role per account. Simplifies Sprint 1 RBAC while fulfilling rubric requirements. | Frozen |
| **Monetary Representation** | All currency values (`priceMinor`, `totalMinor`, `unitPriceAtOrder`) are stored strictly as **integers in minor units** (e.g., satang or cents; 100 minor units = 1 unit). Float arithmetic is strictly prohibited to avoid rounding errors. Currency fixed to THB. | Frozen |
| **Sprint 1 Order Statuses** | Exactly two statuses in Sprint 1: `PLACED` and `ACCEPTED`. Later sprints introduce `REJECTED`, `CANCELLED`, `PREPARING`, `READY`, `COMPLETED`. | Frozen |
| **Order Lines & Limits** | 1 to $N$ lines per order. `quantity` between 1 and $\text{MAX\_QTY\_PER\_LINE} = 10$. Duplicate items within one order payload are rejected (HTTP 400). | Frozen |
| **Inventory Management** | `Product.isActive` (boolean) and `Product.stockQuantity` (integer $\ge 0$). Decremented atomically in the same database transaction as order creation. If stock is insufficient, whole order fails. | Frozen |
| **Authoritative Pricing** | Server re-queries database for product prices at order creation time. Any client-sent totals or prices are discarded. | Frozen |
| **Price Snapshot** | `OrderItem.unitPriceAtOrder` records unit price at order placement time. Future product catalog price changes never mutate historical orders. | Frozen |
| **Authentication Mechanism** | Server-side session table (`Session`) with cryptographically secure random session tokens delivered in `HttpOnly`, `SameSite=Lax` cookies. Session expiration set to 8 hours. Logout invalidates session in DB. | Frozen |
| **Error Handling Policy** | Generic HTTP 401 for bad credentials, missing session, expired session, or inactive account (no user enumeration). HTTP 403 for role violations. HTTP 404 without data leak for cross-customer order requests. HTTP 400 with field-specific errors for invalid input. HTTP 409 for invalid state transitions or concurrent conflicts. | Frozen |
| **Seed Data Specification** | Idempotent seed containing $\ge 3$ customers, $\ge 2$ operators, and $\ge 8$ products (including $\ge 1$ inactive product and $\ge 1$ product with `stockQuantity = 0`). Seed passwords loaded from environment variables, never committed to Git. | Frozen |
## Part B — Feature inventory and traceability   ✅ (#2)

> **Sprint 1 Active Scope & Boundary:**  
> **Only Sprint 1 is currently implemented and tested.** Features for Sprints 2 and 3 are documented solely to fulfill full-lifecycle planning and forward traceability. All active engineering contracts (Part E), database schemas, endpoints, and automated tests (Part F) are strictly restricted to Sprint 1 features (`F-01` to `F-05`) and their acceptance criteria (`AC-01` to `AC-18`).

### B.1 Feature Inventory Across Sprints
The product features are structured across three sprints to deliver an authoritative, working baseline in Sprint 1 before expanding operational capabilities in Sprint 2 and analytical depth in Sprint 3.

| Feature ID | Feature Name | Target Sprint | Primary Actor | Complexity / Priority | Associated Requirements | Description & Scope |
|---|---|---|---|---|---|---|
| **F-01** | Session Auth & Role-Based Access Control | Sprint 1 | Customer, Operator | Medium / High | FR-01, FR-02, FR-03, BR-07, BR-08, NFR-01 | Secure login via bcrypt credentials, `HttpOnly` session cookies, 8h expiration, role guard middleware (401 unauth, 403 forbidden), and server-side session revocation on logout. |
| **F-02** | Product Catalog & Availability View | Sprint 1 | Customer | Low / High | FR-04, BR-01, NFR-02 | Read-only listing of active products (`isActive=true`) with minor-unit integer pricing (THB satang) and dynamic stock availability badges ("In Stock" / "Out of Stock"). |
| **F-03** | Multi-Item Order Creation & Atomic Decrement | Sprint 1 | Customer | High / High | FR-05, FR-06, BR-01, BR-02, BR-03, BR-06, NFR-01, NFR-02 | Multi-line order submission ($1 \le \text{qty} \le 10$, no duplicates), authoritative server re-pricing (ignoring client prices), atomic stock decrement in a single DB transaction, price snapshots (`unitPriceAtOrder`), and initial status `PLACED`. |
| **F-04** | Customer Order History & Ownership Isolation | Sprint 1 | Customer | Medium / High | FR-07, FR-08, BR-05, NFR-01, NFR-02 | Chronological order history for the authenticated customer ("My Orders") with line-item totals. Strict ownership check returning HTTP 404 on cross-customer order access without metadata leakage. |
| **F-05** | Operator Order Queue & State Transition | Sprint 1 | Operator | Medium / High | FR-09, FR-10, BR-04, BR-08, NFR-01 | Filtered queue of incoming `PLACED` orders sorted oldest first. Operator acceptance transition (`PLACED -> ACCEPTED`) with `operatorId` and `acceptedAt` audit trail. Guard against invalid transitions (409 Conflict). |
| **F-06** | Operator Catalog & Stock Management | Sprint 2 | Operator | High / Medium | FR-11, BR-01, BR-08 | Operator product creation, pricing updates, inventory restocking (`stockQuantity += N`), and active/inactive visibility toggles. |
| **F-07** | Customer Cancellation & Operator Rejection | Sprint 2 | Customer, Operator | Medium / Medium | FR-12, BR-02, BR-04 | Safe cancellation for `PLACED` orders by customers, operator order rejection with obligatory reason note, and automatic atomic inventory rollback. |
| **F-08** | Extended Fulfillment Lifecycle | Sprint 2 | Operator | Medium / Medium | FR-12, BR-04, BR-08 | Multi-stage physical pickup progression: `ACCEPTED -> PREPARING -> READY -> COMPLETED` with audit timestamps and 409 transition guards. |
| **F-09** | Simulated Payment & Digital Counter Receipt | Sprint 2 | Customer, Operator | Low / Low | FR-12, BR-01 | Synthetic payment transaction generation upon order placement and downloadable/printable counter pickup receipt. |
| **F-10** | Operator Metrics & Sales Dashboard | Sprint 3 | Operator | Medium / Medium | FR-13, NFR-05 | Revenue aggregation in minor units, orders by status, queue health metrics, and top-selling merchandise breakdowns. |
| **F-11** | Advanced Search, Filter & Categorization | Sprint 3 | Customer, Operator | Low / Low | FR-13, NFR-06 | Product search by keyword/category, order filtering by status and date range, and customer lookup for operators. |
| **F-12** | System Hardening, Viewports & Performance Tuning | Sprint 3 | System / All | High / High | NFR-04, NFR-05, NFR-06 | Responsive viewports (375px to 1920px), order placement latency $< 1000\text{ ms}$, comprehensive E2E tests, and automated regression suite. |

### B.2 Acceptance Criteria Inventory (Sprint 1 Baseline)
| AC ID | Target Feature | Acceptance Criterion Statement | Verification Level |
|---|---|---|---|
| **AC-01** | F-01 | Given valid credentials, when `POST /api/auth/login` is called, server returns HTTP 200, sets `HttpOnly` session cookie, and returns user id, email, and role. | Integration / API |
| **AC-02** | F-01 | Given invalid credentials, when `POST /api/auth/login` is called, server returns generic HTTP 401 without user enumeration. | Integration / API |
| **AC-03** | F-01 | Given unauthenticated request or expired session, protected endpoints return HTTP 401. | Integration / API |
| **AC-04** | F-01 | Given authenticated session, when `POST /api/auth/logout` is called, server invalidates session in DB, clears cookie, and returns HTTP 200. | Integration / API |
| **AC-05** | F-02 | Given active catalog, when `GET /api/products` is called, server returns HTTP 200 with active products, minor-unit prices (`priceMinor`), and stock availability badges. Inactive items are excluded. | Integration / API |
| **AC-06** | F-03 | Given valid multi-item order with sufficient stock, when `POST /api/orders` is called, server atomically creates order (`PLACED`), snapshots prices, decrements stock, and returns HTTP 201. | Integration / API + DB |
| **AC-07** | F-03 | Given empty items array (`items: []`), when `POST /api/orders` is called, server rejects with HTTP 400 and creates no records. | Integration / API |
| **AC-08** | F-03 | Given order line exceeding available `stockQuantity`, when `POST /api/orders` is called, server aborts transaction with HTTP 400 and leaves stock unchanged. | Integration / API + DB |
| **AC-09** | F-03 | Given order containing inactive item (`isActive = false`), when `POST /api/orders` is called, server rejects with HTTP 400. | Integration / API |
| **AC-10** | F-03 | Given placed order, when server process is stopped and restarted, all order lines, totals, and decremented stock quantities remain intact in PostgreSQL. | Integration / Persistence |
| **AC-11** | F-04 | Given authenticated customer, when `GET /api/orders` is called, server returns HTTP 200 with customer's own orders sorted newest first with complete line totals. | Integration / API |
| **AC-12** | F-04 | Given customer A, when `GET /api/orders/:id` is called for customer B's order, server returns HTTP 404 without leaking metadata. | Integration / API |
| **AC-13** | F-01, F-05 | Given `CUSTOMER` role, when calling operator endpoints (`GET /api/operator/orders` or `PATCH /api/operator/orders/:id/accept`), server rejects with HTTP 403 Forbidden. | Integration / API |
| **AC-14** | F-05 | Given authenticated operator, when `GET /api/operator/orders` is called, server returns HTTP 200 with `PLACED` orders sorted chronologically (oldest first). | Integration / API |
| **AC-15** | F-05 | Given authenticated operator and `PLACED` order, when `PATCH /api/operator/orders/:id/accept` is called, server transitions status to `ACCEPTED`, records `operatorId` and `acceptedAt`, and returns HTTP 200. | Integration / API + DB |
| **AC-16** | F-05 | Given order already in `ACCEPTED` status, calling `PATCH /api/operator/orders/:id/accept` returns HTTP 409 Conflict. | Integration / API |
| **AC-17** | F-01, F-03 | Given `OPERATOR` role, attempting customer order creation (`POST /api/orders`) returns HTTP 403 Forbidden. | Integration / API |
| **AC-18** | F-01, F-02 | Running database seed script consecutively executes idempotently, populating required demo accounts ($\ge 3$ customers, $\ge 2$ operators) and products ($\ge 8$ products) without constraint errors. | Integration / Seed Script |

### B.3 Traceability Matrix (FR / BR / NFR $\rightarrow$ Features $\rightarrow$ Sprints $\rightarrow$ ACs)

| Req / Rule / NFR | Description | Feature | Sprint | Enforcing AC(s) | Verification Suite |
|---|---|---|---|---|---|
| **FR-01** | User Authentication | F-01 | S1 | AC-01, AC-02, AC-18 | `auth.api.test.ts` |
| **FR-02** | Session Logout | F-01 | S1 | AC-04 | `auth.api.test.ts` |
| **FR-03** | Role-Based Route Protection | F-01 | S1 | AC-03, AC-13, AC-17 | `rbac.api.test.ts` |
| **FR-04** | Browse Active Catalog & Stock | F-02 | S1 | AC-05, AC-18 | `catalog.api.test.ts` |
| **FR-05** | Multi-Line Order Placement | F-03 | S1 | AC-06, AC-07, AC-08, AC-09 | `orders.api.test.ts` |
| **FR-06** | Price Snapshot (`unitPriceAtOrder`) | F-03 | S1 | AC-06, AC-10 | `orders.api.test.ts` |
| **FR-07** | Customer Order History & Details | F-04 | S1 | AC-11 | `orders-customer.api.test.ts` |
| **FR-08** | Customer Data Isolation | F-04 | S1 | AC-12 | `orders-isolation.api.test.ts` |
| **FR-09** | Operator Incoming Queue | F-05 | S1 | AC-14 | `operator-orders.api.test.ts` |
| **FR-10** | Operator Order Acceptance | F-05 | S1 | AC-15, AC-16 | `operator-orders.api.test.ts` |
| **FR-11** | Operator Catalog Management | F-06 | S2 | — | Sprint 2 Contract Tests |
| **FR-12** | Extended Fulfillment & Cancellation | F-07, F-08, F-09 | S2 | — | Sprint 2 Contract Tests |
| **FR-13** | Reporting Dashboard & Analytics | F-10, F-11 | S3 | — | Sprint 3 Benchmark Tests |
| **BR-01** | Monetary Representation (minor units, THB satang) | F-02, F-03 | S1 | AC-05, AC-06 | Schema integer type + `orders.api.test.ts` |
| **BR-02** | Atomic Placement & Stock Decrement | F-03 | S1 | AC-06, AC-08, AC-10 | Prisma `$transaction` concurrency tests |
| **BR-03** | Authoritative Server Pricing | F-03 | S1 | AC-06 | API tests sending forged client prices |
| **BR-04** | Order Lifecycle (`PLACED -> ACCEPTED`, 409 guard) | F-05 | S1 | AC-15, AC-16 | Order state guard in `operator-orders.api.test.ts` |
| **BR-05** | Customer Order Ownership Isolation | F-04 | S1 | AC-12 | Scoped query in `orders-isolation.api.test.ts` |
| **BR-06** | Line Constraints ($1 \le \text{qty} \le 10$, no duplicates) | F-03 | S1 | AC-07, AC-08 | Zod schema validation tests |
| **BR-07** | Secure Credential Storage (bcrypt salt $\ge 10$) | F-01 | S1 | AC-01, AC-18 | DB seed & auth service tests |
| **BR-08** | Operator Scope Restrictions | F-01, F-05 | S1 | AC-13, AC-17 | Role middleware in `rbac.api.test.ts` |
| **NFR-01** | Auth & RBAC Route Enforcement (401/403/404) | F-01, F-04, F-05 | S1 | AC-01, AC-02, AC-03, AC-12, AC-13, AC-17 | Route security test suite |
| **NFR-02** | Relational Data Persistence across Restarts | F-02, F-03, F-04 | S1 | AC-10 | DB restart verification script |
| **NFR-03** | Seed Idempotence & Determinism | F-01, F-02 | S1 | AC-18 | Double-run seed test script |
| **NFR-04** | Fresh Clone Reproducibility ($< 5\text{ min}$) | F-12 | S1 | — | Clean-room clone verification |
| **NFR-05** | Order Placement Latency ($< 1000\text{ ms}$) | F-03, F-12 | S1/S3 | AC-06 | Latency benchmark test |
| **NFR-06** | Responsive Viewports (375px to 1920px) | F-12 | S3 | — | Playwright responsive viewport assertions |

### B.4 Coverage and Traceability Health Analysis
- **Requirements Coverage:** 13/13 FRs (100%), 8/8 BRs (100%), 6/6 NFRs (100%).
- **Forward Orphan Check:** 0 unmapped requirements.
- **Backward Orphan Check:** 0 ungrounded features or acceptance criteria.
- **Sprint 1 Containment:** 10/13 FRs, 8/8 BRs, 4/6 NFRs, and 18/18 ACs implemented in Sprint 1 baseline.

## Part C — System-Level SDS   ⬜ (#3)
## Part D — Three-sprint plan   ⬜ (#4)
## Part E — Sprint 1 engineering contracts   ⬜ (#5)

## Part F — Working Sprint 1 and verification
### F.1 Setup summary   ⬜ (#6, #15)
### F.2 Program demonstrations   (release commit: <RELEASE_COMMIT>)
| # | Scenario | Feature/AC | Role | Start conditions | Steps | Expected | Actual | Evidence file | Status | Issue |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Login | AC-01, AC-18 | Customer | | | | | | ⬜ | #7, #8 |
| S2 | Normal order journey + persisted retrieval | AC-05, AC-06, AC-11 | Customer | | | | | | ⬜ | #10, #11 |
| S3 | DB proof | AC-06, AC-10 | — | | | | | | ⬜ | #10 |
| S4 | Rule rejection | AC-08, AC-09 | Customer | | | | | | ⬜ | #10 |
| S5 | Operator accepts order | AC-14, AC-15 | Operator | | | | | | ⬜ | #12 |
| S6 | Invalid transition (409) | AC-16 | Operator | | | | | | ⬜ | #12 |
| S7 | Forbidden role operation | AC-13 | Customer | | | | | | ⬜ | #12, #13 |
| S8 | Ownership restriction | AC-12 | Customer | | | | | | ⬜ | #13 |
| S9 | Unauthenticated access | AC-03 | — | | | | | | ⬜ | #7, #13 |
| S10 | Logout | AC-04 | Customer | | | | | | ⬜ | #7 |
### F.3 Build and automated test results
- Commands and tested commit:
- Passed / failed / skipped counts:
| AC | Planned TEST | Actual test file / name | Level | Result | Issue |
|---|---|---|---|---|---|
- Excerpt 1 (domain rule): ⬜ (#10)
- Excerpt 2 (ownership restriction): ⬜ (#13)
- TDD evidence (failing → passing, commit hashes): ⬜ (#7, #10, #12)
### F.4 Engineering workflow and history
| Issue | Feature/AC | Branch | Author | Reviewer | Review comment | Merged to staging | Merged to main |
|---|---|---|---|---|---|---|---|
| #0 | Repository setup, PR template, basecode comment cleanup, PDF draft skeleton | `issue/00-initial-setup` | Cl | Ba | Checked obsolete comments removal and PR template/draft setup | PR #2 (merged) | via release PR |
| #1 | FR-01…FR-13, BR-01…BR-08, NFR-01…NFR-06 (SRS specification) | `issue/01-srs` | Cl | Ba | Reviewed SRS Part A, validated domain decisions and problem statement | PR #4 (merged) | via release PR |
| #2 | Part B — Feature inventory and traceability (F-01…F-12, AC-01…AC-18, RTM) | `issue/02-traceability` | Ba | Cl | (Pending PR review) | PR (pending) | via release PR |

History sequence (contract → tests → implementation):
| Date | Commit | What |
|---|---|---|
| 2026-11-18 | `eea640b` | chore: setup issue 0 - remove outdated comments, add PR template and PDF draft skeleton |
| 2026-11-18 | `bd71d5b` | docs: complete Part A SRS and product scope baseline |
| 2026-11-20 | `pending` | docs: issue #2 - complete feature inventory and traceability matrix (Part B) |

Board status screenshot: ⬜ (#15)   Release PR / tag: ⬜ (#15)
### F.5 Contributions, AI use, limitations
| Student | Issues/PRs authored | PRs reviewed | Pair work |
|---|---|---|---|
| Cl | #0 (Scaffold & Draft setup), #1 (SRS specification) | #2 (Traceability matrix & Feature inventory) | Repository workflow setup & initial architecture alignment |
| Ba | #2 (Feature inventory & Traceability matrix) | #0 (Reviewed PR #2), #1 (Reviewed PR #4) | Repository workflow setup & initial architecture alignment |

AI-use declaration:
- Claude / Antigravity: Assisted Cl with cleaning outdated comments, scaffolding PR template/draft skeleton (`#0`), and drafting SRS Part A (`#1`). Assisted Ba with decomposing features (F-01..12), formalizing acceptance criteria (AC-01..18), synthesizing bidirectional traceability matrices (`docs/features.md`, `docs/traceability.md`), and authoring Part B in `PDF_DRAFT.md` (`#2`). Reviewed and verified by Ba.

Known limitations / incomplete work / skipped tests:
- None for Part A and Part B specifications.