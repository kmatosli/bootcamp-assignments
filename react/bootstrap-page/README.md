# Visible — Bootstrap Landing Page

## Assignment

Bootstrap Basics, Utilities, Forms, and Components
Coding Temple Software Engineering Bootcamp

## Overview

A fully responsive Bootstrap landing page for Visible, a career decision
intelligence platform. Built to satisfy all Bootstrap assignment requirements
while serving as a real marketing page for the product being developed.

## How to View

Open `index.html` directly in any browser.
No installation or build step required.
All Bootstrap dependencies load from CDN.

To verify responsive behavior (navbar collapse, hidden button, responsive table):
resize your browser window to below 768px width.

---

## Bootstrap Requirements — Implementation Reference

This section maps every assignment requirement to the exact location
in `index.html` so each can be verified directly.

---

### Bootstrap CDN

**Requirement:** Bootstrap CDN linked in the `<head>` section.
**Location:** Line 8

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
  rel="stylesheet"
/>
```

Bootstrap JS bundle also loaded at line 666:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

---

### Container Layout

**Requirement:** Use a `container` or `container-fluid` to structure the layout.
**Location:** Every section uses `class="container"`.
Examples: lines 303, 322, 370, 452, 554.

---

### Part 1: Registration Form

**Requirement:** First Name and Last Name fields side by side using Bootstrap grid.
**Location:** Lines 566–577

```html
<div class="row g-3 mb-3">
  <div class="col-md-6">First Name</div>
  <div class="col-md-6">Last Name</div>
</div>
```

**Requirement:** Email field with required validation.
**Location:** Lines 579–583

```html
<input type="email" class="form-control" id="email" required />
```

**Requirement:** Password field with required validation.
**Location:** Lines 585–589

```html
<input
  type="password"
  class="form-control"
  id="password"
  minlength="8"
  required
/>
```

**Requirement:** Checkbox for agreeing to terms.
**Location:** Lines 626–634

```html
<div class="form-check">
  <input class="form-check-input" type="checkbox" id="terms" required />
</div>
```

**Requirement:** Submit button styled with `btn-success`.
**Location:** Lines 636–640

```html
<button type="submit" class="btn btn-success btn-lg" id="submitBtn">
  Get Early Access
</button>
```

**Requirement:** Bootstrap validation classes applied.
**Location:** Line 564 — `class="needs-validation"` on the form.
Lines 668–685 — JavaScript applies `was-validated` class on submit attempt,
triggering Bootstrap's built-in validation display for required fields.

---

### Part 2: Table

**Requirement:** Bootstrap table with striped and hoverable rows.
**Location:** Lines 499–548

```html
<table
  class="table table-striped table-hover table-visible align-middle"
></table>
```

- `table-striped` ✓
- `table-hover` ✓
- Three hardcoded rows of sample data ✓

**Requirement:** Table wrapped in `table-responsive` div.
**Location:** Line 498

```html
<div class="table-responsive"></div>
```

---

### Part 3: Image and Button Utilities

**Requirement:** Responsive image using `img-fluid` inside a fluid container.
**Location:** Lines 320–325

```html
<img src="..." class="img-fluid hero-main-img" />
```

**Requirement:** Circular image using `rounded-circle`.
**Location:** Lines 327–332

```html
<img src="..." class="img-fluid rounded-circle hero-badge-avatar" />
```

**Requirement:** Button visible on all screen sizes.
**Location:** Line 338

```html
<a href="#contact" class="btn-primary-visible">Get Early Access — Free</a>
```

No display restriction applied. Visible on all screen sizes.

**Requirement:** Button hidden on small screens using `d-none d-md-block`.
**Location:** Line 341

```html
<a href="#how" class="btn-gold-visible d-none d-md-block">See How It Works</a>
```

- `d-none` hides on xs and sm screens ✓
- `d-md-block` shows from md (768px) and above ✓

---

### Part 4: Navigation Bar

**Requirement:** Navbar with links to Home, About, Contact sections.
**Location:** Lines 294–315
Links present: Home (`#home`), About (`#about`), How It Works (`#how`), Get Started (`#contact`).

**Requirement:** Navbar collapses into hamburger menu on smaller screens.
**Location:** Lines 299–305

```html
<button
  class="navbar-toggler"
  type="button"
  data-bs-toggle="collapse"
  data-bs-target="#mainNav"
>
  <span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="mainNav"></div>
```

- `navbar-toggler` ✓
- `data-bs-toggle="collapse"` ✓
- `data-bs-target="#mainNav"` ✓
- `collapse navbar-collapse` on the collapsible div ✓
- Bootstrap JS bundle loaded to power the collapse behavior ✓

**Requirement:** Bootstrap utilities and components used to style the navbar.
**Location:** Line 293

```html
<nav class="navbar navbar-expand-lg"></nav>
```

- `navbar` ✓
- `navbar-expand-lg` collapses below lg breakpoint ✓

---

### Responsiveness Summary

| Requirement                 | Bootstrap Class               | Location                      |
| --------------------------- | ----------------------------- | ----------------------------- |
| Responsive image            | `img-fluid`                   | Line 322                      |
| Circular image              | `rounded-circle`              | Line 329                      |
| Hidden button small screens | `d-none d-md-block`           | Line 341                      |
| Responsive table            | `table-responsive`            | Line 498                      |
| Striped table               | `table-striped`               | Line 499                      |
| Hoverable table             | `table-hover`                 | Line 499                      |
| Submit button               | `btn btn-success`             | Line 637                      |
| Grid layout                 | `row` / `col-md-6`            | Lines 566–577                 |
| Collapsing navbar           | `navbar-toggler` / `collapse` | Lines 299–309                 |
| Container layout            | `container`                   | Lines 303, 322, 370, 452, 554 |

---

## Project Structure

```
react/bootstrap-page/
  index.html    — complete single-file Bootstrap page
  README.md     — this file
```

## Notes

The page is intentionally built as a single self-contained HTML file.
All Bootstrap classes, utilities, and components are applied directly
in `index.html`. There are no separate CSS or JS files required.
Custom CSS is scoped inside a `<style>` block in the `<head>` and
does not override or replace any Bootstrap functionality.
