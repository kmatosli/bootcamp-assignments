"""
FILE: impact_tracker/reporting.py

PURPOSE
Generate derived metrics and promotion-ready reports from:
- tasks (current state: materialized view)
- events (history: append-only event log)

WHY THIS FILE EXISTS
The bootcamp assignment requires an in-memory list of tasks, but the "impact
tracker" goal is bigger than a to-do list.

This reporting layer turns logged work into reusable outputs:
- daily summary
- weekly accomplishments
- standup report
- promotion evidence report
- derived metrics (counts, rates, top tags, time-to-complete)

DATA PIPELINE MENTAL MODEL
User action -> event recorded -> state updated -> reporting derived

Where:
- tasks = current snapshot ("what we believe is true now")
- events = history ("what happened and when")

This module intentionally supports both:
- metrics primarily from events (audit-friendly)
- some fields from tasks for convenience and readability in reports

OUTPUTS USING THIS MODULE
storage.py will export:
- outputs/metrics.json
- outputs/reports.json
- outputs/reports.md
- outputs/promotion_report.md (promotion_evidence_report markdown output)

DESIGN PRINCIPLES
1) Deterministic, testable pure functions (no input(), no printing)
2) Prefer event log for metrics to avoid relying on mutable state
3) Keep report outputs simple JSON + Markdown so they are easy to diff in Git

INVARIANTS / EXPECTATIONS
- tasks: list[dict], each dict has keys like id, title, status, created_at, etc.
- events: list[dict], each dict has keys like event_type, timestamp, payload, etc.
- ISO timestamps are parsed using utils.parse_iso_datetime()
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from impact_tracker.config import IMPACT_CATEGORIES
from impact_tracker.utils import iso_week_key, now_iso, parse_iso_datetime


# region Derived Metrics (Events + State)
# -----------------------------------------------------------------------------
# SECTION: Derived Metrics (Events + State)
#
# WHAT
# compute_derived_metrics() calculates analytics that help answer:
# - how much work is being logged over time?
# - how much work is being completed over time?
# - what is the completion rate?
# - what tags and categories dominate the work?
# - how much "flagship work" is being produced?
# - how long does work take from creation to completion?
#
# WHY
# This is the "Quantified" part of the pipeline.
# These metrics support weekly review, performance reviews, and promotion docs.
#
# DESIGN NOTES
# - Weekly created/completed counts come from EVENTS for auditability.
# - Tag/category counts come from TASKS because tags/categories are stored
#   directly in the task records and reflect the current view.
# - Time-to-complete uses timestamps captured during TASK_ADDED and TASK_COMPLETED.
# -----------------------------------------------------------------------------
def compute_derived_metrics(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute derived metrics primarily from event log, with some support from state.

    Parameters
    ----------
    tasks : list[dict]
        Current in-memory state (materialized view).

    events : list[dict]
        Append-only history of user actions (event log).

    Returns
    -------
    dict
        A JSON-serializable metrics dictionary suitable for exporting.
    """
    # Created / completed counts by ISO week key
    created_week: Counter[str] = Counter()
    completed_week: Counter[str] = Counter()

    # Track create/complete timestamps by task so we can compute time-to-complete
    created_at_by_task: Dict[int, datetime] = {}
    completed_at_by_task: Dict[int, datetime] = {}

    # ---- Event-sourced counting and timestamps --------------------------------
    for e in events:
        if e.get("event_type") == "TASK_ADDED":
            t = e.get("payload", {}).get("task", {})
            tid = t.get("id")
            ts = parse_iso_datetime(e.get("timestamp"))
            if isinstance(tid, int) and ts:
                created_week[iso_week_key(ts)] += 1
                created_at_by_task[tid] = parse_iso_datetime(t.get("created_at")) or ts

        if e.get("event_type") == "TASK_COMPLETED":
            tid = e.get("task_id")
            ts = parse_iso_datetime(e.get("timestamp"))
            if isinstance(tid, int) and ts:
                completed_week[iso_week_key(ts)] += 1
                completed_at_by_task[tid] = parse_iso_datetime(e.get("payload", {}).get("completed_at")) or ts

    total_created = sum(created_week.values())
    total_completed = sum(completed_week.values())
    completion_rate = (total_completed / total_created) if total_created else 0.0

    # ---- State-sourced counts (tags, categories, flagship work) ----------------
    tag_counts: Counter[str] = Counter()
    impact_cat_counts: Counter[str] = Counter()
    flagship_count = 0

    for t in tasks:
        for tag in t.get("tags", []) or []:
            tag_counts[tag] += 1

        impact_cat = t.get("impact_category")
        if impact_cat:
            impact_cat_counts[impact_cat] += 1

        if t.get("priority") == "⭐ major initiative":
            flagship_count += 1

    # ---- Time-to-complete distribution ----------------------------------------
    # Compute time-to-complete (hours) where both timestamps exist.
    ttc_hours: List[float] = []
    for tid, created_dt in created_at_by_task.items():
        done_dt = completed_at_by_task.get(tid)
        if created_dt and done_dt:
            delta_hours = (done_dt - created_dt).total_seconds() / 3600.0
            if delta_hours >= 0:
                ttc_hours.append(delta_hours)

    # Bucketize into human-readable bins (easy to present in a demo/video).
    buckets: Dict[str, int] = {"<1h": 0, "1-8h": 0, "8-24h": 0, "1-3d": 0, "3-7d": 0, "7d+": 0}
    for h in ttc_hours:
        if h < 1:
            buckets["<1h"] += 1
        elif h < 8:
            buckets["1-8h"] += 1
        elif h < 24:
            buckets["8-24h"] += 1
        elif h < 72:
            buckets["1-3d"] += 1
        elif h < 168:
            buckets["3-7d"] += 1
        else:
            buckets["7d+"] += 1

    return {
        "generated_at": now_iso(),
        "tasks_created_per_week": dict(sorted(created_week.items())),
        "tasks_completed_per_week": dict(sorted(completed_week.items())),
        "total_tasks_created": total_created,
        "total_tasks_completed": total_completed,
        "completion_rate": round(completion_rate, 4),
        "top_tags": tag_counts.most_common(10),
        "top_impact_categories": impact_cat_counts.most_common(10),
        "flagship_work_count": flagship_count,
        "time_to_complete_hours_buckets": buckets,
    }
