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
    app = Flask(__name__)

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    mail.init_app(app)

    app.secret_key = os.getenv("SECRET_KEY")
    CORS(app, supports_credentials=True)
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE") == "True"
    app.config["SESSION_COOKIE_HTTPONLY"] = os.getenv("SESSION_COOKIE_HTTPONLY") == "True"
    app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    Talisman(app, force_https=False) # change to true out of development force_https=True)
    limiter.init_app(app)
    from .routes import main
    app.register_blueprint(main)

    return app