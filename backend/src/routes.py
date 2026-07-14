"""
API routes: auth, user management and data endpoints
"""

from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection
from dotenv import load_dotenv
import re
import os

load_dotenv()
PEPPER = os.getenv("PASSWORD_PEPPER")

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

@main.route("/api/articles/<int:article_id>", methods=["GET"])
def get_inv_article(article_id):
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
                SELECT article_id, title, content, category
                FROM articles
                WHERE article_id = %s
            """, (article_id,))

        row = cur.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "Article not found"}), 404

    return jsonify({
        "article_id": row[0],
        "title": row[1],
        "content": row[2],
        "category": row[3]
    })


@main.route("/api/quizzes", methods=["GET"])
def get_quizzes():
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
               SELECT * FROM quizzes
               ORDER BY quiz_id
           """, (id,))

        rows = cur.fetchall()

    conn.close()

    if not rows:
        return jsonify({"error": "Quizzes not found"}), 404

    quizzes = []
    for row in rows:
        quizzes.append({
            "quiz_id": row[0],
            "article_id": row[1],
            "question": row[2],
            "option_a": row[3],
            "option_b": row[4],
            "option_c":	row[5],
            "option_d": row[6],
            "correct_answer": row[7]
    })
    return jsonify(quizzes)

@main.route("/api/quiz/<int:article_id>", methods=["GET"])
def get_inv_quiz(article_id):
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                q.quiz_id,
                q.article_id,
                a.title,
                q.question,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,
                q.correct_answer
            FROM quizzes q
            JOIN articles a
                ON q.article_id = a.article_id
            WHERE q.article_id = %s
            ORDER BY q.quiz_id
        """, (article_id,))
        rows = cur.fetchall()

    conn.close()

    if not rows:
        return jsonify({"error": "Quizzes not found"}), 404

    quizzes = []
    for row in rows:
        quizzes.append({
            "quiz_id": row[0],
            "article_id": row[1],
            "article_title": row[2],
            "question": row[3],
            "option_a": row[4],
            "option_b": row[5],
            "option_c": row[6],
            "option_d": row[7],
            "correct_answer": row[8]
    })
    return jsonify(quizzes)




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

@main.route("/api/register", methods=["POST"])
def register():
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    password = data.get("password")

    if not all([firstName, lastName, email, password]):
        return jsonify({"message": "Missing required fields"}), 400
    if not re.match(email_regex, email):
        return jsonify({"message": "Invalid email format"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters long"}), 400
    if len(password) > 28:
        return jsonify({"message": "Password must be at most 28 characters long"}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify({"message": "Password must contain an uppercase letter"}), 400
    if not re.search(r"[a-z]", password):
        return jsonify({"message": "Password must contain a lowercase letter"}), 400
    if not re.search(r"\d", password):
        return jsonify({"message": "Password must contain a number"}), 400
    if not re.search(r"[!@#$%^&*()]", password):
        return jsonify({"message": "Password must contain a special character"}), 400

    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
    conn.close()

    if user is not None:
        return jsonify({"message": "Email already exists"}), 400


    peppered_password = password + PEPPER
    hashed_password = generate_password_hash(peppered_password)
    created_date = datetime.now(timezone.utc)
    role_id = 2 #automatically a user role

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (username, email, password_hash, role_id, created_at) VALUES (%s, %s, %s, %s, %s)", (firstName +  lastName, email, hashed_password, role_id, created_date))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@main.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    peppered_password = password + PEPPER

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT user_id, username, password_hash, role_id FROM users WHERE email = %s", (email,))

        user = cur.fetchone()
    conn.close()
    if user is None:
        return jsonify({"message": "Invalid email or password"}), 401

    if not check_password_hash(user[2], peppered_password):
        return jsonify({"message": "Invalid email or password"}), 401

    session["user_id"] = user[0]

    return jsonify({
        "message": "Login successful",
        "user_id": user[0],
        "username": user[1],
        "role_id": user[3]
    }), 200

@main.route("/api/changePassword", methods=["POST"])
def change_password():
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    data = request.get_json()

    email = data.get("email")
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    confirm_new_password = data.get("confirmPassword")

    if new_password != confirm_new_password:
        return jsonify({"message": "New passwords must match"}), 401

    if not all([email, old_password, new_password, confirm_new_password]):
        return jsonify({"message": "Missing required fields"}), 400
    if not re.match(email_regex, email):
        return jsonify({"message": "Invalid email format"}), 400
    if len(confirm_new_password) < 8:
        return jsonify({"message": "Password must be at least 8 characters long"}), 400
    if len(confirm_new_password) > 28:
        return jsonify({"message": "Password must be at most 28 characters long"}), 400
    if not re.search(r"[A-Z]", confirm_new_password):
        return jsonify({"message": "Password must contain an uppercase letter"}), 400
    if not re.search(r"[a-z]", confirm_new_password):
        return jsonify({"message": "Password must contain a lowercase letter"}), 400
    if not re.search(r"\d", confirm_new_password):
        return jsonify({"message": "Password must contain a number"}), 400
    if not re.search(r"[!@#$%^&*()]", confirm_new_password):
        return jsonify({"message": "Password must contain a special character"}), 400

    peppered_new_password = confirm_new_password + PEPPER
    hashed_password = generate_password_hash(peppered_new_password)

    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password,email,))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Password changed successfully",
        "email": email,
    }), 200

@main.route("/api/updateAccount", methods=["POST"])
def update_account():
    data = request.get_json()
    email = data.get("email")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    role_id = data.get("role_id")



@main.route("/api/deleteAccount", methods=["POST"])
def delete_account():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE email = %s", (email,))
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Account deleted successfully",
        "email": email,
    }), 200