from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, department TEXT, email TEXT)")
    conn.commit()
    conn.close()


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    students = []
    for row in rows:
        students.append(dict(row))
    return jsonify(students)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(row))


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
                 (data["name"], data["department"], data["email"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added"}), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    conn.execute("UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?",
                 (data["name"], data["department"], data["email"], student_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
