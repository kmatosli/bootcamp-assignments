# Impact Tracker CLI (Maintainable Bootcamp Project)

A terminal-based **personal impact tracking system** — not a basic to-do list.

It treats your work like a data pipeline:

**Work → Logged → Structured → Quantified → Reported**

The goal is to continuously build **promotion-ready evidence** while you work.

---

## What you get in 5 minutes (demo value)

- Log work with **impact + metrics + evidence**
- Produce **promotion-ready artifacts** automatically:
  - `outputs/promotion_report.md`
  - `outputs/metrics.json`
  - `outputs/event_log.json`

---

## Bootcamp requirements satisfied

- Runs in the terminal
- Stores tasks in a **Python list** (in-memory)
- Supports:
  1. Add tasks
  2. View tasks
  3. Delete tasks
  4. Quit
- Uses:
  - `input()`
  - `try/except/else/finally`
  - functions
  - input validation

---

## Event sourcing (why it matters)

In addition to the `tasks` list, the app maintains an **append-only `events` list**.

Every user action:

1. appends an event dict to `events`
2. updates the `tasks` list (current state)
3. enables reports/metrics derived from the event history

Pipeline concept:

**User action → event recorded → state updated → reports/metrics generated**

Benefits:

- audit trail (history never overwritten)
- reproducible metrics (can be rebuilt from events)
- scalable foundation for future features

---

## Exports (auto-generated on quit)

On exit, the app writes to `./outputs/`:

Required:

- `outputs/event_log.json`
- `outputs/metrics.json`
- `outputs/promotion_report.md`

Also included:

- `outputs/reports.json`
- `outputs/reports.md`

---

## How to run

```bash
python impact_tracker.py
```
