# Feature Inventory

**Project:** UniMerch Campus Store (Theme 4: E-Commerce or Ordering System)  
**Course:** CPE 334 — Introduction to Software Engineering in the Age of AI Agents  
**Authors:** Student Ba (Author, Issue #2) & Student Cl (Reviewer)  
**Status:** Approved Baseline  

---

## 1. Overview & Feature Strategy

The UniMerch Campus Store feature breakdown follows a strict incremental strategy across three sprints:
- **Sprint 1 (Baseline & Working Slice - CURRENT TARGET):** Complete end-to-end purchasing workflow from authenticated customer catalog browsing to atomic multi-line order placement and operator order acceptance.
- **Sprint 2 (Core Operational Expansion - DEFERRED):** Operator catalog and stock management, customer cancellation, operator order rejection, extended fulfillment lifecycle, and simulated payment.
- **Sprint 3 (Hardening, Analytics & Experience - DEFERRED):** Operator operational dashboard, search/filtering, responsiveness, and performance hardening.

> **Strict Sprint 1 Boundary Enforcement:**  
> Only Sprint 1 features (`F-01` to `F-05`) and their associated Acceptance Criteria (`AC-01` to `AC-18`) are within the active implementation and testing scope of Deliverable 1. Features listed under Sprint 2 (`F-06`–`F-09`) and Sprint 3 (`F-10`–`F-12`) represent roadmap projections required for holistic traceability planning; they are strictly excluded from Sprint 1 codebase, Prisma schema increments, and test executions.

---

## 2. Sprint 1 Feature Inventory (Baseline Working Slice)

### Feature F-01: Session Authentication and Role-Based Access Control
- **Primary Actor:** Customer, Operator
- **Target Sprint:** Sprint 1
- **Complexity:** Medium
- **Purpose:** Secure the application using server-side session management with role-based segregation (`CUSTOMER` vs. `OPERATOR`).
- **Core Capabilities:**
  - Login via email and password using bcrypt-hashed credentials (`BR-07`).
  - Issue cryptographically secure random session tokens delivered in `HttpOnly`, `SameSite=Lax` cookies.
  - Active session validation middleware rejecting unauthenticated requests with generic HTTP 401 (`NFR-01`).
  - Role-based authorization middleware rejecting unauthorized operations with HTTP 403 (`FR-03`, `BR-08`).
  - Explicit logout endpoint invalidating sessions server-side in the database (`FR-02`).
- **Associated Requirements:** `FR-01`, `FR-02`, `FR-03`, `BR-07`, `BR-08`, `NFR-01`
- **Acceptance Criteria:** `AC-01`, `AC-02`, `AC-03`, `AC-04`, `AC-13`

### Feature F-02: Authoritative Product Catalog & Availability Display
- **Primary Actor:** Customer
- **Target Sprint:** Sprint 1
- **Complexity:** Low
- **Purpose:** Provide customers with an authoritative, read-only view of merchandise with real-time stock levels and non-floating-point prices.
- **Core Capabilities:**
  - Retrieve active products (`isActive = true`) ordered predictably (`FR-04`).
  - Display prices strictly in minor units (integer satang, e.g. 25000 = 250.00 THB) (`BR-01`).
  - Compute availability badges dynamically: "In Stock" (`stockQuantity > 0`) or "Out of Stock" (`stockQuantity = 0`).
  - Filter out inactive products from standard customer catalog view.
- **Associated Requirements:** `FR-04`, `BR-01`, `NFR-02`
- **Acceptance Criteria:** `AC-05`

### Feature F-03: Multi-Item Order Creation with Server-Side Validation & Atomic Decrement
- **Primary Actor:** Customer
- **Target Sprint:** Sprint 1
- **Complexity:** High
- **Purpose:** Enable customers to assemble and submit multi-item orders with strict server-side inventory verification, authoritative pricing, and atomic stock updates.
- **Core Capabilities:**
  - Accept order payloads containing 1 to $N$ order lines (`productId`, `quantity`).
  - Enforce quantity boundaries ($1 \le \text{quantity} \le 10$) and reject duplicate product IDs within a single payload (`BR-06`).
  - Discard any client-sent prices; re-query authoritative prices from database (`BR-03`).
  - Execute inventory validation and atomic stock decrement inside an all-or-nothing database transaction (`BR-02`).
  - Reject order with HTTP 400 if any requested item is inactive (`isActive = false`) or has insufficient stock.
  - Capture price snapshots (`unitPriceAtOrder`) for every line item to preserve historical accuracy (`FR-06`).
  - Initialize order with status `PLACED` and record creation timestamp (`FR-05`).
- **Associated Requirements:** `FR-05`, `FR-06`, `BR-01`, `BR-02`, `BR-03`, `BR-06`, `NFR-01`, `NFR-02`
- **Acceptance Criteria:** `AC-06`, `AC-07`, `AC-08`, `AC-09`, `AC-10`

### Feature F-04: Customer Order History and Ownership-Isolated Detail Retrieval
- **Primary Actor:** Customer
- **Target Sprint:** Sprint 1
- **Complexity:** Medium
- **Purpose:** Allow customers to track their own orders while strictly preventing cross-customer data leakage.
- **Core Capabilities:**
  - Retrieve customer's own order history ("My Orders") ordered newest first (`FR-07`).
  - Retrieve individual order detail including item lines, quantities, unit prices at order time, and order total (`FR-07`).
  - Enforce ownership isolation: return HTTP 404 (with no metadata leak) if a customer attempts to query an order belonging to another customer (`FR-08`, `BR-05`).
- **Associated Requirements:** `FR-07`, `FR-08`, `BR-05`, `NFR-01`, `NFR-02`
- **Acceptance Criteria:** `AC-11`, `AC-12`

### Feature F-05: Operator Order Queue and Single-Step Acceptance Transition
- **Primary Actor:** Operator
- **Target Sprint:** Sprint 1
- **Complexity:** Medium
- **Purpose:** Allow store staff to view incoming customer orders and accept them for processing with full auditability.
- **Core Capabilities:**
  - Display incoming orders queue restricted to status `PLACED`, sorted chronologically (oldest first) (`FR-09`).
  - Enforce role check: reject access by `CUSTOMER` role with HTTP 403 (`FR-03`, `BR-08`).
  - Execute atomic order acceptance (`PLACED -> ACCEPTED`), recording accepting `operatorId` and `acceptedAt` timestamp (`FR-10`).
  - Guard state transitions: reject transitions on orders not in `PLACED` state with HTTP 409 Conflict (`BR-04`).
- **Associated Requirements:** `FR-09`, `FR-10`, `BR-04`, `BR-08`, `NFR-01`
- **Acceptance Criteria:** `AC-13`, `AC-14`, `AC-15`, `AC-16`, `AC-17`

---

## 3. Sprint 2 Feature Inventory (Core Expansion)

### Feature F-06: Operator Catalog & Inventory Management
- **Primary Actor:** Operator
- **Target Sprint:** Sprint 2
- **Complexity:** High
- **Purpose:** Empower store operators to manage the merchandise catalog without direct database access.
- **Core Capabilities:**
  - Create new product items with title, description, category, minor-unit price, initial stock, and active status.
  - Update product details, update prices (without affecting past orders), and restock inventory (`stockQuantity += N`).
  - Toggle product active state (`isActive: true/false`).
- **Associated Requirements:** `FR-11`, `BR-01`, `BR-08`

### Feature F-07: Customer Order Cancellation and Operator Rejection
- **Primary Actor:** Customer, Operator
- **Target Sprint:** Sprint 2
- **Complexity:** Medium
- **Purpose:** Provide safe escape paths for orders prior to physical preparation, with automatic inventory rollback.
- **Core Capabilities:**
  - Customer can cancel an order while it remains in `PLACED` status (`PLACED -> CANCELLED`).
  - Operator can reject an order with an obligatory reason note (`PLACED -> REJECTED` or `ACCEPTED -> REJECTED`).
  - Atomically restore product inventory on order cancellation or rejection.
- **Associated Requirements:** `FR-12`, `BR-02`, `BR-04`

### Feature F-08: Extended Order Fulfillment Lifecycle
- **Primary Actor:** Operator
- **Target Sprint:** Sprint 2
- **Complexity:** Medium
- **Purpose:** Track orders through physical pickup stages at the campus store counter.
- **Core Capabilities:**
  - Linear state progression: `ACCEPTED -> PREPARING -> READY -> COMPLETED`.
  - Record stage transition timestamps and acting operator ID.
  - Reject invalid or backwards state transitions with HTTP 409 Conflict.
- **Associated Requirements:** `FR-12`, `BR-04`, `BR-08`

### Feature F-09: Simulated Payment & Digital Counter Receipt
- **Primary Actor:** Customer, Operator
- **Target Sprint:** Sprint 2
- **Complexity:** Low
- **Purpose:** Provide realistic checkout payment confirmation without connecting to live bank APIs.
- **Core Capabilities:**
  - Synthetic payment transaction record created upon order confirmation.
  - Printable/downloadable HTML counter pickup receipt with QR code placeholder and order ID.
- **Associated Requirements:** `FR-12`, `BR-01`

---

## 4. Sprint 3 Feature Inventory (Hardening, Analytics & Polish)

### Feature F-10: Operator Metrics & Sales Analytics Dashboard
- **Primary Actor:** Operator
- **Target Sprint:** Sprint 3
- **Complexity:** Medium
- **Purpose:** Give store operators visibility into store performance, revenue, and queue health.
- **Core Capabilities:**
  - Compute summary metrics: total revenue (minor units), completed order count, active queue depth (`PLACED` + `ACCEPTED`).
  - Top-selling merchandise breakdown by units sold.
  - Daily/weekly order volume aggregation.
- **Associated Requirements:** `FR-13`, `NFR-05`

### Feature F-11: Advanced Search, Filtering, and Categorization
- **Primary Actor:** Customer, Operator
- **Target Sprint:** Sprint 3
- **Complexity:** Low
- **Purpose:** Streamline navigation in expanding merchandise catalogs and large order archives.
- **Core Capabilities:**
  - Full-text search by title/description for products.
  - Filter orders by date range, customer email (operator only), and fulfillment status.
- **Associated Requirements:** `FR-13`, `NFR-06`

### Feature F-12: System Hardening, Responsive Viewports & Performance Tuning
- **Primary Actor:** System / All
- **Target Sprint:** Sprint 3
- **Complexity:** High
- **Purpose:** Ensure production-grade reliability, accessibility, and high performance.
- **Core Capabilities:**
  - Responsive layout verified across mobile (375px), tablet (768px), and desktop (1920px) viewports (`NFR-06`).
  - Latency optimization ensuring 10-line order placement under 1000ms (`NFR-05`).
  - Comprehensive automated end-to-end regression test suite.
- **Associated Requirements:** `NFR-04`, `NFR-05`, `NFR-06`
