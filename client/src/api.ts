const API_BASE_URL = import.meta.env.VITE_API_URL ?? "";

export type Role = "CUSTOMER" | "OPERATOR";

export interface User {
  id: string;
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
