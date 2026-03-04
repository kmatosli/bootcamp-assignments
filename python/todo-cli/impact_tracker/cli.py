from __future__ import annotations

from typing import Any, Dict, List

from impact_tracker.config import IMPACT_CATEGORIES, PRIORITY_LEVELS, OUTPUT_DIR
from impact_tracker.models import build_task
from impact_tracker.services import (
    add_task,
    complete_task,
    delete_task,
    emit_event,
    next_task_id,
    record_view,
)
from impact_tracker.storage import export_outputs
from impact_tracker.validators import (
    validate_impact_category,
    validate_menu_choice,
    validate_non_empty,
    validate_priority,
    validate_tags,
    validate_task_id,
)
from impact_tracker.utils import write_json
import os


# =============================================================================
# Section: CLI Layer
# =============================================================================

def print_header() -> None:
    print("\n" + "=" * 72)
    print("Impact Tracker — Work → Logged → Structured → Quantified → Reported")
    print("=" * 72)


def print_menu() -> None:
    print("\nMain Menu")
    print("1) Add task")
    print("2) View tasks")
    print("3) Delete task")
    print("4) Quit")


def prompt_required(label: str) -> str:
    """
    Prompt until non-empty.
    Uses try/except/else/finally for assignment compliance.
    """
    while True:
        try:
            raw = input(f"{label}: ")
            value = validate_non_empty(label, raw)
        except ValueError as e:
            print(f"  ❌ {e}")
        else:
            return value
        finally:
            # minimal finally for assignment requirement visibility
            pass


def prompt_priority() -> str:
    print("\nPriority")
    for k, v in PRIORITY_LEVELS.items():
        print(f"{k}) {v}")

    while True:
        try:
            raw = input("Choose priority (1/2/3): ")
            pr = validate_priority(raw)
        except ValueError as e:
            print(f"  ❌ {e}")
        else:
            return pr
        finally:
            pass


def prompt_impact_category() -> str:
    print("\nImpact Categories (promotion criteria)")
    for cat in IMPACT_CATEGORIES:
        print(f"- {cat}")

    while True:
        try:
            raw = input("Choose impact category (type exact value): ")
            cat = validate_impact_category(raw)
        except ValueError as e:
            print(f"  ❌ {e}")
        else:
            return cat
        finally:
            pass


def prompt_tags() -> List[str]:
    raw = input("Tags (e.g., #automation #leadership) (optional): ")
    return validate_tags(raw)


def print_task(t: Dict[str, Any]) -> None:
    print("-" * 72)
    print(f"ID: {t['id']} | {t['title']}")
    print(f"Status: {t.get('status')} | Priority: {t.get('priority')} | Category: {t.get('impact_category')}")
    print(f"Created: {t.get('created_at')} | Completed: {t.get('completed_at')}")
    tags = t.get("tags", [])
    if tags:
        print(f"Tags: {' '.join(tags)}")
    print(f"Problem: {t.get('problem')}")
    print(f"Action: {t.get('action')}")
    print(f"Impact: {t.get('impact')}")
    print(f"Metrics: {t.get('metrics')}")
    print(f"Evidence: {t.get('evidence')}")


def add_task_cli(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    print("\nAdd Task — capture evidence of impact")
    title = prompt_required("Title")
    problem = prompt_required("Problem / context (why it mattered)")
    action = prompt_required("Action (what you did)")
    impact = prompt_required("Impact (who benefited + outcome)")
    metrics = prompt_required("Measurable impact (numbers, scale, time saved, risk reduced)")
    evidence = prompt_required("Evidence (links, docs, PRs, emails, dashboards)")
    tags = prompt_tags()
    priority = prompt_priority()
    impact_category = prompt_impact_category()

    tid = next_task_id(tasks)
    task = build_task(
        task_id=tid,
        title=title,
        problem=problem,
        action=action,
        impact=impact,
        metrics=metrics,
        evidence=evidence,
        tags=tags,
        priority=priority,
        impact_category=impact_category,
    )

    add_task(tasks, events, task)
    print(f"\n✅ Added task id={tid}")


def view_tasks_cli(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    record_view(events)

    if not tasks:
        print("\n(No tasks yet. Add one to start building your promotion case.)")
        return

    print("\nTasks")
    for t in sorted(tasks, key=lambda x: x["id"]):
        print_task(t)

    print("\nOptional action: mark a task completed.")
    print("Enter a task id to complete, or press Enter to return to menu.")
    raw = input("Complete task id: ").strip()
    if not raw:
        return

    try:
        task_id = validate_task_id(raw, tasks)
        complete_task(tasks, events, task_id)
    except ValueError as e:
        print(f"  ❌ {e}")
    else:
        print(f"✅ Marked task id={task_id} as completed.")
    finally:
        pass


def delete_task_cli(tasks: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    if not tasks:
        print("\n(No tasks to delete.)")
        return

    print("\nDelete Task")
    print("Existing task ids: " + ", ".join(str(t["id"]) for t in sorted(tasks, key=lambda x: x["id"])))

    while True:
        try:
            raw = input("Enter task id to delete (or press Enter to cancel): ").strip()
            if not raw:
                return
            task_id = validate_task_id(raw, tasks)
        except ValueError as e:
            print(f"  ❌ {e}")
        else:
            delete_task(tasks, events, task_id)
            print(f"✅ Deleted task id={task_id}")
            return
        finally:
            pass


def main() -> None:
    """
    Application entry point.

    Assignment requirement: tasks stored in a Python list (in-memory).
    Enhancement: events stored in append-only Python list (in-memory).
    """
    tasks: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []

    emit_event(events, "APP_STARTED", None, {"version": "1.0", "notes": "Impact tracker started"})

    try:
        while True:
            print_header()
            print_menu()

            try:
                choice = input("\nChoose an option (1-4): ")
                choice = validate_menu_choice(choice, ["1", "2", "3", "4"])
            except ValueError as e:
                print(f"  ❌ {e}")
                continue
            else:
                if choice == "1":
                    add_task_cli(tasks, events)
                elif choice == "2":
                    view_tasks_cli(tasks, events)
                elif choice == "3":
                    delete_task_cli(tasks, events)
                elif choice == "4":
                    emit_event(events, "APP_QUIT", None, {"reason": "user_exit"})
                    break
            finally:
                # minimal finally, visible for the assignment
                pass
    finally:
        # Always export on exit (even if unexpected error).
        try:
            export_outputs(tasks, events)
            emit_event(events, "OUTPUTS_EXPORTED", None, {"dir": OUTPUT_DIR})
            # Re-write event log so it includes OUTPUTS_EXPORTED
            write_json(os.path.join(OUTPUT_DIR, "event_log.json"), {"events": events})
        except Exception as e:
            print(f"\n⚠️ Failed to export outputs: {e}")

        print(f"\nDone. Exports written to ./{OUTPUT_DIR}/")