/**
 * ============================================================
 * File: TaskContext.tsx
 * Purpose: Provides typed global task state and task workflows
 * to the presentation layer using React Context.
 * Context: This provider owns task loading, task CRUD actions,
 * task event retrieval, and user-visible loading/error state.
 * Inputs: React children.
 * Outputs: Context value with typed state and actions.
 * Notes:
 * - Keep domain validation in the domain layer.
 * - Keep persistence behind repository abstractions.
 * - Keep React components free of repository orchestration.
 * ============================================================
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { Task } from "../../domain/tasks/task.types";
import type { TaskEvent } from "../../domain/taskEvents/taskEvent.types";
import type {
  CreateTaskInput,
  UpdateTaskInput,
} from "../../application/actions/taskActions";
import {
  createTask as createTaskAction,
  deleteTask as deleteTaskAction,
  getTaskById as getTaskByIdAction,
  getTaskEventsByTaskId as getTaskEventsByTaskIdAction,
  updateTask as updateTaskAction,
} from "../../application/actions/taskActions";
import { LocalTaskRepository } from "../../infrastructure/repositories/local/LocalTaskRepository";
import { LocalTaskEventRepository } from "../../infrastructure/repositories/local/LocalTaskEventRepository";

interface TaskContextValue {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  reloadTasks: () => Promise<void>;
  createTask: (input: CreateTaskInput) => Promise<Task>;
  updateTask: (taskId: string, updates: UpdateTaskInput) => Promise<Task>;
  deleteTask: (taskId: string) => Promise<void>;
  getTaskById: (taskId: string) => Promise<Task | null>;
  getTaskEventsByTaskId: (taskId: string) => Promise<TaskEvent[]>;
  clearError: () => void;
}

const TaskContext = createContext<TaskContextValue | undefined>(undefined);

interface TaskProviderProps {
  children: ReactNode;
}

export function TaskProvider({ children }: TaskProviderProps) {
  const taskRepository = useMemo(() => new LocalTaskRepository(), []);
  const taskEventRepository = useMemo(() => new LocalTaskEventRepository(), []);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const reloadTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const storedTasks = await taskRepository.getAll();
      setTasks(storedTasks);
    } catch (loadError) {
      setError(
        loadError instanceof Error
          ? loadError.message
          : "Failed to load tasks.",
      );
    } finally {
      setIsLoading(false);
    }
  }, [taskRepository]);

  useEffect(() => {
    void reloadTasks();
  }, [reloadTasks]);

  const handleCreateTask = useCallback(
    async (input: CreateTaskInput): Promise<Task> => {
      try {
        setError(null);

        const createdTask = await createTaskAction(
          taskRepository,
          taskEventRepository,
          input,
        );

        setTasks((current) => [createdTask, ...current]);

        return createdTask;
      } catch (createError) {
        const message =
          createError instanceof Error
            ? createError.message
            : "Failed to create task.";

        setError(message);
        throw new Error(message);
      }
    },
    [taskRepository, taskEventRepository],
  );

  const handleUpdateTask = useCallback(
    async (taskId: string, updates: UpdateTaskInput): Promise<Task> => {
      try {
        setError(null);

        const updatedTask = await updateTaskAction(
          taskRepository,
          taskEventRepository,
          taskId,
          updates,
        );

        setTasks((current) =>
          current.map((task) =>
            task.id === updatedTask.id ? updatedTask : task,
          ),
        );

        return updatedTask;
      } catch (updateError) {
        const message =
          updateError instanceof Error
            ? updateError.message
            : "Failed to update task.";

        setError(message);
        throw new Error(message);
      }
    },
    [taskRepository, taskEventRepository],
  );

  const handleDeleteTask = useCallback(
    async (taskId: string): Promise<void> => {
      try {
        setError(null);

        await deleteTaskAction(taskRepository, taskEventRepository, taskId);

        setTasks((current) => current.filter((task) => task.id !== taskId));
      } catch (deleteError) {
        const message =
          deleteError instanceof Error
            ? deleteError.message
            : "Failed to delete task.";

        setError(message);
        throw new Error(message);
      }
    },
    [taskRepository, taskEventRepository],
  );

  const handleGetTaskById = useCallback(
    async (taskId: string): Promise<Task | null> => {
      try {
        setError(null);
        return await getTaskByIdAction(taskRepository, taskId);
      } catch (getError) {
        const message =
          getError instanceof Error ? getError.message : "Failed to load task.";

        setError(message);
        throw new Error(message);
      }
    },
    [taskRepository],
  );

  const handleGetTaskEventsByTaskId = useCallback(
    async (taskId: string): Promise<TaskEvent[]> => {
      try {
        setError(null);
        return await getTaskEventsByTaskIdAction(taskEventRepository, taskId);
      } catch (getError) {
        const message =
          getError instanceof Error
            ? getError.message
            : "Failed to load task history.";

        setError(message);
        throw new Error(message);
      }
    },
    [taskEventRepository],
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value = useMemo<TaskContextValue>(
    () => ({
      tasks,
      isLoading,
      error,
      reloadTasks,
      createTask: handleCreateTask,
      updateTask: handleUpdateTask,
      deleteTask: handleDeleteTask,
      getTaskById: handleGetTaskById,
      getTaskEventsByTaskId: handleGetTaskEventsByTaskId,
      clearError,
    }),
    [
      tasks,
      isLoading,
      error,
      reloadTasks,
      handleCreateTask,
      handleUpdateTask,
      handleDeleteTask,
      handleGetTaskById,
      handleGetTaskEventsByTaskId,
      clearError,
    ],
  );

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
}

export function useTaskContext(): TaskContextValue {
  const context = useContext(TaskContext);

  if (!context) {
    throw new Error("useTaskContext must be used within a TaskProvider.");
  }

  return context;
}
