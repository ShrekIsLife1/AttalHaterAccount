import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { MyOrders } from "../../src/components/MyOrders.js";
import * as api from "../../src/api.js";

describe("Issue #11: My Orders View (F-04 / AC-11 / TEST-14)", () => {
  const mockOrders: api.Order[] = [
    {
      id: 201,
      customerId: 1,
      status: "PLACED",
      totalMinor: 150000,
      createdAt: "2026-11-22T10:00:00.000Z",
      acceptedAt: null,
      acceptedByOperatorId: null,
      items: [
        {
          id: 1,
          orderId: 201,
          productId: 1,
          quantity: 2,
          unitPriceAtOrder: 75000,
        },
      ],
    },
    {
      id: 202,
      customerId: 1,
      status: "ACCEPTED",
      totalMinor: 36000,
      createdAt: "2026-11-21T14:30:00.000Z",
      acceptedAt: "2026-11-21T15:00:00.000Z",
      acceptedByOperatorId: 2,
      items: [
        {
          id: 2,
          orderId: 202,
          productId: 2,
          quantity: 2,
          unitPriceAtOrder: 18000,
        },
      ],
    },
  ];

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("displays loading indicator initially while orders are being fetched", () => {
    vi.spyOn(api, "getMyOrders").mockImplementation(() => new Promise(() => {}));

    render(<MyOrders onSelectOrder={vi.fn()} onGoToCatalog={vi.fn()} />);

    expect(screen.getByTestId("my-orders-loading")).toBeInTheDocument();
    expect(screen.getByText(/Loading your past orders.../i)).toBeInTheDocument();
  });

  it("renders list of orders with IDs, status badges, and formatted totals", async () => {
    vi.spyOn(api, "getMyOrders").mockResolvedValue(mockOrders);

    render(<MyOrders onSelectOrder={vi.fn()} onGoToCatalog={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByTestId("customer-orders-view")).toBeInTheDocument();
    });

    expect(screen.getByText("#201")).toBeInTheDocument();
    expect(screen.getByText("#202")).toBeInTheDocument();

    expect(screen.getByTestId("order-status-201")).toHaveTextContent("PLACED");
    expect(screen.getByTestId("order-status-202")).toHaveTextContent("ACCEPTED");

    expect(screen.getByTestId("order-total-201")).toHaveTextContent("฿1,500.00");
    expect(screen.getByTestId("order-total-202")).toHaveTextContent("฿360.00");
  });

  it("calls onSelectOrder with the correct orderId when 'View Details' is clicked", async () => {
    vi.spyOn(api, "getMyOrders").mockResolvedValue(mockOrders);
    const selectOrderMock = vi.fn();

    render(<MyOrders onSelectOrder={selectOrderMock} onGoToCatalog={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByTestId("view-order-201")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByTestId("view-order-201"));
    expect(selectOrderMock).toHaveBeenCalledWith(201);
  });

  it("renders friendly empty state when customer has zero orders", async () => {
    vi.spyOn(api, "getMyOrders").mockResolvedValue([]);
    const goToCatalogMock = vi.fn();

    render(<MyOrders onSelectOrder={vi.fn()} onGoToCatalog={goToCatalogMock} />);

    await waitFor(() => {
      expect(screen.getByTestId("my-orders-empty")).toBeInTheDocument();
    });

    expect(screen.getByText(/No orders placed yet/i)).toBeInTheDocument();
    expect(screen.getByText(/Start shopping!/i)).toBeInTheDocument();

    fireEvent.click(screen.getByTestId("start-shopping-button"));
    expect(goToCatalogMock).toHaveBeenCalled();
  });

  it("renders error state when fetching orders fails", async () => {
    vi.spyOn(api, "getMyOrders").mockRejectedValue(new Error("Network connection error"));

    render(<MyOrders onSelectOrder={vi.fn()} onGoToCatalog={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByTestId("my-orders-error")).toBeInTheDocument();
    });

    expect(screen.getByText(/Network connection error/i)).toBeInTheDocument();
  });
});
