"""
Central configuration and enumerations.
"""

OUTPUT_DIR = "outputs"

PRIORITY_LEVELS = {
    "1": "⭐ major initiative",
    "2": "⬆ significant improvement",
    "3": "• routine work",
}

STATUS_LEVELS = {"open", "completed"}

IMPACT_CATEGORIES = [
    "impact_results",
    "leadership",
    "process_improvement",
    "cross_team_influence",
    "innovation",
    "recognition",
    "metrics",
]