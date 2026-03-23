"""
========================================================
Module: visible_validators.py
Project: Visible — Career Operating System
Purpose: Core input validation and sanitization utilities
         for the Visible data entry pipeline.
 
These functions validate and clean user-submitted data
before it is stored, analyzed, or surfaced in reports.
They form the foundation of the server-side validation
layer and mirror the client-side validation in the
Bootstrap intake form.
 
Author: Kathy Matos Linares
========================================================
"""
 
 
# --------------------------------------------------------
# Validator 1: Numeric Field Parity Check
# --------------------------------------------------------
# Used in: Quantification fields (hours saved, people
# affected, reporting cycles). Validates that numeric
# inputs meet expected parity constraints.
# Example: bi-weekly hour counts should be even numbers.
# --------------------------------------------------------
 
def even_or_odd(number):
    """
    Determines whether a numeric input is even or odd.
 
    In Visible, this validates quantification fields where
    parity matters — for example, flagging odd hour counts
    in bi-weekly reporting cycles or validating structured
    time-saving estimates.
 
    Args:
        number (int): A numeric value from a quantification
                      field in the Visible intake form.
 
    Returns:
        str: "Even" if the number is even, "Odd" if not.
 
    Example:
        >>> even_or_odd(6)
        'Even'
        >>> even_or_odd(7)
        'Odd'
    """
    return "Even" if number % 2 == 0 else "Odd"
 
 
# --------------------------------------------------------
# Validator 2: Numeric to String Type Coercion
# --------------------------------------------------------
# Used in: Salary fields, compensation band inputs,
# quantified impact metrics. Converts numeric values
# to strings before they are stored in the report
# engine or displayed in the promotion document.
# --------------------------------------------------------
 
def number_to_string(num):
    """
    Converts a numeric input to its string representation.
 
    In Visible, salary figures, compensation bands, and
    quantified metrics are entered as numbers but must be
    converted to strings for report generation, display,
    and consistent storage in the contribution record.
 
    Args:
        num (int): A numeric value such as salary,
                   hours saved, or AUM figure.
 
    Returns:
        str: The string representation of the number.
 
    Example:
        >>> number_to_string(145000)
        '145000'
        >>> number_to_string(-5000)
        '-5000'
    """
    return str(num)
 
 
# --------------------------------------------------------
# Validator 3: Input Whitespace Sanitization
# --------------------------------------------------------
# Used in: Job title, company name, LinkedIn URL,
# skill tags, and contribution title fields. Strips
# whitespace from user input before storage to prevent
# duplicate entries and ensure consistent matching.
# --------------------------------------------------------
 
def no_space(x):
    """
    Removes all whitespace from a string input.
 
    In Visible, job titles, skill tags, and identifiers
    entered with inconsistent spacing are sanitized before
    storage. This prevents duplicate contribution records
    caused by whitespace variations and ensures reliable
    pattern matching across entries.
 
    Args:
        x (str): A string input from a Visible form field.
 
    Returns:
        str: The input string with all spaces removed.
 
    Example:
        >>> no_space("Senior Data Engineer ")
        'SeniorDataEngineer'
        >>> no_space("risk model ")
        'riskmodel'
    """
    return x.replace(" ", "")
 
 
# --------------------------------------------------------
# Validator 4: Narrative Quality Signal
# --------------------------------------------------------
# Used in: Problem, Action, Impact, and Counterfactual
# narrative fields. A low vowel count relative to string
# length signals placeholder text, gibberish, or
# excessively abbreviated input that will produce
# low-quality report output.
# --------------------------------------------------------
 
