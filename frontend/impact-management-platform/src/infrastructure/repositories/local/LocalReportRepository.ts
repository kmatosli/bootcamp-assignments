/**
 * ============================================================
 * File: LocalReportRepository.ts
 * Purpose: Implements the ReportRepository contract using browser
 * localStorage for derived impact report persistence.
 * Context: This is the first concrete storage implementation for
 * generated reports in the Impact Management Platform.
 * Inputs: Impact report objects.
 * Outputs: Promise-based report persistence operations backed by
 * localStorage.
 * Notes:
 * - This implementation is for local development and MVP usage.
 * - Reports are derived artifacts, not canonical source data.
 * - Application logic should depend on ReportRepository, not this class directly.
 * ============================================================
 */

import type { ImpactReport } from "../../../domain/reports/report.types";
import type { ReportRepository } from "../ReportRepository";

const REPORT_STORAGE_KEY = "impact-platform.latest-report";

export class LocalReportRepository implements ReportRepository {
  async getLatest(): Promise<ImpactReport | null> {
    const raw = localStorage.getItem(REPORT_STORAGE_KEY);

    if (!raw) {
      return null;
    }

    return JSON.parse(raw) as ImpactReport;
  }

  async save(report: ImpactReport): Promise<void> {
    localStorage.setItem(REPORT_STORAGE_KEY, JSON.stringify(report));
  }
}
