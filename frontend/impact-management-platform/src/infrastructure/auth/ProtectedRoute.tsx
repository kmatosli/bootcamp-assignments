/**
 * ============================================================
 * File: ProtectedRoute.tsx
 * Purpose: Route guard for authenticated pages.
 * Context: Uses Auth0 auth state to protect routed pages.
 * Inputs: React children.
 * Outputs: Either protected content or login redirect flow.
 * ============================================================
 */

import { useEffect, type ReactNode } from "react";
import { useAuth0 } from "@auth0/auth0-react";

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      void loginWithRedirect();
    }
  }, [isAuthenticated, isLoading, loginWithRedirect]);

  if (isLoading) {
    return (
      <main
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          padding: "32px",
          fontFamily: "Arial, sans-serif",
          color: "#111827",
        }}
      >
        <p>Checking authentication...</p>
      </main>
    );
  }

  if (!isAuthenticated) {
    return (
      <main
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          padding: "32px",
          fontFamily: "Arial, sans-serif",
          color: "#111827",
        }}
      >
        <p>Redirecting to login...</p>
      </main>
    );
  }

  return <>{children}</>;
}
