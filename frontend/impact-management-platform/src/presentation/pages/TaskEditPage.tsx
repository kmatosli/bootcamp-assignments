/**
 * ============================================================
 * File: TaskEditPage.tsx
 * Purpose: Routed page for editing an existing task.
 * Context: Loads a task by route parameter and submits updates
 * through TaskContext.
 * Inputs: taskId route param and form submission.
 * Outputs: Rendered edit-task page UI.
 * ============================================================
 */

import { useEffect, useState, type CSSProperties } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import type { Task } from "../../domain/tasks/task.types";
import { useTaskContext } from "../context/TaskContext";
import TaskForm from "../components/TaskForm";

export default function TaskEditPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const { getTaskById, updateTask, error, clearError } = useTaskContext();

  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadTask() {
      if (!taskId) {
        setIsLoading(false);
        return;
      }

      try {
        clearError();
        setIsLoading(true);
        const loadedTask = await getTaskById(taskId);
        setTask(loadedTask);
      } finally {
        setIsLoading(false);
      }
    }

    void loadTask();
  }, [taskId, getTaskById, clearError]);

  if (isLoading) {
    return (
      <main style={styles.pageShell}>
        <p style={styles.helperText}>Loading task for editing...</p>
      </main>
    );
  }

  if (!task) {
    return (
      <main style={styles.pageShell}>
        <h1 style={styles.title}>Task Not Found</h1>
        <Link to="/" style={styles.linkButton}>
          Back to Dashboard
        </Link>
      </main>
    );
  }

  return (
    <main style={styles.pageShell}>
      <div style={styles.headerRow}>
        <div>
          <p style={styles.breadcrumb}>
            <Link to="/" style={styles.breadcrumbLink}>
              Dashboard
            </Link>{" "}
            /{" "}
            <Link to={`/tasks/${task.id}`} style={styles.breadcrumbLink}>
              Task Details
            </Link>{" "}
            / Edit
          </p>
          <h1 style={styles.title}>Edit Task</h1>
          <p style={styles.subtitle}>
            Update task details while preserving canonical state and event
            history.
          </p>
        </div>
      </div>

      {error && <section style={styles.errorBox}>{error}</section>}

      <TaskForm
        mode="edit"
        initialData={{
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
          category: task.category,
          tags: task.tags,
          problem: task.impactFields.problem,
          action: task.impactFields.action,
          impact: task.impactFields.impact,
        }}
        onSubmit={async (input) => {
          await updateTask(task.id, {
            title: input.title,
            description: input.description,
            status: input.status,
            priority: input.priority,
            category: input.category,
            tags: input.tags,
            impactFields: {
              problem: input.problem,
              action: input.action,
              impact: input.impact,
            },
          });

          navigate(`/tasks/${task.id}`);
        }}
      />
    </main>
  );
}

const styles: Record<string, CSSProperties> = {
  pageShell: {
    maxWidth: "1080px",
    margin: "0 auto",
    padding: "32px",
    fontFamily: "Arial, sans-serif",
    color: "#111827",
  },
  headerRow: {
    marginBottom: "24px",
  },
  breadcrumb: {
    margin: 0,
    fontSize: "0.9rem",
    color: "#6b7280",
  },
  breadcrumbLink: {
    color: "#2563eb",
    textDecoration: "none",
  },
  title: {
    margin: "8px 0 6px 0",
    fontSize: "2rem",
  },
  subtitle: {
    margin: 0,
    color: "#4b5563",
  },
  helperText: {
    color: "#6b7280",
  },
  linkButton: {
    display: "inline-block",
    padding: "10px 16px",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    color: "#111827",
    textDecoration: "none",
  },
  errorBox: {
    marginBottom: "16px",
    padding: "12px 16px",
    borderRadius: "8px",
    backgroundColor: "#fee2e2",
    color: "#991b1b",
    border: "1px solid #fecaca",
  },
};
