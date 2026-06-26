"""
API routes: auth, user management and data endpoints
"""

from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request, current_app, session
from .db import get_db_connection

main = Blueprint('main', __name__)

@main.route('/api/test')
def test():
    return jsonify({
        "message": "AIWise API Working"
    })
# Read-only fetchers - return full table contents for each domain entity

@main.route("/api/articles", methods=["GET"])
def get_articles():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM articles ORDER BY article_id")
        rows = cur.fetchall()
    conn.close()

    return jsonify([
        {
            "article_id": row[0],
            "title": row[1],
            "category": row[2]
        }
        for row in rows
    ])