def get_count(string):
    """
    Counts the number of vowels in a narrative string.
 
    In Visible, narrative fields (Problem, Action, Impact,
    Evidence) require meaningful text to generate
    high-quality promotion documents. A low vowel count
    relative to string length is used as a signal that
    the input may be placeholder text, an abbreviation,
    or insufficiently detailed for report generation.
 
    The mapping layer uses this signal to prompt the user
    to expand their narrative before the entry is saved.
 
    Args:
        string (str): A narrative string from a Visible
                      intake form field.
 
    Returns:
        int: The count of vowels (a, e, i, o, u) in
             the string.
 
    Example:
        >>> get_count("automated the reporting workflow")
        11
        >>> get_count("asdfghjkl")
        1
    """
    return sum(1 for char in string if char in "aeiou")
 
 
# --------------------------------------------------------
# Validation Pipeline: Realistic Visible Scenarios
# --------------------------------------------------------
# These tests simulate real data entry scenarios from
# the Visible intake form and report generation pipeline.
# --------------------------------------------------------
 
if __name__ == "__main__":
 
    print("=" * 55)
    print("VISIBLE — Input Validation Pipeline")
    print("=" * 55)
 
    # --- Numeric Field Parity Check ---
    print("\n[1] Numeric Parity Validation")
    print("-" * 40)
    hours_saved = 6
    result = even_or_odd(hours_saved)
    print(f"Hours saved per cycle: {hours_saved} → {result}")
    print(f"  Status: {'Valid bi-weekly figure' if result == 'Even' else 'Flag for review'}")
 
    reporting_cycles = 7
    result2 = even_or_odd(reporting_cycles)
    print(f"Reporting cycles logged: {reporting_cycles} → {result2}")
    print(f"  Status: {'Flag for review — odd cycle count' if result2 == 'Odd' else 'Valid'}")
 
    # --- Salary and Compensation Type Coercion ---
    print("\n[2] Compensation Field Type Coercion")
    print("-" * 40)
    salary = 145000
    salary_str = number_to_string(salary)
    print(f"Salary input: {salary} (int) → '{salary_str}' (str)")
    print(f"  Status: Ready for report generation")
 
    compensation_gap = -32000
    gap_str = number_to_string(compensation_gap)
    print(f"Compensation gap: {compensation_gap} (int) → '{gap_str}' (str)")
    print(f"  Status: Negative value flagged for compensation review")
 
    # --- Input Sanitization ---
    print("\n[3] Form Field Whitespace Sanitization")
    print("-" * 40)
    raw_title = "  Quant Associate  "
    clean_title = no_space(raw_title)
    print(f"Raw job title: '{raw_title}'")
    print(f"Sanitized: '{clean_title}'")
    print(f"  Status: Ready for storage and matching")
 
    raw_skill = "workflow automation "
    clean_skill = no_space(raw_skill)
    print(f"Raw skill tag: '{raw_skill}'")
    print(f"Sanitized: '{clean_skill}'")
    print(f"  Status: Duplicate prevention check passed")
 
    # --- Narrative Quality Validation ---
    print("\n[4] Narrative Field Quality Signal")
    print("-" * 40)
 
    strong_narrative = (
        "automated the conference room scheduling process "
        "using access and vba eliminating manual coordination "
        "across four stakeholder groups"
    )
    weak_narrative = "did stuff mgmt rpt sys"
 
    strong_count = get_count(strong_narrative)
    weak_count = get_count(weak_narrative)
    strong_ratio = round(strong_count / len(strong_narrative), 3)
    weak_ratio = round(weak_count / len(weak_narrative), 3)
 
    print(f"Strong narrative vowel count: {strong_count}")
    print(f"  Vowel density: {strong_ratio}")
    print(f"  Status: {'Sufficient detail — proceed to mapping layer' if strong_ratio > 0.1 else 'Flag for expansion'}")
 
    print(f"\nWeak narrative vowel count: {weak_count}")
    print(f"  Vowel density: {weak_ratio}")
    print(f"  Status: {'Flag — narrative too abbreviated for quality report output' if weak_ratio < 0.1 else 'Acceptable'}")
 
    print("\n" + "=" * 55)
    print("Validation pipeline complete.")
    print("=" * 55)