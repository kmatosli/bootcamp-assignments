/**
 * ============================================================
 * File: DashboardPage.tsx
 * Purpose: Main dashboard page for the Impact Management
 * Platform MVP.
 * Context: This page composes presentation components and
 * displays top-level summary information for tasks and reports.
 * Inputs: Tasks, latest report, loading flags, error messages,
 * and UI event handlers passed down from App.tsx.
 * Outputs: Rendered dashboard page UI.
 * Notes:
 * - Keep domain logic out of this file.
 * - Keep repository logic out of this file.
 * - Keep application orchestration in App.tsx or application actions.
 * ============================================================
 */

import type { CSSProperties } from "react";
import type { Task } from "../../domain/tasks/task.types";
import type { ImpactReport } from "../../domain/reports/report.types";
import type { CreateTaskInput } from "../../application/actions/taskActions";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import ReportSummary from "../components/ReportSummary";

interface DashboardPageProps {
  tasks: Task[];
  report: ImpactReport | null;
  totalTasks: number;
  completedTaskCount: number;
  isGeneratingReport: boolean;
  error: string | null;
  onCreateTask: (input: CreateTaskInput) => Promise<void>;
  onGenerateReport: () => Promise<void>;
}

export default function DashboardPage({
  tasks,
  report,
  totalTasks,
  completedTaskCount,
  isGeneratingReport,
  error,
  onCreateTask,
  onGenerateReport,
}: DashboardPageProps) {
  return (
    <main style={styles.pageShell}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>Impact Management Platform</h1>
          <p style={styles.subtitle}>
            Structured work tracking, evidence capture, and impact reporting.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            void onGenerateReport();
          }}
          disabled={isGeneratingReport}
          style={styles.primaryButton}
        >
          {isGeneratingReport ? "Generating..." : "Generate Report"}
        </button>
      </header>

      {error && (
        <section style={styles.errorBox}>
          <strong>Error:</strong> {error}
        </section>
      )}

      <section style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Total Tasks</span>
          <strong style={styles.summaryValue}>{totalTasks}</strong>
        </div>

        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Completed Tasks</span>
          <strong style={styles.summaryValue}>{completedTaskCount}</strong>
        </div>

        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>Latest Report</span>
          <strong style={styles.summaryValue}>
            {report ? "Available" : "Not Generated"}
          </strong>
        </div>
      </section>

      <section style={styles.mainGrid}>
        <TaskForm onCreate={onCreateTask} />
        <TaskList tasks={tasks} />
      </section>

      <ReportSummary report={report} />
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
  primaryButton: {
    padding: "10px 16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "#ffffff",
    cursor: "pointer",
    fontWeight: 600,
    whiteSpace: "nowrap",
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
};
