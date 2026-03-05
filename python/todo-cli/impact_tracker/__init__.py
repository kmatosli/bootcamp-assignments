"""
Impact Tracker Package
======================

A CLI-based personal impact tracking system designed to capture, structure,
and report professional accomplishments over time.

Conceptual Pipeline
-------------------
The application models work as a simple data pipeline:

    Work → Logged → Structured → Quantified → Reported

1. Work is recorded as tasks.
2. Tasks generate events (an append-only activity log).
3. Reports derive metrics and summaries from those events.
4. Results are exported as JSON and Markdown artifacts.

This approach mirrors real-world analytics systems where raw activity
logs become the source of truth for metrics and reporting.

Architecture Overview
---------------------
The package is organized into clear responsibility layers:

    config.py
        Constants and enumerations used across the system.

    validators.py
        Input validation and normalization.

    models.py
        Builders for structured task and event objects.

    services.py
        State transitions and event emission.

    reporting.py
        Derived metrics and structured reports.

    storage.py
        Export layer for JSON and Markdown outputs.

    utils.py
        Shared helpers (timestamps, file I/O, formatting).

Design Principles
-----------------
- Event-driven architecture (append-only event log)
- Clear separation of concerns between modules
- Deterministic report generation
- Human-readable output artifacts

Typical Outputs
---------------
Running the tracker generates artifacts under `./outputs/`:

    event_log.json
        Full append-only history of user actions.

    metrics.json
        Derived analytics from the event stream.

    promotion_report.md
        Structured narrative suitable for performance reviews.

    reports.json / reports.md
        Additional summaries (daily, weekly, standup).

Primary Use Case
----------------
Help professionals track and present evidence of impact for:

- promotion packets
- performance reviews
- leadership reporting
- personal productivity analysis
"""