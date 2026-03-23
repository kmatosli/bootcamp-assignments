# Visible — Behavioral Onboarding Quiz

## Assignment

DOMination: Build a JavaScript Fundamentals Quiz
Coding Temple Software Engineering Bootcamp

## Overview

A JavaScript-powered behavioral assessment quiz built as part of
the Visible career intelligence platform. Instead of generic trivia,
this quiz measures the ten behavioral signals that managers use to
evaluate whether someone is ready for advancement — almost always
without ever saying so directly.

The quiz satisfies all DOMination assignment requirements while
serving as the behavioral onboarding entry point for the Visible app.

## How to View

Open `behavioral-quiz.html` directly in any browser.
No installation, build step, or server required.
Pure HTML, CSS, and vanilla JavaScript.

---

## Assignment Requirements — Implementation Reference

| Requirement                          | Implementation                                                    |
| ------------------------------------ | ----------------------------------------------------------------- |
| Questions stored in JavaScript array | `quizData` array of objects (line ~180)                           |
| question, options, answer fields     | Each object has `signal`, `question`, `options[]`, `answer` index |
| Show questions one at a time         | `loadQuestion()` function renders one question then hides         |
| Buttons created dynamically with JS  | `forEach` loop creates buttons via `createElement`                |
| Event listeners on answer buttons    | `addEventListener('click')` on each option button                 |
| Immediate color feedback             | `.correct` = green, `.incorrect` = red CSS classes                |
| Score tracking                       | `score` variable incremented on correct answers                   |
| Show final results                   | `showScore()` function shows `#score-container`                   |
| Restart functionality                | `restartButton` resets all state and reloads first question       |
| Show/hide sections                   | `classList.add('hidden')` / `classList.remove('hidden')`          |
| Next Question button                 | `#next-button` advances `currentIndex`                            |
| DOM manipulation                     | `textContent`, `innerHTML`, `createElement`, `appendChild`        |
| Conditional logic                    | Profile level determined by `flagCount` thresholds                |
| Arrays and loops                     | `quizData` array, `forEach` loops, `flaggedSignals` array         |

---

## Structure

```
javascript/behavioral-quiz/
  behavioral-quiz.html    — complete single-file quiz application
  README.md               — this file
```

---

## Quiz Content

Ten questions mapping to the Visible `BehavioralSignal` domain model:

1. **Initiative** — Problem solving before escalation
2. **Reliability** — Willingness to estimate deadlines
3. **Quality** — Checking work before submission
4. **Discovery vs Reporting** — How manager learns of outcomes
5. **Manager Time** — Time consumption relative to peers
6. **Listening** — Full presence in conversations
7. **Learning** — Technology adaptability
8. **Documentation** — Knowledge transfer and backup
9. **Completion** — Full project close-out
10. **Purpose** — Output over presence

---

## Score Output

The quiz produces a behavioral profile in one of three levels:

- **Strong (0–2 flags):** Already demonstrating advancement-ready behaviors
- **Developing (3–5 flags):** Solid foundation with specific addressable areas
- **Significant Gap (6+ flags):** Clear map of highest-priority development areas

Each result includes a signal breakdown and a first priority recommendation
telling the user which specific behavior to focus on in the next 90 days.

---

## Real-World Context

This quiz is the behavioral onboarding entry point for Visible,
a career decision intelligence platform. The `quizData` array maps
directly to the `BehavioralOnboarding` TypeScript interface in the
Visible domain model. The quiz output populates:

- `initialBlindSpotFlags`
- `initialStrengthSignals`
- `firstPriorityDevelopmentArea`
- `onboardingInsight`

The same ten behavioral signals are tracked continuously through
the `BehavioralCheckIn` system after onboarding completes.
