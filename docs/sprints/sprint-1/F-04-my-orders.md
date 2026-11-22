# Feature Contract: F-04 — Customer Order History & Ownership Isolation

**Sprint:** Sprint 1 Baseline  
**Feature ID:** F-04  
**Primary Actors:** Customer  
**Linked Requirements:** `FR-07`, `FR-08`, `BR-05`, `NFR-01`, `NFR-02`  
**Planned Acceptance Criteria:** `AC-11`, `AC-12`  
**STS Test Mappings:** `TEST-13`, `TEST-14`, `TEST-15`  

---

## 1. Overview & Business Workflow

`F-04` enables authenticated customers to view their purchase history and track the fulfillment status of their orders. A core security requirement is **ownership isolation**: customers can only query orders associated with their own authenticated session ID. Attempts to query orders belonging to other customers are rejected with HTTP 404 (Not Found) without confirming the order's existence, preventing data leakage or user enumeration.

### Order History Workflow
1. Customer navigates to "My Orders" (`/orders`).
2. Client queries `GET /api/orders`.
3. Server identifies customer from session cookie (`session.userId`) and queries the `Order` table strictly filtered by `customerId = session.userId`, sorted newest first (`createdAt DESC`).
4. Response returns a summary list of orders (ID, date, status, total).
5. Customer clicks on a specific order to view details (`/orders/:id`).
6. Client queries `GET /api/orders/:id`.
7. Server queries the order by ID. If the order does not exist OR `order.customerId !== session.userId`, the server returns HTTP 404 with a generic error message.
8. If ownership matches, the server returns full order details including line items, snapshot unit prices, and status.

---

## 2. Dependencies & Enforced Business Rules

- **Dependencies:** `F-01` (authenticated session), `F-03` (placed orders).
- **Enforced Business Rules:**
  - `BR-05` (Customer Order Ownership Isolation): A customer can only access order records where `customerId == req.session.userId`.
  - `NFR-01` (Security & Data Isolation): Attempting to access an order belonging to another customer must return `HTTP 404 Not Found` with an empty/generic error payload. The server must never return HTTP 403 or confirm the order ID exists for another customer.

---

## 3. Boundary, Negative & Failure Cases

- **Cross-Customer Order Access:** Customer A attempts to access Customer B's order (`GET /api/orders/ord_customer_b`) $\rightarrow$ `HTTP 404 Not Found` with `{ "error": "Order not found" }`.
- **Non-Existent Order:** `GET /api/orders/ord_nonexistent` $\rightarrow$ `HTTP 404 Not Found`.
- **Unauthenticated Access:** Request without session cookie $\rightarrow$ `HTTP 401 Unauthorized`.
- **Empty Order History:** Customer with no orders receives `HTTP 200` with `[]`; UI renders friendly empty state ("You haven't placed any orders yet").

---

## 4. UI Behavior & View States

- **My Orders List (`/orders`):**
  - Table of past orders: Order ID, Placement Date/Time, Status Badge (`PLACED` in blue, `ACCEPTED` in green), Total Amount (formatted THB), and "View Details" link.
  - Sorted newest first.
  - Empty State: Message with link back to catalog ("No orders found. Start shopping!").
- **Order Detail View (`/orders/:id`):**
  - Order header with status badge, creation date, and accepted timestamp (if accepted).
  - Detailed line items table: Product Name, Snapshot Unit Price, Quantity, Line Total.
  - Grand total summary in formatted THB.
  - "Back to Orders" navigation button.

---

## 5. API Specification

### 5.1 GET `/api/orders`
- **Access:** Authenticated (`CUSTOMER` only)
- **Headers:** `Cookie: sid=<token>`
- **Response `200 OK`:**
  ```json
  [
    {
      "id": "ord_a1b2c3d4",
      "status": "PLACED",
      "totalMinor": 165000,
      "createdAt": "2026-11-22T08:30:00.000Z",
      "acceptedAt": null,
      "itemCount": 2
    }
  ]
  ```

### 5.2 GET `/api/orders/:id`
- **Access:** Authenticated (`CUSTOMER` matching order ownership)
- **Headers:** `Cookie: sid=<token>`
- **Response `200 OK`:**
  ```json
  {
    "id": "ord_a1b2c3d4",
    "customerId": "usr_c1a2b3c4d5",
    "status": "PLACED",
    "totalMinor": 165000,
    "createdAt": "2026-11-22T08:30:00.000Z",
    "acceptedAt": null,
    "acceptedByOperatorId": null,
    "items": [
      {
        "id": "item_111",
        "productId": "prod_hoodie01",
        "productName": "UniMerch Heavyweight Hoodie",
        "quantity": 2,
        "unitPriceAtOrder": 75000,
        "lineTotalMinor": 150000
      }
    ]
  }
  ```
- **Error Responses:**
  - `401 Unauthorized`: `{ "error": "Authentication required" }`
  - `404 Not Found`: `{ "error": "Order not found" }` (Returned for non-existent IDs and cross-customer IDs alike)

---

## 6. Data Model & Database Constraints

- Reuses `Order` and `OrderItem` models specified in `F-03`.
- Relies on database foreign key index on `Order.customerId` for high-performance scoped lookups.

---

## 7. Acceptance Criteria (AC)

- **AC-11:** Given authenticated customer, calling `GET /api/orders` returns only orders belonging to that customer, sorted newest first with complete totals.
- **AC-12:** Given Customer A, calling `GET /api/orders/:id` for an order belonging to Customer B returns HTTP 404 and leaks no metadata.
