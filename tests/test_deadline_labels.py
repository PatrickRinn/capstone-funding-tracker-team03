"""Tests for the deadline labels in static/deadlines.js.

The labels are worked out in JavaScript, so these tests ask Node to run
deadlineLabel() and print the answer. The rules are in AGENTS.md.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

DEADLINES_JS = Path(__file__).parent.parent / "static" / "deadlines.js"

# GitHub's test machines have Node. Skip, don't fail, on a laptop without it.
pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node is not installed")


def label_for(status, days_left):
    """Run deadlineLabel(status, days_left) in Node and return its answer."""
    script = (
        "const fs = require('fs');"
        "const vm = require('vm');"
        "const page = {};"
        f"vm.runInNewContext(fs.readFileSync({json.dumps(str(DEADLINES_JS))}, 'utf8'), page);"
        f"console.log(JSON.stringify(page.deadlineLabel({json.dumps(status)}, {days_left})));"
    )
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


@pytest.mark.parametrize("status", ["Interested", "Preparing"])
@pytest.mark.parametrize(
    "days_left, text, colour",
    [
        (-30, "Overdue", "deadline-overdue"),
        (-1, "Overdue", "deadline-overdue"),  # yesterday
        (0, "Due today", "deadline-soon"),  # today
        (1, "Due in 1 day", "deadline-soon"),  # tomorrow
        (3, "Due in 3 days", "deadline-soon"),
        (7, "Due in 7 days", "deadline-soon"),
    ],
)
def test_open_rows_get_a_label(status, days_left, text, colour):
    assert label_for(status, days_left) == {"text": text, "colour": colour}


@pytest.mark.parametrize("status", ["Interested", "Preparing"])
def test_open_rows_more_than_7_days_away_get_no_label(status):
    assert label_for(status, 8) is None


@pytest.mark.parametrize("status", ["Submitted", "Successful", "Unsuccessful"])
@pytest.mark.parametrize("days_left", [-30, -1, 0, 1, 7, 8])
def test_finished_rows_never_get_a_label(status, days_left):
    assert label_for(status, days_left) is None
