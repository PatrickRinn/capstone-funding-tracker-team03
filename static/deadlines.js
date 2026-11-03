// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const label = deadlineLabel(opportunity.days_left, opportunity.status);
  if (label === "") {
    return;
  }

  const badge = document.createElement("span");
  badge.textContent = label;
  if (opportunity.days_left < 0) {
    badge.className = "deadline deadline-overdue";
  } else {
    badge.className = "deadline deadline-soon";
  }
  cell.appendChild(badge);
}

// Statuses where the application has already been sent in.
const SUBMITTED_STATUSES = ["Submitted", "Successful", "Unsuccessful"];

// Turns days_left into a label. Deadlines more than 7 days away get no label.
// Rows that are already submitted are never labelled "Overdue".
function deadlineLabel(daysLeft, status) {
  if (daysLeft < 0) {
    if (SUBMITTED_STATUSES.includes(status)) {
      return "";
    }
    return "Overdue";
  }
  if (daysLeft === 0) {
    return "Due today";
  }
  if (daysLeft === 1) {
    return "Due in 1 day";
  }
  if (daysLeft <= 7) {
    return "Due in " + daysLeft + " days";
  }
  return "";
}
