/**
 * ============================================================
 * File: taskEvent.types.ts
 * Purpose: Defines the canonical task event domain model.
 * Context: Task events store append-only history for task activity.
 * Inputs: N/A
 * Outputs: TypeScript types and interfaces used for task event
 * tracking across the application and infrastructure layers.
 * Notes:
 * - Task events are historical records, not current task state.
 * - Task events should be append-only and never edited in place.
 * - Keep validation, storage, and UI logic out of this file.
 * ============================================================
 */

export type TaskEventType =
  | "task_created"
  | "task_updated"
  | "task_status_changed"
  | "task_completed"
  | "task_archived"
  | "evidence_added"
  | "metric_added"
  | "workflow_sync_requested"
  | "workflow_sync_succeeded"
  | "workflow_sync_failed";

export interface TaskEvent {
  id: string;
  taskId: string;
  type: TaskEventType;
  occurredAt: string;
  actor: string;
  summary: string;
  metadata?: Record<string, unknown>;
}
