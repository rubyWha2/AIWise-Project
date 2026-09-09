from backend.src import routes
from backend.src.routes import login_rate_limit_key
from backend.src.routes import verify_recaptcha_token
from tests.test_helpers import FakeConnection, FakeCursor, login_as


ADMIN_EMAIL = "admin@aiwise.com"
ADMIN_PASSWORD = "wJ@x94pgW3LUmYU"


def test_login_rate_limit_key_uses_ip_and_lowercase_email(app):
    with app.test_request_context(
        "/api/login",
        method="POST",
        json={"email": "  Test@Example.com  "},
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    ):
        assert login_rate_limit_key() == "127.0.0.1:test@example.com"


def test_verify_recaptcha_allows_debug_without_secret(app, monkeypatch):
    monkeypatch.delenv("RECAPTCHA_SECRET_KEY", raising=False)
    app.debug = True

    with app.app_context():
        assert verify_recaptcha_token("", "login") == (True, "", 200)


def test_verify_recaptcha_requires_token_when_secret_exists(app, monkeypatch):
    monkeypatch.setenv("RECAPTCHA_SECRET_KEY", "secret")

    with app.app_context():
        ok, message, status = verify_recaptcha_token("", "login")

    assert ok is False
    assert message == "Recaptcha token is required"
    assert status == 400


def test_current_user_is_admin_returns_true_for_admin(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1,)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    login_as(client, user_id=1, role_id=1)

    with client.application.test_request_context():
        with client.session_transaction() as saved_session:
            for key, value in saved_session.items():
                routes.session[key] = value

        assert routes.current_user_is_admin() is True


def test_login_accepts_valid_admin_credentials(client, monkeypatch):
    cursor = FakeCursor(fetchone=[(1, "admin1", "stored-admin-hash", 1, 0, None, False)])
    monkeypatch.setattr(routes, "get_db_connection", lambda: FakeConnection(cursor))
    monkeypatch.setattr(routes, "verify_recaptcha_token", lambda token, action: (True, "", 200))
    monkeypatch.setattr(
        routes,
        "check_password_hash",
        lambda stored_hash, password: (
            stored_hash == "stored-admin-hash"
            and password == f"{ADMIN_PASSWORD}{routes.PEPPER}"
        ),
    )

    response = client.post(
        "/api/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "recaptchaToken": "test-token",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"
    assert response.get_json()["username"] == "admin1"
    assert response.get_json()["role_id"] == 1


def test_login_rejects_missing_password(client):
    response = client.post("/api/login", json={"email": ADMIN_EMAIL})

    assert response.status_code == 400
    assert response.get_json()["message"] == "Email and password are required"


def test_register_rejects_invalid_email(client):
    response = client.post(
        "/api/register",
        json={
            "firstName": "Admin",
            "lastName": "One",
            "email": "not-an-email",
            "password": ADMIN_PASSWORD,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid email format"


def test_register_creates_user(client, monkeypatch):
    select_cursor = FakeCursor(fetchone=[None])
    insert_cursor = FakeCursor()
    connections = iter([FakeConnection(select_cursor), FakeConnection(insert_cursor)])

    monkeypatch.setattr(routes, "get_db_connection", lambda: next(connections))
    monkeypatch.setattr(routes, "generate_password_hash", lambda password: "hashed-password")

    response = client.post(
        "/api/register",
        json={
            "firstName": "New",
            "lastName": "User",
            "email": "NewUser@Example.com",
            "password": "StrongPass1!",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"
    assert insert_cursor.queries[0][1][0] == "NewUser"
    assert insert_cursor.queries[0][1][1] == "newuser@example.com"
