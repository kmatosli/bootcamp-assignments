# Codewars Solutions — Python Kata

## Assignment

SE Foundations Knowledge Check: Embarking on Your Codewars Journey
Coding Temple Software Engineering Bootcamp

## Author

Kathy Matos Linares

## Kata Solved

| #   | Kata                         | Difficulty | Function           | Codewars Link                                          |
| --- | ---------------------------- | ---------- | ------------------ | ------------------------------------------------------ |
| 1   | Even or Odd                  | 8 kyu      | `even_or_odd`      | https://www.codewars.com/kata/53da3dbb4a5168369a0000fe |
| 2   | Convert a Number to a String | 8 kyu      | `number_to_string` | https://www.codewars.com/kata/5265326f5fda8eb1160004c8 |
| 3   | Remove String Spaces         | 8 kyu      | `no_space`         | https://www.codewars.com/kata/57eae20f31dd3048b4000139 |
| 4   | Vowel Count                  | 7 kyu      | `get_count`        | https://www.codewars.com/kata/54ff3102c1bad923760001f3 |

All four solutions passed Codewars test suites on submission.
All four use only Python built-ins. No external libraries required.

---

## How to Run the Tests

The file includes an assertion-based test suite that mirrors
the Codewars test cases. Run it directly from the terminal:

```bash
python codewars_solutions.py
```

Expected output:

```
Running tests...

[1] even_or_odd
    All even_or_odd tests passed ✓
[2] number_to_string
    All number_to_string tests passed ✓
[3] no_space
    All no_space tests passed ✓
[4] get_count
    All get_count tests passed ✓

========================================
All tests passed.
========================================
```

If any assertion fails the test stops immediately and prints
which specific case failed. No output means no errors.

---

## Implementation Notes

Each function:

- Uses the exact function name required by Codewars
- Includes a docstring with description, args, return type, and examples
- Is preceded by a comment block naming the kata, difficulty, and constraints
- Uses only Python built-in operations (%, str(), replace(), sum())

---

## Real-World Context

These functions are also used as input validation utilities
in Visible, a career decision intelligence platform being developed
as a capstone project. Each function maps to a specific validation
need in the data entry pipeline:

- `even_or_odd` — validates parity in quantification fields
- `number_to_string` — coerces salary and compensation figures for report generation
- `no_space` — sanitizes job titles and skill tags before storage
- `get_count` — signals low-quality narrative input via vowel density analysis

---

## File Structure

```
python/codewars/
  codewars_solutions.py    — all four kata solutions with docstrings and tests
  README.md                — this file
```
