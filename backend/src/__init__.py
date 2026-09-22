from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from flask_talisman import Talisman
import os
from pathlib import Path


limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

def create_app():
    # Central Flask app factory used by backend/app.py.
    app = Flask(__name__)

    # Sessions are cookie based; these values control how that browser cookie behaves.
    app.secret_key = os.getenv("SECRET_KEY")
    CORS(
        app,
        origins=[
            "http://localhost:5174",
            "http://localhost:5173",
            "https://aiwise-arzh.onrender.com"
        ],
        supports_credentials=True
    )
    # HTTPS is disabled here for local development; enable it before production deployment.
    Talisman(app, force_https=False) # change to true out of development force_https=True)

    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_PATH"] = "/"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    limiter.init_app(app)

    # Register every API endpoint from routes.py under this Flask app.
    from .routes import main
    app.register_blueprint(main)

    return app
