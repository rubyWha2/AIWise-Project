"""
API routes: auth, user management and data endpoints
"""

from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request, current_app, session
from flask_wtf.csrf import generate_csrf
from functools import wraps
#from . import limiter

main = Blueprint('main', __name__)

@main.route('/api/test')
def test():
    return jsonify({
        "message": "AIWise API Working"
    })

@main.route("/api/articles")
def get_articles():
    return jsonify([
        {
            "article_id": 1,
            "title": "Article 1",
        }
    ])