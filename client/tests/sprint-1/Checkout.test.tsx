import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { Checkout } from "../../src/components/Checkout.js";
import * as api from "../../src/api.js";

describe("Issue #11: Checkout & Order Submission UI (F-03 / AC-06..AC-10)", () => {
  const mockCart: api.CartItem[] = [
    {
      product: {
        id: 1,
        name: "Campus Hoodie",
        description: "Navy blue hoodie",
        priceMinor: 75000,
        stockQuantity: 10,
        isActive: true,
      },
      quantity: 2,
    },
    {
      product: {
        id: 2,
        name: "Ceramic Mug",
        description: "Uni logo mug",
        priceMinor: 18000,
        stockQuantity: 5,
        isActive: true,
      },
      quantity: 1,
    },
  ];

  const mockCreatedOrder: api.Order = {
    id: 101,
    customerId: 1,
    status: "PLACED",
    totalMinor: 168000, // 2 * 75000 + 1 * 18000 = 168000 satang
    createdAt: new Date().toISOString(),
    acceptedAt: null,
    acceptedByOperatorId: null,
    items: [
      {
        id: 11,
        orderId: 101,
        productId: 1,
        quantity: 2,
        unitPriceAtOrder: 75000,
        product: mockCart[0].product,
      },
      {
        id: 12,
        orderId: 101,
        productId: 2,
        quantity: 1,
        unitPriceAtOrder: 18000,
        product: mockCart[1].product,
      },
    ],
  };

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders cart items, line subtotals, and estimated total clearly labelled", () => {
    render(
      <Checkout
        cart={mockCart}
        onUpdateQuantity={vi.fn()}
        onRemoveItem={vi.fn()}
        onClearCart={vi.fn()}
        onBackToCatalog={vi.fn()}
      />
    );

    expect(screen.getByText("Campus Hoodie")).toBeInTheDocument();
    expect(screen.getByText("Ceramic Mug")).toBeInTheDocument();
    expect(screen.getByText("฿750.00")).toBeInTheDocument();
    expect(screen.getAllByText("฿180.00").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("฿1,500.00")).toBeInTheDocument(); // 2 * 750

    // Check estimated total label
    expect(screen.getByText(/Estimated total/i)).toBeInTheDocument();
    expect(screen.getByText(/confirmed by server on submit/i)).toBeInTheDocument();
    expect(screen.getByTestId("estimated-total")).toHaveTextContent("฿1,680.00");
  });

  it("submits order, shows busy state, and displays persisted order detail afterwards", async () => {
    let resolvePromise: (value: api.Order) => void;
    const createOrderSpy = vi.spyOn(api, "createOrder").mockImplementation(
      () =>
        new Promise((resolve) => {
          resolvePromise = resolve;
        })
    );
    const clearCartMock = vi.fn();

    render(
      <Checkout
        cart={mockCart}
        onUpdateQuantity={vi.fn()}
        onRemoveItem={vi.fn()}
        onClearCart={clearCartMock}
        onBackToCatalog={vi.fn()}
      />
    );

    const submitBtn = screen.getByTestId("submit-order-button");
    fireEvent.click(submitBtn);

    // Verify busy state & disabled button (prevents double submit)
    expect(submitBtn).toBeDisabled();
    expect(screen.getByText(/Submitting Order.../i)).toBeInTheDocument();

    // Resolve the creation
    resolvePromise!(mockCreatedOrder);

    // Verify confirmation and order detail appear
    await waitFor(() => {
      expect(screen.getByTestId("order-confirmation-banner")).toBeInTheDocument();
    });

    expect(screen.getByRole("heading", { name: /Order #101/i })).toBeInTheDocument();
    expect(screen.getByTestId("order-status-badge")).toHaveTextContent("PLACED");
    expect(screen.getByTestId("order-grand-total")).toHaveTextContent("฿1,680.00");
    expect(clearCartMock).toHaveBeenCalled();
  });

  it("displays server rejection error clearly when product is out of stock", async () => {
    vi.spyOn(api, "createOrder").mockRejectedValue(
      new Error("Insufficient stock for product 'Ceramic Mug'. Available: 0, requested: 1")
    );

    render(
      <Checkout
        cart={mockCart}
        onUpdateQuantity={vi.fn()}
        onRemoveItem={vi.fn()}
        onClearCart={vi.fn()}
        onBackToCatalog={vi.fn()}
      />
    );

    const submitBtn = screen.getByTestId("submit-order-button");
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByTestId("checkout-error")).toBeInTheDocument();
    });

    expect(
      screen.getByText(/Insufficient stock for product 'Ceramic Mug'/i)
    ).toBeInTheDocument();
    // Verify confirmation is NOT rendered
    expect(screen.queryByTestId("checkout-success-view")).not.toBeInTheDocument();
  });

  it("renders friendly empty cart state when cart has no items", () => {
    render(
      <Checkout
        cart={[]}
        onUpdateQuantity={vi.fn()}
        onRemoveItem={vi.fn()}
        onClearCart={vi.fn()}
        onBackToCatalog={vi.fn()}
      />
    );

    expect(screen.getByTestId("checkout-empty")).toBeInTheDocument();
    expect(screen.getByText(/Your cart is currently empty/i)).toBeInTheDocument();
    expect(screen.queryByTestId("submit-order-button")).not.toBeInTheDocument();
  });
});
