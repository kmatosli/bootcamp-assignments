# Impact Tracker CLI (Maintainable Bootcamp Project)

**Python • CLI Application • Event-Sourced Reporting System**

A terminal-based personal impact tracking system — _not a basic to-do list_.

It treats your work like a data pipeline:

**Work → Logged → Structured → Quantified → Reported**

The goal is to continuously build promotion-ready evidence while you work.

## What You Get in 5 Minutes (Demo Value)

- Log work with impact + metrics + evidence
- Automatically produce promotion-ready artifacts:
  - `outputs/promotion_report.md`
  - `outputs/metrics.json`
  - `outputs/event_log.json`

This turns everyday work into structured documentation for performance reviews and promotion packets.

## Bootcamp Requirements Satisfied

This project intentionally meets all bootcamp CLI requirements.

The application:

- Runs entirely in the terminal
- Stores tasks in a Python list (in-memory)
- Supports:
  - Add tasks
  - View tasks
  - Delete tasks
  - Quit

The implementation demonstrates:

- `input()` usage
- `try` / `except` / `else` / `finally`
- Modular functions
- Structured validation logic

## Event Sourcing (Why It Matters)

In addition to the tasks list, the app maintains an append-only events list.

Every user action:

- Appends an event to events
- Updates the tasks list (current state)
- Enables metrics and reports derived from the event history

**Pipeline Concept:**

User action → event recorded → state updated → reports generated

**Benefits:**

- **Audit trail** — history is never overwritten
- **Reproducible metrics** — reports derived from event history
- **Scalable architecture** for future persistence or APIs

## Architecture

The project is organized into small modules with clear responsibilities.

impact_tracker/
│
├── init.py
│ Package description
│
├── cli.py
│ Terminal interface and user interaction
│
├── config.py
│ Shared constants and configuration
│
├── validators.py
│ Input validation and normalization
│
├── models.py
│ Builders for task and event objects
│
├── services.py
│ State mutations and event emission
│
├── reporting.py
│ Derived metrics and report generation
│
├── storage.py
│ Export layer for JSON and Markdown outputs
│
└── utils.py
Shared helpers (timestamps, file writing)

This layered structure keeps responsibilities isolated and makes the project easier to maintain or extend.

## Exports (Auto-Generated on Quit)

When the application exits, it automatically writes outputs to:

`./outputs/`

**Required Artifacts:**

- `outputs/event_log.json`
- `outputs/metrics.json`
- `outputs/promotion_report.md`

**Additional Artifacts:**

- `outputs/reports.json`
- `outputs/reports.md`

These files provide both machine-readable analytics and human-readable reports.

## Why This Project Exists

Most task trackers only record _what you did_.

Impact Tracker focuses on evidence of impact:

- The problem
- The action taken
- The measurable outcome
- Supporting evidence

This structure allows work captured throughout the year to automatically become promotion-ready documentation.
