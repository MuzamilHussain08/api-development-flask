import streamlit as st
import requests

URL = "http://127.0.0.1:5000/students"

st.title("Student Management")

response = requests.get(URL)
students = response.json()


st.header("All Students")
if len(students) == 0:
    st.write("No students yet.")
else:
    st.table(students)


st.header("Add Student")
with st.form("add_form", clear_on_submit=True):
    name = st.text_input("Name")
    department = st.text_input("Department")
    email = st.text_input("Email")
    add_button = st.form_submit_button("Add")

if add_button:
    if name == "" or department == "" or email == "":
        st.error("Please fill all fields")
    else:
        data = {"name": name, "department": department, "email": email}
        r = requests.post(URL, json=data)
        if r.status_code == 201:
            st.success("Student added")
            st.rerun()
        else:
            st.error("Could not add student")

st.header("Update or Delete Student")
if len(students) > 0:
    ids = []
    for s in students:
        ids.append(s["id"])

    selected_id = st.selectbox("Select student ID", ids)


    selected = None
    for s in students:
        if s["id"] == selected_id:
            selected = s

    new_name = st.text_input("Name", value=selected["name"], key="name_" + str(selected_id))
    new_department = st.text_input("Department", value=selected["department"], key="dept_" + str(selected_id))
    new_email = st.text_input("Email", value=selected["email"], key="email_" + str(selected_id))

    if st.button("Update"):
        data = {"name": new_name, "department": new_department, "email": new_email}
        r = requests.put(URL + "/" + str(selected_id), json=data)
        if r.status_code == 200:
            st.success("Student updated")
            st.rerun()
        else:
            st.error("Could not update student")

    if st.button("Delete"):
        r = requests.delete(URL + "/" + str(selected_id))
        if r.status_code == 200:
            st.success("Student deleted")
            st.rerun()
        else:
            st.error("Could not delete student")
