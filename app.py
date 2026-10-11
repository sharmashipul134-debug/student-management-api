import os
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DATABASE = os.environ.get("DATABASE_PATH", "students.db")
API_KEY = os.environ.get("API_KEY", "change-this-development-key")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def require_api_key(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        supplied_key = request.headers.get("X-API-Key")
        if not supplied_key or supplied_key != API_KEY:
            return jsonify({"error": "Unauthorized. Provide a valid X-API-Key header."}), 401
        return view(*args, **kwargs)
    return wrapped


def validate_student(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."
    required = ["name", "course", "email"]
    if not partial:
        missing = [field for field in required if not data.get(field)]
        if missing:
            return "Missing required fields: " + ", ".join(missing)
    for field in required:
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            return f"'{field}' must be a non-empty string."
    if "email" in data and ("@" not in data["email"] or "." not in data["email"].split("@")[-1]):
        return "'email' must be a valid email address."
    return None


def student_dict(row):
    return {"id": row["id"], "name": row["name"], "course": row["course"], "email": row["email"]}


@app.get("/")
def home():
    return jsonify({
        "message": "Student Management REST API",
        "endpoints": {
            "GET /students": "List students",
            "GET /students/<id>": "Get one student",
            "POST /students": "Create student",
            "PUT /students/<id>": "Replace student details",
            "PATCH /students/<id>": "Update selected fields",
            "DELETE /students/<id>": "Delete student"
        },
        "authentication": "Protected endpoints require the X-API-Key header."
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/students")
@require_api_key
def list_students():
    rows = get_db().execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([student_dict(row) for row in rows])


@app.get("/students/<int:student_id>")
@require_api_key
def get_student(student_id):
    row = get_db().execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Student not found."}), 404
    return jsonify(student_dict(row))


@app.post("/students")
@require_api_key
def create_student():
    data = request.get_json(silent=True)
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400
    try:
        db = get_db()
        cursor = db.execute(
            "INSERT INTO students (name, course, email) VALUES (?, ?, ?)",
            (data["name"].strip(), data["course"].strip(), data["email"].strip().lower())
        )
        db.commit()
        row = db.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(student_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists."}), 409


@app.put("/students/<int:student_id>")
@require_api_key
def replace_student(student_id):
    data = request.get_json(silent=True)
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400
    db = get_db()
    existing = db.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
    if existing is None:
        return jsonify({"error": "Student not found."}), 404
    try:
        db.execute(
            "UPDATE students SET name = ?, course = ?, email = ? WHERE id = ?",
            (data["name"].strip(), data["course"].strip(), data["email"].strip().lower(), student_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists."}), 409
    row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return jsonify(student_dict(row))


@app.patch("/students/<int:student_id>")
@require_api_key
def patch_student(student_id):
    data = request.get_json(silent=True)
    error = validate_student(data, partial=True)
    if error:
        return jsonify({"error": error}), 400
    allowed = {"name", "course", "email"}
    if not data or not any(field in data for field in allowed):
        return jsonify({"error": "Provide at least one field to update."}), 400
    db = get_db()
    row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Student not found."}), 404
    values = {key: row[key] for key in allowed}
    values.update({key: value.strip() for key, value in data.items() if key in allowed})
    values["email"] = values["email"].lower()
    try:
        db.execute(
            "UPDATE students SET name = ?, course = ?, email = ? WHERE id = ?",
            (values["name"], values["course"], values["email"], student_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists."}), 409
    updated = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return jsonify(student_dict(updated))


@app.delete("/students/<int:student_id>")
@require_api_key
def delete_student(student_id):
    db = get_db()
    cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"message": "Student deleted successfully."})


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found."}), 404


if __name__ == "__main__":
    # Debug mode is for local development only; do not use it in production.
    app.run(debug=True)
