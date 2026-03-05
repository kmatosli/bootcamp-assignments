Impact Tracker CLI (Maintainable Bootcamp Project)

Python • CLI Application • Event-Sourced Reporting System

A terminal-based personal impact tracking system — not a basic to-do list.

It treats your work like a data pipeline:

Work → Logged → Structured → Quantified → Reported

The goal is to continuously build promotion-ready evidence while you work.

What you get in 5 minutes (demo value)

Log work with impact + metrics + evidence

Automatically produce promotion-ready artifacts:

outputs/promotion_report.md
outputs/metrics.json
outputs/event_log.json

This turns everyday work into structured documentation for performance reviews and promotion packets.

Bootcamp requirements satisfied

This project intentionally meets all bootcamp CLI requirements.

The application:

Runs entirely in the terminal

Stores tasks in a Python list (in-memory)

Supports:

Add tasks

View tasks

Delete tasks

Quit

The implementation demonstrates:

input() usage

try / except / else / finally

modular functions

structured validation logic

Event Sourcing (why it matters)

In addition to the tasks list, the app maintains an append-only events list.

Every user action:

appends an event to events

updates the tasks list (current state)

enables metrics and reports derived from the event history

Pipeline concept:

User action → event recorded → state updated → reports generated

Benefits:

audit trail — history is never overwritten

reproducible metrics — reports derived from event history

scalable architecture for future persistence or APIs

Architecture

The project is organized into small modules with clear responsibilities.

User Input (CLI)
↓
Validation Layer
↓
Service Layer (state changes + event emission)
↓
Event Log + Task State
↓
Reporting Layer (derived analytics)
↓
Storage Layer (export JSON + Markdown)

Design goals:

separation of concerns

event-driven analytics

deterministic reporting

maintainable code structure

Project Structure
impact_tracker/
│
├── **init**.py
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

Exports (auto-generated on quit)

When the application exits, it automatically writes outputs to:

./outputs/

Required artifacts:

outputs/event_log.json
outputs/metrics.json
outputs/promotion_report.md

Additional artifacts:

outputs/reports.json
outputs/reports.md

These files provide both machine-readable analytics and human-readable reports.

Why this project exists

Most task trackers only record what you did.

Impact Tracker focuses on evidence of impact:

the problem

the action taken

the measurable outcome

supporting evidence

This structure allows work captured throughout the year to automatically become promotion-ready documentation.
