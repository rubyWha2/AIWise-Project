from backend.src import routes
from tests.test_helpers import FakeConnection, FakeCursor


QUIZ_ROWS = [
    (
        1,
        1,
        "What is data handling?",
        "Collecting and managing data",
        "Deleting all data",
        "Ignoring customer records",
        "Only printing data",
        "A",
        "What Is Data Handling in Business?",
    )
]


def test_get_quizzes_returns_quiz_rows(client, monkeypatch):
    cursor = FakeCursor(fetchall=QUIZ_ROWS)
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/quizzes")

    assert response.status_code == 200
    assert response.get_json()[0]["quiz_id"] == 1
    assert response.get_json()[0]["title"] == "What Is Data Handling in Business?"


def test_get_quizzes_returns_404_when_empty(client, monkeypatch):
    cursor = FakeCursor(fetchall=[])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/quizzes")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Quizzes not found"


def test_get_inv_quiz_returns_article_quiz(client, monkeypatch):
    row = (
        1,
        1,
        "What Is Data Handling in Business?",
        "What is data handling?",
        "Collecting and managing data",
        "Deleting all data",
        "Ignoring customer records",
        "Only printing data",
        "A",
    )
    cursor = FakeCursor(fetchall=[row])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))

    response = client.get("/api/quiz/1")

    assert response.status_code == 200
    assert response.get_json()[0]["article_id"] == 1
    assert response.get_json()[0]["article_title"] == "What Is Data Handling in Business?"
