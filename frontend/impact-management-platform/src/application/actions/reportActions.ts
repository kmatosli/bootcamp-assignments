/**
 * ============================================================
 * File: reportActions.ts
 * Purpose: Provides application-level report generation actions
 * that derive impact reports from canonical task data.
 * Context: This layer orchestrates report generation without
 * placing calculation logic in React components or storage
 * implementation details in the UI.
 * Inputs: Repository dependencies for tasks and reports.
 * Outputs: Generated and persisted ImpactReport objects.
 * Notes:
 * - Keep UI rendering logic out of this file.
 * - Keep storage implementation details out of this file.
 * - Reports are derived artifacts, not source-of-truth records.
 * ============================================================
 */

import type { ImpactReport } from "../../domain/reports/report.types";
import {
  selectBlockedTasks,
  selectCompletedTasks,
  selectFlagshipTasks,
  selectInProgressTasks,
  selectPromotionEvidence,
} from "../../domain/selectors/task.selectors";
import type { TaskRepository } from "../../infrastructure/repositories/TaskRepository";
import type { ReportRepository } from "../../infrastructure/repositories/ReportRepository";

export async function generateImpactReport(
  taskRepository: TaskRepository,
  reportRepository: ReportRepository,
): Promise<ImpactReport> {
  const tasks = await taskRepository.getAll();

  const completedTasks = selectCompletedTasks(tasks);
  const inProgressTasks = selectInProgressTasks(tasks);
  const blockedTasks = selectBlockedTasks(tasks);
  const flagshipTasks = selectFlagshipTasks(tasks);
  const promotionEvidence = selectPromotionEvidence(tasks);

  const report: ImpactReport = {
    generatedAt: new Date().toISOString(),
    counts: {
      totalTasks: tasks.length,
      completedTasks: completedTasks.length,
      inProgressTasks: inProgressTasks.length,
      blockedTasks: blockedTasks.length,
      flagshipTasks: flagshipTasks.length,
    },
    promotionEvidence,
    completedTasks,
    flagshipTasks,
  };

  await reportRepository.save(report);

  return report;
}
