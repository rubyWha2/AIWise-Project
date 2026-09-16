import sys
from pathlib import Path

import pytest

# Make the backend package importable when tests are run from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

for path in (PROJECT_ROOT, BACKEND_DIR):
    sys.path.insert(0, str(path))

from backend.src import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret",
        WTF_CSRF_ENABLED=False,
        RATELIMIT_ENABLED=False,
    )
    app.secret_key = "test-secret"
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
