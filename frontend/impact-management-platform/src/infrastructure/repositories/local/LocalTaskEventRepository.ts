/**
 * ============================================================
 * File: LocalTaskEventRepository.ts
 * Purpose: Implements the TaskEventRepository contract using
 * browser localStorage for append-only task event persistence.
 * Context: This is the first concrete storage implementation for
 * task event history in the Impact Management Platform.
 * Inputs: Task event entities and task identifiers.
 * Outputs: Promise-based task event persistence operations backed
 * by localStorage.
 * Notes:
 * - This implementation is for local development and MVP usage.
 * - Task events are append-only historical records.
 * - Application logic should depend on TaskEventRepository, not this class directly.
 * ============================================================
 */

import type { TaskEvent } from "../../../domain/taskEvents/taskEvent.types";
import type { TaskEventRepository } from "../TaskEventRepository";

const TASK_EVENT_STORAGE_KEY = "impact-platform.task-events";

export class LocalTaskEventRepository implements TaskEventRepository {
  async getAll(): Promise<TaskEvent[]> {
    const raw = localStorage.getItem(TASK_EVENT_STORAGE_KEY);

    if (!raw) {
      return [];
    }

    return JSON.parse(raw) as TaskEvent[];
  }

  async getByTaskId(taskId: string): Promise<TaskEvent[]> {
    const events = await this.getAll();

    return events.filter((event) => event.taskId === taskId);
  }

  async append(event: TaskEvent): Promise<void> {
    const events = await this.getAll();

    events.push(event);

    localStorage.setItem(TASK_EVENT_STORAGE_KEY, JSON.stringify(events));
  }
}
