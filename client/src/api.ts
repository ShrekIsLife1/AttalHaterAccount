const API_BASE_URL = import.meta.env.VITE_API_URL ?? "";

export type Role = "CUSTOMER" | "OPERATOR";

export interface User {
  id: string | number;
  name: string;
  email: string;
  role: Role;
}

export interface AuthResponse {
  user: User;
}

export interface ApiError {
  error: string;
  details?: string[];
}

export interface Product {
  id: number;
  name: string;
  description?: string | null;
  priceMinor: number;
  stockQuantity: number;
  isActive: boolean;
}

export interface OrderItem {
  id: number;
  orderId: number;
  productId: number;
  quantity: number;
  unitPriceAtOrder: number;
  product?: Product;
}

export interface Order {
  id: number;
  customerId: number;
  status: string;
  totalMinor: number;
  createdAt: string;
  acceptedAt?: string | null;
  acceptedByOperatorId?: number | null;
  items: OrderItem[];
}

export interface CartItem {
  product: Product;
  quantity: number;
}

/**
 * Helper to format satang (minor units) to Thai Baht string
 * e.g. 75000 -> "฿750.00"
 */
export function formatTHB(minor: number): string {
  const baht = minor / 100;
  return `฿${baht.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/**
 * Perform login request with HttpOnly session cookie
 */
export async function login(email: string, password: string): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ email, password })
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Invalid email or password");
  }

  return (data as AuthResponse).user;
}

/**
 * Fetch current authenticated user identity
 */
export async function getMe(): Promise<User | null> {
  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    method: "GET",
    credentials: "include"
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json().catch(() => ({}));
  return (data as AuthResponse).user || null;
}

/**
 * Invalidate session on server and clear cookie
 */
export async function logout(): Promise<void> {
  await fetch(`${API_BASE_URL}/api/auth/logout`, {
    method: "POST",
    credentials: "include"
  });
}

/**
 * Fetch active products catalog
 */
export async function getProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/api/products`, {
    method: "GET",
    credentials: "include"
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || "Failed to fetch products");
  }

  return response.json();
}

/**
 * Create a new order with requested items
 */
export async function createOrder(items: { productId: number; quantity: number }[]): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/api/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ items })
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Failed to place order");
  }

  return data.order;
}

/**
 * Fetch orders for authenticated customer
 */
export async function getMyOrders(): Promise<Order[]> {
  const response = await fetch(`${API_BASE_URL}/api/orders`, {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Failed to fetch orders");
  }

  return data.orders || [];
}

/**
 * Fetch a single order by ID
 */
export async function getOrderById(id: number): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/api/orders/${id}`, {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Order not found");
  }

  return data.order;
}

/**
 * Fetch incoming orders queue for operators
 * F-05 / AC-14 / TEST-17
 */
export async function getOperatorOrders(): Promise<Order[]> {
  const response = await fetch(`${API_BASE_URL}/api/operator/orders`, {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Failed to fetch operator orders");
  }

  return Array.isArray(data) ? data : data.orders || [];
}

/**
 * Accept a placed order as operator
 * F-05 / AC-15, AC-16 / TEST-19, TEST-20
 */
export async function acceptOrder(id: number): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/api/operator/orders/${id}/accept`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include"
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Failed to accept order");
  }

  return data.order;
}
