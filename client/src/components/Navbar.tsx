import React from "react";
import { useAuth } from "../context/AuthContext.js";

interface NavbarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, onTabChange }) => {
  const { user, logout } = useAuth();

  if (!user) {
    return null;
  }

  const isCustomer = user.role === "CUSTOMER";
  const isOperator = user.role === "OPERATOR";

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container">
        <span className="navbar-brand fw-bold d-flex align-items-center">
          <span className="text-warning me-2">★</span> UniMerch Store
        </span>

        <div className="d-flex align-items-center flex-grow-1 ms-4">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0" data-testid="nav-links">
            {isCustomer && (
              <>
                <li className="nav-item">
                  <button
                    className={`btn nav-link px-3 ${activeTab === "catalog" ? "active fw-bold text-white" : ""}`}
                    onClick={() => onTabChange("catalog")}
                    data-testid="nav-catalog"
                  >
                    Catalog
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    className={`btn nav-link px-3 ${activeTab === "my-orders" ? "active fw-bold text-white" : ""}`}
                    onClick={() => onTabChange("my-orders")}
                    data-testid="nav-my-orders"
                  >
                    My Orders
                  </button>
                </li>
              </>
            )}

            {isOperator && (
              <li className="nav-item">
                <button
                  className={`btn nav-link px-3 ${activeTab === "incoming-orders" ? "active fw-bold text-white" : ""}`}
                  onClick={() => onTabChange("incoming-orders")}
                  data-testid="nav-incoming-orders"
                >
                  Incoming Orders
                </button>
              </li>
            )}
          </ul>

          <div className="d-flex align-items-center">
            <div className="me-3 text-end d-none d-sm-block text-light">
              <div className="small fw-semibold" data-testid="user-name">
                {user.name}
              </div>
              <div className="d-flex align-items-center justify-content-end gap-1">
                <span className="text-muted" style={{ fontSize: "0.75rem" }} data-testid="user-email">
                  {user.email}
                </span>
                <span
                  className={`badge ${isCustomer ? "bg-primary" : "bg-warning text-dark"}`}
                  style={{ fontSize: "0.65rem" }}
                  data-testid="user-role-badge"
                >
                  {user.role}
                </span>
              </div>
            </div>

            <button
              className="btn btn-outline-danger btn-sm"
              onClick={logout}
              data-testid="logout-button"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};
