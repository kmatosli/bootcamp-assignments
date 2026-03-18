/**
 * ============================================================
 * File: task.selectors.ts
 * Purpose: Provides reusable derived selectors for Task data.
 * Context: Selectors centralize filtering and derived task views
 * so components and application services do not duplicate logic.
 * Inputs: Arrays of Task entities and selector parameters.
 * Outputs: Filtered task lists and derived promotion evidence.
 * Notes:
 * - Keep storage logic out of this file.
 * - Keep React/UI rendering logic out of this file.
 * - Keep report formatting logic out of this file.
 * ============================================================
 */

import type { PromotionEvidenceItem } from "../reports/report.types";
import type { Task } from "../tasks/task.types";

export function selectCompletedTasks(tasks: Task[]): Task[] {
  return tasks.filter((task) => task.status === "completed");
}

export function selectInProgressTasks(tasks: Task[]): Task[] {
  return tasks.filter((task) => task.status === "in_progress");
}

export function selectBlockedTasks(tasks: Task[]): Task[] {
  return tasks.filter((task) => task.status === "blocked");
}

export function selectTasksByCategory(
  tasks: Task[],
  category: Task["category"],
): Task[] {
  return tasks.filter((task) => task.category === category);
}

export function selectFlagshipTasks(tasks: Task[]): Task[] {
  return tasks.filter((task) => {
    const hasProblem = task.impactFields.problem.trim().length > 0;
    const hasAction = task.impactFields.action.trim().length > 0;
    const hasImpact = task.impactFields.impact.trim().length > 0;
    const hasEvidence = task.impactFields.evidence.length > 0;
    const hasMetrics = task.impactFields.metrics.length > 0;

    return hasProblem && hasAction && hasImpact && (hasEvidence || hasMetrics);
  });
}

export function selectPromotionEvidence(
  tasks: Task[],
): PromotionEvidenceItem[] {
  return selectFlagshipTasks(tasks).map((task) => ({
    taskId: task.id,
    title: task.title,
    category: task.category,
    problem: task.impactFields.problem,
    action: task.impactFields.action,
    impact: task.impactFields.impact,
    metrics: task.impactFields.metrics.map(
      (metric) => `${metric.label}: ${metric.value}`,
    ),
    evidenceCount: task.impactFields.evidence.length,
    completedAt: task.timestamps.completedAt ?? null,
  }));
}
