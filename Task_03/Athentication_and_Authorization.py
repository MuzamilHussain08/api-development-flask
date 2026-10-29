from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)


users = {
    "john": {"password": "emp123", "role": "employee"},
    "admin": {"password": "admin123", "role": "admin"},
}
tokens = {}
employees = [
    {"id": 1, "name": "Muzamil", "position": "Developer"},
    {"id": 2, "name": "Ali Raza", "position": "Designer"},
]
next_id = 3

def get_current_user():
    token = request.headers.get("Token")
    if token is None:
        return None
    if token not in tokens:
        return None
    username = tokens[token]
    return users[username]


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        token = secrets.token_hex(16)
        tokens[token] = username
        return jsonify({"token": token})

    return jsonify({"error": "Wrong username or password"}), 401

@app.route("/employees", methods=["GET"])
def view_employees():
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Please login first"}), 401
    return jsonify(employees)



@app.route("/employees", methods=["POST"])
def add_employee():
    global next_id
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Please login first"}), 401
    if user["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()
    employee = {"id": next_id, "name": data["name"], "position": data["position"]}
    employees.append(employee)
    next_id = next_id + 1
    return jsonify(employee), 201


@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Please login first"}), 401
    if user["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()
    for emp in employees:
        if emp["id"] == emp_id:
            emp["name"] = data["name"]
            emp["position"] = data["position"]
            return jsonify(emp)
    return jsonify({"error": "Employee not found"}), 404


@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Please login first"}), 401
    if user["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            return jsonify({"message": "Employee deleted"})
    return jsonify({"error": "Employee not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)