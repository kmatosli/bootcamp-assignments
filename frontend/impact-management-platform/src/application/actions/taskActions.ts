/**
 * ============================================================
 * File: taskActions.ts
 * Purpose: Provides application-level task actions that
 * coordinate validation, canonical task persistence, and
 * append-only task event logging.
 * Context: This layer orchestrates task workflows without placing
 * business validation in React components or storage details in
 * the UI.
 * Inputs: Repository dependencies, task identifiers, and task
 * creation or update payloads.
 * Outputs: Created, updated, retrieved, or deleted task results.
 * Notes:
 * - Keep UI logic out of this file.
 * - Keep storage implementation details out of this file.
 * - Use domain validators to enforce correctness before saving.
 * ============================================================
 */

import type { Task } from "../../domain/tasks/task.types";
import type { TaskEvent } from "../../domain/taskEvents/taskEvent.types";
import {
  validateTask,
  validateTaskPartial,
} from "../../domain/tasks/task.validators";
import type { TaskRepository } from "../../infrastructure/repositories/TaskRepository";
import type { TaskEventRepository } from "../../infrastructure/repositories/TaskEventRepository";

export interface CreateTaskInput {
  title: string;
  description: string;
  status: Task["status"];
  priority: Task["priority"];
  category: Task["category"];
  tags?: string[];
  problem: string;
  action: string;
  impact: string;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  status?: Task["status"];
  priority?: Task["priority"];
  category?: Task["category"];
  tags?: string[];
  impactFields?: Partial<Task["impactFields"]>;
  workflow?: Partial<Task["workflow"]>;
}

function createId(prefix: string): string {
  return `${prefix}_${crypto.randomUUID()}`;
}

function createTaskEvent(
  taskId: string,
  type: TaskEvent["type"],
  summary: string,
  metadata?: Record<string, unknown>,
): TaskEvent {
  return {
    id: createId("evt"),
    taskId,
    type,
    occurredAt: new Date().toISOString(),
    actor: "user",
    summary,
    metadata,
  };
}

export async function createTask(
  taskRepository: TaskRepository,
  taskEventRepository: TaskEventRepository,
  input: CreateTaskInput,
): Promise<Task> {
  const now = new Date().toISOString();

  const task: Task = {
    id: createId("task"),
    title: input.title,
    description: input.description,
    status: input.status,
    priority: input.priority,
    category: input.category,
    tags: input.tags ?? [],
    timestamps: {
      createdAt: now,
      updatedAt: now,
      startedAt: input.status === "in_progress" ? now : null,
      completedAt: input.status === "completed" ? now : null,
    },
    impactFields: {
      problem: input.problem,
      action: input.action,
      impact: input.impact,
      metrics: [],
      evidence: [],
    },
    workflow: {
      externalCalendarEventId: null,
      externalTaskId: null,
      externalProvider: null,
      syncStatus: "not_synced",
    },
  };

  const validationResult = validateTask(task);

  if (!validationResult.isValid) {
    throw new Error(validationResult.errors.join(" "));
  }

  await taskRepository.create(task);

  await taskEventRepository.append(
    createTaskEvent(task.id, "task_created", `Task created: ${task.title}`),
  );

  return task;
}

export async function updateTask(
  taskRepository: TaskRepository,
  taskEventRepository: TaskEventRepository,
  taskId: string,
  updates: UpdateTaskInput,
): Promise<Task> {
  const partialCandidate: Partial<Task> = {
    title: updates.title,
    description: updates.description,
    status: updates.status,
    priority: updates.priority,
    category: updates.category,
    tags: updates.tags,
    impactFields: updates.impactFields
      ? {
          problem: updates.impactFields.problem ?? "",
          action: updates.impactFields.action ?? "",
          impact: updates.impactFields.impact ?? "",
          metrics: updates.impactFields.metrics ?? [],
          evidence: updates.impactFields.evidence ?? [],
        }
      : undefined,
    workflow: updates.workflow,
  };

  const partialValidationResult = validateTaskPartial(partialCandidate);

  if (!partialValidationResult.isValid) {
    throw new Error(partialValidationResult.errors.join(" "));
  }

  const existingTask = await taskRepository.getById(taskId);

  if (!existingTask) {
    throw new Error("Task not found.");
  }

  const nextStatus = updates.status ?? existingTask.status;
  const now = new Date().toISOString();

  const completedAt =
    nextStatus === "completed"
      ? (existingTask.timestamps.completedAt ?? now)
      : null;

  const updatedTask: Task = {
    ...existingTask,
    title: updates.title ?? existingTask.title,
    description: updates.description ?? existingTask.description,
    status: nextStatus,
    priority: updates.priority ?? existingTask.priority,
    category: updates.category ?? existingTask.category,
    tags: updates.tags ?? existingTask.tags,
    timestamps: {
      ...existingTask.timestamps,
      updatedAt: now,
      startedAt:
        nextStatus === "in_progress" && !existingTask.timestamps.startedAt
          ? now
          : existingTask.timestamps.startedAt,
      completedAt,
    },
    impactFields: {
      ...existingTask.impactFields,
      ...updates.impactFields,
      metrics:
        updates.impactFields?.metrics ?? existingTask.impactFields.metrics,
      evidence:
        updates.impactFields?.evidence ?? existingTask.impactFields.evidence,
    },
    workflow: {
      ...existingTask.workflow,
      ...updates.workflow,
    },
  };

  const fullValidationResult = validateTask(updatedTask);

  if (!fullValidationResult.isValid) {
    throw new Error(fullValidationResult.errors.join(" "));
  }

  await taskRepository.update(updatedTask);

  await taskEventRepository.append(
    createTaskEvent(
      taskId,
      "task_updated",
      `Task updated: ${updatedTask.title}`,
      {
        updatedFields: Object.keys(updates),
      },
    ),
  );

  if (existingTask.status !== updatedTask.status) {
    const eventType: TaskEvent["type"] =
      updatedTask.status === "completed"
        ? "task_completed"
        : updatedTask.status === "archived"
          ? "task_archived"
          : "task_status_changed";

    await taskEventRepository.append(
      createTaskEvent(
        taskId,
        eventType,
        `Task status changed from ${existingTask.status} to ${updatedTask.status}`,
        {
          previousStatus: existingTask.status,
          newStatus: updatedTask.status,
        },
      ),
    );
  }

  return updatedTask;
}

export async function deleteTask(
  taskRepository: TaskRepository,
  taskEventRepository: TaskEventRepository,
  taskId: string,
): Promise<void> {
  const existingTask = await taskRepository.getById(taskId);

  if (!existingTask) {
    throw new Error("Task not found.");
  }

  await taskEventRepository.append(
    createTaskEvent(
      taskId,
      "task_archived",
      `Task removed from active list: ${existingTask.title}`,
      {
        deletedTaskId: taskId,
        deletedAt: new Date().toISOString(),
      },
    ),
  );

  await taskRepository.delete(taskId);
}

export async function getTaskById(
  taskRepository: TaskRepository,
  taskId: string,
): Promise<Task | null> {
  return taskRepository.getById(taskId);
}

export async function getTaskEventsByTaskId(
  taskEventRepository: TaskEventRepository,
  taskId: string,
): Promise<TaskEvent[]> {
  const events = await taskEventRepository.getByTaskId(taskId);

  return [...events].sort((left, right) =>
    right.occurredAt.localeCompare(left.occurredAt),
  );
}
