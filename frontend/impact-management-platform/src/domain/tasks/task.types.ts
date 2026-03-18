/**
 * ============================================================
 * File: task.types.ts
 * Purpose: Defines the canonical Task domain model for the
 * Impact Management Platform.
 * Context: Tasks are the primary source of truth in the system.
 * Inputs: N/A
 * Outputs: TypeScript types and interfaces used by the domain,
 * application, infrastructure, and presentation layers.
 * Notes:
 * - Keep validation logic out of this file.
 * - Keep storage logic out of this file.
 * - Keep UI logic out of this file.
 * ============================================================
 */

export type TaskStatus =
  | "draft"
  | "planned"
  | "in_progress"
  | "blocked"
  | "completed"
  | "archived";

export type TaskPriority = "low" | "medium" | "high" | "critical";

export type TaskCategory =
  | "delivery"
  | "analysis"
  | "leadership"
  | "stakeholder"
  | "process"
  | "learning"
  | "career"
  | "other";

export type SyncStatus = "not_synced" | "pending" | "synced" | "failed";

export interface TaskMetric {
  id: string;
  label: string;
  value: string;
}

export interface TaskEvidence {
  id: string;
  type: "note" | "link" | "file_ref" | "metric" | "quote";
  title: string;
  content: string;
  createdAt: string;
}

export interface WorkflowIntegrationFields {
  externalCalendarEventId?: string | null;
  externalTaskId?: string | null;
  externalProvider?:
    | "google_calendar"
    | "outlook_calendar"
    | "microsoft_todo"
    | null;
  syncStatus?: SyncStatus;
}

export interface TaskTimestamps {
  createdAt: string;
  updatedAt: string;
  startedAt?: string | null;
  completedAt?: string | null;
}

export interface TaskImpactFields {
  problem: string;
  action: string;
  impact: string;
  metrics: TaskMetric[];
  evidence: TaskEvidence[];
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  category: TaskCategory;
  tags: string[];
  timestamps: TaskTimestamps;
  impactFields: TaskImpactFields;
  workflow: WorkflowIntegrationFields;
}
