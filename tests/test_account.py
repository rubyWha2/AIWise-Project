from backend.src import routes
from tests.test_helpers import FakeConnection, FakeCursor, login_as


def test_load_details_requires_login(client):
    response = client.get("/api/loadDetails")

    assert response.status_code == 401
    assert response.get_json()["message"] == "No user found."


def test_load_details_returns_user_identity(client, monkeypatch):
    cursor = FakeCursor(fetchone=[("admin1", "admin@aiwise.com")])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client)

    response = client.get("/api/loadDetails")

    assert response.status_code == 200
    assert response.get_json() == {"username": "admin1", "email": "admin@aiwise.com"}


def test_update_account_updates_profile(client, monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    login_as(client)

    response = client.post(
        "/api/updateAccount",
        json={"firstName": "Admin", "lastName": "One", "bio": "Testing admin account"},
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Account updated successfully"
    assert cursor.queries[0][1] == ("AdminOne", "Testing admin account", 1)


def test_delete_account_removes_results_before_user(client, monkeypatch):
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    login_as(client, user_id=9)

    response = client.post("/api/deleteAccount")

    assert response.status_code == 200
    assert "DELETE FROM results" in cursor.queries[0][0]
    assert "DELETE FROM users" in cursor.queries[1][0]
    assert connection.committed is True


def test_logout_clears_session(client):
    login_as(client)

    response = client.post("/api/logout")

    assert response.status_code == 200
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_change_password_requires_login(client):
    response = client.post("/api/changePassword", json={})

    assert response.status_code == 401
    assert response.get_json()["message"] == "Please log in"


def test_change_password_updates_password(client, monkeypatch):
    cursor = FakeCursor(fetchone=[("old-hash",)])
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    monkeypatch.setattr(routes, "check_password_hash", lambda stored_hash, password: True)
    monkeypatch.setattr(routes, "generate_password_hash", lambda password: "new-hash")
    monkeypatch.setattr(routes, "verify_recaptcha_token", lambda token, action: (True, "", 200))
    login_as(client, user_id=9)

    response = client.post(
        "/api/changePassword",
        json={
            "email": "admin@aiwise.com",
            "oldPassword": "OldPass1!",
            "newPassword": "NewPass1!",
            "confirmPassword": "NewPass1!",
            "recaptchaToken": "test-token",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Password changed successfully"
    assert cursor.queries[-1][1] == ("new-hash", 9)


def test_send_verification_email_requires_login(client):
    response = client.post("/api/sendVerificationEmail")

    assert response.status_code == 401
    assert response.get_json()["message"] == "Please log in"


def test_send_verification_email_sends_message(client, monkeypatch):
    cursor = FakeCursor(fetchone=[("admin@aiwise.com", "admin1")])
    connection = FakeConnection(cursor)
    sent_messages = []
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    monkeypatch.setattr(routes.secrets, "token_urlsafe", lambda length: "verify-token")
    monkeypatch.setattr(
        routes,
        "send_verification_email",
        lambda email, username, link: sent_messages.append((email, username, link)) or True,
    )
    login_as(client)

    response = client.post("/api/sendVerificationEmail")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Verification email sent."
    assert sent_messages[0][0] == "admin@aiwise.com"
    assert sent_messages[0][2].endswith("/verify-email?token=verify-token")


def test_verify_email_requires_token(client):
    response = client.post("/api/verifyEmail", json={})

    assert response.status_code == 400
    assert response.get_json()["message"] == "Token is required"


def test_verify_email_accepts_valid_token(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(9,)])
    connection = FakeConnection(cursor)
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)

    response = client.post("/api/verifyEmail", json={"token": "valid-token"})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Email verification successful."
    assert connection.committed is True


def test_resend_verification_email_requires_login(client):
    response = client.post("/api/resendVerificationEmail")

    assert response.status_code == 401
    assert response.get_json()["message"] == "Please log in"


def test_resend_verification_email_sends_message(client, monkeypatch):
    cursor = FakeCursor(fetchone=[("admin@aiwise.com", "admin1")])
    connection = FakeConnection(cursor)
    sent_messages = []
    monkeypatch.setattr(routes, "get_db_connection", lambda: connection)
    monkeypatch.setattr(routes.secrets, "token_urlsafe", lambda length: "new-token")
    monkeypatch.setattr(
        routes,
        "send_verification_email",
        lambda email, username, link: sent_messages.append((email, username, link)) or True,
    )
    login_as(client)

    response = client.post("/api/resendVerificationEmail")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Verification email resent."
    assert sent_messages[0][0] == "admin@aiwise.com"
    assert sent_messages[0][2].endswith("/verify-email?token=new-token")
