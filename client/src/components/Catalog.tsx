import React, { useState, useEffect } from "react";
import { Product, getProducts, formatTHB } from "../api.js";

interface CatalogProps {
  onAddToCart: (product: Product, quantity: number) => void;
  cartItemCount: number;
  onGoToCheckout: () => void;
}

export const Catalog: React.FC<CatalogProps> = ({
  onAddToCart,
  cartItemCount,
  onGoToCheckout,
}) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quantities, setQuantities] = useState<Record<number, number>>({});
  const [addedNotice, setAddedNotice] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    getProducts()
      .then((data) => {
        if (isMounted) {
          setProducts(data);
          // Initialize quantity selectors to 1
          const initQty: Record<number, number> = {};
          data.forEach((p) => {
            initQty[p.id] = 1;
          });
          setQuantities(initQty);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err instanceof Error ? err.message : "Failed to load products");
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleQtyChange = (productId: number, val: number) => {
    setQuantities((prev) => ({
      ...prev,
      [productId]: Math.max(1, Math.min(10, val)),
    }));
  };

  const handleAdd = (product: Product) => {
    const qty = quantities[product.id] || 1;
    onAddToCart(product, qty);
    setAddedNotice(`Added ${qty} × ${product.name} to cart.`);
    setTimeout(() => setAddedNotice(null), 3000);
  };

  if (loading) {
    return (
      <div className="card shadow-sm p-4 text-center" data-testid="catalog-loading">
        <div className="spinner-border text-primary my-4" role="status">
          <span className="visually-hidden">Loading catalog...</span>
        </div>
        <p className="text-muted">Loading campus merchandise...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger shadow-sm" role="alert" data-testid="catalog-error">
        <h5>Failed to load catalog</h5>
        <p className="mb-0">{error}</p>
      </div>
    );
  }

  return (
    <div data-testid="customer-catalog-view">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="h4 fw-bold mb-1">Campus Merchandise Catalog</h2>
          <p className="text-muted small mb-0">Browse and order official UniMerch items</p>
        </div>
        {cartItemCount > 0 && (
          <button
            className="btn btn-primary d-flex align-items-center gap-2"
            onClick={onGoToCheckout}
            data-testid="go-to-checkout-button"
          >
            <span>View Cart / Checkout</span>
            <span className="badge bg-white text-primary rounded-pill">{cartItemCount}</span>
          </button>
        )}
      </div>

      {addedNotice && (
        <div className="alert alert-success py-2 mb-3 small shadow-sm" role="status">
          {addedNotice}
        </div>
      )}

      {products.length === 0 ? (
        <div className="card shadow-sm p-4 text-center text-muted" data-testid="catalog-empty">
          No products currently available in the catalog.
        </div>
      ) : (
        <div className="row g-4" data-testid="product-grid">
          {products.map((product) => {
            const inStock = product.stockQuantity > 0;
            const currentQty = quantities[product.id] || 1;

            return (
              <div key={product.id} className="col-12 col-md-6 col-lg-4">
                <div className="card h-100 shadow-sm border-0 d-flex flex-column" data-testid={`product-card-${product.id}`}>
                  <div className="card-body d-flex flex-column">
                    <div className="d-flex justify-content-between align-items-start mb-2">
                      <h3 className="h6 fw-bold mb-0 text-dark">{product.name}</h3>
                      {inStock ? (
                        <span className="badge bg-success-subtle text-success border border-success-subtle" data-testid={`badge-stock-${product.id}`}>
                          In Stock ({product.stockQuantity})
                        </span>
                      ) : (
                        <span className="badge bg-danger-subtle text-danger border border-danger-subtle" data-testid={`badge-stock-${product.id}`}>
                          Out of Stock
                        </span>
                      )}
                    </div>

                    <p className="text-muted small flex-grow-1">{product.description || "Official UniMerch gear."}</p>

                    <div className="d-flex justify-content-between align-items-center mt-3 pt-2 border-top">
                      <span className="fs-5 fw-bold text-primary" data-testid={`price-${product.id}`}>
                        {formatTHB(product.priceMinor)}
                      </span>

                      {inStock ? (
                        <div className="d-flex align-items-center gap-2">
                          <input
                            type="number"
                            min="1"
                            max={Math.min(10, product.stockQuantity)}
                            value={currentQty}
                            onChange={(e) => handleQtyChange(product.id, parseInt(e.target.value) || 1)}
                            className="form-control form-control-sm"
                            style={{ width: "65px" }}
                            aria-label={`Quantity for ${product.name}`}
                            data-testid={`qty-input-${product.id}`}
                          />
                          <button
                            className="btn btn-sm btn-outline-primary fw-semibold text-nowrap"
                            onClick={() => handleAdd(product)}
                            data-testid={`add-to-cart-${product.id}`}
                          >
                            Add to Cart
                          </button>
                        </div>
                      ) : (
                        <button
                          className="btn btn-sm btn-secondary disabled"
                          disabled
                          data-testid={`unavailable-btn-${product.id}`}
                        >
                          Unavailable
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