# endregion


# region Daily Summary
# -----------------------------------------------------------------------------
# SECTION: Daily Summary
#
# WHAT
# daily_summary() lists tasks completed today.
#
# WHY
# This supports end-of-day reflection and helps build habit:
# "What did I ship today, and what evidence exists?"
#
# NOTE
# Uses the task state's completed_at timestamp (already updated by services.py).
# -----------------------------------------------------------------------------
def daily_summary(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Daily summary: tasks completed today.

    Parameters
    ----------
    tasks : list[dict]
        Current task state.

    Returns
    -------
    dict
        JSON-serializable summary for "today".
    """
    today = date.today()
    completed_today: List[Dict[str, Any]] = []

    for t in tasks:
        if t.get("status") == "completed":
            dt = parse_iso_datetime(t.get("completed_at"))
            if dt and dt.date() == today:
                completed_today.append(t)

    return {
        "date": today.isoformat(),
        "completed_count": len(completed_today),
        "completed_tasks": [
            {
                "id": t["id"],
                "title": t["title"],
                "impact_category": t.get("impact_category"),
                "tags": t.get("tags", []),
            }
            for t in completed_today
        ],
    }
# endregion


# region Weekly Accomplishments
# -----------------------------------------------------------------------------
# SECTION: Weekly Accomplishments
#
# WHAT
# weekly_accomplishments() lists tasks completed in the last N days.
#
# WHY
# Weekly review is the bridge between "tasks" and "promotion narrative".
# A weekly list makes it easy to write:
# - what shipped
# - what impact happened
# - what metrics moved
# -----------------------------------------------------------------------------
def weekly_accomplishments(tasks: List[Dict[str, Any]], days: int = 7) -> Dict[str, Any]:
    """
    Weekly accomplishments: tasks completed in last N days.

    Parameters
    ----------
    tasks : list[dict]
        Current task state.

    days : int
        Window size (defaults to 7).

    Returns
    -------
    dict
        JSON-serializable summary for last N days.
    """
    now = datetime.now().replace(microsecond=0)
    start = now.fromtimestamp(now.timestamp() - days * 24 * 3600)

    completed: List[Dict[str, Any]] = []
    for t in tasks:
        if t.get("status") == "completed":
            dt = parse_iso_datetime(t.get("completed_at"))
            if dt and dt >= start:
                completed.append(t)

    return {
        "window_days": days,
        "start": start.isoformat(),
        "end": now_iso(),
        "completed_count": len(completed),
        "completed_tasks": [
            {"id": t["id"], "title": t["title"], "impact": t.get("impact"), "metrics": t.get("metrics")}
            for t in completed
        ],
    }
# endregion


# region Standup Report
# -----------------------------------------------------------------------------
# SECTION: Standup Report
#
# WHAT
# standup_report() builds three lists:
# - yesterday completed
# - today working on (everything not completed)
# - blocked by (tagged with #blocked)
#
# WHY
# This supports daily communication and creates "portable narrative":
# you can paste this output into Slack, Jira comments, or notes.
# -----------------------------------------------------------------------------
def standup_report(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Standup report:
    - Yesterday I completed
    - Today I am working on
    - Blocked by (tasks tagged #blocked)

    Parameters
    ----------
    tasks : list[dict]
        Current task state.

    Returns
    -------
    dict
        JSON-serializable standup structure.
    """
    today = date.today()
    yesterday = date.fromordinal(today.toordinal() - 1)

    completed_yesterday: List[Dict[str, Any]] = []
    open_today: List[Dict[str, Any]] = []
    blocked: List[Dict[str, Any]] = []

    for t in tasks:
        if t.get("status") == "completed":
            dt = parse_iso_datetime(t.get("completed_at"))
            if dt and dt.date() == yesterday:
                completed_yesterday.append(t)
        else:
            open_today.append(t)

        tags = set(t.get("tags", []) or [])
        if "#blocked" in tags:
            blocked.append(t)

    return {
        "yesterday_completed": [{"id": t["id"], "title": t["title"]} for t in completed_yesterday],
        "today_working_on": [{"id": t["id"], "title": t["title"], "priority": t.get("priority")} for t in open_today],
        "blocked_by": [{"id": t["id"], "title": t["title"], "evidence": t.get("evidence")} for t in blocked],
    }
# endregion


# region Promotion Evidence Report (JSON + Markdown)
# -----------------------------------------------------------------------------
# SECTION: Promotion Evidence Report
#
# WHAT
# promotion_evidence_report() produces:
# - a structured JSON report for export
# - a Markdown narrative for easy reading and sharing
#
# WHY
# This is the core differentiator vs. a normal to-do list:
# it organizes accomplishments by promotion criteria categories.
#
# INPUTS
# - tasks: current task state (each task carries its evidence narrative)
# - metrics: derived metrics bundle (counts, top tags, completion rate, etc.)
#
# OUTPUTS
# - report_json: structured data for machine use / exporting
# - markdown: human readable report suitable for GitHub or docs
#
# NOTE ON ORDERING
# Within each category:
# - flagship work first
# - completed work before open work
# - earlier created tasks first
# -----------------------------------------------------------------------------
def promotion_evidence_report(tasks: List[Dict[str, Any]], metrics: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    """
    Build promotion evidence report in JSON and Markdown.

    Parameters
    ----------
    tasks : list[dict]
        Current task state.

    metrics : dict
        Derived metrics bundle (from compute_derived_metrics()).

    Returns
    -------
    tuple[dict, str]
        (report_json, markdown_text)
    """
    by_cat: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for t in tasks:
        cat = t.get("impact_category") or "uncategorized"
        by_cat[cat].append(t)

    def sort_key(t: Dict[str, Any]):
        flagship = 0 if t.get("priority") == "⭐ major initiative" else 1
        completed = 0 if t.get("status") == "completed" else 1
        created = t.get("created_at") or ""
        return (flagship, completed, created)

    for cat in by_cat:
        by_cat[cat].sort(key=sort_key)

    report_json = {
        "generated_at": now_iso(),
        "executive_summary": {
            "total_tasks": len(tasks),
            "flagship_work_count": metrics.get("flagship_work_count", 0),
            "completion_rate": metrics.get("completion_rate", 0.0),
            "top_tags": metrics.get("top_tags", []),
        },
        "sections": {
            cat: [
                {
                    "id": t["id"],
                    "title": t["title"],
                    "problem": t["problem"],
                    "action": t["action"],
                    "impact": t["impact"],
                    "metrics": t["metrics"],
                    "evidence": t["evidence"],
                    "tags": t.get("tags", []),
                    "priority": t.get("priority"),
                    "status": t.get("status"),
                    "created_at": t.get("created_at"),
                    "completed_at": t.get("completed_at"),
                }
                for t in by_cat.get(cat, [])
            ]
            for cat in IMPACT_CATEGORIES
        },
    }

    # ---- Markdown rendering ---------------------------------------------------
    md: List[str] = []
    md.append("# Promotion Evidence Report\n")
    md.append(f"_Generated: {report_json['generated_at']}_\n")

    md.append("## Executive Summary")
    md.append(f"- Total tasks logged: **{len(tasks)}**")
    md.append(f"- Flagship work (⭐): **{metrics.get('flagship_work_count', 0)}**")
    md.append(f"- Completion rate: **{metrics.get('completion_rate', 0.0)}**")

    top_tags = metrics.get("top_tags", [])
    if top_tags:
        md.append("- Top tags: " + ", ".join([f"`{t}` ({c})" for t, c in top_tags[:8]]))
    md.append("")

    md.append("## Evidence by Promotion Criteria\n")
    for cat in IMPACT_CATEGORIES:
        md.append(f"### {cat}")
        items = by_cat.get(cat, [])
        if not items:
            md.append("_No entries yet._\n")
            continue

        for t in items:
            md.append(f"- **{t['title']}** (id={t['id']}) — {t.get('priority')} — {t.get('status')}")
            md.append(f"  - Problem: {t.get('problem')}")
            md.append(f"  - Action: {t.get('action')}")
            md.append(f"  - Impact: {t.get('impact')}")
            md.append(f"  - Metrics: {t.get('metrics')}")
            md.append(f"  - Evidence: {t.get('evidence')}")
            tags = t.get("tags", [])
            if tags:
                md.append(f"  - Tags: {' '.join(tags)}")
        md.append("")

    return report_json, "\n".join(md).rstrip() + "\n"
# endregion


# region Report Bundling (One Export Payload)
# -----------------------------------------------------------------------------
# SECTION: Report Bundling
#
# WHAT
# build_reports_bundle() composes all reports into one JSON object.
#
# WHY
# storage.py exports a single reports.json and reports.md per run.
# This function centralizes what "reports" means.
# -----------------------------------------------------------------------------
def build_reports_bundle(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build all reports in one JSON bundle.

    Parameters
    ----------
    tasks : list[dict]
        Current task state.

    events : list[dict]
        Event log.

    Returns
    -------
    dict
        JSON-serializable bundle containing all reports and metrics.
    """
    metrics = compute_derived_metrics(tasks, events)
    return {
        "generated_at": now_iso(),
        "daily_summary": daily_summary(tasks),
        "weekly_accomplishments": weekly_accomplishments(tasks, days=7),
        "standup": standup_report(tasks),
        "promotion_evidence": promotion_evidence_report(tasks, metrics)[0],
        "metrics": metrics,
    }
# endregion


# region Markdown Export (Daily/Weekly/Standup)
# -----------------------------------------------------------------------------
# SECTION: Markdown Export
#
# WHAT
# reports_to_markdown() converts the daily/weekly/standup sections into a
# human-readable Markdown document.
#
# WHY
# This is the "Reported" part of the pipeline:
# - a user can open outputs/reports.md in GitHub and read it easily
# - no special tools required
#
# NOTE
# Promotion report markdown is exported separately (promotion_report.md).
# -----------------------------------------------------------------------------
def reports_to_markdown(reports: Dict[str, Any]) -> str:
    """
    Convert daily/weekly/standup into readable Markdown.

    Parameters
    ----------
    reports : dict
        JSON bundle produced by build_reports_bundle().

    Returns
    -------
    str
        Markdown document.
    """
    md: List[str] = []
    md.append("# Impact Reports\n")
    md.append(f"_Generated: {reports.get('generated_at')}_\n")

    # ---- Daily ---------------------------------------------------------------
    d = reports.get("daily_summary", {})
    md.append("## Daily Summary")
    md.append(f"- Date: **{d.get('date')}**")
    md.append(f"- Completed today: **{d.get('completed_count', 0)}**")
    for t in d.get("completed_tasks", []):
        md.append(f"  - {t.get('title')} (id={t.get('id')})")
    md.append("")

    # ---- Weekly --------------------------------------------------------------
    w = reports.get("weekly_accomplishments", {})
    md.append("## Weekly Accomplishments")
    md.append(f"- Window: last **{w.get('window_days', 7)}** days")
    md.append(f"- Completed: **{w.get('completed_count', 0)}**")
    for t in w.get("completed_tasks", []):
        md.append(f"  - {t.get('title')} (id={t.get('id')}) — Metrics: {t.get('metrics')}")
    md.append("")

    # ---- Standup -------------------------------------------------------------
    s = reports.get("standup", {})
    md.append("## Standup")

    md.append("### Yesterday I completed")
    if s.get("yesterday_completed"):
        for t in s["yesterday_completed"]:
            md.append(f"- {t['title']} (id={t['id']})")
    else:
        md.append("_None._")
    md.append("")

    md.append("### Today I am working on")
    if s.get("today_working_on"):
        for t in s["today_working_on"]:
            md.append(f"- {t['title']} (id={t['id']}) — {t.get('priority')}")
    else:
        md.append("_None._")
    md.append("")

    md.append("### Blocked by")
    if s.get("blocked_by"):
        for t in s["blocked_by"]:
            md.append(f"- {t['title']} (id={t['id']})")
    else:
        md.append("_None._")
    md.append("")

    return "\n".join(md).rstrip() + "\n"
# endregion