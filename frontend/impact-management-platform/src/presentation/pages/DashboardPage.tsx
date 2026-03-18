/**
 * ============================================================
 * File: DashboardPage.tsx
 * Purpose: Main dashboard page for the Impact Management
 * Platform.
 * Context: Uses TaskContext for task state and actions and
 * composes presentation components for dashboard workflows.
 * Inputs: Context state and actions.
 * Outputs: Rendered dashboard page UI.
 * Notes:
 * - Keep domain logic out of this file.
 * - Keep repository logic out of this file.
 * ============================================================
 */

import type { CSSProperties } from "react";
import { useNavigate } from "react-router-dom";
import { useTaskContext } from "../context/TaskContext";
import { selectCompletedTasks } from "../../domain/selectors/task.selectors";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";

export default function DashboardPage() {
  const navigate = useNavigate();
  const { tasks, isLoading, error, createTask } = useTaskContext();

  const completedTaskCount = selectCompletedTasks(tasks).length;

  if (isLoading) {
    return (
      <main style={styles.pageShell}>
        <h1 style={styles.title}>Impact Management Platform</h1>
        <p style={styles.helperText}>Loading dashboard...</p>
      </main>
    );
  }

  return (
    <main style={styles.pageShell}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>Impact Management Platform</h1>
          <p style={styles.subtitle}>
            Structured work tracking, evidence capture, and impact reporting.
          </p>
        </div>
      </header>

      {error && <section style={styles.errorBox}>{error}</section>}

      <section style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Total Tasks</span>
          <strong style={styles.summaryValue}>{tasks.length}</strong>
        </div>

        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Completed Tasks</span>
          <strong style={styles.summaryValue}>{completedTaskCount}</strong>
        </div>

        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Open Tasks</span>
          <strong style={styles.summaryValue}>
            {tasks.length - completedTaskCount}
          </strong>
        </div>
      </section>

      <section style={styles.mainGrid}>
        <TaskForm onCreate={createTask} />
        <TaskList
          tasks={tasks}
          onViewTask={(taskId) => {
            navigate(`/tasks/${taskId}`);
          }}
        />
      </section>
    </main>
  );
}

const styles: Record<string, CSSProperties> = {
  pageShell: {
    maxWidth: "1280px",
    margin: "0 auto",
    padding: "32px",
    fontFamily: "Arial, sans-serif",
    color: "#111827",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "16px",
    marginBottom: "24px",
  },
  title: {
    margin: 0,
    fontSize: "2rem",
  },
  subtitle: {
    marginTop: "8px",
    marginBottom: 0,
    color: "#4b5563",
  },
  errorBox: {
    marginBottom: "16px",
    padding: "12px 16px",
    borderRadius: "8px",
    backgroundColor: "#fee2e2",
    color: "#991b1b",
    border: "1px solid #fecaca",
  },
  summaryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "12px",
    marginBottom: "24px",
  },
  summaryCard: {
    padding: "16px",
    borderRadius: "10px",
    border: "1px solid #e5e7eb",
    backgroundColor: "#ffffff",
  },
  summaryLabel: {
    display: "block",
    fontSize: "0.85rem",
    color: "#6b7280",
    marginBottom: "6px",
  },
  summaryValue: {
    fontSize: "1.25rem",
  },
  mainGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "24px",
    alignItems: "start",
    marginBottom: "24px",
  },
  helperText: {
    color: "#6b7280",
  },
};
