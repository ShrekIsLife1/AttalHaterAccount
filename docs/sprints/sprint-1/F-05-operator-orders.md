# Feature Contract: F-05 — Operator Order Queue & Single-Step Acceptance

**Sprint:** Sprint 1 Baseline  
**Feature ID:** F-05  
**Primary Actors:** Operator  
**Linked Requirements:** `FR-09`, `FR-10`, `BR-04`, `BR-08`, `NFR-01`  
**Planned Acceptance Criteria:** `AC-13`, `AC-14`, `AC-15`, `AC-16`  
**STS Test Mappings:** `TEST-16`, `TEST-17`, `TEST-18`, `TEST-19`, `TEST-20`  

---

## 1. Overview & Business Workflow

`F-05` implements the store operator's order processing workflow for Sprint 1. Operators monitor incoming customer orders and accept them for preparation. The system enforces strict role-based authorization and state machine transition guards: only orders in the `PLACED` status can transition to `ACCEPTED`. Any invalid or duplicate transition attempt is rejected with HTTP 409 Conflict.

### Operator Workflow
1. Operator logs in and accesses the "Incoming Orders" view (`/operator/orders`).
2. Client queries `GET /api/operator/orders`.
3. Server verifies operator session (`role === 'OPERATOR'`).
4. Server retrieves orders with status `PLACED`, ordered chronologically (oldest first: `createdAt ASC`) to prioritize first-come-first-served fulfillment.
5. Operator reviews order lines, customer email, and total, and clicks "Accept Order".
6. Client issues `PATCH /api/operator/orders/:id/accept`.
7. Server validates order state:
   - If order is not found $\rightarrow$ `HTTP 404 Not Found`.
   - If order is already in status `ACCEPTED` (or any non-PLACED state) $\rightarrow$ `HTTP 409 Conflict`.
   - If order is in status `PLACED`:
     - Updates `status` to `ACCEPTED`.
     - Records `acceptedAt = now()`.
     - Records `acceptedByOperatorId = session.userId`.
8. Server responds with HTTP 200 OK and updated order payload.

---

## 2. Dependencies & Enforced Business Rules

- **Dependencies:** `F-01` (operator session), `F-03` (placed orders).
- **Enforced Business Rules:**
  - `BR-04` (Order Lifecycle): In Sprint 1, the only allowed status transition is `PLACED -> ACCEPTED`. Any attempt to transition an already accepted order must return `HTTP 409 Conflict`.
  - `BR-08` (Operator Scope and Role Restrictions): Only authenticated users with role `OPERATOR` are authorized to list incoming orders or trigger the accept transition. Requests by a `CUSTOMER` must be rejected with `HTTP 403 Forbidden`.

---

## 3. Boundary, Negative & Failure Cases

- **Role Violation:** Customer attempts to call `GET /api/operator/orders` or `PATCH /api/operator/orders/:id/accept` $\rightarrow$ `HTTP 403 Forbidden`.
- **Double Acceptance:** Operator calls accept on an order that is already `ACCEPTED` $\rightarrow$ `HTTP 409 Conflict` with `{ "error": "Order is already accepted" }`. Order data and timestamps remain unchanged.
- **Unauthenticated Call:** Operator endpoint called without session cookie $\rightarrow$ `HTTP 401 Unauthorized`.
- **Non-Existent Order:** `PATCH /api/operator/orders/invalid_id/accept` $\rightarrow$ `HTTP 404 Not Found`.

---

## 4. UI Behavior & View States

- **Operator Incoming Orders Queue (`/operator/orders`):**
  - Queue table listing pending orders: Order ID, Customer Email, Placement Time, Elapsed Time, Total Items, Grand Total, and an "Accept Order" action button.
  - Sorted oldest first (`createdAt ASC`).
  - "Accept Order" button triggers immediate optimistic UI state update with disabled loading spinner.
  - Upon successful acceptance, order disappears from the `PLACED` queue and moves to an "Accepted Today" summary section or displays confirmation toast.
  - Empty Queue: Friendly alert ("All caught up! No pending incoming orders.").

---

## 5. API Specification

### 5.1 GET `/api/operator/orders`
- **Access:** Authenticated (`OPERATOR` only)
- **Headers:** `Cookie: sid=<token>`
- **Response `200 OK`:**
  ```json
  [
    {
      "id": "ord_a1b2c3d4",
      "customerId": "usr_c1a2b3c4d5",
      "customerEmail": "customer1@example.com",
      "status": "PLACED",
      "totalMinor": 165000,
      "createdAt": "2026-11-22T08:30:00.000Z",
      "items": [
        {
          "productName": "UniMerch Heavyweight Hoodie",
          "quantity": 2,
          "unitPriceAtOrder": 75000
        }
      ]
    }
  ]
  ```
- **Error Responses:**
  - `401 Unauthorized`: Missing or invalid session.
  - `403 Forbidden`: User role is `CUSTOMER`.

### 5.2 PATCH `/api/operator/orders/:id/accept`
- **Access:** Authenticated (`OPERATOR` only)
- **Headers:** `Cookie: sid=<token>`
- **Response `200 OK`:**
  ```json
  {
    "order": {
      "id": "ord_a1b2c3d4",
      "status": "ACCEPTED",
      "acceptedAt": "2026-11-22T08:35:12.000Z",
      "acceptedByOperatorId": "usr_op111222"
    }
  }
  ```
- **Error Responses:**
  - `403 Forbidden`: User role is `CUSTOMER`.
  - `404 Not Found`: Order ID does not exist.
  - `409 Conflict`: Order is not in `PLACED` status (`{ "error": "Order cannot be accepted from current status" }`).

---

## 6. Data Model & Database Constraints

- Updates `Order.status`, `Order.acceptedAt`, and `Order.acceptedByOperatorId`.
- Database index on `Order.status` ensures efficient filtering for the operator incoming queue.

---

## 7. Acceptance Criteria (AC)

- **AC-13:** Calling operator endpoints (`GET /api/operator/orders` or `PATCH /api/operator/orders/:id/accept`) as a user with role `CUSTOMER` returns HTTP 403 Forbidden.
- **AC-14:** Calling `GET /api/operator/orders` as an operator returns all incoming orders with status `PLACED`, ordered chronologically (oldest first).
- **AC-15:** Given an order in `PLACED` status, calling `PATCH /api/operator/orders/:id/accept` transitions status to `ACCEPTED`, records `operatorId` and `acceptedAt` timestamp, and returns HTTP 200.
- **AC-16:** Calling `PATCH /api/operator/orders/:id/accept` on an already accepted order returns HTTP 409 Conflict and leaves database records unchanged.
