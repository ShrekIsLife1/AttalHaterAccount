import { describe, it, expect } from "vitest";
import {
  calculateOrderPricing,
  OrderValidationError,
  ProductPriceInfo,
  MAX_QTY_PER_LINE
} from "../../src/domain/pricing.js";

describe("Domain Pricing Engine (F-03 / BR-01, BR-02, BR-03, BR-06 / TEST-09)", () => {
  const mockProducts = new Map<number, ProductPriceInfo>([
    [
      1,
      {
        id: 1,
        name: "UniMerch Hoodie",
        priceMinor: 75000, // 750.00 THB
        stockQuantity: 10,
        isActive: true
      }
    ],
    [
      2,
      {
        id: 2,
        name: "UniMerch Pen",
        priceMinor: 5000, // 50.00 THB
        stockQuantity: 50,
        isActive: true
      }
    ],
    [
      3,
      {
        id: 3,
        name: "Inactive Mug",
        priceMinor: 15000,
        stockQuantity: 5,
        isActive: false
      }
    ],
    [
      4,
      {
        id: 4,
        name: "Sold Out T-Shirt",
        priceMinor: 30000,
        stockQuantity: 0,
        isActive: true
      }
    ],
    [
      5,
      {
        id: 5,
        name: "Limited Edition Badge",
        priceMinor: 10000,
        stockQuantity: 3,
        isActive: true
      }
    ]
  ]);

  it("calculates line totals and grand total accurately in integer satang", () => {
    const input = [
      { productId: 1, quantity: 2 }, // 75000 * 2 = 150000
      { productId: 2, quantity: 3 }  // 5000 * 3 = 15000
    ];

    const result = calculateOrderPricing(input, mockProducts);

    expect(result.totalMinor).toBe(165000); // 1650.00 THB
    expect(result.lines).toHaveLength(2);
    expect(result.lines[0]).toEqual({
      productId: 1,
      quantity: 2,
      unitPriceAtOrder: 75000,
      lineTotalMinor: 150000
    });
    expect(result.lines[1]).toEqual({
      productId: 2,
      quantity: 3,
      unitPriceAtOrder: 5000,
      lineTotalMinor: 15000
    });
  });

  it("rejects empty items array with OrderValidationError", () => {
    expect(() => calculateOrderPricing([], mockProducts)).toThrow(OrderValidationError);
  });

  it("rejects duplicate product IDs in the same order payload", () => {
    const input = [
      { productId: 1, quantity: 1 },
      { productId: 1, quantity: 2 }
    ];
    expect(() => calculateOrderPricing(input, mockProducts)).toThrow(
      /Duplicate product/i
    );
  });

  it("rejects non-integer, zero, or negative quantities", () => {
    expect(() =>
      calculateOrderPricing([{ productId: 1, quantity: 0 }], mockProducts)
    ).toThrow(OrderValidationError);

    expect(() =>
      calculateOrderPricing([{ productId: 1, quantity: -2 }], mockProducts)
    ).toThrow(OrderValidationError);

    expect(() =>
      calculateOrderPricing([{ productId: 1, quantity: 1.5 }], mockProducts)
    ).toThrow(OrderValidationError);
  });

  it(`rejects quantity exceeding MAX_QTY_PER_LINE (${MAX_QTY_PER_LINE})`, () => {
    expect(() =>
      calculateOrderPricing(
        [{ productId: 1, quantity: MAX_QTY_PER_LINE + 1 }],
        mockProducts
      )
    ).toThrow(/Quantity exceeds maximum allowed/i);
  });

  it("rejects order containing an inactive product", () => {
    const input = [{ productId: 3, quantity: 1 }];
    expect(() => calculateOrderPricing(input, mockProducts)).toThrow(
      /Product is inactive/i
    );
  });

  it("rejects order when requested quantity exceeds available stock", () => {
    const input = [{ productId: 5, quantity: 5 }]; // only 3 in stock
    expect(() => calculateOrderPricing(input, mockProducts)).toThrow(
      /Insufficient stock/i
    );
  });

  it("rejects order for a product with zero stock", () => {
    const input = [{ productId: 4, quantity: 1 }];
    expect(() => calculateOrderPricing(input, mockProducts)).toThrow(
      /Insufficient stock/i
    );
  });

  it("rejects order referencing non-existent product ID", () => {
    const input = [{ productId: 999, quantity: 1 }];
    expect(() => calculateOrderPricing(input, mockProducts)).toThrow(
      /Product not found/i
    );
  });
});
