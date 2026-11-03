// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const label = deadlineLabel(opportunity.days_left);
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

// Turns days_left into a label. Deadlines more than 7 days away get no label.
function deadlineLabel(daysLeft) {
  if (daysLeft < 0) {
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
