import React, { useState } from "react";
import { CartItem, Order, createOrder, formatTHB } from "../api.js";
import { OrderDetail } from "./OrderDetail.js";

interface CheckoutProps {
  cart: CartItem[];
  onUpdateQuantity: (productId: number, quantity: number) => void;
  onRemoveItem: (productId: number) => void;
  onClearCart: () => void;
  onBackToCatalog: () => void;
  onOrderCreated?: (order: Order) => void;
}

export const Checkout: React.FC<CheckoutProps> = ({
  cart,
  onUpdateQuantity,
  onRemoveItem,
  onClearCart,
  onBackToCatalog,
  onOrderCreated,
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [createdOrder, setCreatedOrder] = useState<Order | null>(null);

  // Compute local estimated total
  const estimatedTotalMinor = cart.reduce(
    (acc, item) => acc + item.product.priceMinor * item.quantity,
    0
  );

  const handleSubmitOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (cart.length === 0 || isSubmitting) return;

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const orderPayload = cart.map((item) => ({
        productId: item.product.id,
        quantity: item.quantity,
      }));

      const newOrder = await createOrder(orderPayload);
      setCreatedOrder(newOrder);
      onClearCart();
      if (onOrderCreated) {
        onOrderCreated(newOrder);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to place order";
      setErrorMessage(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  // If order was placed, display persisted order detail confirmation
  if (createdOrder) {
    return (
      <div data-testid="checkout-success-view">
        <div className="alert alert-success d-flex align-items-center gap-2 mb-4 shadow-sm" role="status" data-testid="order-confirmation-banner">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-check-circle-fill text-success" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
          </svg>
          <div>
            <h5 className="alert-heading mb-0">Order Placed Successfully!</h5>
            <div className="small">Your order #{createdOrder.id} has been recorded in status <strong>{createdOrder.status}</strong>.</div>
          </div>
        </div>

        <OrderDetail order={createdOrder} onBack={onBackToCatalog} backLabel="Continue Shopping" />
      </div>
    );
  }

  return (
    <div className="card shadow-sm border-0 p-4" data-testid="checkout-view">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="h4 fw-bold mb-1">Order Checkout</h2>
          <p className="text-muted small mb-0">Review your selected items and confirm your order</p>
        </div>
        <button className="btn btn-outline-secondary btn-sm" onClick={onBackToCatalog}>
          &larr; Back to Catalog
        </button>
      </div>

      {errorMessage && (
        <div className="alert alert-danger py-2 mb-3 small shadow-sm" role="alert" data-testid="checkout-error">
          <strong>Order rejected:</strong> {errorMessage}
        </div>
      )}

      {cart.length === 0 ? (
        <div className="text-center py-5 text-muted" data-testid="checkout-empty">
          <p className="mb-3">Your cart is currently empty.</p>
          <button className="btn btn-primary" onClick={onBackToCatalog}>
            Browse Catalog
          </button>
        </div>
      ) : (
        <div>
          <div className="table-responsive mb-4">
            <table className="table align-middle" data-testid="cart-items-table">
              <thead className="table-light">
                <tr>
                  <th scope="col">Product</th>
                  <th scope="col" className="text-end">Price</th>
                  <th scope="col" className="text-center" style={{ width: "130px" }}>Quantity</th>
                  <th scope="col" className="text-end">Subtotal</th>
                  <th scope="col" className="text-center" style={{ width: "80px" }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {cart.map((item) => (
                  <tr key={item.product.id} data-testid={`cart-row-${item.product.id}`}>
                    <td>
                      <div className="fw-semibold text-dark">{item.product.name}</div>
                      <div className="text-muted small">{item.product.description}</div>
                    </td>
                    <td className="text-end font-monospace">{formatTHB(item.product.priceMinor)}</td>
                    <td className="text-center">
                      <div className="input-group input-group-sm">
                        <button
                          className="btn btn-outline-secondary"
                          type="button"
                          disabled={item.quantity <= 1 || isSubmitting}
                          onClick={() => onUpdateQuantity(item.product.id, item.quantity - 1)}
                        >
                          -
                        </button>
                        <input
                          type="text"
                          readOnly
                          className="form-control text-center bg-white"
                          value={item.quantity}
                          aria-label={`Quantity for ${item.product.name}`}
                        />
                        <button
                          className="btn btn-outline-secondary"
                          type="button"
                          disabled={item.quantity >= 10 || isSubmitting}
                          onClick={() => onUpdateQuantity(item.product.id, item.quantity + 1)}
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td className="text-end fw-semibold font-monospace">
                      {formatTHB(item.product.priceMinor * item.quantity)}
                    </td>
                    <td className="text-center">
                      <button
                        className="btn btn-outline-danger btn-sm"
                        disabled={isSubmitting}
                        onClick={() => onRemoveItem(item.product.id)}
                        aria-label={`Remove ${item.product.name}`}
                        data-testid={`remove-item-${item.product.id}`}
                      >
                        &times;
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="bg-light p-3 rounded mb-4 d-flex justify-content-between align-items-center">
            <div>
              <div className="text-muted small">
                Estimated total <span className="fw-semibold">(confirmed by server on submit)</span>:
              </div>
              <div className="small text-muted fst-italic">
                Final authoritative calculation executed on server in minor units.
              </div>
            </div>
            <div className="fs-4 fw-bold text-primary font-monospace" data-testid="estimated-total">
              {formatTHB(estimatedTotalMinor)}
            </div>
          </div>

          <div className="d-flex justify-content-end gap-2">
            <button
              className="btn btn-outline-secondary"
              onClick={onBackToCatalog}
              disabled={isSubmitting}
            >
              Continue Shopping
            </button>
            <button
              className="btn btn-primary px-4 fw-semibold"
              disabled={isSubmitting || cart.length === 0}
              onClick={handleSubmitOrder}
              data-testid="submit-order-button"
            >
              {isSubmitting ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Submitting Order...
                </>
              ) : (
                "Submit Order"
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
