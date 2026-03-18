/**
 * ============================================================
 * File: task.validation.ts
 * Purpose: Provides domain validation rules for Task entities.
 * Context: Validation belongs in the domain layer so it can be
 * reused across forms, actions, repositories, and future APIs.
 * Inputs: Full Task objects and partial Task updates.
 * Outputs: Validation results describing whether the task data
 * is valid and, if not, which rules failed.
 * Notes:
 * - Keep UI-specific validation messaging out of this file.
 * - Keep storage logic out of this file.
 * - Keep React component logic out of this file.
 * ============================================================
 */

import type {
  Task,
  TaskCategory,
  TaskPriority,
  TaskStatus,
} from "./task.types";

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

const VALID_STATUSES: TaskStatus[] = [
  "draft",
  "planned",
  "in_progress",
  "blocked",
  "completed",
  "archived",
];

const VALID_PRIORITIES: TaskPriority[] = ["low", "medium", "high", "critical"];

const VALID_CATEGORIES: TaskCategory[] = [
  "delivery",
  "analysis",
  "leadership",
  "stakeholder",
  "process",
  "learning",
  "career",
  "other",
];

export function validateTask(task: Task): ValidationResult {
  const errors: string[] = [];

  if (!task.id.trim()) {
    errors.push("Task id is required.");
  }

  if (!task.title.trim()) {
    errors.push("Task title is required.");
  }

  if (!VALID_STATUSES.includes(task.status)) {
    errors.push("Task status is invalid.");
  }

  if (!VALID_PRIORITIES.includes(task.priority)) {
    errors.push("Task priority is invalid.");
  }

  if (!VALID_CATEGORIES.includes(task.category)) {
    errors.push("Task category is invalid.");
  }

  if (!task.timestamps.createdAt) {
    errors.push("Created timestamp is required.");
  }

  if (!task.timestamps.updatedAt) {
    errors.push("Updated timestamp is required.");
  }

  if (!task.impactFields.problem.trim()) {
    errors.push("Problem statement is required.");
  }

  if (!task.impactFields.action.trim()) {
    errors.push("Action statement is required.");
  }

  if (!task.impactFields.impact.trim()) {
    errors.push("Impact statement is required.");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

export function validateTaskPartial(task: Partial<Task>): ValidationResult {
  const errors: string[] = [];

  if (task.title !== undefined && !task.title.trim()) {
    errors.push("Task title cannot be empty.");
  }

  if (task.status !== undefined && !VALID_STATUSES.includes(task.status)) {
    errors.push("Task status is invalid.");
  }

  if (
    task.priority !== undefined &&
    !VALID_PRIORITIES.includes(task.priority)
  ) {
    errors.push("Task priority is invalid.");
  }

  if (
    task.category !== undefined &&
    !VALID_CATEGORIES.includes(task.category)
  ) {
    errors.push("Task category is invalid.");
  }

  if (
    task.impactFields?.problem !== undefined &&
    !task.impactFields.problem.trim()
  ) {
    errors.push("Problem statement cannot be empty.");
  }

  if (
    task.impactFields?.action !== undefined &&
    !task.impactFields.action.trim()
  ) {
    errors.push("Action statement cannot be empty.");
  }

  if (
    task.impactFields?.impact !== undefined &&
    !task.impactFields.impact.trim()
  ) {
    errors.push("Impact statement cannot be empty.");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
