/**
 * ============================================================
 * File: ReportSummary.tsx
 * Purpose: Presentation component for displaying the latest
 * generated impact report and its promotion evidence.
 * Context: This component belongs to the presentation layer and
 * should only render report data passed in from parent state.
 * Inputs: ImpactReport object or null.
 * Outputs: Rendered report summary UI.
 * Notes:
 * - Keep report calculation logic out of this file.
 * - Keep repository/storage logic out of this file.
 * - Keep application orchestration out of this file.
 * ============================================================
 */

import type { ImpactReport } from "../../domain/reports/report.types";

interface ReportSummaryProps {
  report: ImpactReport | null;
}

export default function ReportSummary({ report }: ReportSummaryProps) {
  return (
    <section style={styles.container}>
      <h2 style={styles.sectionTitle}>Latest Impact Report</h2>

      {!report ? (
        <p style={styles.metaText}>
          No report generated yet. Create tasks, then generate a report.
        </p>
      ) : (
        <>
          <p style={styles.metaText}>
            Generated at: {new Date(report.generatedAt).toLocaleString()}
          </p>

          <div style={styles.summaryGrid}>
            <div style={styles.summaryCard}>
              <span style={styles.summaryLabel}>Total</span>
              <strong style={styles.summaryValue}>
                {report.counts.totalTasks}
              </strong>
            </div>

            <div style={styles.summaryCard}>
              <span style={styles.summaryLabel}>Completed</span>
              <strong style={styles.summaryValue}>
                {report.counts.completedTasks}
              </strong>
            </div>

            <div style={styles.summaryCard}>
              <span style={styles.summaryLabel}>In Progress</span>
              <strong style={styles.summaryValue}>
                {report.counts.inProgressTasks}
              </strong>
            </div>

            <div style={styles.summaryCard}>
              <span style={styles.summaryLabel}>Blocked</span>
              <strong style={styles.summaryValue}>
                {report.counts.blockedTasks}
              </strong>
            </div>

            <div style={styles.summaryCard}>
              <span style={styles.summaryLabel}>Flagship</span>
              <strong style={styles.summaryValue}>
                {report.counts.flagshipTasks}
              </strong>
            </div>
          </div>

          <h3 style={styles.subsectionTitle}>Promotion Evidence</h3>

          {report.promotionEvidence.length === 0 ? (
            <p style={styles.metaText}>No promotion evidence available yet.</p>
          ) : (
            <ul style={styles.evidenceList}>
              {report.promotionEvidence.map((item) => (
                <li key={item.taskId} style={styles.evidenceCard}>
                  <strong style={styles.evidenceTitle}>{item.title}</strong>

                  <p style={styles.metaText}>
                    Category: {formatLabel(item.category)}
                  </p>

                  <p style={styles.evidenceText}>
                    <strong>Problem:</strong> {item.problem}
                  </p>

                  <p style={styles.evidenceText}>
                    <strong>Action:</strong> {item.action}
                  </p>

                  <p style={styles.evidenceText}>
                    <strong>Impact:</strong> {item.impact}
                  </p>

                  <p style={styles.metaText}>
                    Metrics: {item.metrics.length} | Evidence Count:{" "}
                    {item.evidenceCount}
                  </p>

                  {item.metrics.length > 0 && (
                    <ul style={styles.metricList}>
                      {item.metrics.map((metric, index) => (
                        <li
                          key={`${item.taskId}-metric-${index}`}
                          style={styles.metricItem}
                        >
                          {metric}
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </section>
  );
}

function formatLabel(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    border: "1px solid #e5e7eb",
    borderRadius: "12px",
    padding: "20px",
    backgroundColor: "#ffffff",
  },
  sectionTitle: {
    marginTop: 0,
    marginBottom: "12px",
    fontSize: "1.25rem",
    color: "#111827",
  },
  subsectionTitle: {
    marginTop: "20px",
    marginBottom: "12px",
    fontSize: "1rem",
    color: "#111827",
  },
  summaryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "12px",
    marginBottom: "20px",
  },
  summaryCard: {
    padding: "16px",
    borderRadius: "10px",
    border: "1px solid #e5e7eb",
    backgroundColor: "#f9fafb",
  },
  summaryLabel: {
    display: "block",
    fontSize: "0.85rem",
    color: "#6b7280",
    marginBottom: "6px",
  },
  summaryValue: {
    fontSize: "1.25rem",
    color: "#111827",
  },
  evidenceList: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  evidenceCard: {
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "14px",
    backgroundColor: "#f9fafb",
  },
  evidenceTitle: {
    display: "block",
    marginBottom: "6px",
    color: "#111827",
  },
  evidenceText: {
    margin: "6px 0",
    color: "#374151",
  },
  metaText: {
    margin: "6px 0",
    fontSize: "0.9rem",
    color: "#6b7280",
  },
  metricList: {
    marginTop: "10px",
    marginBottom: 0,
    paddingLeft: "18px",
    color: "#374151",
  },
  metricItem: {
    marginBottom: "4px",
  },
};
