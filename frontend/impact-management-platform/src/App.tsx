/**
 * ============================================================
 * File: App.tsx
 * Purpose: Top-level routed application shell.
 * Context: Composes public and protected routes for the app.
 * Inputs: Route navigation and page interactions.
 * Outputs: Routed application UI.
 * ============================================================
 */

import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import DashboardPage from "./presentation/pages/DashboardPage";
import LoginPage from "./presentation/pages/LoginPage";
import TaskDetailsPage from "./presentation/pages/TaskDetailsPage";
import TaskEditPage from "./presentation/pages/TaskEditPage";
import { TaskProvider } from "./presentation/context/TaskContext";
import ProtectedRoute from "./infrastructure/auth/ProtectedRoute";

function ProtectedApp() {
  const { user, logout } = useAuth0();

  return (
    <TaskProvider>
      <div style={styles.appShell}>
        <header style={styles.header}>
          <div>
            <strong style={styles.brand}>Impact Management Platform</strong>
            <p style={styles.userText}>
              Signed in as {user?.name ?? user?.email ?? "Authenticated User"}
            </p>
          </div>

          <button
            type="button"
            onClick={() => {
              logout({
                logoutParams: {
                  returnTo: window.location.origin,
                },
              });
            }}
            style={styles.logoutButton}
          >
            Log Out
          </button>
        </header>

        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/tasks/:taskId" element={<TaskDetailsPage />} />
          <Route path="/tasks/:taskId/edit" element={<TaskEditPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </TaskProvider>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <ProtectedApp />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

const styles: Record<string, React.CSSProperties> = {
  appShell: {
    minHeight: "100vh",
    backgroundColor: "#f9fafb",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "16px",
    padding: "16px 24px",
    borderBottom: "1px solid #e5e7eb",
    backgroundColor: "#ffffff",
  },
  brand: {
    display: "block",
    color: "#111827",
  },
  userText: {
    margin: "4px 0 0 0",
    color: "#6b7280",
    fontSize: "0.9rem",
  },
  logoutButton: {
    padding: "10px 14px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    backgroundColor: "#ffffff",
    color: "#111827",
    cursor: "pointer",
    fontWeight: 600,
  },
};

export default App;
