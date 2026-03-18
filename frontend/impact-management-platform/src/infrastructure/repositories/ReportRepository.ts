/**
 * ============================================================
 * File: ReportRepository.ts
 * Purpose: Defines the repository contract for storing and
 * retrieving derived impact reports.
 * Context: Reports are generated artifacts derived from canonical
 * task data and task event history. They are not the source of
 * truth and should never replace task data.
 * Inputs: Impact report objects.
 * Outputs: Promise-based report persistence operations.
 * Notes:
 * - This file defines a contract, not an implementation.
 * - Reports are derived outputs, not manually authored records.
 * - Keep storage-specific details out of this file.
 * ============================================================
 */

import type { ImpactReport } from "../../domain/reports/report.types";

export interface ReportRepository {
  getLatest(): Promise<ImpactReport | null>;
  save(report: ImpactReport): Promise<void>;
}
