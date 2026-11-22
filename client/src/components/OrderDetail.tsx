import React, { useState, useEffect } from "react";
import { Order, getOrderById, formatTHB } from "../api.js";

interface OrderDetailProps {
  orderId?: number;
  order?: Order;
  onBack: () => void;
  backLabel?: string;
}

export const OrderDetail: React.FC<OrderDetailProps> = ({
  orderId,
  order: initialOrder,
  onBack,
  backLabel = "Back to My Orders",
}) => {
  const [order, setOrder] = useState<Order | null>(initialOrder || null);
  const [loading, setLoading] = useState<boolean>(!initialOrder && !!orderId);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialOrder) {
      setOrder(initialOrder);
      setLoading(false);
      return;
    }

    if (orderId) {
      let isMounted = true;
      setLoading(true);
      setError(null);
      getOrderById(orderId)
        .then((fetched) => {
          if (isMounted) {
            setOrder(fetched);
            setLoading(false);
          }
        })
        .catch((err) => {
          if (isMounted) {
            setError(err instanceof Error ? err.message : "Failed to load order details");
            setLoading(false);
          }
        });

      return () => {
        isMounted = false;
      };
    }
  }, [orderId, initialOrder]);

  if (loading) {
    return (
      <div className="card shadow-sm p-4 text-center" data-testid="order-detail-loading">
        <div className="spinner-border text-primary my-4" role="status">
          <span className="visually-hidden">Loading order details...</span>
        </div>
        <p className="text-muted">Retrieving order details from server...</p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="card shadow-sm p-4" data-testid="order-detail-error">
        <div className="alert alert-danger" role="alert">
          <h5>Order Lookup Error</h5>
          <p className="mb-0">{error || "Order not found."}</p>
        </div>
        <div>
          <button className="btn btn-outline-secondary btn-sm" onClick={onBack}>
            &larr; {backLabel}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card shadow-sm border-0 p-4" data-testid="order-detail-view">
      <div className="d-flex justify-content-between align-items-start mb-4">
        <div>
          <div className="d-flex align-items-center gap-2 mb-1">
            <h2 className="h4 fw-bold mb-0">Order #{order.id}</h2>
            <span
              className={`badge ${
                order.status === "ACCEPTED"
                  ? "bg-success-subtle text-success border border-success-subtle"
                  : "bg-primary-subtle text-primary border border-primary-subtle"
              } px-2 py-1`}
              data-testid="order-status-badge"
            >
              {order.status}
            </span>
          </div>
          <div className="text-muted small">
            Placed on: {new Date(order.createdAt).toLocaleString()}
          </div>
          {order.acceptedAt && (
            <div className="text-success small">
              Accepted on: {new Date(order.acceptedAt).toLocaleString()}
            </div>
          )}
        </div>
        <button className="btn btn-outline-secondary btn-sm" onClick={onBack} data-testid="back-button">
          &larr; {backLabel}
        </button>
      </div>

      <div className="table-responsive mb-4">
        <table className="table align-middle" data-testid="order-items-table">
          <thead className="table-light">
            <tr>
              <th scope="col">Product Item</th>
              <th scope="col" className="text-end">Unit Price (at order time)</th>
              <th scope="col" className="text-center">Quantity</th>
              <th scope="col" className="text-end">Line Total</th>
            </tr>
          </thead>
          <tbody>
            {order.items && order.items.map((item) => (
              <tr key={item.id} data-testid={`order-item-row-${item.productId}`}>
                <td>
                  <div className="fw-semibold text-dark">
                    {item.product?.name || `Product #${item.productId}`}
                  </div>
                  {item.product?.description && (
                    <div className="text-muted small">{item.product.description}</div>
                  )}
                </td>
                <td className="text-end font-monospace" data-testid={`item-price-${item.productId}`}>
                  {formatTHB(item.unitPriceAtOrder)}
                </td>
                <td className="text-center fw-semibold font-monospace" data-testid={`item-qty-${item.productId}`}>
                  {item.quantity}
                </td>
                <td className="text-end fw-semibold font-monospace" data-testid={`item-total-${item.productId}`}>
                  {formatTHB(item.unitPriceAtOrder * item.quantity)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-light p-3 rounded d-flex justify-content-between align-items-center">
        <div>
          <span className="fw-semibold text-dark">Authoritative Order Total</span>
          <div className="text-muted small">Persisted in database minor units (satang)</div>
        </div>
        <div className="fs-4 fw-bold text-primary font-monospace" data-testid="order-grand-total">
          {formatTHB(order.totalMinor)}
        </div>
      </div>
    </div>
  );
};
