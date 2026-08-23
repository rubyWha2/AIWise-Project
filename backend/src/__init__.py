from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from flask_talisman import Talisman
import os
from flask_mail import Mail


limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
load_dotenv()
mail = Mail()

def create_app():
    # Central Flask app factory used by backend/app.py.
    app = Flask(__name__)

    # Mail settings are read from the environment so secrets stay out of source code.
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)

    # Sessions are cookie based; these values control how that browser cookie behaves.
    app.secret_key = os.getenv("SECRET_KEY")
    CORS(app, supports_credentials=True)
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE") == "True"
    app.config["SESSION_COOKIE_HTTPONLY"] = os.getenv("SESSION_COOKIE_HTTPONLY") == "True"
    app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    # HTTPS is disabled here for local development; enable it before production deployment.
    Talisman(app, force_https=False) # change to true out of development force_https=True)
    limiter.init_app(app)

    # Register every API endpoint from routes.py under this Flask app.
    from .routes import main
    app.register_blueprint(main)

    return app
