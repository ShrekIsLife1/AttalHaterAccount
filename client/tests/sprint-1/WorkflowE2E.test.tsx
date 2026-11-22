import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import App from "../../src/App.js";
import * as api from "../../src/api.js";

describe("Sprint 1 E2E Workflow & User Journeys (AC-19, AC-20 / TEST-24, TEST-25, TEST-26)", () => {
  const customerUser: api.User = {
    id: 1,
    email: "customer1@example.com",
    name: "Alice Customer",
    role: "CUSTOMER"
  };

  const operatorUser: api.User = {
    id: 4,
    email: "operator1@example.com",
    name: "Dave Operator",
    role: "OPERATOR"
  };

  const mockProducts: api.Product[] = [
    {
      id: 1,
      name: "UniMerch Hoodie",
      description: "Warm campus hoodie",
      priceMinor: 75000,
      stockQuantity: 10,
      isActive: true
    },
    {
      id: 2,
      name: "UniMerch Pen",
      description: "Ballpoint pen",
      priceMinor: 5000,
      stockQuantity: 50,
      isActive: true
    }
  ];

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("TEST-24: Full Customer Journey - login -> browse catalog -> add to cart -> checkout -> order detail", async () => {
    // Initially unauthenticated
    vi.spyOn(api, "getMe").mockResolvedValue(null);
    vi.spyOn(api, "login").mockResolvedValue(customerUser);
    vi.spyOn(api, "getProducts").mockResolvedValue(mockProducts);

    const placedOrder: api.Order = {
      id: 501,
      customerId: 1,
      status: "PLACED",
      totalMinor: 80000,
      createdAt: new Date().toISOString(),
      acceptedAt: null,
      acceptedByOperatorId: null,
      items: [
        {
          id: 1,
          orderId: 501,
          productId: 1,
          quantity: 1,
          unitPriceAtOrder: 75000,
          product: mockProducts[0]
        },
        {
          id: 2,
          orderId: 501,
          productId: 2,
          quantity: 1,
          unitPriceAtOrder: 5000,
          product: mockProducts[1]
        }
      ]
    };

    vi.spyOn(api, "createOrder").mockResolvedValue(placedOrder);
    vi.spyOn(api, "getOrderById").mockResolvedValue(placedOrder);
    vi.spyOn(api, "getMyOrders").mockResolvedValue([placedOrder]);

    render(<App />);

    // 1. Unauthenticated Login screen rendered
    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    // 2. Perform Customer Login
    fireEvent.change(screen.getByLabelText(/Email address/i), { target: { value: "customer1@example.com" } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: "password123" } });
    fireEvent.click(screen.getByRole("button", { name: /Sign In/i }));

    // 3. Authenticated customer lands on Catalog
    expect(await screen.findByText(/UniMerch Hoodie/i)).toBeInTheDocument();
    expect(screen.getByText(/UniMerch Pen/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /My Orders/i })).toBeInTheDocument();

    // 4. Add items to cart
    const addButtons = screen.getAllByRole("button", { name: /Add to Cart/i });
    fireEvent.click(addButtons[0]); // Add Hoodie
    fireEvent.click(addButtons[1]); // Add Pen

    // 5. Navigate to Checkout
    const viewCartBtn = screen.getByRole("button", { name: /View Cart/i });
    fireEvent.click(viewCartBtn);

    // 6. Review checkout items and click Place Order
    expect(await screen.findByTestId("submit-order-button")).toBeInTheDocument();
    expect(screen.getByTestId("estimated-total")).toBeInTheDocument();

    fireEvent.click(screen.getByTestId("submit-order-button"));

    // 7. Verify order creation and order confirmation view
    await waitFor(() => {
      expect(api.createOrder).toHaveBeenCalledTimes(1);
    });

    expect(await screen.findByText(/Order #501/i)).toBeInTheDocument();
    expect(screen.getByTestId("order-status-badge")).toHaveTextContent("PLACED");
    expect(screen.getByText(/Authoritative Order Total/i)).toBeInTheDocument();
  });

  it("TEST-25: Full Operator Journey - operator login -> incoming queue -> accept order", async () => {
    vi.spyOn(api, "getMe").mockResolvedValue(null);
    vi.spyOn(api, "login").mockResolvedValue(operatorUser);

    const pendingOrder: any = {
      id: 601,
      customerId: 1,
      customerEmail: "customer1@example.com",
      status: "PLACED",
      totalMinor: 75000,
      createdAt: new Date().toISOString(),
      acceptedAt: null,
      acceptedByOperatorId: null,
      items: [
        {
          id: 1,
          productId: 1,
          quantity: 1,
          unitPriceAtOrder: 75000,
          product: { name: "UniMerch Hoodie" }
        }
      ]
    };

    vi.spyOn(api, "getOperatorOrders").mockResolvedValue([pendingOrder]);
    vi.spyOn(api, "acceptOrder").mockResolvedValue({
      ...pendingOrder,
      status: "ACCEPTED",
      acceptedAt: new Date().toISOString(),
      acceptedByOperatorId: 4
    });

    render(<App />);

    // 1. Operator Login
    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });
    fireEvent.change(screen.getByLabelText(/Email address/i), { target: { value: "operator1@example.com" } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: "password123" } });
    fireEvent.click(screen.getByRole("button", { name: /Sign In/i }));

    await waitFor(() => {
      expect(api.login).toHaveBeenCalledWith("operator1@example.com", "password123");
    });

    // 2. Operator dashboard renders incoming orders queue
    expect(await screen.findByText(/Incoming Orders Queue/i)).toBeInTheDocument();
    expect(screen.getByText(/#601/i)).toBeInTheDocument();
    expect(screen.getByText("customer1@example.com")).toBeInTheDocument();

    // 3. Operator accepts the order
    const acceptBtn = screen.getByRole("button", { name: /Accept/i });
    fireEvent.click(acceptBtn);

    // 4. Verify order accepted and queue clears
    await waitFor(() => {
      expect(api.acceptOrder).toHaveBeenCalledWith(601);
    });

    expect(await screen.findByTestId("operator-orders-empty")).toBeInTheDocument();
    expect(screen.getByText(/All caught up! No pending incoming orders/i)).toBeInTheDocument();
  });

  it("TEST-26: Access & Boundary Protection - role segregation in navigation", async () => {
    // Customer login sees only Customer tabs (Catalog, My Orders), never Incoming Orders
    vi.spyOn(api, "getMe").mockResolvedValue(customerUser);
    vi.spyOn(api, "getProducts").mockResolvedValue([]);

    const { unmount } = render(<App />);

    expect(await screen.findByRole("button", { name: /Catalog/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /My Orders/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Incoming Orders/i })).not.toBeInTheDocument();

    unmount();

    // Operator login sees only Operator tabs (Incoming Orders), never Customer tabs
    vi.spyOn(api, "getMe").mockResolvedValue(operatorUser);
    vi.spyOn(api, "getOperatorOrders").mockResolvedValue([]);

    render(<App />);

    expect(await screen.findByRole("button", { name: /Incoming Orders/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Catalog/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /My Orders/i })).not.toBeInTheDocument();
  });
});
