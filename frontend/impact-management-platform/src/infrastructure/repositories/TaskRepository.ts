/**
 * ============================================================
 * File: TaskRepository.ts
 * Purpose: Defines the repository contract for canonical Task
 * storage and retrieval.
 * Context: Application logic should depend on repository
 * interfaces rather than concrete storage implementations such
 * as localStorage, APIs, or databases.
 * Inputs: Task entities and task identifiers.
 * Outputs: Promise-based task persistence operations.
 * Notes:
 * - This file defines a contract, not an implementation.
 * - Keep storage-specific details out of this file.
 * - Tasks remain the canonical source of truth.
 * ============================================================
 */

import type { Task } from "../../domain/tasks/task.types";

export interface TaskRepository {
  getAll(): Promise<Task[]>;
  getById(id: string): Promise<Task | null>;
  create(task: Task): Promise<void>;
  update(task: Task): Promise<void>;
  delete(id: string): Promise<void>;
}
