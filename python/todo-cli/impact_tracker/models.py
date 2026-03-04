from __future__ import annotations

from typing import Any, Dict, List, Optional

from impact_tracker.utils import now_iso


# =============================================================================
# Section: Model Layer
# =============================================================================

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


def build_event(
    event_id: int,
    event_type: str,
    task_id: Optional[int],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create an append-only event record.
    """
    return {
        "event_id": event_id,
        "event_type": event_type,
        "task_id": task_id,
        "timestamp": now_iso(),
        "payload": payload,
    }