HOW TO RUN
----------
pip install flask streamlit requests

Run one API at a time. Stop the old one with Ctrl+C before starting another.

Task 1 (port 5000):
  python task1_api.py            (terminal 1)
  streamlit run task1_app.py     (terminal 2)

Task 2 (port 5000):
  python task2_generate_keys.py  (creates keys.json, prints 3 keys)
  python task2_api.py

Task 3 (port 5001):
  python task3_api.py


NOTES (Windows PowerShell)
--------------------------
Use curl.exe, not curl.
JSON goes inside single quotes, inner quotes use a backslash.
-i shows the status code (200, 401, 403).


TASK 2 CURL TESTS (replace KEY1, KEY2, KEY3 with the printed keys)
------------------------------------------------------------------
Tester 1 (200):
curl.exe -i -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -H "X-API-Key: KEY1" -d '{\"text\": \"hello world\"}'

Tester 2 (200):
curl.exe -i -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -H "X-API-Key: KEY2" -d '{\"text\": \"hello world\"}'

Tester 3 (200):
curl.exe -i -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -H "X-API-Key: KEY3" -d '{\"text\": \"hello world\"}'

Invalid key (401):
curl.exe -i -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -H "X-API-Key: wrongkey" -d '{\"text\": \"hello world\"}'

Missing key (401):
curl.exe -i -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -d '{\"text\": \"hello world\"}'


TASK 3 CURL TESTS (port 5001)
-----------------------------
0. Check the right server is running (should be 401 JSON, not HTML 404):
curl.exe -i http://127.0.0.1:5001/employees

1. Wrong password (authentication fails, 401):
curl.exe -i -X POST http://127.0.0.1:5001/login -H "Content-Type: application/json" -d '{\"username\": \"john\", \"password\": \"wrong\"}'

2. No login (401):
curl.exe -i http://127.0.0.1:5001/employees

3. Login as employee (200), copy the token:
curl.exe -i -X POST http://127.0.0.1:5001/login -H "Content-Type: application/json" -d '{\"username\": \"john\", \"password\": \"emp123\"}'

4. Employee can view (200), replace EMPLOYEE_TOKEN:
curl.exe -i http://127.0.0.1:5001/employees -H "Token: EMPLOYEE_TOKEN"

5. Employee tries to add (authorization fails, 403):
curl.exe -i -X POST http://127.0.0.1:5001/employees -H "Content-Type: application/json" -H "Token: EMPLOYEE_TOKEN" -d '{\"name\": \"Omar\", \"position\": \"Tester\"}'

6. Employee tries to delete (403):
curl.exe -i -X DELETE http://127.0.0.1:5001/employees/1 -H "Token: EMPLOYEE_TOKEN"

7. Login as admin (200), copy the token:
curl.exe -i -X POST http://127.0.0.1:5001/login -H "Content-Type: application/json" -d '{\"username\": \"admin\", \"password\": \"admin123\"}'

8. Admin adds (201), replace ADMIN_TOKEN:
curl.exe -i -X POST http://127.0.0.1:5001/employees -H "Content-Type: application/json" -H "Token: ADMIN_TOKEN" -d '{\"name\": \"Omar\", \"position\": \"Tester\"}'

9. Admin updates (200):
curl.exe -i -X PUT http://127.0.0.1:5001/employees/1 -H "Content-Type: application/json" -H "Token: ADMIN_TOKEN" -d '{\"name\": \"Ali Khan\", \"position\": \"Senior Developer\"}'

10. Admin deletes (200):
curl.exe -i -X DELETE http://127.0.0.1:5001/employees/2 -H "Token: ADMIN_TOKEN"

Difference:
  401 = authentication problem (not logged in / wrong login)
  403 = authorization problem (logged in but not allowed)
