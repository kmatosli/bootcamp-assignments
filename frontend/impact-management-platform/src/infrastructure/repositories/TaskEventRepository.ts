/**
 * ============================================================
 * File: TaskEventRepository.ts
 * Purpose: Defines the repository contract for append-only task
 * event storage and retrieval.
 * Context: Task events capture historical activity and should be
 * stored separately from canonical task state. Application logic
 * should depend on this interface rather than a concrete storage
 * implementation.
 * Inputs: Task event entities and task identifiers.
 * Outputs: Promise-based task event persistence operations.
 * Notes:
 * - This file defines a contract, not an implementation.
 * - Task events are append-only and should not be updated in place.
 * - Keep storage-specific details out of this file.
 * ============================================================
 */

import type { TaskEvent } from "../../domain/taskEvents/taskEvent.types";

export interface TaskEventRepository {
  getAll(): Promise<TaskEvent[]>;
  getByTaskId(taskId: string): Promise<TaskEvent[]>;
  append(event: TaskEvent): Promise<void>;
}
