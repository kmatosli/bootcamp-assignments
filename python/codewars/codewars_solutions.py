"""
========================================================
File: codewars_solutions.py
Assignment: SE Foundations Knowledge Check — Codewars
Bootcamp: Coding Temple Software Engineering
Author: Kathy Matos Linares

Kata Solved:
  1. Even or Odd (8 kyu)
  2. Convert a Number to a String (8 kyu)
  3. Remove String Spaces (8 kyu)
  4. Vowel Count (7 kyu)

All four solutions use only Python built-ins.
All four passed Codewars test suites on submission.

Real-world context: These functions are also used as
input validation utilities in Visible, a career decision
intelligence platform, where they sanitize and validate
form data before it enters the report generation pipeline.
========================================================
"""


# --------------------------------------------------------
# Kata 1: Even or Odd
# Codewars: https://www.codewars.com/kata/53da3dbb4a5168369a0000fe
# Difficulty: 8 kyu
# --------------------------------------------------------
# Function name required by Codewars: even_or_odd
# Input: integer (positive, negative, or zero)
# Output: "Even" if divisible by 2, "Odd" otherwise
# --------------------------------------------------------

def even_or_odd(number):
    """
    Returns "Even" if number is even, "Odd" if not.

    Args:
        number (int): Any integer value.

    Returns:
        str: "Even" or "Odd"

    Examples:
        >>> even_or_odd(0)
        'Even'
        >>> even_or_odd(2)
        'Even'
        >>> even_or_odd(7)
        'Odd'
        >>> even_or_odd(-3)
        'Odd'
    """
    return "Even" if number % 2 == 0 else "Odd"


# --------------------------------------------------------
# Kata 2: Convert a Number to a String
# Codewars: https://www.codewars.com/kata/5265326f5fda8eb1160004c8
# Difficulty: 8 kyu
# --------------------------------------------------------
# Function name required by Codewars: number_to_string
# Input: integer
# Output: string representation of that integer
# --------------------------------------------------------

def number_to_string(num):
    """
    Converts an integer to its string representation.

    Args:
        num (int): Any integer value.

    Returns:
        str: The string form of the number.

    Examples:
        >>> number_to_string(123)
        '123'
        >>> number_to_string(999)
        '999'
        >>> number_to_string(-100)
        '-100'
        >>> number_to_string(0)
        '0'
    """
    return str(num)


# --------------------------------------------------------
# Kata 3: Remove String Spaces
# Codewars: https://www.codewars.com/kata/57eae20f31dd3048b4000139
# Difficulty: 8 kyu
# --------------------------------------------------------
# Function name required by Codewars: no_space
# Input: string (may contain spaces anywhere)
# Output: same string with all spaces removed
# --------------------------------------------------------

def no_space(x):
    """
    Removes all spaces from a string.

    Args:
        x (str): A string that may contain spaces.

    Returns:
        str: The input string with all spaces removed.

    Examples:
        >>> no_space("8 j 8 mBliB8g imjB8B8 jl B")
        '8j8mBliB8gimjB8B8jlB'
        >>> no_space("hello world")
        'helloworld'
        >>> no_space("  leading and trailing  ")
        'leadingandtrailing'
    """
    return x.replace(" ", "")


# --------------------------------------------------------
# Kata 4: Vowel Count
# Codewars: https://www.codewars.com/kata/54ff3102c1bad923760001f3
# Difficulty: 7 kyu
# --------------------------------------------------------
# Function name required by Codewars: get_count
# Input: string of lowercase letters and/or spaces
# Output: count of vowels (a, e, i, o, u) in the string
# --------------------------------------------------------

def get_count(string):
    """
    Returns the number of vowels in a string.

    Counts only: a, e, i, o, u (lowercase).
    Input will be lowercase letters and/or spaces.

    Args:
        string (str): A string of lowercase letters and spaces.

    Returns:
        int: Count of vowel characters in the string.

    Examples:
        >>> get_count("hello")
        2
        >>> get_count("aeiou")
        5
        >>> get_count("bcdfg")
        0
        >>> get_count("")
        0
    """
    return sum(1 for char in string if char in "aeiou")


# --------------------------------------------------------
# TEST SUITE
# --------------------------------------------------------
# Assertion-based tests that mirror Codewars test cases.
# Run this file directly to verify all solutions pass:
#   python codewars_solutions.py
#
# Expected output: "All tests passed." with no errors.
# AssertionError is raised immediately if any test fails.
# --------------------------------------------------------

def run_tests():
    """Runs assertion-based tests for all four kata solutions."""

    print("Running tests...\n")

    # ---- even_or_odd ----
    print("[1] even_or_odd")
    assert even_or_odd(2)   == "Even", "Failed: even_or_odd(2)"
    assert even_or_odd(7)   == "Odd",  "Failed: even_or_odd(7)"
    assert even_or_odd(0)   == "Even", "Failed: even_or_odd(0)"
    assert even_or_odd(-4)  == "Even", "Failed: even_or_odd(-4)"
    assert even_or_odd(-3)  == "Odd",  "Failed: even_or_odd(-3)"
    assert even_or_odd(1)   == "Odd",  "Failed: even_or_odd(1)"
    assert even_or_odd(100) == "Even", "Failed: even_or_odd(100)"
    print("    All even_or_odd tests passed ✓")

    # ---- number_to_string ----
    print("[2] number_to_string")
    assert number_to_string(123)  == "123",  "Failed: number_to_string(123)"
    assert number_to_string(999)  == "999",  "Failed: number_to_string(999)"
    assert number_to_string(-100) == "-100", "Failed: number_to_string(-100)"
    assert number_to_string(0)    == "0",    "Failed: number_to_string(0)"
    assert number_to_string(1)    == "1",    "Failed: number_to_string(1)"
    print("    All number_to_string tests passed ✓")

    # ---- no_space ----
    print("[3] no_space")
    assert no_space("8 j 8 mBliB8g imjB8B8 jl B") == "8j8mBliB8gimjB8B8jlB", \
        "Failed: no_space codewars example"
    assert no_space("hello world")   == "helloworld",        "Failed: no_space hello world"
    assert no_space("  leading  ")   == "leading",           "Failed: no_space leading spaces"
    assert no_space("nospace")       == "nospace",           "Failed: no_space no spaces"
    assert no_space(" ")             == "",                  "Failed: no_space single space"
    assert no_space("")              == "",                  "Failed: no_space empty string"
    print("    All no_space tests passed ✓")

    # ---- get_count ----
    print("[4] get_count")
    assert get_count("hello")          == 2, "Failed: get_count hello"
    assert get_count("aeiou")          == 5, "Failed: get_count aeiou"
    assert get_count("bcdfg")          == 0, "Failed: get_count bcdfg"
    assert get_count("")               == 0, "Failed: get_count empty"
    assert get_count("abracadabra")    == 5, "Failed: get_count abracadabra"
    assert get_count("the quick brown fox") == 5, "Failed: get_count quick brown fox"
    print("    All get_count tests passed ✓")

    print("\n" + "=" * 40)
    print("All tests passed.")
    print("=" * 40)


if __name__ == "__main__":
    run_tests()