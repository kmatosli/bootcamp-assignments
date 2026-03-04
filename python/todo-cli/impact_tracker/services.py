from __future__ import annotations

from typing import Any, Dict, List, Optional

from impact_tracker.models import build_event


# =============================================================================
# Section: Service Layer (State Changes + Event Emission)
# =============================================================================

def next_task_id(tasks: List[Dict[str, Any]]) -> int:
    """
    Allocate next task id (monotonic within this run).
    """
    return 1 if not tasks else max(t["id"] for t in tasks) + 1


def next_event_id(events: List[Dict[str, Any]]) -> int:
    """
    Allocate next event id (monotonic within this run).
    """
    return 1 if not events else max(e["event_id"] for e in events) + 1


def emit_event(
    events: List[Dict[str, Any]],
    event_type: str,
    task_id: Optional[int],
    payload: Dict[str, Any],
) -> None:
    """
    Append event to append-only event log.
    """
    eid = next_event_id(events)
    events.append(build_event(eid, event_type, task_id, payload))


def add_task(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]], task: Dict[str, Any]) -> None:
    """
    Add task to state and emit TASK_ADDED.
    """
    tasks.append(task)
    emit_event(events, "TASK_ADDED", task["id"], {"task": task})


def delete_task(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]], task_id: int) -> None:
    """
    Delete task from state and emit TASK_DELETED.
    """
    before = len(tasks)
    removed: Optional[Dict[str, Any]] = None

    for i, t in enumerate(list(tasks)):
        if t["id"] == task_id:
            removed = t
            del tasks[i]
            break

    after = len(tasks)
    emit_event(
        events,
        "TASK_DELETED",
        task_id,
        {"removed": removed, "count_before": before, "count_after": after},
    )


def complete_task(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]], task_id: int) -> None:
    """
    Mark a task completed and emit TASK_COMPLETED.

    Raises
    ------
    ValueError
        If task not found or already completed.
    """
    for t in tasks:
        if t["id"] == task_id:
            if t.get("status") == "completed":
                raise ValueError("Task is already completed.")
            t["status"] = "completed"
            # timestamp comes from event but store in task for convenience
            from impact_tracker.utils import now_iso
            t["completed_at"] = now_iso()
            emit_event(events, "TASK_COMPLETED", task_id, {"completed_at": t["completed_at"]})
            return
    raise ValueError("Task not found.")


def record_view(events: List[Dict[str, Any]]) -> None:
    """
    Emit a view event (views are still user actions).
    """
    emit_event(events, "TASKS_VIEWED", None, {})