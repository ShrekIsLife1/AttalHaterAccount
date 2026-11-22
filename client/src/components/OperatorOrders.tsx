import React, { useState, useEffect } from "react";
import { getOperatorOrders, acceptOrder, Order } from "../api.js";

export const OperatorOrders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [acceptingId, setAcceptingId] = useState<number | null>(null);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getOperatorOrders();
      setOrders(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load incoming orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleAccept = async (orderId: number) => {
    try {
      setAcceptingId(orderId);
      setError(null);
      setSuccessMessage(null);
      await acceptOrder(orderId);
      setOrders((prev) => prev.filter((o) => o.id !== orderId));
      setSuccessMessage(`Order #${orderId} accepted successfully.`);
    } catch (err: any) {
      setError(err?.message || `Failed to accept order #${orderId}`);
    } finally {
      setAcceptingId(null);
    }
  };

  const formatPrice = (minor: number) => {
    return (minor / 100).toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  const formatDate = (isoString: string) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    } catch {
      return isoString;
    }
  };

  if (loading) {
    return (
      <div className="card shadow-sm p-4 text-center" data-testid="operator-orders-loading">
        <div className="spinner-border text-primary my-3" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="text-muted">Loading incoming orders queue...</p>
      </div>
    );
  }

  return (
    <div className="card shadow-sm p-4" data-testid="operator-orders-view">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h2 className="h4 fw-bold mb-1">Incoming Orders Queue</h2>
          <p className="text-muted small mb-0">
            Real-time queue of customer orders awaiting operator acceptance and preparation.
          </p>
        </div>
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={fetchOrders}
          disabled={loading || acceptingId !== null}
        >
          ↻ Refresh Queue
        </button>
      </div>

      {error && (
        <div className="alert alert-danger py-2 small mb-3" role="alert">
          {error}
        </div>
      )}

      {successMessage && (
        <div className="alert alert-success py-2 small mb-3" role="alert">
          {successMessage}
        </div>
      )}

      {orders.length === 0 ? (
        <div className="text-center py-5" data-testid="operator-orders-empty">
          <div className="display-6 text-muted mb-2">✓</div>
          <h3 className="h6 fw-semibold text-secondary mb-1">All caught up! No pending incoming orders</h3>
          <p className="text-muted small">New customer orders will appear here automatically.</p>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th scope="col" style={{ width: "90px" }}>Order</th>
                <th scope="col">Customer</th>
                <th scope="col">Items</th>
                <th scope="col">Placed At</th>
                <th scope="col" className="text-end">Total</th>
                <th scope="col" className="text-center" style={{ width: "140px" }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => {
                const isAccepting = acceptingId === order.id;
                const customerEmail =
                  (order as any).customer?.email ||
                  (order as any).customerEmail ||
                  `Customer #${order.customerId}`;
                const totalItemCount =
                  order.items?.reduce((sum, item) => sum + item.quantity, 0) || 0;

                return (
                  <tr key={order.id} data-testid={`order-row-${order.id}`}>
                    <td className="fw-bold text-primary">#{order.id}</td>
                    <td>
                      <div>{customerEmail}</div>
                      {(order as any).customer?.name && (
                        <div className="text-muted small">{(order as any).customer.name}</div>
                      )}
                    </td>
                    <td>
                      <span className="badge bg-secondary me-1">{totalItemCount} items</span>
                      <small className="text-muted">
                        {order.items
                          ?.map(
                            (i) => `${(i as any).product?.name || `Item ${i.productId}`} (×${i.quantity})`
                          )
                          .join(", ")}
                      </small>
                    </td>
                    <td className="text-muted small">{formatDate(order.createdAt)}</td>
                    <td className="text-end fw-bold">{formatPrice(order.totalMinor)} THB</td>
                    <td className="text-center">
                      <button
                        className="btn btn-sm btn-success px-3"
                        onClick={() => handleAccept(order.id)}
                        disabled={isAccepting}
                      >
                        {isAccepting ? (
                          <>
                            <span
                              className="spinner-border spinner-border-sm me-1"
                              role="status"
                              aria-hidden="true"
                            ></span>
                            Accepting...
                          </>
                        ) : (
                          "Accept"
                        )}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
