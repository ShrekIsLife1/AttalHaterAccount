import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { Catalog } from "../../src/components/Catalog.js";
import * as api from "../../src/api.js";

describe("Product Catalog UI (F-02 / AC-05 / TEST-06)", () => {
  const mockProducts: api.Product[] = [
    {
      id: 1,
      name: "UniMerch Heavyweight Hoodie",
      description: "Premium campus hoodie",
      priceMinor: 75000,
      stockQuantity: 15,
      isActive: true,
    },
    {
      id: 2,
      name: "Ceramic Campus Mug",
      description: "Matte finish ceramic mug",
      priceMinor: 18000,
      stockQuantity: 0,
      isActive: true,
    },
  ];

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders active products with formatted THB prices and availability badges", async () => {
    vi.spyOn(api, "getProducts").mockResolvedValue(mockProducts);

    render(
      <Catalog
        onAddToCart={vi.fn()}
        cartItemCount={0}
        onGoToCheckout={vi.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByTestId("product-card-1")).toBeInTheDocument();
    });

    // Verify product 1 (in stock)
    expect(screen.getByText("UniMerch Heavyweight Hoodie")).toBeInTheDocument();
    expect(screen.getByTestId("price-1")).toHaveTextContent("฿750.00");
    expect(screen.getByTestId("badge-stock-1")).toHaveTextContent("In Stock (15)");
    expect(screen.getByTestId("add-to-cart-1")).toBeEnabled();

    // Verify product 2 (out of stock)
    expect(screen.getByText("Ceramic Campus Mug")).toBeInTheDocument();
    expect(screen.getByTestId("price-2")).toHaveTextContent("฿180.00");
    expect(screen.getByTestId("badge-stock-2")).toHaveTextContent("Out of Stock");
    expect(screen.getByTestId("unavailable-btn-2")).toBeDisabled();
    expect(screen.getByTestId("unavailable-btn-2")).toHaveTextContent("Unavailable");
  });

  it("adds selected quantity to cart when 'Add to Cart' is clicked", async () => {
    vi.spyOn(api, "getProducts").mockResolvedValue(mockProducts);
    const addToCartMock = vi.fn();

    render(
      <Catalog
        onAddToCart={addToCartMock}
        cartItemCount={0}
        onGoToCheckout={vi.fn()}
      />
    );

    await waitFor(() => {
      expect(screen.getByTestId("product-card-1")).toBeInTheDocument();
    });

    const qtyInput = screen.getByTestId("qty-input-1");
    fireEvent.change(qtyInput, { target: { value: "3" } });

    const addBtn = screen.getByTestId("add-to-cart-1");
    fireEvent.click(addBtn);

    expect(addToCartMock).toHaveBeenCalledWith(mockProducts[0], 3);
  });
});
