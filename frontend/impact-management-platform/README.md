Impact Management Platform

A small system for capturing the impact of your work — not just the tasks.

Why I built this

Something strange happens during performance reviews.

You remember being busy.
You remember the meetings.
You remember the projects.

But when someone asks:

“What impact did your work actually have?”

…it’s harder than it should be to answer clearly.

Not because the work wasn’t valuable —
but because the value wasn’t structured as it happened.

Most tools help you do the work.
Very few help you explain why it mattered.

What this does

This app captures work as impact events instead of tasks.

Each entry records four things:

Problem — what needed to be solved

Action — what you actually did

Impact — what changed as a result

Evidence — how you can prove it

Over time, this turns day-to-day activity into something much more useful:

a structured record of contributions that’s ready when you need it

What it looks like in practice

Add a new entry as you complete meaningful work

Edit or refine entries as outcomes become clearer

Review everything in one place when you need to communicate your impact

Instead of reconstructing your year from memory, the record already exists.

Features

Create, edit, and delete impact entries

Structured input (Problem → Action → Impact → Evidence)

Simple dashboard for reviewing all entries

Authentication (Auth0)

Protected routes

Local persistence (designed to be extended to a backend)

Tech stack

React + TypeScript

Vite

Context API (state management)

Auth0 (authentication)

Layered structure:

domain

application

infrastructure

presentation

Running locally

Clone the repo, then:

npm install
npm run dev
Environment variables

Create a .env file:

VITE_AUTH0_DOMAIN=your-auth0-domain
VITE_AUTH0_CLIENT_ID=your-client-id
Build
npm run build
What I’d do next

If I were taking this further:

Add persistence (API + database)

Introduce tagging / filtering for impact categories

Generate exportable reports (review-ready summaries)

Add analytics (e.g., type of impact over time)

Closing thought

Most systems optimize for execution.
This one is meant to support explanation.

That difference matters more than it seems.
