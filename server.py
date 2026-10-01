import os
import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "admin_data.db"

secret_key = os.environ.get("KOC_SECRET_KEY")
if not secret_key:
    raise RuntimeError("Set KOC_SECRET_KEY before starting the server.")

app = Flask(__name__, static_folder=None)
app.secret_key = secret_key

PUBLIC_FILES = {
    "About.html",
    "accesories.html",
    "contact.html",
    "five 5.jpg",
    "four 4.jpg",
    "index.html",
    "inventory.js",
    "logo.jpg",
    "men.html",
    "products.html",
    "products.json",
    "six 6.jpg",
    "three 3.jpg",
    "two 2.jpg",
    "women.html",
}


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        existing = conn.execute("SELECT COUNT(*) AS count FROM admins").fetchone()["count"]
        if existing == 0:
            admins = []
            for index in (1, 2):
                username = (os.environ.get(f"KOC_ADMIN{index}_USERNAME") or "").strip()
                password = os.environ.get(f"KOC_ADMIN{index}_PASSWORD") or ""
                if not username or not password:
                    raise RuntimeError(
                        f"Set KOC_ADMIN{index}_USERNAME and KOC_ADMIN{index}_PASSWORD "
                        "before initializing a new admin database."
                    )
                admins.append((username, password))

            for username, password in admins:
                conn.execute(
                    "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
        elif existing > 2:
            raise RuntimeError("Only two admin accounts are allowed.")
        conn.commit()
    finally:
        conn.close()


@app.before_request
def ensure_db_ready():
    init_db()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        conn = get_db_connection()
        user = conn.execute(
            "SELECT username, password_hash FROM admins WHERE username = ?",
            (username,),
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["admin_user"] = user["username"]
            return redirect(url_for("admin_dashboard"))

        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/admin")
def admin_dashboard():
    if session.get("admin_user") is None:
        return redirect(url_for("login"))

    conn = get_db_connection()
    admins = conn.execute("SELECT username FROM admins ORDER BY username").fetchall()
    conn.close()

    return render_template("admin.html", current_user=session["admin_user"], admins=admins)


@app.route("/admin.html")
def admin_file():
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/<path:filename>")
def serve_public_file(filename):
    if filename in PUBLIC_FILES or filename.startswith("product-images/"):
        return send_from_directory(BASE_DIR, filename)
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
