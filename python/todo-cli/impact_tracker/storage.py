"""
FILE: impact_tracker/storage.py

PURPOSE
Export the app's derived artifacts to disk under ./outputs/.

This module is intentionally small and boring:
- It does not contain business logic.
- It does not compute metrics directly.
- It only orchestrates "build report -> write file".

WHY THIS FILE EXISTS
The core app runs fully in-memory (bootcamp requirement):
- tasks: list[dict]
- events: list[dict]

But a real "impact tracker" must persist shareable outputs.
This export layer creates artifacts that are:
- readable in GitHub
- diffable in version control
- usable in performance reviews / promotion packets

DATA PIPELINE MENTAL MODEL
User action -> event recorded -> state updated -> export derived outputs

OUTPUT CONTRACT
Always writes to OUTPUT_DIR (default: "outputs"):

Required assignment artifacts (per project spec):
- outputs/event_log.json
- outputs/metrics.json
- outputs/promotion_report.md

Additional convenience artifacts:
- outputs/reports.json
- outputs/reports.md

DESIGN PRINCIPLES
1) Single responsibility: write files, nothing else.
2) Deterministic outputs: same inputs produce same exported bundle.
3) Human + machine formats: Markdown for reading, JSON for tooling.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from impact_tracker.config import OUTPUT_DIR
from impact_tracker.reporting import (
    build_reports_bundle,
    promotion_evidence_report,
    reports_to_markdown,
)
from impact_tracker.utils import ensure_dir, write_json, write_text


# region Storage / Export Layer
# -----------------------------------------------------------------------------
# SECTION: Storage / Export Layer
#
# WHAT THIS SECTION DOES
# export_outputs() is the single entry point for writing artifacts to disk.
#
# WHY IT EXISTS
# This keeps file I/O out of:
# - CLI layer (so UI stays clean)
# - service layer (so state mutation stays pure)
# - reporting layer (so reporting functions stay testable)
#
# WHEN IT RUNS
# The CLI calls export_outputs() on exit (normally and in error cases).
#
# INPUTS
# - tasks: current materialized state
# - events: append-only event log
#
# OUTPUTS (FILES)
# Required:
# - outputs/event_log.json
# - outputs/metrics.json
# - outputs/promotion_report.md
#
# Additional:
# - outputs/reports.json
# - outputs/reports.md
# -----------------------------------------------------------------------------
def export_outputs(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    """
    Export derived outputs to disk.

    Parameters
    ----------
    tasks : list[dict]
        Current in-memory task state (materialized view).

    events : list[dict]
        Append-only event log capturing user actions.

    Returns
    -------
    None
        Writes files to OUTPUT_DIR; does not return data.

    Error Behavior
    --------------
    This function intentionally does not swallow exceptions.
    The caller (CLI) decides whether to handle/export errors.
    """
    # Step 1: Make sure the output folder exists.
    ensure_dir(OUTPUT_DIR)

    # Step 2 (Required): Export the event log.
    # This is the audit trail and the foundation for derived metrics.
    write_json(os.path.join(OUTPUT_DIR, "event_log.json"), {"events": events})

    # Step 3: Build the full reports bundle and extract metrics.
    # reports.json is the "single object" representation of everything.
    reports = build_reports_bundle(tasks, events)
    metrics = reports.get("metrics", {})

    # Step 4 (Required): Export metrics.json.
    # Metrics are generated primarily from the event log.
    write_json(os.path.join(OUTPUT_DIR, "metrics.json"), metrics)

    # Step 5 (Required): Export promotion_report.md.
    # This is the promotion-ready narrative organized by impact categories.
    _, promo_md = promotion_evidence_report(tasks, metrics)
    write_text(os.path.join(OUTPUT_DIR, "promotion_report.md"), promo_md)

    # Step 6 (Convenience): Export full report bundle in JSON + Markdown.
    # These are useful for quick review and demos.
    write_json(os.path.join(OUTPUT_DIR, "reports.json"), reports)
    write_text(os.path.join(OUTPUT_DIR, "reports.md"), reports_to_markdown(reports))
# endregion