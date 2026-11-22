export const MAX_QTY_PER_LINE = 10;

export interface OrderItemInput {
  productId: number;
  quantity: number;
}

export interface ProductPriceInfo {
  id: number;
  name: string;
  priceMinor: number;
  stockQuantity: number;
  isActive: boolean;
}

export interface CalculatedLine {
  productId: number;
  quantity: number;
  unitPriceAtOrder: number;
  lineTotalMinor: number;
}

export interface CalculatedOrder {
  lines: CalculatedLine[];
  totalMinor: number;
}

export class OrderValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "OrderValidationError";
  }
}

/**
 * Pure domain function to validate order lines and compute authoritative totals.
 * Throws OrderValidationError on any constraint or business rule violation.
 * BR-01: Items array must be non-empty.
 * BR-02: No duplicate product IDs per order.
 * BR-03: Server re-queries prices from DB (products map), ignores client price.
 * BR-06: Quantities must be integers in [1, MAX_QTY_PER_LINE].
 */
export function calculateOrderPricing(
  items: OrderItemInput[],
  products: Map<number, ProductPriceInfo>
): CalculatedOrder {
  // BR-01: non-empty
  if (items.length === 0) {
    throw new OrderValidationError("Order must contain at least one item");
  }

  // BR-02: no duplicate product IDs
  const seenIds = new Set<number>();
  for (const item of items) {
    if (seenIds.has(item.productId)) {
      throw new OrderValidationError(
        `Duplicate product ID ${item.productId} in order payload`
      );
    }
    seenIds.add(item.productId);
  }

  // Validate each line
  const lines: CalculatedLine[] = [];
  for (const item of items) {
    // BR-06: quantity must be a positive integer ≤ MAX_QTY_PER_LINE
    if (!Number.isInteger(item.quantity) || item.quantity < 1) {
      throw new OrderValidationError(
        `Invalid quantity ${item.quantity} for product ${item.productId}: must be a positive integer`
      );
    }
    if (item.quantity > MAX_QTY_PER_LINE) {
      throw new OrderValidationError(
        `Quantity exceeds maximum allowed (${MAX_QTY_PER_LINE}) for product ${item.productId}`
      );
    }

    // Product must exist in DB map (BR-03: server fetches prices)
    const product = products.get(item.productId);
    if (!product) {
      throw new OrderValidationError(
        `Product not found: ID ${item.productId}`
      );
    }

    // Product must be active
    if (!product.isActive) {
      throw new OrderValidationError(
        `Product is inactive: ID ${item.productId} (${product.name})`
      );
    }

    // Sufficient stock
    if (product.stockQuantity < item.quantity) {
      throw new OrderValidationError(
        `Insufficient stock for product ${item.productId} (${product.name}): requested ${item.quantity}, available ${product.stockQuantity}`
      );
    }

    const unitPriceAtOrder = product.priceMinor;
    const lineTotalMinor = unitPriceAtOrder * item.quantity;
    lines.push({
      productId: item.productId,
      quantity: item.quantity,
      unitPriceAtOrder,
      lineTotalMinor,
    });
  }

  const totalMinor = lines.reduce((sum, l) => sum + l.lineTotalMinor, 0);
  return { lines, totalMinor };
}
