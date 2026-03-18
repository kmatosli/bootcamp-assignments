/**
 * ============================================================
 * File: auth0.tsx
 * Purpose: Auth0 provider setup for the Impact Management Platform.
 * Context: Centralizes Auth0 configuration and exposes a provider
 * for the routed application.
 * Inputs: React children.
 * Outputs: Auth0Provider-wrapped application tree.
 * ============================================================
 */

import { Auth0Provider } from "@auth0/auth0-react";
import type { ReactNode } from "react";

interface AuthProviderProps {
  children: ReactNode;
}

const domain = import.meta.env.VITE_AUTH0_DOMAIN;
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID;

export function AuthProvider({ children }: AuthProviderProps) {
  if (!domain || !clientId) {
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
        <h1 style={{ marginTop: 0 }}>Auth0 Configuration Required</h1>
        <p>
          Add <code>VITE_AUTH0_DOMAIN</code> and{" "}
          <code>VITE_AUTH0_CLIENT_ID</code> to your local <code>.env</code>{" "}
          file.
        </p>
      </main>
    );
  }

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
    >
      {children}
    </Auth0Provider>
  );
}
