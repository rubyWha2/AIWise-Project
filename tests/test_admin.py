from datetime import datetime, timezone

from backend.src import routes
from tests.test_helpers import FakeConnection, FakeCursor, login_as


def test_count_all_requires_login(client):
    response = client.get("/api/count_all")

    assert response.status_code == 401
    assert response.get_json()["message"] == "Please log in"


def test_get_roles_returns_roles(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1,)], fetchall=[(1, "admin", True), (2, "user", False)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/roles")

    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "admin"
    assert response.get_json()[1]["privileged"] is False


def test_get_users_returns_users(client, monkeypatch):
    created_at = datetime(2026, 9, 8, tzinfo=timezone.utc)
    cursor = FakeCursor(fetchone=[(1,)], fetchall=[(1, "admin1", "admin@aiwise.com", 1, created_at, False)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/users")

    assert response.status_code == 200
    assert response.get_json()[0]["username"] == "admin1"
    assert response.get_json()[0]["banned"] is False
    assert "password_hash" not in response.get_json()[0]


def test_get_admin_status_returns_403_for_non_admin(client, monkeypatch):
    cursor = FakeCursor(fetchone=[None])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client, user_id=2, username="learner", role_id=2)

    response = client.get("/api/getAdminStatus")

    assert response.status_code == 403
    assert response.get_json()["message"] == "User is not an admin."


def test_get_admin_status_returns_admin(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1, 1)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/getAdminStatus")

    assert response.status_code == 200
    assert response.get_json() == {"user_id": 1, "role_id": 1}


def test_count_all_returns_dashboard_totals(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1,), (3, 9, 12, 20)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/count_all")

    assert response.status_code == 200
    assert response.get_json() == {
        "users": 3,
        "articles": 9,
        "quizzes_taken": 12,
        "questions": 20,
    }


def test_get_top_6_users_returns_recent_users(client, monkeypatch):
    created_at = datetime(2026, 9, 8, tzinfo=timezone.utc)
    cursor = FakeCursor(fetchone=[(1,)], fetchall=[(1, "admin1", "admin@aiwise.com", created_at)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/getTop6users")

    assert response.status_code == 200
    assert response.get_json()[0]["email"] == "admin@aiwise.com"


def test_ban_user_updates_user_when_admin(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1,)], rowcount=1)
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    login_as(client, user_id=1, role_id=1)

    response = client.put("/api/users/2/ban")

    assert response.status_code == 200
    assert response.get_json()["message"] == "User banned successfully"
    assert connection.committed is True


def test_ban_user_blocks_self_ban(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1,)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client, user_id=1, role_id=1)

    response = client.put("/api/users/1/ban")

    assert response.status_code == 400
    assert response.get_json()["message"] == "You cannot ban your own account"


def test_delete_article_requires_admin(client, monkeypatch):
    monkeypatch.setattr(routes, "current_user_is_admin", lambda: False)

    response = client.delete("/api/articles/1")

    assert response.status_code == 403
    assert response.get_json()["message"] == "Admin access required"


def test_delete_article_removes_article_and_dependencies(client, monkeypatch):
    cursor = FakeCursor(rowcount=1)
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "current_user_is_admin", lambda: True)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)

    response = client.delete("/api/articles/1")

    assert response.status_code == 200
    assert "DELETE FROM results" in cursor.queries[0][0]
    assert "DELETE FROM quizzes" in cursor.queries[1][0]
    assert "DELETE FROM articles" in cursor.queries[2][0]


def test_delete_quiz_removes_question(client, monkeypatch):
    cursor = FakeCursor(rowcount=1)
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "current_user_is_admin", lambda: True)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)

    response = client.delete("/api/quizzes/1")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Quiz question deleted successfully"
