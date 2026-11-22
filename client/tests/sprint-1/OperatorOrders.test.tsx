import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { OperatorOrders } from "../../src/components/OperatorOrders.js";
import * as api from "../../src/api.js";

describe("Issue #12: Operator Orders Queue UI (F-05 / AC-14 / TEST-18)", () => {
  const mockIncomingOrders: any[] = [
    {
      id: 301,
      customerId: 1,
      customerEmail: "alice@example.com",
      customer: { id: 1, email: "alice@example.com", name: "Alice Customer" },
      status: "PLACED",
      totalMinor: 150000,
      createdAt: "2026-11-22T08:30:00.000Z",
      acceptedAt: null,
      acceptedByOperatorId: null,
      items: [
        {
          id: 1,
          productId: 1,
          quantity: 2,
          unitPriceAtOrder: 75000,
          product: { name: "UniMerch Hoodie" }
        }
      ]
    },
    {
      id: 302,
      customerId: 2,
      customerEmail: "bob@example.com",
      customer: { id: 2, email: "bob@example.com", name: "Bob Customer" },
      status: "PLACED",
      totalMinor: 5000,
      createdAt: "2026-11-22T08:35:00.000Z",
      acceptedAt: null,
      acceptedByOperatorId: null,
      items: [
        {
          id: 2,
          productId: 2,
          quantity: 1,
          unitPriceAtOrder: 5000,
          product: { name: "UniMerch Pen" }
        }
      ]
    }
  ];

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("displays loading indicator initially while fetching incoming orders", () => {
    vi.spyOn(api, "getOperatorOrders" as any).mockImplementation(() => new Promise(() => {}));

    render(<OperatorOrders />);

    expect(screen.getByTestId("operator-orders-loading")).toBeInTheDocument();
    expect(screen.getByText(/Loading incoming orders/i)).toBeInTheDocument();
  });

  it("renders table of incoming orders with customer email, total, and enabled Accept button", async () => {
    vi.spyOn(api, "getOperatorOrders" as any).mockResolvedValue(mockIncomingOrders as any);

    render(<OperatorOrders />);

    await waitFor(() => {
      expect(screen.queryByTestId("operator-orders-loading")).not.toBeInTheDocument();
    });

    // Check order IDs
    expect(screen.getByText(/#301/i)).toBeInTheDocument();
    expect(screen.getByText(/#302/i)).toBeInTheDocument();

    // Check customer emails
    expect(screen.getByText("alice@example.com")).toBeInTheDocument();
    expect(screen.getByText("bob@example.com")).toBeInTheDocument();

    // Check Accept buttons
    const acceptButtons = screen.getAllByRole("button", { name: /Accept/i });
    expect(acceptButtons.length).toBe(2);
  });

  it("triggers acceptOrder API, disables button during submission, and removes order from queue", async () => {
    vi.spyOn(api, "getOperatorOrders" as any).mockResolvedValue(mockIncomingOrders as any);
    const acceptSpy = vi.spyOn(api, "acceptOrder" as any).mockImplementation(
      () =>
        new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              ...mockIncomingOrders[0],
              status: "ACCEPTED",
              acceptedAt: new Date().toISOString(),
              acceptedByOperatorId: 1
            });
          }, 50);
        })
    );

    render(<OperatorOrders />);

    await waitFor(() => {
      expect(screen.getByText(/#301/i)).toBeInTheDocument();
    });

    const acceptButtons = screen.getAllByRole("button", { name: /Accept/i });
    fireEvent.click(acceptButtons[0]);

    // Button should be disabled during submission
    expect(acceptButtons[0]).toBeDisabled();

    // Wait for resolution
    await waitFor(() => {
      expect(acceptSpy).toHaveBeenCalledWith(301);
    });

    // Order 301 should no longer be in the incoming queue (or marked as accepted)
    await waitFor(() => {
      expect(screen.queryByTestId("order-row-301")).not.toBeInTheDocument();
    });
    // Order 302 remains in the queue
    expect(screen.getByText(/#302/i)).toBeInTheDocument();
  });

  it("displays friendly empty state message when there are no incoming orders", async () => {
    vi.spyOn(api, "getOperatorOrders" as any).mockResolvedValue([] as any);

    render(<OperatorOrders />);

    await waitFor(() => {
      expect(screen.queryByTestId("operator-orders-loading")).not.toBeInTheDocument();
    });

    expect(screen.getByTestId("operator-orders-empty")).toBeInTheDocument();
    expect(screen.getByText(/All caught up! No pending incoming orders/i)).toBeInTheDocument();
  });

  it("displays error alert when fetching fails", async () => {
    vi.spyOn(api, "getOperatorOrders" as any).mockRejectedValue(new Error("Network connection error"));

    render(<OperatorOrders />);

    await waitFor(() => {
      expect(screen.queryByTestId("operator-orders-loading")).not.toBeInTheDocument();
    });

    expect(screen.getByText(/Network connection error/i)).toBeInTheDocument();
  });
});
