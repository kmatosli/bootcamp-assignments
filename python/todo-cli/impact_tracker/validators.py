"""
FILE: impact_tracker/validators.py

PURPOSE
Input validation functions for the Impact Tracker CLI.

WHY THIS FILE EXISTS
The CLI should never trust raw user input. This module provides reusable,
testable validation functions that enforce data quality and protect the rest
of the application from malformed or missing values.

This separation makes the system easier to maintain:
- cli.py focuses on user interaction (prompting and printing)
- validators.py focuses on correctness and data quality rules
- services.py focuses on business operations (mutating state + emitting events)

VALIDATION STRATEGY
- Validators return "clean" values (trimmed/normalized) when valid.
- Validators raise ValueError when invalid.
- The CLI catches ValueError and prints a user-facing message.

DESIGN PRINCIPLE
Raise exceptions inside validators; handle and display errors in the CLI.
This keeps business logic deterministic and avoids scattered print statements.

INVARIANTS
- Menu choices must match allowed options exactly (after stripping whitespace).
- Required text fields cannot be empty.
- Priority must map to a canonical label from config.PRIORITY_LEVELS.
- Impact categories must match config.IMPACT_CATEGORIES.
- Tags are normalized to a stable format: lowercase, leading '#', safe chars.
- Task IDs must be integers and must exist in the provided tasks list.

DEBUGGING NOTES
If the CLI appears to accept invalid input, confirm:
- the CLI is calling these validators
- errors are not being swallowed
- config constants match what the CLI displays
"""

from __future__ import annotations

from typing import Any, Dict, List

from impact_tracker.config import IMPACT_CATEGORIES, PRIORITY_LEVELS


# region Menu Validation
# -----------------------------------------------------------------------------
# SECTION: Menu Validation
#
# WHAT
# validate_menu_choice() verifies a main-menu selection is valid.
#
# WHY
# Protects the program loop from unexpected choices and satisfies the rubric:
# "Alert the user if they select an option on the main menu that doesn't exist."
#
# CONTRACT
# - returns the cleaned choice when valid
# - raises ValueError when invalid
# -----------------------------------------------------------------------------
def validate_menu_choice(choice: str, allowed: List[str]) -> str:
    """
    Validate that a menu choice is in the allowed list.

    Parameters
    ----------
    choice : str
        Raw user input (may include whitespace).

    allowed : list[str]
        Allowed menu keys (e.g., ["1", "2", "3", "4"]).

    Returns
    -------
    str
        Cleaned choice.

    Raises
    ------
    ValueError
        If the choice is not one of the allowed values.
    """
    c = choice.strip()
    if c not in allowed:
        raise ValueError(f"Invalid choice. Expected one of: {', '.join(allowed)}")
    return c
# endregion


