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


# =============================================================================
# Section: Storage / Export Layer
# =============================================================================

def export_outputs(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    """
    Export required outputs:

      Required:
      - outputs/event_log.json
      - outputs/metrics.json
      - outputs/promotion_report.md

      Also:
      - outputs/reports.json
      - outputs/reports.md
    """
    ensure_dir(OUTPUT_DIR)

    # Required: event log
    write_json(os.path.join(OUTPUT_DIR, "event_log.json"), {"events": events})

    # Reports bundle + metrics
    reports = build_reports_bundle(tasks, events)
    metrics = reports.get("metrics", {})
    write_json(os.path.join(OUTPUT_DIR, "metrics.json"), metrics)

    # Required: promotion report markdown
    _, promo_md = promotion_evidence_report(tasks, metrics)
    write_text(os.path.join(OUTPUT_DIR, "promotion_report.md"), promo_md)

    # Helpful: full reports
    write_json(os.path.join(OUTPUT_DIR, "reports.json"), reports)
    write_text(os.path.join(OUTPUT_DIR, "reports.md"), reports_to_markdown(reports))