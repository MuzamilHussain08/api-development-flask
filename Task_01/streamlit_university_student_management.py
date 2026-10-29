
import streamlit as st
import requests
import pandas as pd

url = "http://127.0.0.1:5000/students"

st.title("University Student Records")

tab1, tab2, tab3, tab4 = st.tabs([
    "View Students", "Add Student", "Update Student", "Delete Student"
])


with tab1:
    if st.button("Refresh Records"):
        st.rerun()
    response = requests.get(url)
    if response.status_code == 200:
        students = response.json()

        if students:
            st.dataframe(pd.DataFrame(students), hide_index=True)
        else:
            st.write("No student records available.")

with tab2:
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    email = st.text_input("Email Address")

    if st.button("Save Student"):
        data = {
            "name": name,
            "department": department,
            "email": email
        }

        response = requests.post(url, json=data)

        if response.status_code == 201:
            st.success("Student saved successfully.")
        else:
            st.error("Unable to save student.")


with tab3:
    response = requests.get(url)
    students = response.json()

    if students:
        ids = [s["id"] for s in students]
        student_id = st.selectbox("Select Student ID", ids)

        student = next(s for s in students if s["id"] == student_id)

        new_name = st.text_input("Name", value=student["name"])
        new_department = st.text_input(
            "Department", value=student["department"]
        )
        new_email = st.text_input("Email", value=student["email"])

        if st.button("Update Record"):
            data = {
                "name": new_name,
                "department": new_department,
                "email": new_email
            }

            response = requests.put(
                url + "/" + str(student_id), json=data
            )

            if response.status_code == 200:
                st.success("Student updated successfully.")
            else:
                st.error("Unable to update student.")
    else:
        st.write("No students available to update.")


with tab4:
    response = requests.get(url)
    students = response.json()

    if students:
        ids = [s["id"] for s in students]
        delete_id = st.selectbox("Choose Student ID", ids)

        if st.button("Delete Record"):
            response = requests.delete(url + "/" + str(delete_id))

            if response.status_code == 200:
                st.success("Student deleted successfully.")
                st.rerun()
            else:
                st.error("Unable to delete student.")
    else:
        st.write("No students available to delete.")
