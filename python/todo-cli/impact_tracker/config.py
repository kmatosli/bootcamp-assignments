"""
FILE: impact_tracker/config.py

PURPOSE
Central configuration for the Impact Tracker CLI.

WHY THIS FILE EXISTS
This module is the single source of truth for values that must stay consistent
across the application (menu labels, priority meanings, status values, and
promotion-aligned impact categories).

Keeping these values here prevents "string drift" where different parts of the
code silently diverge (e.g., one module uses "completed" while another uses
"done").

HOW THIS MODULE IS USED
- cli.py displays labels to users (priority menu, categories list)
- validators.py validates user input against allowed values
- services.py and reporting.py rely on consistent strings to drive logic
- storage.py uses OUTPUT_DIR to know where to write exported artifacts

INVARIANTS
- OUTPUT_DIR is a relative path (project-local outputs)
- Priority values are keyed by menu choice ("1", "2", "3")
- Status values are stable tokens used for comparisons and reporting
- Impact categories are stable promotion criteria labels

NOTE ON EDITING
If you change a label here, you may also need to adjust:
- validators that check exact values
- reporting logic that groups/sorts by category/priority
"""

# region Output Configuration
# -----------------------------------------------------------------------------
# SECTION: Output Configuration
#
# WHAT
# - OUTPUT_DIR: folder where JSON/Markdown exports are written.
#
# WHY
# Keeping export paths centralized makes the app predictable and easy to run
# from different working directories (and easier to explain in README).
# -----------------------------------------------------------------------------
OUTPUT_DIR: str = "outputs"
# endregion


# region Enumerations: Priority
# -----------------------------------------------------------------------------
# SECTION: Priority Levels
#
# WHAT
# - PRIORITY_LEVELS: menu choice -> user-facing label
#
# WHY
# Priority expresses "significance" of work so reports can highlight flagship
# initiatives vs routine maintenance. The labels are deliberately user-facing.
#
# INVARIANT
# Keys remain "1", "2", "3" because the CLI prompts for numeric menu input.
# -----------------------------------------------------------------------------
PRIORITY_LEVELS: dict[str, str] = {
    "1": "⭐ major initiative",
    "2": "⬆ significant improvement",
    "3": "• routine work",
}
# endregion


# region Enumerations: Status
# -----------------------------------------------------------------------------
# SECTION: Status Levels
#
# WHAT
# - STATUS_LEVELS: set of allowed task statuses
#
# WHY
# Status is used by reporting to determine what's completed vs still open.
#
# INVARIANT
# The tokens here are expected to be stable across the whole app.
# -----------------------------------------------------------------------------
STATUS_LEVELS: set[str] = {"open", "completed"}
# endregion


# region Enumerations: Impact Categories
# -----------------------------------------------------------------------------
# SECTION: Impact Categories (Promotion Criteria)
#
# WHAT
# - IMPACT_CATEGORIES: list of category tokens used to group tasks in reports
#
# WHY
# These map directly to promotion review criteria so the system can generate
# a "promotion evidence report" automatically over time.
#
# INVARIANT
# Values are treated as canonical identifiers. If you rename one, also update:
# - any validation logic that checks exact matches
# - any report templates that print category headings
# -----------------------------------------------------------------------------
IMPACT_CATEGORIES: list[str] = [
    "impact_results",
    "leadership",
    "process_improvement",
    "cross_team_influence",
    "innovation",
    "recognition",
    "metrics",
]
# endregion