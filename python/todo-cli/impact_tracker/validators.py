from __future__ import annotations

from typing import Any, Dict, List

from impact_tracker.config import IMPACT_CATEGORIES, PRIORITY_LEVELS


# =============================================================================
# Section: Validation Layer
# =============================================================================

def validate_menu_choice(choice: str, allowed: List[str]) -> str:
    """
    Validate that menu choice is in allowed list.
    """
    c = choice.strip()
    if c not in allowed:
        raise ValueError(f"Invalid choice. Expected one of: {', '.join(allowed)}")
    return c


def validate_non_empty(field_name: str, value: str) -> str:
    """
    Validate a required string field is not empty.
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required and cannot be empty.")
    return cleaned


def validate_impact_category(value: str) -> str:
    """
    Validate impact category is one of the allowed categories.
    """
    cleaned = value.strip()
    if cleaned not in IMPACT_CATEGORIES:
        raise ValueError(f"Impact category must be one of: {', '.join(IMPACT_CATEGORIES)}")
    return cleaned


def validate_priority(choice: str) -> str:
    """
    Validate priority selection:
    - accepts '1','2','3' or exact label
    """
    c = choice.strip()
    if c in PRIORITY_LEVELS:
        return PRIORITY_LEVELS[c]
    if c in PRIORITY_LEVELS.values():
        return c
    raise ValueError("Invalid priority. Choose 1, 2, or 3.")


def validate_tags(raw: str) -> List[str]:
    """
    Parse tags from input:
      - '#automation #leadership'
      - 'automation, leadership'
      - 'automation leadership'

    Returns normalized tags like ['#automation', '#leadership'].
    """
    text = raw.strip()
    if not text:
        return []

    text = text.replace(",", " ")
    parts = [p.strip() for p in text.split() if p.strip()]

    tags: List[str] = []
    for p in parts:
        t = p.lower()
        if not t.startswith("#"):
            t = "#" + t
        # keep only alnum/_/-
        t = "#" + "".join(ch for ch in t[1:] if ch.isalnum() or ch in ("_", "-"))
        if t != "#":
            tags.append(t)

    # de-duplicate while preserving order
    seen = set()
    unique: List[str] = []
    for t in tags:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    return unique


def validate_task_id(task_id_raw: str, tasks: List[Dict[str, Any]]) -> int:
    """
    Validate task id exists in tasks list.
    """
    try:
        task_id = int(task_id_raw.strip())
    except ValueError as e:
        raise ValueError("Task ID must be an integer.") from e

    if not any(t.get("id") == task_id for t in tasks):
        raise ValueError(f"No task found with id={task_id}.")
    return task_id