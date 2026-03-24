# Visible — Career Intelligence Dashboard

## Assignment

Final JavaScript Project: API Dashboard
Coding Temple Software Engineering Bootcamp

## Overview

A single-page dashboard of eight mini apps, each powered by a
different public API. Every panel maps to a real feature in
Visible, a career decision intelligence platform in development.

## Live Demo

https://kmatosli.github.io/bootcamp-assignments/javascript/api-dashboard/api-dashboard.html

## How to View

Open `api-dashboard.html` directly in any browser.
No installation, build step, or API keys required.
All eight APIs are free and keyless.

---

## Eight Panels — APIs and Visible Feature Mapping

| Panel                    | API              | No Key | Visible Feature                   |
| ------------------------ | ---------------- | ------ | --------------------------------- |
| 🌤️ Work Location Weather | Open-Meteo       | ✅     | Commute cost calculator context   |
| 💱 Compensation FX       | ExchangeRate-API | ✅     | International offer comparison    |
| 🧑‍💻 Skills Profile        | GitHub REST API  | ✅     | Public contribution evidence      |
| 📊 Job Market Signal     | RemoteOK API     | ✅     | Skills demand trajectory          |
| 💡 Career Insight        | Quotable API     | ✅     | Daily strategic insight           |
| 🌍 Market Geography      | REST Countries   | ✅     | Geographic compensation context   |
| 🐶 Morale Break          | Dog CEO API      | ✅     | End of day decompression          |
| 📚 Development Reading   | Open Library     | ✅     | Skill gap reading recommendations |

---

## JavaScript Concepts Demonstrated

- `async/await` for all API calls
- `fetch()` for HTTP requests to eight different APIs
- `try/catch` error handling on every panel
- `Promise.all()` for parallel fetching (GitHub panel)
- DOM manipulation with `innerHTML` and dynamic content
- ES6 arrow functions and destructuring
- Template literals for dynamic HTML generation
- Event listeners on input fields (Enter key support)
- Independent panel loading so one failure does not block others

---

## API Details

### Open-Meteo

- URL: `https://api.open-meteo.com/v1/forecast`
- Returns: Current temperature, wind speed, weather code
- No key required

### ExchangeRate-API

- URL: `https://open.er-api.com/v6/latest/USD`
- Returns: Live exchange rates for 160 currencies
- No key required (open endpoint)

### GitHub REST API

- URL: `https://api.github.com/users/{username}`
- Returns: User profile, repos, follower counts, languages
- No key required for public data
- Interactive: search any GitHub username

### RemoteOK API

- URL: `https://remoteok.com/api`
- Returns: Live remote job listings with skill tags
- No key required

### Quotable API

- URL: `https://api.quotable.io/quotes/random`
- Returns: Random curated quotes filtered by tag
- No key required
- Fallback quotes included for when API is unavailable

### REST Countries

- URL: `https://restcountries.com/v3.1/name/{country}`
- Returns: Country data including currency, population, language
- No key required
- Interactive: search any country name

### Dog CEO API

- URL: `https://dog.ceo/api/breeds/image/random`
- Returns: Random dog image URL
- No key required

### Open Library

- URL: `https://openlibrary.org/search.json`
- Returns: Book search results by topic
- No key required
- Interactive: search any development topic

---

## File Structure

```
javascript/api-dashboard/
  api-dashboard.html    — complete single-file dashboard
  README.md             — this file
```

---

## Real-World Context

This dashboard is the market intelligence layer for Visible,
a career decision intelligence platform being built as a
capstone project. Each panel surfaces real-time data relevant
to career decisions — compensation comparisons, skill demand
signals, development resources, and geographic context for
job offer evaluations.
