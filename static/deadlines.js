// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const label = document.createElement("span");
  label.className = "deadline-label";

  if (opportunity.days_left < 0) {
    label.classList.add("deadline-overdue");
    label.textContent = "Overdue";
  } else if (opportunity.days_left === 0) {
    label.classList.add("deadline-today");
    label.textContent = "Due today";
  } else {
    label.classList.add("deadline-upcoming");
    const unit = opportunity.days_left === 1 ? "day" : "days";
    label.textContent = `Due in ${opportunity.days_left} ${unit}`;
  }

  cell.appendChild(document.createElement("br"));
  cell.appendChild(label);
}
