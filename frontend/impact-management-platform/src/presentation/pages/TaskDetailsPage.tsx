import { useEffect, useState, type CSSProperties } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import type { Task } from "../../domain/tasks/task.types";
import type { TaskEvent } from "../../domain/taskEvents/taskEvent.types";
import { useTaskContext } from "../context/TaskContext";

function formatLabel(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function TaskDetailsPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const { getTaskById, getTaskEventsByTaskId, deleteTask, error, clearError } =
    useTaskContext();

  const [task, setTask] = useState<Task | null>(null);
  const [events, setEvents] = useState<TaskEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    async function loadTaskDetails() {
      if (!taskId) {
        setIsLoading(false);
        return;
      }

      try {
        clearError();
        setIsLoading(true);

        const [loadedTask, loadedEvents] = await Promise.all([
          getTaskById(taskId),
          getTaskEventsByTaskId(taskId),
        ]);

        setTask(loadedTask);
        setEvents(loadedEvents);
      } finally {
        setIsLoading(false);
      }
    }

    void loadTaskDetails();
  }, [taskId, getTaskById, getTaskEventsByTaskId, clearError]);

  async function handleDelete(): Promise<void> {
    if (!taskId || !task) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${task.title}" from the active task list?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      setIsDeleting(true);
      await deleteTask(taskId);
      navigate("/", { replace: true });
    } finally {
      setIsDeleting(false);
    }
  }

  if (isLoading) {
    return (
      <main style={styles.pageShell}>
        <p style={styles.helperText}>Loading task details...</p>
      </main>
    );
  }

  if (!task) {
    return (
      <main style={styles.pageShell}>
        <div style={styles.headerRow}>
          <h1 style={styles.title}>Task Not Found</h1>
          <Link to="/" style={styles.linkButton}>
            Back to Dashboard
          </Link>
        </div>
        <p style={styles.helperText}>The requested task could not be found.</p>
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
            / Task Details
          </p>
          <h1 style={styles.title}>{task.title}</h1>
          <p style={styles.subtitle}>
            Detailed task record with impact evidence and event history.
          </p>
        </div>

        <div style={styles.actionRow}>
          <Link to={`/tasks/${task.id}/edit`} style={styles.primaryButton}>
            Edit Task
          </Link>
          <button
            type="button"
            onClick={() => {
              void handleDelete();
            }}
            disabled={isDeleting}
            style={styles.dangerButton}
          >
            {isDeleting ? "Deleting..." : "Delete Task"}
          </button>
        </div>
      </div>

      {error && <section style={styles.errorBox}>{error}</section>}

      <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Overview</h2>
        <div style={styles.metaGrid}>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Status</span>
            <strong>{formatLabel(task.status)}</strong>
          </div>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Priority</span>
            <strong>{formatLabel(task.priority)}</strong>
          </div>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Category</span>
            <strong>{formatLabel(task.category)}</strong>
          </div>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Tags</span>
            <strong>{task.tags.length ? task.tags.join(", ") : "None"}</strong>
          </div>
        </div>

        <div style={styles.contentBlock}>
          <h3 style={styles.subheading}>Description</h3>
          <p style={styles.bodyText}>
            {task.description || "No description provided."}
          </p>
        </div>
      </section>

      <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Impact Record</h2>

        <div style={styles.contentBlock}>
          <h3 style={styles.subheading}>Problem</h3>
          <p style={styles.bodyText}>{task.impactFields.problem}</p>
        </div>

        <div style={styles.contentBlock}>
          <h3 style={styles.subheading}>Action</h3>
          <p style={styles.bodyText}>{task.impactFields.action}</p>
        </div>

        <div style={styles.contentBlock}>
          <h3 style={styles.subheading}>Impact</h3>
          <p style={styles.bodyText}>{task.impactFields.impact}</p>
        </div>

        <div style={styles.metaGrid}>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Metrics</span>
            <strong>{task.impactFields.metrics.length}</strong>
          </div>
          <div style={styles.metaCard}>
            <span style={styles.metaLabel}>Evidence Items</span>
            <strong>{task.impactFields.evidence.length}</strong>
          </div>
        </div>
      </section>

      <section style={styles.card}>
        <h2 style={styles.sectionTitle}>Task Timeline</h2>

        {events.length === 0 ? (
          <p style={styles.helperText}>No events recorded yet.</p>
        ) : (
          <ul style={styles.timelineList}>
            {events.map((event) => (
              <li key={event.id} style={styles.timelineItem}>
                <div style={styles.timelineHeader}>
                  <strong>{formatLabel(event.type)}</strong>
                  <span style={styles.timelineDate}>
                    {new Date(event.occurredAt).toLocaleString()}
                  </span>
                </div>
                <p style={styles.timelineText}>{event.summary}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
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
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "16px",
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
  actionRow: {
    display: "flex",
    gap: "12px",
    alignItems: "center",
  },
  primaryButton: {
    display: "inline-block",
    padding: "10px 16px",
    borderRadius: "8px",
    backgroundColor: "#2563eb",
    color: "#ffffff",
    textDecoration: "none",
    fontWeight: 600,
  },
  dangerButton: {
    padding: "10px 16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#dc2626",
    color: "#ffffff",
    cursor: "pointer",
    fontWeight: 600,
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
  card: {
    border: "1px solid #e5e7eb",
    borderRadius: "12px",
    backgroundColor: "#ffffff",
    padding: "20px",
    marginBottom: "20px",
  },
  sectionTitle: {
    marginTop: 0,
    marginBottom: "16px",
    fontSize: "1.25rem",
  },
  subheading: {
    margin: "0 0 8px 0",
    fontSize: "1rem",
  },
  contentBlock: {
    marginBottom: "16px",
  },
  bodyText: {
    margin: 0,
    color: "#374151",
    lineHeight: 1.5,
  },
  helperText: {
    color: "#6b7280",
  },
  metaGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "12px",
  },
  metaCard: {
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "14px",
    backgroundColor: "#f9fafb",
  },
  metaLabel: {
    display: "block",
    fontSize: "0.8rem",
    color: "#6b7280",
    marginBottom: "6px",
  },
  timelineList: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  timelineItem: {
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "14px",
    backgroundColor: "#f9fafb",
  },
  timelineHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "12px",
    marginBottom: "6px",
  },
  timelineDate: {
    color: "#6b7280",
    fontSize: "0.85rem",
  },
  timelineText: {
    margin: 0,
    color: "#374151",
  },
};
