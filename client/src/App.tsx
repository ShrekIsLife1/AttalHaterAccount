import React, { useState, useEffect } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext.js";
import { Login } from "./components/Login.js";
import { Navbar } from "./components/Navbar.js";

const AppContent: React.FC = () => {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState<string>("catalog");

  // Keep active tab in sync with user role
  useEffect(() => {
    if (user) {
      if (user.role === "CUSTOMER") {
        setActiveTab("catalog");
      } else if (user.role === "OPERATOR") {
        setActiveTab("incoming-orders");
      }
    }
  }, [user]);

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
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="container py-4">
        {user.role === "CUSTOMER" && (
          <div>
            {activeTab === "catalog" && (
              <div className="card shadow-sm p-4" data-testid="customer-catalog-view">
                <h3 className="h5 fw-bold mb-3">Product Catalog</h3>
                <p className="text-muted">Browse official campus merchandise and add items to your order.</p>
                <div className="alert alert-info py-2 small">
                  Catalog product listing is active and ready for Sprint 1 orders.
                </div>
              </div>
            )}

            {activeTab === "my-orders" && (
              <div className="card shadow-sm p-4" data-testid="customer-orders-view">
                <h3 className="h5 fw-bold mb-3">My Orders</h3>
                <p className="text-muted">Track your placed orders and counter pickup status.</p>
                <div className="alert alert-secondary py-2 small">
                  No orders placed yet.
                </div>
              </div>
            )}
          </div>
        )}

        {user.role === "OPERATOR" && (
          <div className="card shadow-sm p-4" data-testid="operator-orders-view">
            <h3 className="h5 fw-bold mb-3">Incoming Orders Queue</h3>
            <p className="text-muted">Orders awaiting operator review and counter acceptance.</p>
            <div className="alert alert-warning py-2 small">
              Operator fulfillment dashboard active.
            </div>
          </div>
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
