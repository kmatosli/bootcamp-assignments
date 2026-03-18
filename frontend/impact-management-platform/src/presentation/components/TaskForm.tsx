/**
 * ============================================================
 * File: TaskForm.tsx
 * Purpose: UI component responsible for collecting task input
 * from the user and emitting a create-task event.
 * Context: This component is part of the presentation layer and
 * should not contain domain validation or repository logic.
 * Inputs: onCreate callback function.
 * Outputs: CreateTaskInput payload passed to the parent component.
 * ============================================================
 */

import {
  useState,
  type ChangeEvent,
  type CSSProperties,
  type FormEvent,
} from "react";
import type { CreateTaskInput } from "../../application/actions/taskActions";

interface TaskFormProps {
  onCreate: (input: CreateTaskInput) => Promise<void>;
}

const initialFormData: CreateTaskInput = {
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

export default function TaskForm({ onCreate }: TaskFormProps) {
  const [formData, setFormData] = useState<CreateTaskInput>(initialFormData);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleChange(
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name, value } = e.target;

    setFormData((currentFormData: CreateTaskInput) => ({
      ...currentFormData,
      [name]: value,
    }));
  }

  function resetForm() {
    setFormData(initialFormData);
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    try {
      setIsSubmitting(true);
      await onCreate(formData);
      resetForm();
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section style={styles.container}>
      <h2>Create Task</h2>

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
          {isSubmitting ? "Creating..." : "Create Task"}
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
