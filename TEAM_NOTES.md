# Team notes

Notes from our team.

- **Vinay:** I asked my AI to build the deadline labels and colours from the Task 1 text. Then I checked the page and saw that the Nov 3 deadline said "Overdue". The AI found an off-by-one bug in `days_left()`, and I let it fix `app/dates.py` and add tests for today, tomorrow and yesterday.
- **Patrick:** I asked my AI to set up the project, implement the deadline badges and colours, and investigate why today's date was marked as overdue. Then I checked the dashboard in the browser, verified the edge cases, and reviewed our team's PRs.
- **Evan:** I asked my AI to complete Task 1. Then I checked the colours and labels on the page in Chrome.
- **Michael:** I asked my AI to do Task 1 from TASKS.md. It read AGENTS.md first and wrote the label code in deadlines.js and deadlines.css. Then I checked that pytest passed and looked at what the API sent back, which showed that days_left was one day short.
