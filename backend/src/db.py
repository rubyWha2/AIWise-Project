import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

def get_db_connection():
    """
    Create and return a PostgreSQL connection.

    Uses psycopg (v3) if available, otherwise falls back to psycopg2.
    Raises a clear error if no supported driver is installed.
    """
    # Database credentials come from .env rather than being hardcoded.
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")
    connect_timeout = os.getenv("DB_CONNECT_TIMEOUT", "3")

    if not all([host, dbname, user, password, port]):
        raise RuntimeError(
            "Database configuration is incomplete. Please set "
            "DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, and DB_PORT."
        )

    # Try psycopg (v3)
    try:
        import psycopg  # type: ignore
        return psycopg.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            connect_timeout=connect_timeout,
        )
    except ModuleNotFoundError:
        pass

    # Fallback to psycopg2
    try:
        import psycopg2  # type: ignore
        return psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            connect_timeout=connect_timeout,
        )
    except ModuleNotFoundError:
        raise RuntimeError(
            "PostgreSQL driver is missing. Install either `psycopg` (v3) or `psycopg2` "
            "in the same Python environment you're running the Flask app."
        )
