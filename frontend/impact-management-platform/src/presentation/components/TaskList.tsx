/**
 * ============================================================
 * File: TaskList.tsx
 * Purpose: Presentation component for rendering a list of tasks.
 * Context: This component belongs to the presentation layer and
 * should only display task data passed in from parent state.
 * Inputs: Array of Task entities.
 * Outputs: Rendered task list UI.
 * Notes:
 * - Keep domain filtering logic out of this file.
 * - Keep repository/storage logic out of this file.
 * - Keep application orchestration out of this file.
 * ============================================================
 */

import type { Task } from "../../domain/tasks/task.types";

interface TaskListProps {
  tasks: Task[];
}

export default function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <section style={styles.container}>
        <h2 style={styles.heading}>Tasks</h2>
        <p style={styles.emptyState}>
          No tasks yet. Create your first task to begin tracking impact.
        </p>
      </section>
    );
  }

  return (
    <section style={styles.container}>
      <h2 style={styles.heading}>Tasks</h2>

      <ul style={styles.list}>
        {tasks.map((task) => (
          <li key={task.id} style={styles.card}>
            <div style={styles.cardHeader}>
              <h3 style={styles.title}>{task.title}</h3>
              <span style={styles.statusBadge}>{formatLabel(task.status)}</span>
            </div>

            <p style={styles.description}>
              {task.description || "No description provided."}
            </p>

            <div style={styles.metaRow}>
              <span style={styles.metaItem}>
                <strong>Priority:</strong> {formatLabel(task.priority)}
              </span>
              <span style={styles.metaItem}>
                <strong>Category:</strong> {formatLabel(task.category)}
              </span>
            </div>

            <div style={styles.impactBlock}>
              <p style={styles.impactText}>
                <strong>Problem:</strong> {task.impactFields.problem}
              </p>
              <p style={styles.impactText}>
                <strong>Action:</strong> {task.impactFields.action}
              </p>
              <p style={styles.impactText}>
                <strong>Impact:</strong> {task.impactFields.impact}
              </p>
            </div>

            <div style={styles.metaRow}>
              <span style={styles.metaItem}>
                <strong>Metrics:</strong> {task.impactFields.metrics.length}
              </span>
              <span style={styles.metaItem}>
                <strong>Evidence:</strong> {task.impactFields.evidence.length}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

function formatLabel(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    border: "1px solid #e5e7eb",
    padding: "20px",
    borderRadius: "10px",
    background: "#ffffff",
  },
  heading: {
    marginTop: 0,
    marginBottom: "16px",
    fontSize: "1.25rem",
    color: "#111827",
  },
  emptyState: {
    margin: 0,
    color: "#6b7280",
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "16px",
    background: "#f9fafb",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "12px",
    marginBottom: "8px",
  },
  title: {
    margin: 0,
    fontSize: "1rem",
    color: "#111827",
  },
  statusBadge: {
    display: "inline-block",
    padding: "4px 10px",
    borderRadius: "999px",
    background: "#dbeafe",
    color: "#1d4ed8",
    fontSize: "0.8rem",
    fontWeight: 600,
    whiteSpace: "nowrap",
  },
  description: {
    margin: "0 0 12px 0",
    color: "#374151",
  },
  metaRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: "16px",
    marginBottom: "10px",
  },
  metaItem: {
    fontSize: "0.9rem",
    color: "#4b5563",
  },
  impactBlock: {
    borderTop: "1px solid #e5e7eb",
    borderBottom: "1px solid #e5e7eb",
    padding: "10px 0",
    marginBottom: "10px",
  },
  impactText: {
    margin: "6px 0",
    color: "#374151",
  },
};
