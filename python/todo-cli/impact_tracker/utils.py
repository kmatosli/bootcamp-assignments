"""
FILE: impact_tracker/utils.py

PURPOSE
Shared utility helpers used across the application.

This module contains small, reusable functions that do not belong to a
specific business layer such as services, reporting, or storage.

CATEGORIES
1) Time helpers
2) File helpers

WHY THIS FILE EXISTS
Without a utilities module, the same code tends to get duplicated in
multiple places (for example writing JSON, parsing timestamps, etc).

Centralizing these helpers provides:

- Consistent timestamp formatting
- Safe datetime parsing
- Reliable file writing
- Small, testable functions

DESIGN PRINCIPLES
Utilities should be:

- Stateless
- Deterministic
- Side-effect minimal (except for file writing)

COMMON DEBUGGING TIP
If reports show incorrect time windows or weekly buckets,
this is the first place to check.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional


# region Time Helpers
# -----------------------------------------------------------------------------
# SECTION: Time Helpers
#
# WHAT THESE FUNCTIONS DO
# Provide consistent timestamp creation and parsing across the application.
#
# WHY THEY EXIST
# Multiple modules rely on timestamps:
# - services.py (task completion times)
# - reporting.py (weekly metrics)
# - storage.py (report generation timestamps)
#
# Using a single set of helpers prevents format drift.
#
# FORMAT STANDARD
# ISO-8601 timestamps with second precision:
#
#     2026-03-05T14:32:18
#
# This format is:
# - human readable
# - machine parseable
# - natively supported by Python
# -----------------------------------------------------------------------------
def now_iso() -> str:
    """
    Return current local timestamp as ISO string.

    Behavior
    --------
    - Uses local system time
    - Removes microseconds for stable formatting

    Returns
    -------
    str
        ISO timestamp like:
        "2026-03-05T14:32:18"
    """
    return datetime.now().replace(microsecond=0).isoformat()


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """
    Safely parse ISO datetime string.

    This function intentionally **never throws an exception**.
    Invalid values simply return None.

    Parameters
    ----------
    value : Optional[str]
        ISO formatted datetime string.

    Returns
    -------
    datetime | None
        Parsed datetime if valid, otherwise None.

    Example
    -------
    "2026-03-05T14:32:18" → datetime object
    None → None
    invalid string → None
    """
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def iso_week_key(dt: datetime) -> str:
    """
    Convert datetime to a stable ISO week identifier.

    WHY THIS EXISTS
    Weekly productivity metrics require grouping tasks by week.

    Using ISO week numbering ensures consistency across years.

    Example
    -------
    2026-03-05 → "2026-W10"

    Returns
    -------
    str
        Week key formatted as:
        YYYY-W##
    """
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"
# endregion


# region File Helpers
# -----------------------------------------------------------------------------
# SECTION: File Helpers
#
# WHAT THESE FUNCTIONS DO
# Provide safe file writing utilities used by the storage layer.
#
# WHY THEY EXIST
# Writing files repeatedly across the project requires consistent behavior:
#
# - Ensure directories exist
# - Use UTF-8 encoding
# - Format JSON cleanly
#
# These helpers standardize those operations.
#
# DESIGN CHOICES
# - JSON files are pretty-printed (indent=2) for GitHub readability
# - UTF-8 encoding ensures compatibility with Markdown and Unicode
# -----------------------------------------------------------------------------
def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists.

    If the directory does not exist, it is created.

    Parameters
    ----------
    path : str
        Directory path.

    Returns
    -------
    None
    """
    os.makedirs(path, exist_ok=True)


def write_json(path: str, data: Any) -> None:
    """
    Write JSON data to disk.

    Behavior
    --------
    - Automatically creates parent directory
    - Pretty formatted JSON (indent=2)
    - UTF-8 encoding

    Parameters
    ----------
    path : str
        Destination file path.

    data : Any
        JSON serializable object.

    Returns
    -------
    None
    """
    dirpath = os.path.dirname(path) or "."
    ensure_dir(dirpath)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_text(path: str, text: str) -> None:
    """
    Write plain text to disk.

    Used primarily for exporting Markdown reports.

    Behavior
    --------
    - Ensures parent directory exists
    - Writes UTF-8 encoded text

    Parameters
    ----------
    path : str
        Destination file path.

    text : str
        Content to write.

    Returns
    -------
    None
    """
    dirpath = os.path.dirname(path) or "."
    ensure_dir(dirpath)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
# endregion