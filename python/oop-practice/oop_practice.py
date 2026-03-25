# ============================================================
# Visible — Contribution Intelligence Engine
# OOP Python Practice Assignment
# Coding Temple Advanced Python Module
#
# This module implements core domain objects for Visible,
# a career decision intelligence platform. It demonstrates
# OOP concepts using real product domain models.
#
# Domain model:
#   ContributionEntry — a single documented work contribution
#
# OOP concepts demonstrated:
#   - Class definition with __init__, methods, attributes
#   - Object instantiation and interaction
#   - Dictionary and set integration
#   - Tuple immutability
#   - List operations
#   - Bonus: regex validation
# ============================================================

import re
from datetime import date


# ============================================================
# PART 1: CLASS DEFINITION
# ============================================================

class ContributionEntry:
    """
    Represents a single documented work contribution in Visible.

    In the real Visible app, users document their contributions
    to build evidence for promotion conversations, compensation
    negotiations, and departure decisions.

    Attributes:
        title (str):          Short description of the contribution
        category (str):       Type of contribution (revenue, process, etc.)
        impact_scores (list): List of integer impact scores (0-100)
                              where 100 = highest organizational impact
    """

    # Valid contribution categories for the Visible platform
    VALID_CATEGORIES = {
        "revenue",      # Directly connected to revenue generation
        "process",      # Process improvement or automation
        "leadership",   # Team development, mentoring, managing up
        "strategic",    # Long-term, above-scope contributions
        "invisible",    # Operational work that holds things together
    }

    def __init__(self, title, category, impact_scores):
        """
        Initialize a ContributionEntry.

        Args:
            title (str):          Contribution title
            category (str):       Contribution category
            impact_scores (list): Initial list of impact scores (0-100)
        """
        self.title = title
        self.category = category.lower()
        self.impact_scores = impact_scores    # Mutable list
        self.max_impact = 100
        self.date_created = date.today()

    def add_impact_score(self, score):
        """
        Add a new impact score to this contribution entry.
        Scores represent how strongly this contribution
        demonstrated organizational impact.

        Args:
            score (int): Impact score between 0 and 100
        """
        if not 0 <= score <= 100:
            print(f"  Score {score} out of range. Must be 0-100.")
            return
        self.impact_scores.append(score)
        print(f"  Added impact score {score} to '{self.title}'")

    def average_impact(self):
        """
        Calculate the average impact score for this contribution.
        Used in Visible to assess the strength of the contribution
        as evidence in a promotion or compensation conversation.

        Returns:
            float: Average impact score, or 0 if no scores exist
        """
        if not self.impact_scores:
            return 0.0
        return sum(self.impact_scores) / len(self.impact_scores)

    def display_entry(self):
        """
        Print a formatted summary of this contribution entry.
        """
        print(f"\n  Title:    {self.title}")
        print(f"  Category: {self.category.upper()}")
        print(f"  Scores:   {self.impact_scores}")
        print(f"  Average:  {self.average_impact():.1f} / 100")
        print(f"  Signal:   {self.promotion_signal()}")

    def impact_snapshot(self):
        """
        Return the impact scores as an immutable tuple.
        Used when passing scores to a report generator that
        should not modify the original entry data.

        Returns:
            tuple: Impact scores as an immutable sequence
        """
        return tuple(self.impact_scores)

    def promotion_signal(self):
        """
        Assess whether this contribution is strong enough
        to use as promotion evidence.

        Returns:
            str: Signal level
        """
        avg = self.average_impact()
        if avg >= 80:
            return "Strong — use as lead evidence"
        elif avg >= 60:
            return "Moderate — use as supporting evidence"
        else:
            return "Weak — needs stronger documentation"


# ============================================================
# PART 2: WORKING WITH OBJECTS
# ============================================================

print("=" * 55)
print("PART 2: Creating Contribution Entry Objects")
print("=" * 55)

# Create 3 ContributionEntry objects representing real
# career contributions a Visible user might document

entry1 = ContributionEntry(
    title="Automated monthly reconciliation process",
    category="process",
    impact_scores=[85, 90, 88]
)

entry2 = ContributionEntry(
    title="Closed Q3 enterprise deal — $2.4M ARR",
    category="revenue",
    impact_scores=[95, 92, 98]
)

entry3 = ContributionEntry(
    title="Onboarded and mentored 3 new analysts",
    category="leadership",
    impact_scores=[72, 68, 75]
)

# Add 2 new impact scores to each entry
print("\nAdding impact scores to each entry:")
entry1.add_impact_score(92)
entry1.add_impact_score(87)

entry2.add_impact_score(99)
entry2.add_impact_score(94)

entry3.add_impact_score(80)
entry3.add_impact_score(77)

# Print full info for each entry
print("\nContribution Record:")
entry1.display_entry()
entry2.display_entry()
entry3.display_entry()


# ============================================================
# PART 3: DICTIONARY & SET INTEGRATION
# ============================================================

print("\n" + "=" * 55)
print("PART 3: Dictionary and Set Integration")
print("=" * 55)

