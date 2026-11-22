import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../../src/App.js";
import * as api from "../../src/api.js";

vi.mock("../../src/api.js", () => ({
  login: vi.fn(),
  getMe: vi.fn(),
  logout: vi.fn()
}));

describe("Issue #8: Login UI and Authenticated Shell", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the login form when unauthenticated", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce(null);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /UniMerch Campus Store/i })).toBeInTheDocument();
    });

    expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Sign In/i })).toBeInTheDocument();
  });

  it("displays generic error message without field enumeration on invalid credentials", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce(null);
    vi.mocked(api.login).mockRejectedValueOnce(new Error("Invalid email or password"));

    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText(/Email address/i), "unknown@example.com");
    await user.type(screen.getByLabelText(/Password/i), "wrongpass");
    await user.click(screen.getByRole("button", { name: /Sign In/i }));

    await waitFor(() => {
      const alert = screen.getByTestId("login-error");
      expect(alert).toBeInTheDocument();
      expect(alert).toHaveTextContent("Invalid email or password");
    });

    // Verify it does not reveal whether the email exists
    expect(screen.queryByText(/Email not found/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Wrong password/i)).not.toBeInTheDocument();
  });

  it("disables submit button and shows busy state during login submission", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce(null);
    let resolveLogin: (val: any) => void;
    const loginPromise = new Promise((resolve) => {
      resolveLogin = resolve;
    });
    vi.mocked(api.login).mockReturnValueOnce(loginPromise as any);

    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText(/Email address/i), "customer1@example.com");
    await user.type(screen.getByLabelText(/Password/i), "Secret123!");
    
    const submitBtn = screen.getByRole("button", { name: /Sign In/i });
    await user.click(submitBtn);

    // Button should be disabled and show busy text
    expect(submitBtn).toBeDisabled();
    expect(screen.getByText(/Signing in.../i)).toBeInTheDocument();

    // Resolve login
    resolveLogin!({
      id: "usr_1",
      name: "Alice Student",
      email: "customer1@example.com",
      role: "CUSTOMER"
    });

    await waitFor(() => {
      expect(screen.getByText(/Alice Student/i)).toBeInTheDocument();
    });
  });

  it("renders only Customer navigation (Catalog, My Orders) upon Customer login", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce(null);
    vi.mocked(api.login).mockResolvedValueOnce({
      id: "usr_c1",
      name: "Alice Student",
      email: "customer1@example.com",
      role: "CUSTOMER"
    });

    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText(/Email address/i), "customer1@example.com");
    await user.type(screen.getByLabelText(/Password/i), "Secret123!");
    await user.click(screen.getByRole("button", { name: /Sign In/i }));

    await waitFor(() => {
      expect(screen.getByTestId("nav-catalog")).toBeInTheDocument();
    });

    expect(screen.getByTestId("nav-my-orders")).toBeInTheDocument();
    expect(screen.queryByTestId("nav-incoming-orders")).not.toBeInTheDocument();
    expect(screen.getByTestId("user-role-badge")).toHaveTextContent("CUSTOMER");
  });

  it("renders only Operator navigation (Incoming Orders) upon Operator login", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce(null);
    vi.mocked(api.login).mockResolvedValueOnce({
      id: "usr_op1",
      name: "Bob Operator",
      email: "operator1@example.com",
      role: "OPERATOR"
    });

    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText(/Email address/i), "operator1@example.com");
    await user.type(screen.getByLabelText(/Password/i), "Secret123!");
    await user.click(screen.getByRole("button", { name: /Sign In/i }));

    await waitFor(() => {
      expect(screen.getByTestId("nav-incoming-orders")).toBeInTheDocument();
    });

    expect(screen.queryByTestId("nav-catalog")).not.toBeInTheDocument();
    expect(screen.queryByTestId("nav-my-orders")).not.toBeInTheDocument();
    expect(screen.getByTestId("user-role-badge")).toHaveTextContent("OPERATOR");
  });

  it("logs out, clears user state, and returns to the login screen", async () => {
    vi.mocked(api.getMe).mockResolvedValueOnce({
      id: "usr_c1",
      name: "Alice Student",
      email: "customer1@example.com",
      role: "CUSTOMER"
    });
    vi.mocked(api.logout).mockResolvedValueOnce(undefined);

    const user = userEvent.setup();
    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId("user-name")).toHaveTextContent("Alice Student");
    });

    const logoutBtn = screen.getByTestId("logout-button");
    await user.click(logoutBtn);

    await waitFor(() => {
      expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    });

    expect(screen.queryByTestId("user-name")).not.toBeInTheDocument();
    expect(screen.queryByTestId("nav-catalog")).not.toBeInTheDocument();
    expect(api.logout).toHaveBeenCalledTimes(1);
  });
});
