/**
 * ============================================================
 * File: App.tsx
 * Purpose: Top-level routed application shell for the Impact
 * Management Platform.
 * Context: Composes route-level pages and shared providers.
 * Inputs: Route navigation and page interactions.
 * Outputs: Routed application UI.
 * Notes:
 * - Keep domain logic out of this file.
 * - Keep repository orchestration inside context/providers.
 * - BrowserRouter is owned by main.tsx.
 * ============================================================
 */

import { Navigate, Route, Routes } from "react-router-dom";
import DashboardPage from "./presentation/pages/DashboardPage";
import TaskDetailsPage from "./presentation/pages/TaskDetailsPage";
import TaskEditPage from "./presentation/pages/TaskEditPage";
import { TaskProvider } from "./presentation/context/TaskContext";

function App() {
  return (
    <TaskProvider>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/tasks/:taskId" element={<TaskDetailsPage />} />
        <Route path="/tasks/:taskId/edit" element={<TaskEditPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </TaskProvider>
  );
}

export default App;
