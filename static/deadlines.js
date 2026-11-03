// Statuses that are finished. These rows never get a deadline label.
const FINISHED_STATUSES = ["Submitted", "Successful", "Unsuccessful"];

// Works out the deadline label for one row.
// Returns { text, colour }, or null when the row gets no label.
// The rules are in AGENTS.md under "Deadline labels".
function deadlineLabel(status, daysLeft) {
  if (FINISHED_STATUSES.includes(status)) {
    return null;
  }
  if (daysLeft < 0) {
    return { text: "Overdue", colour: "deadline-overdue" };
  }
  if (daysLeft === 0) {
    return { text: "Due today", colour: "deadline-soon" };
  }
  if (daysLeft === 1) {
    return { text: "Due in 1 day", colour: "deadline-soon" };
  }
  if (daysLeft <= 7) {
    return { text: "Due in " + daysLeft + " days", colour: "deadline-soon" };
  }
  return null; // More than 7 days away.
}

// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const label = deadlineLabel(opportunity.status, opportunity.days_left);
  if (label === null) {
    return;
  }

  const span = document.createElement("span");
  span.className = "deadline-label " + label.colour;
  span.textContent = label.text;
  cell.appendChild(span);
}
