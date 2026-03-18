/**
 * ============================================================
 * File: report.types.ts
 * Purpose: Defines derived report contracts for the Impact
 * Management Platform.
 * Context: Reports are generated outputs derived from canonical
 * task data and task event history. Reports are never the source
 * of truth and are never manually authored.
 * Inputs: N/A
 * Outputs: TypeScript interfaces used by report builders,
 * repositories, and presentation components.
 * Notes:
 * - Keep calculation logic out of this file.
 * - Keep formatting logic out of this file.
 * - Keep UI rendering logic out of this file.
 * ============================================================
 */

import type { Task } from "../tasks/task.types";

export interface PromotionEvidenceItem {
  taskId: string;
  title: string;
  category: string;
  problem: string;
  action: string;
  impact: string;
  metrics: string[];
  evidenceCount: number;
  completedAt?: string | null;
}

export interface ImpactSummaryCounts {
  totalTasks: number;
  completedTasks: number;
  inProgressTasks: number;
  blockedTasks: number;
  flagshipTasks: number;
}

export interface ImpactReport {
  generatedAt: string;
  counts: ImpactSummaryCounts;
  promotionEvidence: PromotionEvidenceItem[];
  completedTasks: Task[];
  flagshipTasks: Task[];
}
