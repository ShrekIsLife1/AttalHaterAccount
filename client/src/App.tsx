import React, { useState, useEffect } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext.js";
import { Login } from "./components/Login.js";
import { Navbar } from "./components/Navbar.js";
import { Catalog } from "./components/Catalog.js";
import { Checkout } from "./components/Checkout.js";
import { MyOrders } from "./components/MyOrders.js";
import { OrderDetail } from "./components/OrderDetail.js";
import { OperatorOrders } from "./components/OperatorOrders.js";
import { Product, CartItem, Order } from "./api.js";

const AppContent: React.FC = () => {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState<string>("catalog");
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);

  // Keep active tab in sync with user role
  useEffect(() => {
    if (user) {
      if (user.role === "CUSTOMER") {
        setActiveTab("catalog");
      } else if (user.role === "OPERATOR") {
        setActiveTab("incoming-orders");
      }
    } else {
      setCart([]);
      setSelectedOrderId(null);
    }
  }, [user]);

  // Cart operations
  const handleAddToCart = (product: Product, quantity: number) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: Math.min(10, item.quantity + quantity) }
            : item
        );
      }
      return [...prev, { product, quantity }];
    });
  };

  const handleUpdateQuantity = (productId: number, quantity: number) => {
    if (quantity <= 0) {
      handleRemoveItem(productId);
      return;
    }
    setCart((prev) =>
      prev.map((item) =>
        item.product.id === productId
          ? { ...item, quantity: Math.min(10, quantity) }
          : item
      )
    );
  };

  const handleRemoveItem = (productId: number) => {
    setCart((prev) => prev.filter((item) => item.product.id !== productId));
  };

  const handleClearCart = () => {
    setCart([]);
  };

  const totalCartCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <div className="spinner-border text-primary mb-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="text-muted small">Checking session...</div>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Login />;
  }

  return (
    <div className="min-vh-100 bg-light">
      <Navbar
        activeTab={activeTab}
        onTabChange={(tab) => {
          setSelectedOrderId(null);
          setActiveTab(tab);
        }}
      />

      <main className="container py-4">
        {user.role === "CUSTOMER" && (
          <div>
            {activeTab === "catalog" && (
              <Catalog
                onAddToCart={handleAddToCart}
                cartItemCount={totalCartCount}
                onGoToCheckout={() => setActiveTab("checkout")}
              />
            )}

            {activeTab === "checkout" && (
              <Checkout
                cart={cart}
                onUpdateQuantity={handleUpdateQuantity}
                onRemoveItem={handleRemoveItem}
                onClearCart={handleClearCart}
                onBackToCatalog={() => setActiveTab("catalog")}
                onOrderCreated={(order: Order) => {
                  setSelectedOrderId(order.id);
                  setActiveTab("my-orders");
                }}
              />
            )}

            {activeTab === "my-orders" && !selectedOrderId && (
              <MyOrders
                onSelectOrder={(orderId) => setSelectedOrderId(orderId)}
                onGoToCatalog={() => {
                  setSelectedOrderId(null);
                  setActiveTab("catalog");
                }}
              />
            )}

            {activeTab === "my-orders" && selectedOrderId && (
              <OrderDetail
                orderId={selectedOrderId}
                onBack={() => setSelectedOrderId(null)}
                backLabel="Back to My Orders"
              />
            )}
          </div>
        )}

        {user.role === "OPERATOR" && (
          <OperatorOrders />
        )}
      </main>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
