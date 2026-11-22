# Feature Contract: F-03 — Multi-Item Order Placement with Server Pricing & Atomic Stock Decrement

**Sprint:** Sprint 1 Baseline  
**Feature ID:** F-03  
**Primary Actors:** Customer  
**Linked Requirements:** `FR-05`, `FR-06`, `BR-01`, `BR-02`, `BR-03`, `BR-06`, `NFR-01`, `NFR-02`, `NFR-05`  
**Planned Acceptance Criteria:** `AC-06`, `AC-07`, `AC-08`, `AC-09`, `AC-10`  
**STS Test Mappings:** `TEST-07`, `TEST-08`, `TEST-09`, `TEST-10`, `TEST-11`, `TEST-12`, `TEST-21`  

---

## 1. Overview & Business Workflow

`F-03` is the transactional core of the UniMerch store. It allows authenticated customers to submit orders containing multiple items. The server guarantees transactional integrity, authoritative pricing, historical price preservation, and atomic inventory reduction.

### Order Submission Workflow
1. Customer selects 1 to $N$ catalog items with quantities ($1 \le \text{qty} \le 10$).
2. Customer reviews cart summary and clicks "Place Order".
3. Client issues `POST /api/orders` sending only an array of `{ productId, quantity }`. Any client-sent prices or totals are strictly ignored.
4. Server initiates an isolated database transaction (`prisma.$transaction`):
   - Validates user session and role (`CUSTOMER`).
   - Validates payload format (checks for empty array, non-integer quantity, duplicate `productId`).
   - Fetches target products by ID from PostgreSQL with row locks.
   - Verifies each product is active (`isActive = true`) and has sufficient inventory (`stockQuantity >= quantity`).
   - Computes line total (`unitPrice * quantity`) and order total in integer satang (`BR-01`, `BR-03`).
   - Creates the `Order` record with status `PLACED`, `customerId = session.userId`, and calculated `totalMinor`.
   - Creates child `OrderItem` records recording `quantity` and snapshotting `unitPriceAtOrder` (`FR-06`).
   - Atomically decrements `stockQuantity` on each ordered product (`BR-02`).
5. Transaction commits. Server responds with HTTP 201 Created and the full order record.
6. If any product is inactive, missing, or has insufficient stock, the transaction is **aborted completely**. Stock remains untouched, and no records are persisted.

---

## 2. Dependencies & Enforced Business Rules

- **Dependencies:** `F-01` (authenticated session), `F-02` (product catalog).
- **Enforced Business Rules:**
  - `BR-01` (Minor-Unit Currency): All prices and totals computed in satang (`Int`).
  - `BR-02` (Atomic Decrement & Rollback): All validation and updates execute inside a single atomic ACID transaction. If one item fails, the whole order rolls back.
  - `BR-03` (Authoritative Server Pricing): Client-supplied prices/totals are discarded; prices are queried from the database at order time.
  - `BR-04` (Order Lifecycle): Initial status is strictly `PLACED`.
  - `BR-06` (Line Constraints): $1 \le \text{quantity} \le 10$. Exactly one line per unique product (no duplicate `productId` in same payload).
  - `FR-06` (Price Snapshot): `OrderItem.unitPriceAtOrder` captures the exact price at order placement time, preserving historical accuracy against future product price modifications.

---

## 3. Boundary, Negative & Failure Cases

- **Empty Items Array:** `POST /api/orders` with `items: []` $\rightarrow$ `HTTP 400 Bad Request`.
- **Invalid Quantity:** `quantity = 0`, `-2`, `1.5`, or `11` $\rightarrow$ `HTTP 400 Bad Request`.
- **Duplicate Product Lines:** Payload containing multiple lines for the same `productId` $\rightarrow$ `HTTP 400 Bad Request`.
- **Insufficient Stock:** Requested quantity exceeds `Product.stockQuantity` $\rightarrow$ `HTTP 400 Bad Request` with `{ "error": "Insufficient stock for product: <name>" }`.
- **Inactive Product:** Payload references an item with `isActive = false` $\rightarrow$ `HTTP 400 Bad Request`.
- **Client Price Tampering:** Payload includes `"price": 1` or `"total": 100` $\rightarrow$ Server ignores client values and calculates true total from database.
- **Role Violation:** User with `OPERATOR` role attempts to place order $\rightarrow$ `HTTP 403 Forbidden`.

---

## 4. UI Behavior & View States

- **Checkout Modal / Screen (`/cart`):**
  - Summary table listing items, quantities, unit prices, line totals, and grand total.
  - "Place Order" button with loading indicator during submission.
  - Immediate visual feedback on failure: specific error alert displaying stockout or validation message.
  - On HTTP 201: Redirect to Order Confirmation screen (`/orders/:id`) displaying order ID, status badge `PLACED`, line items, and pickup instructions.

---

## 5. API Specification

### 5.1 POST `/api/orders`
- **Access:** Authenticated (`CUSTOMER` only)
- **Headers:** `Cookie: sid=<token>`, `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "items": [
      {
        "productId": "prod_hoodie01",
        "quantity": 2
      },
      {
        "productId": "prod_pen01",
        "quantity": 3
      }
    ]
  }
  ```
- **Response `201 Created`:**
  ```json
  {
    "order": {
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
        },
        {
          "id": "item_222",
          "productId": "prod_pen01",
          "productName": "Engraved UniMerch Ballpoint Pen",
          "quantity": 3,
          "unitPriceAtOrder": 5000,
          "lineTotalMinor": 15000
        }
      ]
    }
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: `{ "error": "Insufficient stock for product: UniMerch Heavyweight Hoodie" }`
  - `401 Unauthorized`: `{ "error": "Authentication required" }`
  - `403 Forbidden`: `{ "error": "Operators cannot place customer orders" }`

---

## 6. Data Model & Database Constraints

```prisma
model Order {
  id                   String      @id @default(cuid())
  customerId           String
  customer             User        @relation("CustomerOrders", fields: [customerId], references: [id])
  status               OrderStatus @default(PLACED)
  totalMinor           Int         // Computed strictly on server
  createdAt            DateTime    @default(now())
  acceptedAt           DateTime?
  acceptedByOperatorId String?
  items                OrderItem[]

  @@index([customerId])
  @@index([status])
}

model OrderItem {
  id               String   @id @default(cuid())
  orderId          String
  order            Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  productId        String
  product          Product  @relation(fields: [productId], references: [id])
  quantity         Int      // Constraint: 1 <= quantity <= 10
  unitPriceAtOrder Int      // Snapshot of Product.priceMinor at purchase time

  @@unique([orderId, productId])
}

enum OrderStatus {
  PLACED
  ACCEPTED
}
```

---

## 7. Acceptance Criteria (AC)

- **AC-06:** Given authenticated customer and valid multi-item payload with sufficient stock, server atomically creates order with status `PLACED`, snapshots item prices (`unitPriceAtOrder`), decrements product inventory, and returns HTTP 201.
- **AC-07:** Client-supplied totals, unit prices, or line prices are ignored; server computes authoritative total from database prices.
- **AC-08:** Payloads with empty items, zero quantity, negative quantity, quantity $> 10$, or duplicate product IDs are rejected with HTTP 400 and create no records.
- **AC-09:** If any item is inactive or has insufficient stock, server aborts transaction with HTTP 400 and leaves inventory completely unchanged.
- **AC-10:** Subsequent changes to product catalog prices do not alter historical orders or their line item unit prices.
