from datetime import datetime, timezone

from backend.src import routes
from tests.test_helpers import FakeConnection, FakeCursor, login_as


def test_get_results_returns_all_results(client, monkeypatch):
    created_at = datetime(2026, 9, 8, tzinfo=timezone.utc)
    cursor = FakeCursor(fetchall=[(1, 2, 3, 4, 5, created_at)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/results")

    assert response.status_code == 200
    assert response.get_json()[0]["result_id"] == 1
    assert response.get_json()[0]["user_id"] == 2
    assert response.get_json()[0]["score"] == 4


def test_update_results_requires_login(client):
    response = client.post("/api/updateResults", json={"article_id": 1, "score": 4, "max_score": 5})

    assert response.status_code == 401
    assert response.get_json()["message"] == "Please log in"


def test_update_results_inserts_score_for_logged_in_user(client, monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    login_as(client, user_id=9, username="learner", role_id=2)

    response = client.post("/api/updateResults", json={"article_id": 1, "score": 4, "max_score": 5})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Result successfully written to database."
    assert cursor.queries[0][1][0] == 9
    assert cursor.queries[0][1][1] == 1
    assert connection.committed is True


def test_load_results_returns_current_user_history(client, monkeypatch):
    created_at = datetime(2026, 9, 8, tzinfo=timezone.utc)
    cursor = FakeCursor(fetchall=[(1, 9, 4, 5, created_at, 1, "What Is Data Handling in Business?")])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client, user_id=9, username="learner", role_id=2)

    response = client.get("/api/loadResults")

    assert response.status_code == 200
    assert response.get_json()[0]["article_title"] == "What Is Data Handling in Business?"