# Dictionary mapping each entry title to its ContributionEntry object
contribution_dict = {
    entry1.title: entry1,
    entry2.title: entry2,
    entry3.title: entry3,
}

def get_entry_by_title(title):
    """
    Safely retrieve a contribution entry from the dictionary.
    Uses .get() to avoid KeyError if title is not found.

    Args:
        title (str): Contribution title to look up

    Returns:
        ContributionEntry or None
    """
    entry = contribution_dict.get(title)
    if entry:
        print(f"\n  Found: '{entry.title}' [{entry.category}]")
    else:
        print(f"\n  No entry found: '{title}'")
    return entry

# Demonstrate lookup with valid and invalid titles
print("\nLooking up entries by title:")
get_entry_by_title("Closed Q3 enterprise deal — $2.4M ARR")
get_entry_by_title("Gave a presentation to leadership")

# Set of all unique impact scores across all entries
all_scores = set(
    entry1.impact_scores +
    entry2.impact_scores +
    entry3.impact_scores
)
print(f"\n  All unique impact scores: {sorted(all_scores)}")
print(f"  Total unique values: {len(all_scores)}")

# Set of categories documented vs categories not yet documented
all_categories = {entry.category for entry in [entry1, entry2, entry3]}
print(f"\n  Categories documented:     {all_categories}")
print(f"  Categories not documented: "
      f"{ContributionEntry.VALID_CATEGORIES - all_categories}")


# ============================================================
# PART 4: TUPLE PRACTICE
# ============================================================

print("\n" + "=" * 55)
print("PART 4: Tuple Practice — Immutable Impact Snapshots")
print("=" * 55)

# Get impact scores as immutable tuples
# Snapshots passed to report generators cannot modify source data
snapshot1 = entry1.impact_snapshot()
snapshot2 = entry2.impact_snapshot()
snapshot3 = entry3.impact_snapshot()

print(f"\n  Entry 1 snapshot: {snapshot1}")
print(f"  Entry 2 snapshot: {snapshot2}")
print(f"  Entry 3 snapshot: {snapshot3}")

# Demonstrate that tuples are immutable
print("\n  Demonstrating immutability:")
try:
    snapshot1[0] = 99    # This raises TypeError
except TypeError as e:
    print(f"  TypeError caught: {e}")
    print("  Source data is protected. Snapshots are read-only.")


# ============================================================
# PART 5: LIST OPERATIONS
# ============================================================

print("\n" + "=" * 55)
print("PART 5: List Operations")
print("=" * 55)

all_entries = [entry1, entry2, entry3]

# Remove last impact score using .pop()
print("\nRemoving last score from each entry using .pop():")
for entry in all_entries:
    removed = entry.impact_scores.pop()
    print(f"  '{entry.title[:40]}' — removed {removed}")

# Access first and last score using indexing
print("\nFirst and last score per entry:")
for entry in all_entries:
    first = entry.impact_scores[0]     # Index 0
    last  = entry.impact_scores[-1]    # Index -1
    print(f"  '{entry.title[:40]}' — first: {first}, last: {last}")

# Count remaining scores using len()
print("\nNumber of scores remaining per entry:")
for entry in all_entries:
    print(f"  '{entry.title[:40]}' — {len(entry.impact_scores)} scores")


# ============================================================
# PART 6: BONUS — Category Validation and Score Analysis
# ============================================================

print("\n" + "=" * 55)
print("PART 6: Bonus — Validation and Score Analysis")
print("=" * 55)

def validate_category(category):
    """
    Use regex to validate that a contribution category
    contains only lowercase letters, 3-20 characters.
    Mirrors validation in the real Visible API.

    Args:
        category (str): Category to validate

    Returns:
        tuple: (is_valid_format, is_known_category)
    """
    pattern = r'^[a-z]{3,20}$'
    is_valid = bool(re.match(pattern, category.lower()))
    is_known = category.lower() in ContributionEntry.VALID_CATEGORIES
    return is_valid, is_known

print("\nValidating contribution categories:")
test_categories = [
    "revenue", "process", "LEADERSHIP",
    "made up category", "strategic", "invisible", "123invalid"
]

for cat in test_categories:
    is_valid, is_known = validate_category(cat)
    fmt    = "valid format  " if is_valid else "invalid format"
    known  = "known"          if is_known else "unknown"
    print(f"  {cat:<30} {fmt} | {known}")

# Count scores above 90 — strongest promotion evidence
high_impact = [
    score
    for entry in all_entries
    for score in entry.impact_scores
    if score > 90
]

print(f"\n  Scores above 90 (strongest evidence): {len(high_impact)}")
print(f"  Values: {sorted(high_impact, reverse=True)}")

print("\n  Evidence strength by entry:")
for entry in all_entries:
    strong = [s for s in entry.impact_scores if s > 90]
    print(f"  '{entry.title[:40]}'")
    print(f"    Scores > 90: {strong} | {entry.promotion_signal()}")

print("\n" + "=" * 55)
print("Visible Contribution Intelligence — all parts complete.")
print("=" * 55)
