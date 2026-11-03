# AGENTS.md

Rules for AI tools working in this repo.

## The project

A team dashboard for funding opportunities: grants, startup competitions, incubators and company sponsorships. All data is fictional.

## Run and test

- Install: `python -m pip install -r requirements.txt`
- Run: `python -m uvicorn app.main:app --reload`, then open http://localhost:8000
- Test: `python -m pytest`

## Files

- `app/main.py`: the server
- `app/dates.py`: `days_left()` counts the days until a deadline
- `static/deadlines.js` and `static/deadlines.css`: the deadline labels and their colours
- `TEAM_NOTES.md`: notes from the team
- `app/sample_data.py`: the example rows. The app copies them to `data/opportunities.json` on first run.

## Data

- Fields: `id`, `name`, `organization`, `link`, `amount`, `deadline`, `status`, `owner`, `next_step`
- Statuses: `Interested`, `Preparing`, `Submitted`, `Successful`, `Unsuccessful`
- The server adds `days_left` to every row: `0` on the deadline day, `1` the day before, `-1` the day after.

## Deadline labels

Only rows that are still being worked on (`Interested` or `Preparing`) get a deadline label:

| `days_left` | Label | Colour |
| --- | --- | --- |
| below 0 | `Overdue` | red |
| 0 | `Due today` | yellow |
| 1 | `Due in 1 day` | yellow |
| 2 to 7 | `Due in N days` (for example `Due in 3 days`) | yellow |
| more than 7 | no label | none |

Rows that are `Submitted`, `Successful` or `Unsuccessful` are finished, so they never get a deadline label, even if the deadline has passed.

## Rules

- Keep the code simple. A beginner must be able to read it.
- Don't add new libraries.
- Plain JavaScript only. No React, no build step.
- Use `days_left` from the server for deadline labels. Don't count days again in JavaScript.
- `days_left()` in `app/dates.py` can have bugs like any other code. If it's wrong, fix it there and add a test for the case that was wrong.
- When you change behaviour, add tests for it, including edge cases: a deadline today, tomorrow and yesterday, and rows of every status.
- If a rule here stops you from doing the task correctly, stop and say so. Don't quietly work around it.
