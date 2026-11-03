from datetime import date, timedelta

from fastapi.testclient import TestClient

import app.main
from app.models import Opportunity, Status


def test_api_sends_days_left_for_today_tomorrow_and_yesterday(monkeypatch):
    today = date.today()
    rows = [
        Opportunity(id=1, name="Today", deadline=today, status=Status.PREPARING, owner="A"),
        Opportunity(id=2, name="Tomorrow", deadline=today + timedelta(days=1), status=Status.PREPARING, owner="A"),
        Opportunity(id=3, name="Yesterday", deadline=today - timedelta(days=1), status=Status.PREPARING, owner="A"),
    ]
    # Use these rows instead of the real data file.
    monkeypatch.setattr(app.main, "load_opportunities", lambda: rows)

    response = TestClient(app.main.app).get("/api/opportunities")

    days = {row["name"]: row["days_left"] for row in response.json()}
    assert days == {"Today": 0, "Tomorrow": 1, "Yesterday": -1}
