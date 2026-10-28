# API Development

API Development is a collection of three progressive tasks that demonstrate how to design, build, secure, and test RESTful web services using Python and Flask. The projects use SQLite for persistent storage and cover the full lifecycle of a backend service: defining endpoints, validating input, handling errors with meaningful HTTP status codes, and documenting everything for easy testing.

The final task is an Employee Management API that supports complete CRUD operations on employee records. It adds JWT-based authentication, with passwords stored as secure hashes, and role-based authorization that separates administrators from regular employees. Employees can view records, while only administrators can add, update, or delete them. The API returns clear 401, 403, 404, 409, and 400 responses for each failure case.

The repository includes ready-to-run test commands, sample JSON files, and demo scripts for Windows PowerShell and Linux/macOS, along with expected outputs, so anyone can clone the repository and verify the behavior within minutes.

---

## Video Preview

> **TODO:** replace the link below with your video (YouTube unlisted / Google Drive / GitHub Release).

[Watch the demo video](https://YOUR-VIDEO-LINK-HERE)

---

## Table of Contents

1. [Repository structure](#repository-structure)
2. [Requirements and installation](#requirements-and-installation)
3. [Task 1](UNIVERISTY_MANAGEMENT_SYSTEM)
4. [Task 2]()
5. [Task 3: Employee Management API with JWT and roles](#task-3-employee-management-api-with-jwt-and-roles)

---

## Repository structure

```
api-development/
├── README.md              (this file)
├── .gitignore
├── task1/
├── task2/
└── task3/
    ├── app.py
    ├── requirements.txt
    ├── login_admin.json
    ├── login_employee.json
    ├── login_wrong.json
    ├── new_employee.json
    ├── update_employee.json
    ├── demo.sh
    └── demo.ps1
```

## Requirements and installation

- Python 3.9 or newer
- Packages: Flask and PyJWT

```powershell
python -m pip install flask PyJWT
```

> **Important:** install **`PyJWT`**, not `jwt`. They are different packages. Installing the wrong one causes
> `AttributeError: module 'jwt' has no attribute 'encode'`.
> Fix: `pip uninstall jwt PyJWT -y` then `python -m pip install PyJWT`.

Check the install:

```powershell
python -c "import jwt; print(jwt.__version__)"
```

---

## Task 1

> **TODO:** paste your Task 1 README content here (title, what it does, endpoints, how to run, test commands with expected output).

```powershell
cd task1
python app.py
```

## Task 2

> **TODO:** paste your Task 2 README content here (title, what it does, endpoints, how to run, test commands with expected output).

```powershell
cd task2
python app.py
```

---

## Task 3: Employee Management API with JWT and roles

A Flask REST API with **authentication** (JWT login) and **authorization** (roles: `admin` / `employee`).

### Demo users and seed data

| Username | Password      | Role     |
|----------|---------------|----------|
| alice    | `admin123`    | admin    |
| bob      | `employee123` | employee |

| id | name      | department | position   | email            |
|----|-----------|------------|------------|------------------|
| 1  | Sara Khan | HR         | HR Manager | sara@company.com |
| 2  | Omar Ali  | IT         | Developer  | omar@company.com |

### Who can do what

| Endpoint                 | No token | employee (bob) | admin (alice) |
|--------------------------|----------|----------------|---------------|
| `POST /login`            | public   | public         | public        |
| `GET /employees`         | 401      | 200            | 200           |
| `GET /employees/<id>`    | 401      | 200            | 200           |
| `POST /employees`        | 401      | **403**        | 201           |
| `PUT /employees/<id>`    | 401      | **403**        | 200           |
| `DELETE /employees/<id>` | 401      | **403**        | 200           |

- **401** = authentication failed (not logged in / bad token)
- **403** = authorization failed (logged in, but your role is not allowed)

### Start the server (PowerShell Window 1)

```powershell
cd task3
python app.py
```

Expected: a line like `Running on http://127.0.0.1:5000`. **Leave this window open.**

> For a clean start with the original data: stop the server (Ctrl+C), run `Remove-Item employees.db`, then start it again.

### Run the tests (PowerShell Window 2)

Open a **second** PowerShell window, go to the `task3` folder, and run the commands **one at a time**.

> Use `curl.exe` (not `curl`) in PowerShell, and keep `@file.json` inside quotes.

#### Test 1: Login with a WRONG password → 401

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "@login_wrong.json"
```

Expected:
```
HTTP/1.1 401 UNAUTHORIZED
...
{
  "error": "Invalid username or password."
}
```

#### Test 2: Login as admin and save the token

```powershell
$resp = curl.exe -s -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "@login_admin.json"
$ADMIN = ($resp | ConvertFrom-Json).token
$ADMIN
```

Expected: a long text starting with `eyJ...` (differs every time).

#### Test 3: Login as employee and save the token

```powershell
$resp = curl.exe -s -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "@login_employee.json"
$EMP = ($resp | ConvertFrom-Json).token
$EMP
```

Expected: another long `eyJ...` text. Tokens last 1 hour and are lost if you close the window.

#### Test 4: Access /employees with NO token → 401

```powershell
curl.exe -i http://127.0.0.1:5000/employees
```

Expected:
```
HTTP/1.1 401 UNAUTHORIZED
...
{
  "error": "Authentication required. Log in at /login and send 'Authorization: Bearer <token>'."
}
```

#### Test 5: Invalid token → 401

```powershell
curl.exe -i http://127.0.0.1:5000/employees -H "Authorization: Bearer abc"
```

Expected:
```
HTTP/1.1 401 UNAUTHORIZED
...
{
  "error": "Invalid token."
}
```

#### Test 6: Employee views the list → 200

```powershell
curl.exe -i http://127.0.0.1:5000/employees -H "Authorization: Bearer $EMP"
```

Expected:
```
HTTP/1.1 200 OK
...
[
  {
    "department": "HR",
    "email": "sara@company.com",
    "id": 1,
    "name": "Sara Khan",
    "position": "HR Manager"
  },
  {
    "department": "IT",
    "email": "omar@company.com",
    "id": 2,
    "name": "Omar Ali",
    "position": "Developer"
  }
]
```

#### Test 7: Employee views one employee → 200

```powershell
curl.exe http://127.0.0.1:5000/employees/1 -H "Authorization: Bearer $EMP"
```

Expected:
```json
{
  "department": "HR",
  "email": "sara@company.com",
  "id": 1,
  "name": "Sara Khan",
  "position": "HR Manager"
}
```

#### Test 8: Employee not found → 404

```powershell
curl.exe -i http://127.0.0.1:5000/employees/99 -H "Authorization: Bearer $EMP"
```

Expected:
```
HTTP/1.1 404 NOT FOUND
...
{
  "error": "Employee not found"
}
```

#### Test 9: Employee tries to ADD → 403 (logged in but NOT authorized)

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -H "Authorization: Bearer $EMP" -d "@new_employee.json"
```

Expected:
```
HTTP/1.1 403 FORBIDDEN
...
{
  "error": "Forbidden. You are authenticated but not authorized for this action.",
  "required_role": [
    "admin"
  ],
  "your_role": "employee"
}
```

#### Test 10: Employee tries to DELETE → 403

```powershell
curl.exe -i -X DELETE http://127.0.0.1:5000/employees/1 -H "Authorization: Bearer $EMP"
```

Expected: the same `403 FORBIDDEN` response as Test 9.

#### Test 11: Admin ADDS an employee → 201

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN" -d "@new_employee.json"
```

Expected:
```
HTTP/1.1 201 CREATED
...
{
  "department": "Finance",
  "email": "ayesha@company.com",
  "id": 3,
  "name": "Ayesha Noor",
  "position": "Accountant"
}
```

#### Test 12: Add the SAME employee again → 409 (duplicate email)

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN" -d "@new_employee.json"
```

Expected:
```
HTTP/1.1 409 CONFLICT
...
{
  "error": "An employee with this email already exists"
}
```

#### Test 13: Admin UPDATES employee 2 → 200

```powershell
curl.exe -i -X PUT http://127.0.0.1:5000/employees/2 -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN" -d "@update_employee.json"
```

Expected:
```
HTTP/1.1 200 OK
...
{
  "department": "IT",
  "email": "omar@company.com",
  "id": 2,
  "name": "Omar Ali",
  "position": "Senior Developer"
}
```

#### Test 14: Admin DELETES employee 1 → 200

```powershell
curl.exe -i -X DELETE http://127.0.0.1:5000/employees/1 -H "Authorization: Bearer $ADMIN"
```

Expected:
```
HTTP/1.1 200 OK
...
{
  "message": "Employee 1 deleted"
}
```

#### Test 15: Admin views the final list → 200

```powershell
curl.exe http://127.0.0.1:5000/employees -H "Authorization: Bearer $ADMIN"
```

Expected (Sara deleted, Omar updated, Ayesha added):
```json
[
  {
    "department": "IT",
    "email": "omar@company.com",
    "id": 2,
    "name": "Omar Ali",
    "position": "Senior Developer"
  },
  {
    "department": "Finance",
    "email": "ayesha@company.com",
    "id": 3,
    "name": "Ayesha Noor",
    "position": "Accountant"
  }
]
```

### Summary of results

| Test | Who              | Action            | Expected |
|------|------------------|-------------------|----------|
| 1    | alice (wrong pw) | login             | 401      |
| 4    | nobody           | list employees    | 401      |
| 5    | bad token        | list employees    | 401      |
| 6    | bob              | list employees    | 200      |
| 8    | bob              | get employee 99   | 404      |
| 9    | bob              | add employee      | **403**  |
| 10   | bob              | delete employee   | **403**  |
| 11   | alice            | add employee      | 201      |
| 12   | alice            | add duplicate     | 409      |
| 13   | alice            | update employee 2 | 200      |
| 14   | alice            | delete employee 1 | 200      |
| 15   | alice            | list employees    | 200      |

### Automatic run (optional)

With the server running, in a second window:

```powershell
powershell -ExecutionPolicy Bypass -File .\demo.ps1
```

On Linux/macOS/Git Bash: `bash demo.sh`

### Linux / macOS equivalents

```bash
URL=http://127.0.0.1:5000
H='Content-Type: application/json'
ADMIN=$(curl -s -X POST $URL/login -H "$H" -d @login_admin.json | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
EMP=$(curl -s -X POST $URL/login -H "$H" -d @login_employee.json | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
curl -i $URL/employees -H "Authorization: Bearer $EMP"
```

The remaining commands follow the same pattern as the PowerShell versions above.

---

## Troubleshooting

| Problem | Cause / fix |
|---|---|
| `curl: (7) Failed to connect` | Server is not running. Start it with `python app.py` in Window 1. |
| `Failed to open/read local data from file` | Wrong folder. `cd` into the folder that contains the `*.json` files. |
| `The splatting operator '@' cannot be used...` | You used `curl` with unquoted `@file`. Use `curl.exe` and write `"@file.json"` in quotes. |
| `$ADMIN` prints nothing | Run the raw login command (Test 2 without saving) and read the response. Check the server is running. |
| `AttributeError: module 'jwt' has no attribute 'encode'` | Wrong package installed. Install `PyJWT`, not `jwt`. |
| `401 Invalid username or password` for alice/bob | Old `employees.db` has different users. Stop the server, `Remove-Item employees.db`, restart. |
| Test 11 returns 409 | The employee was already added. Reset the database. |
| `Token expired. Please log in again.` | Tokens last 1 hour. Repeat Tests 2 and 3. |

> **Production note:** set a real secret with `$env:SECRET_KEY = "long-random-string"` (the built-in default is for demos only) and run with `debug=False`.
