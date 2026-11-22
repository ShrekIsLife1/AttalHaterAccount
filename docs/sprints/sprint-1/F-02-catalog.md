# Feature Contract: F-02 — Product Catalog & Live Stock Availability

**Sprint:** Sprint 1 Baseline  
**Feature ID:** F-02  
**Primary Actors:** Customer  
**Linked Requirements:** `FR-04`, `BR-01`, `NFR-02`  
**Planned Acceptance Criteria:** `AC-05`, `AC-18`  
**STS Test Mappings:** `TEST-05`, `TEST-06`  

---

## 1. Overview & Business Workflow

`F-02` provides customers with an authoritative, read-only view of merchandise available at the UniMerch Campus Store. All prices are stored and transmitted strictly as integers in minor units (satang: 100 satang = 1.00 THB) to eliminate floating-point rounding inaccuracies.

### Catalog Workflow
1. Customer visits the Store Catalog view (`/catalog`).
2. Client queries `GET /api/products`.
3. Server queries the `Product` table filtering strictly for active products (`isActive = true`), sorted by name or id.
4. Each product displays name, description, price in formatted THB, remaining `stockQuantity`, and an availability badge:
   - "In Stock" (green badge) if `stockQuantity > 0`.
   - "Out of Stock" (red badge) if `stockQuantity == 0`.
5. Products marked inactive (`isActive = false`) in the database are filtered out from the customer catalog query and are never visible or orderable.

---

## 2. Dependencies & Enforced Business Rules

- **Dependencies:** `Product` database table and idempotent seed data.
- **Enforced Business Rules:**
  - `BR-01` (Monetary Representation): All prices (`priceMinor`) are stored strictly as integers in minor currency units (Thai Baht satang). Floating-point arithmetic is strictly prohibited in price storage and calculations.
  - `FR-04` (Browse Active Catalog): Only active items (`isActive = true`) are returned to customer endpoints.

---

## 3. Boundary, Negative & Failure Cases

- **Zero Stock Product:** Included in response with `stockQuantity = 0`; UI displays "Out of Stock" badge and disables the "Add to Cart" button.
- **Inactive Product:** Completely omitted from API response (`isActive = false`).
- **Empty Catalog:** If no active products exist, API returns HTTP 200 with `[]`; UI renders an empty state message ("No products currently available").

---

## 4. UI Behavior & View States

- **Catalog Grid (`/catalog`):**
  - Grid of product cards showing: Product Name, Description, Formatted Price (e.g. `฿250.00` from `25000` satang), Stock Badge, Quantity Selector, and "Add to Cart" button.
  - If `stockQuantity == 0`: Button is disabled with label "Unavailable".
  - Loading State: Skeleton cards while fetching data.
  - Error State: User-friendly error message with retry button if network fails.

---

## 5. API Specification

### 5.1 GET `/api/products`
- **Access:** Public or Authenticated (`CUSTOMER`, `OPERATOR`)
- **Query Parameters:** None in Sprint 1.
- **Response `200 OK`:**
  ```json
  [
    {
      "id": "prod_hoodie01",
      "name": "UniMerch Heavyweight Hoodie",
      "description": "Premium 100% cotton campus hoodie in navy blue.",
      "priceMinor": 75000,
      "stockQuantity": 15,
      "isActive": true
    },
    {
      "id": "prod_mug01",
      "name": "Ceramic Campus Mug",
      "description": "Matte finish ceramic mug with university crest.",
      "priceMinor": 18000,
      "stockQuantity": 0,
      "isActive": true
    }
  ]
  ```
- **Error Responses:**
  - `500 Internal Server Error`: Generic database connection failure payload.

---

## 6. Data Model & Database Constraints

```prisma
model Product {
  id            String      @id @default(cuid())
  name          String
  description   String
  priceMinor    Int         // Integer satang (> 0)
  stockQuantity Int         @default(0) // Integer >= 0
  isActive      Boolean     @default(true)
  createdAt     DateTime    @default(now())
  updatedAt     DateTime    @updatedAt
  orderItems    OrderItem[]

  // Database check constraints enforced via SQL migrations:
  // CHECK (priceMinor > 0)
  // CHECK (stockQuantity >= 0)
}
```

---

## 7. Acceptance Criteria (AC)

- **AC-05:** Catalog lists all seeded active products with minor-unit integer pricing and real-time stock availability badges. Inactive items are excluded.
- **AC-18:** Running database seed populates $\ge 8$ products (including $\ge 1$ inactive item and $\ge 1$ item with `stockQuantity = 0`) idempotently.
