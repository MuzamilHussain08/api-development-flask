from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("students.db")
con.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    email TEXT
)
""")

con.commit()
con.close()


@app.route('/students', methods=['GET'])
def show_students():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    rows = con.execute("SELECT * FROM students").fetchall()

    students = [dict(row) for row in rows]

    con.close()
    return jsonify(students)


@app.route('/students/<int:id>', methods=['GET'])
def show_student(id):
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    row = con.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    con.close()

    if row is None:
        return jsonify({"message": "Student not found"}), 404

    return jsonify(dict(row))

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    con = sqlite3.connect("students.db")

    con.execute(
        "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
        (data['name'], data['department'], data['email'])
    )

    con.commit()
    con.close()

    return jsonify({"message": "Student added"}), 201


@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    con = sqlite3.connect("students.db")

    result = con.execute(
        "UPDATE students SET name=?, department=?, email=? WHERE id=?",
        (data['name'], data['department'], data['email'], id)
    )

    con.commit()
    con.close()

    if result.rowcount == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student updated"})


@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    con = sqlite3.connect("students.db")

    result = con.execute(
        "DELETE FROM students WHERE id=?", (id,)
    )

    con.commit()
    con.close()

    if result.rowcount == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted"})


if __name__ == '__main__':
    app.run(debug=True)
