// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const days = opportunity.days_left;

  let text = "";
  let className = "";

  if (days < 0) {
    text = "Overdue";
    className = "overdue";
  } else if (days === 0) {
    text = "Due today";
    className = "due-soon";
  } else if (days <= 7) {
    const unit = days === 1 ? "day" : "days";
    text = `Due in ${days} ${unit}`;
    className = "due-soon";
  }

  if (text) {
    const badge = document.createElement("span");
    badge.className = `deadline-badge ${className}`;
    badge.textContent = text;
    cell.appendChild(document.createTextNode(" "));
    cell.appendChild(badge);
  }
}
