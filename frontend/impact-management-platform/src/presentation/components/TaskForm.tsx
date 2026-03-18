/**
 * ============================================================
 * File: TaskForm.tsx
 * Purpose: Collects task input for create and edit workflows.
 * Context: Presentation-layer form component with no repository
 * or domain validation logic.
 * Inputs: Initial form data, mode, and submit handler.
 * Outputs: CreateTaskInput payload emitted to parent.
 * ============================================================
 */

import {
  useMemo,
  useState,
  type ChangeEvent,
  type CSSProperties,
  type FormEvent,
} from "react";
import type { CreateTaskInput } from "../../application/actions/taskActions";

interface TaskFormProps {
  onCreate?: (input: CreateTaskInput) => Promise<unknown>;
  onSubmit?: (input: CreateTaskInput) => Promise<unknown>;
  initialData?: Partial<CreateTaskInput>;
  mode?: "create" | "edit";
}

const defaultFormData: CreateTaskInput = {
  title: "",
  description: "",
  status: "planned",
  priority: "medium",
  category: "delivery",
  tags: [],
  problem: "",
  action: "",
  impact: "",
};

export default function TaskForm({
  onCreate,
  onSubmit,
  initialData,
  mode = "create",
}: TaskFormProps) {
  const resolvedInitialData = useMemo<CreateTaskInput>(
    () => ({
      ...defaultFormData,
      ...initialData,
      tags: initialData?.tags ?? [],
    }),
    [initialData],
  );

  const [formData, setFormData] =
    useState<CreateTaskInput>(resolvedInitialData);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleChange(
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name, value } = e.target;

    setFormData((currentFormData) => ({
      ...currentFormData,
      [name]: value,
    }));
  }

  function handleTagsChange(e: ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;

    setFormData((currentFormData) => ({
      ...currentFormData,
      tags: value
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
    }));
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    const submitHandler = onSubmit ?? onCreate;

    if (!submitHandler) {
      return;
    }

    try {
      setIsSubmitting(true);
      await submitHandler(formData);

      if (mode === "create") {
        setFormData(defaultFormData);
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section style={styles.container}>
      <h2>{mode === "edit" ? "Edit Task" : "Create Task"}</h2>

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          name="title"
          placeholder="Task title"
          value={formData.title}
          onChange={handleChange}
          style={styles.input}
        />

        <textarea
          name="description"
          placeholder="Task description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          style={styles.input}
        />

        <select
          name="status"
          value={formData.status}
          onChange={handleChange}
          style={styles.input}
        >
          <option value="draft">Draft</option>
          <option value="planned">Planned</option>
          <option value="in_progress">In Progress</option>
          <option value="blocked">Blocked</option>
          <option value="completed">Completed</option>
        </select>

        <select
          name="priority"
          value={formData.priority}
          onChange={handleChange}
          style={styles.input}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>

        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          style={styles.input}
        >
          <option value="delivery">Delivery</option>
          <option value="analysis">Analysis</option>
          <option value="leadership">Leadership</option>
          <option value="stakeholder">Stakeholder</option>
          <option value="process">Process</option>
          <option value="learning">Learning</option>
          <option value="career">Career</option>
          <option value="other">Other</option>
        </select>

        <input
          name="tags"
          placeholder="Tags (comma separated)"
          value={formData.tags?.join(", ") ?? ""}
          onChange={handleTagsChange}
          style={styles.input}
        />

        <textarea
          name="problem"
          placeholder="Problem"
          value={formData.problem}
          onChange={handleChange}
          rows={2}
          style={styles.input}
        />

        <textarea
          name="action"
          placeholder="Action"
          value={formData.action}
          onChange={handleChange}
          rows={2}
          style={styles.input}
        />

        <textarea
          name="impact"
          placeholder="Impact"
          value={formData.impact}
          onChange={handleChange}
          rows={2}
          style={styles.input}
        />

        <button disabled={isSubmitting} style={styles.button}>
          {isSubmitting
            ? mode === "edit"
              ? "Saving..."
              : "Creating..."
            : mode === "edit"
              ? "Save Changes"
              : "Create Task"}
        </button>
      </form>
    </section>
  );
}

const styles: Record<string, CSSProperties> = {
  container: {
    border: "1px solid #e5e7eb",
    padding: "20px",
    borderRadius: "10px",
    background: "#ffffff",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #d1d5db",
  },
  button: {
    padding: "10px",
    borderRadius: "6px",
    border: "none",
    background: "#2563eb",
    color: "white",
    cursor: "pointer",
  },
};
