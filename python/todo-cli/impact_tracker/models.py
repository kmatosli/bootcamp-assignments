"""
FILE: impact_tracker/models.py

PURPOSE
Defines the data structures used by the Impact Tracker system.

WHY THIS FILE EXISTS
This module acts as a lightweight "model layer" responsible for constructing
structured records used by the application. The goal is to centralize record
creation so the rest of the system does not need to know the exact structure
of task or event dictionaries.

Instead of building dictionaries in multiple places, the application calls
these helper functions. This ensures consistent schemas across the system.

ARCHITECTURE ROLE
The model layer sits between:
    CLI input (cli.py)
    and
    Business logic / event logging (services.py)

CLI → models → services → storage/reporting

DATA STRUCTURES CREATED
1) Task Records
   Represent a unit of professional work captured by the user.

2) Event Records
   Represent immutable log entries describing actions taken in the system.

DESIGN PRINCIPLE
Tasks represent CURRENT STATE.
Events represent HISTORY.

This hybrid structure allows both:
- easy state inspection
- historical auditing and reporting.

DEPENDENCIES
Uses now_iso() from utils.py to generate consistent timestamps.

INVARIANTS
- All timestamps use ISO-8601 format
- Task IDs are unique integers
- Event IDs are sequential integers
- Events are append-only and never modified

DEBUGGING NOTES
If timestamps appear incorrect or inconsistent:
    check utils.now_iso()

If event payloads appear malformed:
    inspect services.emit_event()
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from impact_tracker.utils import now_iso


# region Task Model
# -----------------------------------------------------------------------------
# SECTION: Task Model
#
# WHAT
# Constructs a task dictionary that represents a unit of work captured
# by the CLI application.
#
# WHY
# Centralizing record construction prevents subtle bugs caused by
# inconsistent dictionary keys across different modules.
#
# CALLERS
# services.add_task()
#
# IMPORTANT DESIGN NOTES
# - Tasks begin with status "open"
# - completed_at is None until a completion event occurs
# - created_at is generated automatically at creation time
#
# TASK SCHEMA
#
# {
#   id: int
#   title: str
#   problem: str
#   action: str
#   impact: str
#   metrics: str
#   evidence: str
#   tags: list[str]
#   priority: str
#   impact_category: str
#   status: str
#   created_at: str (ISO timestamp)
#   completed_at: Optional[str]
# }
# -----------------------------------------------------------------------------
def build_task(
    task_id: int,
    title: str,
    problem: str,
    action: str,
    impact: str,
    metrics: str,
    evidence: str,
    tags: List[str],
    priority: str,
    impact_category: str,
) -> Dict[str, Any]:
    """
    Create a structured task record.

    Parameters
    ----------
    task_id : int
        Unique identifier assigned by services.next_task_id().

    title : str
        Short description of the work item.

    problem : str
        Context explaining why the work was necessary.

    action : str
        Description of what was done.

    impact : str
        Explanation of who benefited and how.

    metrics : str
        Quantified results (time saved, cost reduction, scale, etc).

    evidence : str
        Links or references supporting the claim.

    tags : list[str]
        Optional metadata tags used for filtering and grouping.

    priority : str
        Significance level (from config.PRIORITY_LEVELS).

    impact_category : str
        Promotion-aligned classification of the work.

    Returns
    -------
    dict
        A fully structured task record ready for insertion into the
        in-memory task list.

    Notes
    -----
    - created_at is automatically generated.
    - completed_at remains None until completion.
    """
    return {
        "id": task_id,
        "title": title,
        "problem": problem,
        "action": action,
        "impact": impact,
        "metrics": metrics,
        "evidence": evidence,
        "tags": tags,
        "priority": priority,
        "impact_category": impact_category,
        "status": "open",
        "created_at": now_iso(),
        "completed_at": None,
    }
# endregion


# region Event Model
# -----------------------------------------------------------------------------
# SECTION: Event Model
#
# WHAT
# Constructs an immutable event record used for logging system actions.
#
# WHY
# Instead of only mutating state (tasks list), the system also records
# each significant action as an event. This allows reconstruction of
# historical activity and enables richer reporting.
#
# EVENTS REPRESENT
# - task creation
# - task completion
# - task deletion
# - application start/stop
# - report generation
#
# EVENT SCHEMA
#
# {
#   event_id: int
#   event_type: str
#   task_id: Optional[int]
#   timestamp: str (ISO)
#   payload: dict[str, Any]
# }
#
# DESIGN PRINCIPLE
# Events are append-only. They should never be modified once recorded.
#
# CALLERS
# services.emit_event()
# -----------------------------------------------------------------------------
def build_event(
    event_id: int,
    event_type: str,
    task_id: Optional[int],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create an append-only event record.

    Parameters
    ----------
    event_id : int
        Sequential identifier for the event.

    event_type : str
        Classification label describing the event
        (e.g., TASK_CREATED, TASK_COMPLETED).

    task_id : Optional[int]
        The task associated with the event, if applicable.

    payload : dict
        Additional contextual metadata describing the event.

    Returns
    -------
    dict
        Structured event record suitable for insertion into the
        application's event log.
    """
    return {
        "event_id": event_id,
        "event_type": event_type,
        "task_id": task_id,
        "timestamp": now_iso(),
        "payload": payload,
    }
# endregion