# region Required Field Validation
# -----------------------------------------------------------------------------
# SECTION: Required Field Validation
#
# WHAT
# validate_non_empty() ensures required strings are not empty.
#
# WHY
# Your task schema requires the "impact narrative" fields. A blank value makes
# the task unusable later (no evidence, no measurable impact, etc.).
#
# CONTRACT
# - returns stripped text when valid
# - raises ValueError when empty
# -----------------------------------------------------------------------------
def validate_non_empty(field_name: str, value: str) -> str:
    """
    Validate a required string field is not empty.

    Parameters
    ----------
    field_name : str
        Display name used in error messages.

    value : str
        Raw user input.

    Returns
    -------
    str
        Stripped non-empty string.

    Raises
    ------
    ValueError
        If the string is empty after stripping.
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} is required and cannot be empty.")
    return cleaned
# endregion


# region Impact Category Validation
# -----------------------------------------------------------------------------
# SECTION: Impact Category Validation
#
# WHAT
# validate_impact_category() enforces that the category matches the canonical
# set of promotion-aligned categories.
#
# WHY
# Reporting groups tasks by category. If categories drift, promotion reports
# become fragmented (e.g., "leadership" vs "Leadership").
#
# CONTRACT
# - returns stripped category when valid
# - raises ValueError otherwise
# -----------------------------------------------------------------------------
def validate_impact_category(value: str) -> str:
    """
    Validate impact category is one of the allowed categories.

    Parameters
    ----------
    value : str
        Raw category input from the user.

    Returns
    -------
    str
        Cleaned category string.

    Raises
    ------
    ValueError
        If the category is not in config.IMPACT_CATEGORIES.
    """
    cleaned = value.strip()
    if cleaned not in IMPACT_CATEGORIES:
        raise ValueError(f"Impact category must be one of: {', '.join(IMPACT_CATEGORIES)}")
    return cleaned
# endregion


# region Priority Validation
# -----------------------------------------------------------------------------
# SECTION: Priority Validation
#
# WHAT
# validate_priority() accepts either:
# - a numeric menu key ("1", "2", "3")
# - an exact priority label (e.g., "⭐ major initiative")
#
# WHY
# The CLI presents priorities as numeric options, but internally the system
# stores a canonical label. This validator converts numeric choice -> label.
#
# CONTRACT
# - returns canonical label when valid
# - raises ValueError when invalid
# -----------------------------------------------------------------------------
def validate_priority(choice: str) -> str:
    """
    Validate priority selection.

    Accepted inputs
    ---------------
    - "1", "2", "3" (menu keys)
    - Exact label values from PRIORITY_LEVELS.values()

    Parameters
    ----------
    choice : str
        Raw user input.

    Returns
    -------
    str
        Canonical priority label.

    Raises
    ------
    ValueError
        If the input is not a known key or known label.
    """
    c = choice.strip()
    if c in PRIORITY_LEVELS:
        return PRIORITY_LEVELS[c]
    if c in PRIORITY_LEVELS.values():
        return c
    raise ValueError("Invalid priority. Choose 1, 2, or 3.")
# endregion


# region Tag Parsing and Normalization
# -----------------------------------------------------------------------------
# SECTION: Tag Parsing and Normalization
#
# WHAT
# validate_tags() parses optional tag text into a normalized list of tags.
#
# WHY
# Tags are used for later searching, grouping, and derived metrics (top tags).
# Normalizing tags ensures:
# - stable analytics
# - consistent user experience
# - no duplicates from case/formatting differences
#
# INPUT FORMATS SUPPORTED
# - "#automation #leadership"
# - "automation, leadership"
# - "automation leadership"
#
# NORMALIZATION RULES
# - lowercase
# - force leading "#"
# - allow only [a-z0-9] plus "_" and "-"
# - drop empty tags
# - de-duplicate while preserving order
#
# CONTRACT
# - returns [] if user enters nothing
# - returns a list of normalized tags otherwise
# -----------------------------------------------------------------------------
def validate_tags(raw: str) -> List[str]:
    """
    Parse and normalize tags from input.

    Parameters
    ----------
    raw : str
        User-provided tag input string.

    Returns
    -------
    list[str]
        Normalized tags, e.g. ["#automation", "#leadership"].
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

        # Keep only alphanumeric plus "_" and "-"
        t = "#" + "".join(ch for ch in t[1:] if ch.isalnum() or ch in ("_", "-"))

        if t != "#":
            tags.append(t)

    # De-duplicate while preserving order
    seen = set()
    unique: List[str] = []
    for t in tags:
        if t not in seen:
            unique.append(t)
            seen.add(t)
    return unique
# endregion


# region Task ID Validation
# -----------------------------------------------------------------------------
# SECTION: Task ID Validation
#
# WHAT
# validate_task_id() verifies:
# - input is an integer
# - the integer exists in the current tasks list
#
# WHY
# Required by rubric:
# - alert the user if they try to delete a task that doesn't exist
#
# CONTRACT
# - returns the task id as int if valid
# - raises ValueError with a user-facing message otherwise
# -----------------------------------------------------------------------------
def validate_task_id(task_id_raw: str, tasks: List[Dict[str, Any]]) -> int:
    """
    Validate task id exists in the tasks list.

    Parameters
    ----------
    task_id_raw : str
        Raw user input (should parse to integer).

    tasks : list[dict]
        Current in-memory task list.

    Returns
    -------
    int
        Validated task id.

    Raises
    ------
    ValueError
        If task_id_raw is not an integer, or if no matching task exists.
    """
    try:
        task_id = int(task_id_raw.strip())
    except ValueError as e:
        raise ValueError("Task ID must be an integer.") from e

    if not any(t.get("id") == task_id for t in tasks):
        raise ValueError(f"No task found with id={task_id}.")
    return task_id
# endregion