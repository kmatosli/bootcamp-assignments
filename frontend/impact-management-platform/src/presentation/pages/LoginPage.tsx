/**
 * ============================================================
 * File: LoginPage.tsx
 * Purpose: Public landing/login page for the app.
 * Context: Auth entry page using Auth0 Universal Login.
 * Inputs: Auth state from Auth0.
 * Outputs: Login UI or redirect to dashboard.
 * ============================================================
 */

import { useAuth0 } from "@auth0/auth0-react";
import { Navigate } from "react-router-dom";
import type { CSSProperties } from "react";

export default function LoginPage() {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();

  if (isLoading) {
    return (
      <main style={styles.pageShell}>
        <p style={styles.helperText}>Loading authentication...</p>
      </main>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <main style={styles.pageShell}>
      <section style={styles.card}>
        <h1 style={styles.title}>Impact Management Platform</h1>
        <p style={styles.subtitle}>
          Sign in to manage tasks, capture evidence, and build a record of
          impact.
        </p>

        <button
          type="button"
          onClick={() => {
            void loginWithRedirect();
          }}
          style={styles.primaryButton}
        >
          Log In with Auth0
        </button>
      </section>
    </main>
  );
}

const styles: Record<string, CSSProperties> = {
  pageShell: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: "32px",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f9fafb",
  },
  card: {
    width: "100%",
    maxWidth: "560px",
    backgroundColor: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "16px",
    padding: "32px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.06)",
  },
  title: {
    marginTop: 0,
    marginBottom: "12px",
    fontSize: "2rem",
    color: "#111827",
  },
  subtitle: {
    marginTop: 0,
    marginBottom: "24px",
    color: "#4b5563",
    lineHeight: 1.5,
  },
  primaryButton: {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "#ffffff",
    cursor: "pointer",
    fontWeight: 600,
  },
  helperText: {
    color: "#6b7280",
  },
};
