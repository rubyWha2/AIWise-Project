"""
API routes: auth, user management and data endpoints
"""

from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection
from dotenv import load_dotenv
from . import limiter
import re
import os
import secrets
from . import mail
from flask_mail import Message

load_dotenv()
PEPPER = os.getenv("PASSWORD_PEPPER", "")

main = Blueprint('main', __name__)

def login_rate_limit_key():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    return f"{request.remote_addr}:{email}"

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
@limiter.limit("5 per hour")
def register():
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email", "").strip().lower()
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
        cur.execute("SELECT email FROM users WHERE LOWER(email) = %s", (email,))
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
@limiter.limit("7 per minute", key_func=login_rate_limit_key)
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    peppered_password = password + PEPPER

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT user_id, username, password_hash, role_id, failed_attempts, locked_until FROM users WHERE LOWER(email) = %s", (email,))

        user = cur.fetchone()

        if user is None:
            conn.close()
            return jsonify({"message": "Invalid email or password"}), 401

        user_id = user[0]
        username = user[1]
        password_hash = user[2]
        role_id = user[3]
        failed_attempts = user[4] or 0
        locked_until = user[5]

        if locked_until and locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)

        if locked_until and locked_until > datetime.now(timezone.utc):
            conn.close()
            return jsonify({"message": "Account locked. Try again later."}), 423

        if not check_password_hash(password_hash, peppered_password):
            failed_attempts += 1
            if failed_attempts >= 5:
                locked_until = datetime.now(timezone.utc) + timedelta(minutes=10)
                cur.execute("UPDATE users SET failed_attempts = %s, locked_until = %s WHERE user_id = %s", (failed_attempts, locked_until, user_id))

                conn.commit()
                conn.close()

                return jsonify({"message": "Account locked. Try again later."}), 423


            cur.execute("""
                UPDATE users
                SET failed_attempts = %s
                WHERE user_id = %s
            """, (failed_attempts, user_id))

            conn.commit()
            conn.close()
            return jsonify({"message": "Invalid email or password"}), 401


        session.clear()  # clear a session
        # new session
        session["user_id"] = user_id
        session["username"] = username
        session["role_id"] = role_id

        session.modified = True
        session.permanent = True

        cur.execute("""
        UPDATE users
        SET failed_attempts = 0,
            locked_until = NULL
        WHERE user_id = %s
        """, (user_id,))

        conn.commit()

    conn.close()

    return jsonify({
        "message": "Login successful",
        "user_id": user_id,
        "username": username,
        "role_id": role_id,
    }), 200

@main.route("/api/changePassword", methods=["POST"])
@limiter.limit("5 per hour")
def change_password():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"message": "Please log in"}), 401

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

    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT password_hash FROM users WHERE user_id = %s",(user_id,))
        user = cur.fetchone()

        if user is None:
            return jsonify({"message": "User does not exist"}), 401

        if not check_password_hash(user[0], old_password+PEPPER):
            return jsonify({"message": "Old password is incorrect"}), 401

        peppered_new_password = confirm_new_password + PEPPER
        hashed_password = generate_password_hash(peppered_new_password)

        cur.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (hashed_password, user_id,))

        conn.commit()
        conn.close()

        return jsonify({"message": "Password changed successfully"}), 200



@main.route("/api/updateAccount", methods=["POST"])
@limiter.limit("20 per minute")
def update_account():
    user_id = session.get("user_id")

    if not user_id:
        print(session)
        print(session.get("user_id"))
        return jsonify({"message": "Please log in"}), 401

    data = request.get_json()

    #email = data.get("email")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    bio = data.get("bio")

    if not all([firstName, lastName, bio]):
        return jsonify({"message": "Missing required fields"}), 400

    if len(bio) > 255:
        return jsonify({"message": "Bio must be at most 255 characters long"}), 400
    if len(firstName) > 50:
        return jsonify({"message": "First name must be at most 50 characters long"}), 400
    if len(lastName) > 50:
        return jsonify({"message": "Last name must be at most 50 characters long"}), 400

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET username = %s, bio = %s WHERE user_id = %s", (firstName +  lastName, bio, user_id,))

    conn.commit()
    conn.close()
    return jsonify({
        "message": "Account updated successfully"}), 200

@main.route("/api/deleteAccount", methods=["POST"])
@limiter.limit("3 per hour")
def delete_account():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"message": "Please log in"}), 401

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Account deleted successfully",
        "email": user_id,
    }), 200

@main.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({"message": "Logged out"}), 200

@main.route("/api/sendVerificationEmail", methods=["POST"])
def sendVerificationEmail():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "Please log in"}), 401

    token = secrets.token_urlsafe(32)
    verification_link = f"http://localhost:5173/verify-email?token={token}"
    expiry = datetime.utcnow() + timedelta(hours=24)

    conn = get_db_connection()

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT email,username
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )
        row = cur.fetchone()
        if row is None:
            return jsonify({"message": "User not found"}), 404

        email = row[0]
        username = row[1]

        cur.execute(
            """
            UPDATE users
            SET verification_token = %s,
                verification_expiry = %s
            WHERE user_id = %s
            """,
            (token, expiry, user_id)
        )

    conn.commit()
    conn.close()

    msg = Message(
        subject="Verify your AIWise email",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[email]
    )

    msg.body = f"""
    Hello {username},

    Thank you for creating an AIWise account.

    Please verify your email by clicking the link below:

    {verification_link}

    If you did not request this email, you can safely ignore it.

    This link expires in 24 hours.

    The AIWise Team
    """

    mail.send(msg)

    return jsonify({
        "message": "Verification email sent."
    }), 200

@main.route("/api/verifyEmail", methods=["POST"])
def verifyEmail():
    return jsonify({"message": "Verification email sent."}), 200

@main.route("/api/esendVerificationEmail", methods=["POST"])
def resendVerificationEmail():
    return jsonify({"message": "Verification email resent."}), 200
