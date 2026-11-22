import React, { useState, useEffect } from "react";
import { Order, getMyOrders, formatTHB } from "../api.js";

interface MyOrdersProps {
  onSelectOrder: (orderId: number) => void;
  onGoToCatalog: () => void;
}

export const MyOrders: React.FC<MyOrdersProps> = ({
  onSelectOrder,
  onGoToCatalog,
}) => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    getMyOrders()
      .then((data) => {
        if (isMounted) {
          setOrders(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Failed to load orders");
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="card shadow-sm p-4 text-center" data-testid="my-orders-loading">
        <div className="spinner-border text-primary my-4" role="status">
          <span className="visually-hidden">Loading orders...</span>
        </div>
        <p className="text-muted">Loading your past orders...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger shadow-sm" role="alert" data-testid="my-orders-error">
        <h5>Failed to load orders</h5>
        <p className="mb-0">{error}</p>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="card shadow-sm p-5 text-center text-muted" data-testid="my-orders-empty">
        <div className="mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" className="bi bi-bag-x text-muted" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M6.146 8.146a.5.5 0 0 1 .708 0L8 9.293l1.146-1.147a.5.5 0 1 1 .708.708L8.707 10l1.147 1.146a.5.5 0 0 1-.708.708L8 10.707l-1.146 1.147a.5.5 0 0 1-.708-.708L7.293 10 6.146 8.854a.5.5 0 0 1 0-.708z"/>
            <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1m3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/>
          </svg>
        </div>
        <h4 className="h5 fw-bold text-dark mb-2">No orders placed yet</h4>
        <p className="mb-4">You have not placed any campus merchandise orders yet. Start shopping!</p>
        <div>
          <button className="btn btn-primary" onClick={onGoToCatalog} data-testid="start-shopping-button">
            Browse Catalog
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card shadow-sm border-0 p-4" data-testid="customer-orders-view">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="h4 fw-bold mb-1">My Orders</h2>
          <p className="text-muted small mb-0">Track and view your campus merchandise orders</p>
        </div>
        <button className="btn btn-outline-primary btn-sm" onClick={onGoToCatalog}>
          + New Order
        </button>
      </div>

      <div className="table-responsive">
        <table className="table table-hover align-middle" data-testid="orders-table">
          <thead className="table-light">
            <tr>
              <th scope="col">Order #</th>
              <th scope="col">Date Placed</th>
              <th scope="col">Items</th>
              <th scope="col">Status</th>
              <th scope="col" className="text-end">Total</th>
              <th scope="col" className="text-center" style={{ width: "120px" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => {
              const itemCount = order.items
                ? order.items.reduce((acc, i) => acc + i.quantity, 0)
                : 0;

              return (
                <tr key={order.id} data-testid={`order-row-${order.id}`}>
                  <td className="fw-semibold font-monospace">#{order.id}</td>
                  <td className="text-muted small">
                    {new Date(order.createdAt).toLocaleDateString()} {new Date(order.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td>
                    <span className="badge bg-light text-dark border">
                      {itemCount} {itemCount === 1 ? "item" : "items"}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`badge ${
                        order.status === "ACCEPTED"
                          ? "bg-success-subtle text-success border border-success-subtle"
                          : "bg-primary-subtle text-primary border border-primary-subtle"
                      } px-2 py-1`}
                      data-testid={`order-status-${order.id}`}
                    >
                      {order.status}
                    </span>
                  </td>
                  <td className="text-end fw-bold font-monospace text-primary" data-testid={`order-total-${order.id}`}>
                    {formatTHB(order.totalMinor)}
                  </td>
                  <td className="text-center">
                    <button
                      className="btn btn-outline-primary btn-sm"
                      onClick={() => onSelectOrder(order.id)}
                      data-testid={`view-order-${order.id}`}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
