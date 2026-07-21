from flask import Flask
from .routes import main
from dotenv import load_dotenv
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.secret_key = os.getenv("SECRET_KEY")
    CORS(app, supports_credentials=True)
    return app