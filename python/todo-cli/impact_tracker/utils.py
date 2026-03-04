from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional


# =============================================================================
# Section: Time Helpers
# =============================================================================

def now_iso() -> str:
    """
    Return current local timestamp as ISO string (seconds precision).
    """
    return datetime.now().replace(microsecond=0).isoformat()


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """
    Parse ISO datetime string into datetime, returning None if invalid/falsy.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def iso_week_key(dt: datetime) -> str:
    """
    Convert datetime to a stable year-week key like '2026-W10'.
    """
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


# =============================================================================
# Section: File Helpers
# =============================================================================

def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists.
    """
    os.makedirs(path, exist_ok=True)


def write_json(path: str, data: Any) -> None:
    """
    Write JSON to disk (pretty formatted).
    """
    dirpath = os.path.dirname(path) or "."
    ensure_dir(dirpath)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_text(path: str, text: str) -> None:
    """
    Write text to disk.
    """
    dirpath = os.path.dirname(path) or "."
    ensure_dir(dirpath)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)