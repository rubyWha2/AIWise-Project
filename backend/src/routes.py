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
        cur.execute("""
                SELECT article_id, title, content, category
                FROM articles
                ORDER BY article_id
            """)

        rows = cur.fetchall()

    conn.close()

    articles = []

    for row in rows:
        articles.append({
            "article_id": row[0],
            "title": row[1],
            "content": row[2],
            "category": row[3]
        })

    return jsonify(articles)


@main.route("/api/quizzes", methods=["GET"])
def get_quizzes():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
               SELECT * FROM quizzes
               ORDER BY quiz_id
           """, (id,))

        row = cur.fetchall()

    conn.close()

    if row is None:
        return jsonify({"error": "Quizzes not found"}), 404

    return jsonify({
        "quiz_id": row[0],
        "article_id": row[1],
        "question": row[2],
        "option_a": row[3],
        "option_b": row[4],
        "option_c":	row[5],
        "option_d": row[6],
        "correct_answer": row[7]
    })

@main.route("/api/results", methods=["GET"])
def get_results():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
                SELECT result_id, user_id, quiz_id, score, max_score,created_at
                FROM results
                ORDER BY result_id
            """)

        rows = cur.fetchall()

    conn.close()

    results = []

    for row in rows:
        results.append({
            "result_id": row[0],
            "user_id": row[1],
            "quiz_id": row[2],
            "score": row[3],
            "max_score": row[4],
            "created_at": row[5]
        })

    return jsonify(results)


@main.route("/api/roles", methods=["GET"])
def get_roles():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
                SELECT role_id, name, privileged
                FROM roles
                ORDER BY role_id
            """)

        rows = cur.fetchall()

    conn.close()

    roles = []

    for row in rows:
        roles.append({
            "role_id": row[0],
            "name": row[1],
            "privilged": row[2]
        })

    return jsonify(roles)

@main.route("/api/users", methods=["GET"])
def get_users():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
                SELECT user_id, username, email, password_hash, role_id
                FROM users
                ORDER BY user_id
            """)

        rows = cur.fetchall()

    conn.close()

    users = []

    for row in rows:
        users.append({
            "user_id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "role_id": row[4]
        })

    return jsonify(users)