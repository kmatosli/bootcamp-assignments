/**
 * ============================================================
 * File: LocalTaskRepository.ts
 * Purpose: Implements the TaskRepository contract using browser
 * localStorage for task persistence.
 * Context: This is the first concrete storage implementation for
 * the Impact Management Platform. It allows the application to
 * save and retrieve canonical task data without coupling the rest
 * of the app directly to localStorage.
 * Inputs: Task entities and task identifiers.
 * Outputs: Promise-based task persistence operations backed by
 * localStorage.
 * Notes:
 * - This implementation is for local development and MVP usage.
 * - Application logic should depend on TaskRepository, not this class directly.
 * - Tasks remain the canonical source of truth.
 * ============================================================
 */

import type { Task } from "../../../domain/tasks/task.types";
import type { TaskRepository } from "../TaskRepository";

const TASK_STORAGE_KEY = "impact-platform.tasks";

export class LocalTaskRepository implements TaskRepository {
  async getAll(): Promise<Task[]> {
    const raw = localStorage.getItem(TASK_STORAGE_KEY);

    if (!raw) {
      return [];
    }

    return JSON.parse(raw) as Task[];
  }

  async getById(id: string): Promise<Task | null> {
    const tasks = await this.getAll();

    const task = tasks.find((existingTask) => existingTask.id === id);

    return task ?? null;
  }

  async create(task: Task): Promise<void> {
    const tasks = await this.getAll();

    tasks.push(task);

    localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
  }

  async update(task: Task): Promise<void> {
    const tasks = await this.getAll();

    const updatedTasks = tasks.map((existingTask) =>
      existingTask.id === task.id ? task : existingTask,
    );

    localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(updatedTasks));
  }

  async delete(id: string): Promise<void> {
    const tasks = await this.getAll();

    const filteredTasks = tasks.filter((task) => task.id !== id);

    localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(filteredTasks));
  }
}
