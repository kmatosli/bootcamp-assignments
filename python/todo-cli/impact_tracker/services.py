"""
FILE: impact_tracker/services.py

PURPOSE
Service layer functions that mutate in-memory state AND emit append-only events.

WHY THIS FILE EXISTS
This project is intentionally designed as a small "personal impact data pipeline":

    Work → Logged → Structured → Quantified → Reported

To support that pipeline, every user action should do two things:
1) Update the current state (tasks list)
2) Append an immutable historical record (events list)

This module owns those state transitions and event emissions so the rest of the
system stays clean:
- cli.py handles user prompts/printing
- validators.py enforces input quality
- services.py performs state changes + emits events
- reporting.py derives analytics/reports
- storage.py exports data to disk

EVENT SOURCING NOTE
Tasks represent the current "materialized view" (state).
Events represent the complete history of actions.

Even though tasks are required by the bootcamp rubric (Python list storage),
the event log enables auditability and richer reporting:
- counts by week
- completion rate
- promotion evidence report generated from consistent history

INVARIANTS
- tasks is a list[dict] where each dict has a unique integer "id"
- events is a list[dict] where each dict has a unique integer "event_id"
- event_id is monotonic (within a single program run)
- task_id is monotonic (within a single program run)
- events are append-only (never mutate past events)
- state changes should always be paired with a corresponding event

DEBUGGING NOTES
If reports look wrong:
- inspect outputs/event_log.json
- confirm events are being emitted for each action

If IDs look wrong:
- confirm next_task_id() and next_event_id() are being called correctly
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from impact_tracker.models import build_event


# region ID Allocation
# -----------------------------------------------------------------------------
# SECTION: ID Allocation
#
# WHAT
# Helpers to allocate the "next" IDs for tasks and events.
#
# WHY
# IDs give stable references for:
# - viewing tasks
# - deleting tasks
# - event linking (task_id in events)
#
# DESIGN CHOICE
# IDs are monotonic within the current run. Since state is in-memory only,
# IDs reset when the program restarts (acceptable for bootcamp requirements).
# -----------------------------------------------------------------------------
def next_task_id(tasks: List[Dict[str, Any]]) -> int:
    """
    Allocate the next task id (monotonic within this run).

    Parameters
    ----------
    tasks : list[dict]
        Current in-memory task list.

    Returns
    -------
    int
        Next available task id.
    """
    return 1 if not tasks else max(t["id"] for t in tasks) + 1


def next_event_id(events: List[Dict[str, Any]]) -> int:
    """
    Allocate the next event id (monotonic within this run).

    Parameters
    ----------
    events : list[dict]
        Current in-memory event log.

    Returns
    -------
    int
        Next available event id.
    """
    return 1 if not events else max(e["event_id"] for e in events) + 1
# endregion


# region Event Emission
# -----------------------------------------------------------------------------
# SECTION: Event Emission
#
# WHAT
# emit_event() is the single, centralized way to append to the event log.
#
# WHY
# Centralizing event creation:
# - enforces a consistent schema
# - prevents duplicate "event formatting" logic across the codebase
# - makes it easy to audit what actions the app is recording
#
# CONTRACT
# - appends exactly one event record to `events`
# - never mutates existing events
# -----------------------------------------------------------------------------
def emit_event(
    events: List[Dict[str, Any]],
    event_type: str,
    task_id: Optional[int],
    payload: Dict[str, Any],
) -> None:
    """
    Append an event to the append-only event log.

    Parameters
    ----------
    events : list[dict]
        In-memory event log (append-only).

    event_type : str
        Event classification label (e.g., TASK_ADDED).

    task_id : Optional[int]
        Related task id, if applicable.

    payload : dict
        Additional metadata for reporting/debugging.

    Returns
    -------
    None
        The function mutates `events` by appending.
    """
    eid = next_event_id(events)
    events.append(build_event(eid, event_type, task_id, payload))
# endregion


# region Task Operations (State + Events)
# -----------------------------------------------------------------------------
# SECTION: Task Operations
#
# WHAT
# Functions that update the tasks list and emit corresponding events.
#
# WHY
# Keeping state updates and event emission in the same function guarantees
# the event log remains a faithful representation of user actions.
#
# NOTE ON ERROR HANDLING
# - Some functions rely on the CLI to validate task existence first.
# - complete_task() additionally enforces "not already completed".
# -----------------------------------------------------------------------------
def add_task(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]], task: Dict[str, Any]) -> None:
    """
    Add a task to state and emit TASK_ADDED.

    Parameters
    ----------
    tasks : list[dict]
        In-memory task list.

    events : list[dict]
        In-memory event log.

    task : dict
        Fully built task record (typically from models.build_task()).

    Returns
    -------
    None
        Mutates tasks/events.
    """
    tasks.append(task)
    emit_event(events, "TASK_ADDED", task["id"], {"task": task})


def delete_task(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]], task_id: int) -> None:
    """
    Delete a task from state and emit TASK_DELETED.

    Parameters
    ----------
    tasks : list[dict]
        In-memory task list.

    events : list[dict]
        In-memory event log.

    task_id : int
        Identifier of the task to delete.

    Returns
    -------
    None
        Mutates tasks/events.

    Notes
    -----
    This function emits an event even if the task_id was not found.
    In the current architecture, the CLI validates task existence before calling
    this function (validators.validate_task_id()).

    The event payload includes:
    - removed: task dict if found, else None
    - count_before / count_after: state size for auditing/debugging
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

    Parameters
    ----------
    tasks : list[dict]
        In-memory task list.

    events : list[dict]
        In-memory event log.

    task_id : int
        Identifier of the task to mark completed.

    Returns
    -------
    None
        Mutates tasks/events.

    Raises
    ------
    ValueError
        If task not found or already completed.

    Design Notes
    ------------
    - The completion timestamp is stored in the task for convenience (state view).
    - The event log is still the canonical historical record of the completion.
    """
    for t in tasks:
        if t["id"] == task_id:
            if t.get("status") == "completed":
                raise ValueError("Task is already completed.")
            t["status"] = "completed"

            # Timestamp comes from event but store in task for convenience.
            # (Kept as local import to preserve current behavior.)
            from impact_tracker.utils import now_iso

            t["completed_at"] = now_iso()
            emit_event(events, "TASK_COMPLETED", task_id, {"completed_at": t["completed_at"]})
            return

    raise ValueError("Task not found.")
# endregion


# region Non-Mutating User Actions (Still Events)
# -----------------------------------------------------------------------------
# SECTION: Non-Mutating User Actions
#
# WHAT
# record_view() emits an event that does not change task state.
#
# WHY
# Some user actions do not mutate tasks but are still important for analytics
# and auditing (e.g., usage patterns, "views" over time).
#
# CONTRACT
# - emits exactly one event
# - does not modify tasks
# -----------------------------------------------------------------------------
def record_view(events: List[Dict[str, Any]]) -> None:
    """
    Emit a view event (views are still user actions).

    Parameters
    ----------
    events : list[dict]
        In-memory event log.

    Returns
    -------
    None
        Appends one TASKS_VIEWED event.
    """
    emit_event(events, "TASKS_VIEWED", None, {})
# endregion