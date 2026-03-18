/**
 * ============================================================
 * File: App.tsx
 * Purpose: Top-level application composition root for the Impact
 * Management Platform.
 * Context: Wires together repository implementations,
 * application-layer actions, and the main dashboard page.
 * Inputs: User interactions routed through page/component props.
 * Outputs: Rendered application UI.
 * Notes:
 * - Keep domain logic out of this file.
 * - Keep storage implementation details limited to dependency setup.
 * - Prefer delegating workflows to application actions.
 * ============================================================
 */

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";
import type { Task } from "./domain/tasks/task.types";
import type { ImpactReport } from "./domain/reports/report.types";
import type { CreateTaskInput } from "./application/actions/taskActions";
import { createTask } from "./application/actions/taskActions";
import { generateImpactReport } from "./application/actions/reportActions";
import { selectCompletedTasks } from "./domain/selectors/task.selectors";
import { LocalTaskRepository } from "./infrastructure/repositories/local/LocalTaskRepository";
import { LocalTaskEventRepository } from "./infrastructure/repositories/local/LocalTaskEventRepository";
import { LocalReportRepository } from "./infrastructure/repositories/local/LocalReportRepository";
import DashboardPage from "./presentation/pages/DashboardPage";

function App() {
  const taskRepository = useMemo(() => new LocalTaskRepository(), []);
  const taskEventRepository = useMemo(() => new LocalTaskEventRepository(), []);
  const reportRepository = useMemo(() => new LocalReportRepository(), []);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [report, setReport] = useState<ImpactReport | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isGeneratingReport, setIsGeneratingReport] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setIsLoading(true);
        setError(null);

        const [storedTasks, latestReport] = await Promise.all([
          taskRepository.getAll(),
          reportRepository.getLatest(),
        ]);

        setTasks(storedTasks);
        setReport(latestReport);
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Failed to load application data.",
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadInitialData();
  }, [taskRepository, reportRepository]);

  async function handleCreateTask(input: CreateTaskInput): Promise<void> {
    try {
      setError(null);

      const createdTask = await createTask(
        taskRepository,
        taskEventRepository,
        input,
      );

      setTasks((currentTasks) => [createdTask, ...currentTasks]);
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Failed to create task.",
      );
      throw createError;
    }
  }

  async function handleGenerateReport(): Promise<void> {
    try {
      setIsGeneratingReport(true);
      setError(null);

      const generatedReport = await generateImpactReport(
        taskRepository,
        reportRepository,
      );

      setReport(generatedReport);
    } catch (reportError) {
      setError(
        reportError instanceof Error
          ? reportError.message
          : "Failed to generate report.",
      );
    } finally {
      setIsGeneratingReport(false);
    }
  }

  const completedTaskCount = selectCompletedTasks(tasks).length;

  if (isLoading) {
    return (
      <main style={styles.loadingShell}>
        <h1 style={styles.loadingTitle}>Impact Management Platform</h1>
        <p style={styles.loadingText}>Loading application data...</p>
      </main>
    );
  }

  return (
    <DashboardPage
      tasks={tasks}
      report={report}
      totalTasks={tasks.length}
      completedTaskCount={completedTaskCount}
      isGeneratingReport={isGeneratingReport}
      error={error}
      onCreateTask={handleCreateTask}
      onGenerateReport={handleGenerateReport}
    />
  );
}

const styles: Record<string, CSSProperties> = {
  loadingShell: {
    maxWidth: "1280px",
    margin: "0 auto",
    padding: "32px",
    fontFamily: "Arial, sans-serif",
    color: "#111827",
  },
  loadingTitle: {
    margin: 0,
    fontSize: "2rem",
  },
  loadingText: {
    marginTop: "12px",
    color: "#6b7280",
  },
};

export default App;
