import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="benak@2010",
        database="FarmManagement"
    )

# Function to execute query and return results
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Function to execute an update/insert query
def run_action(query, values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Streamlit App
def main():
    st.title("Farm Management System")

    # Login Page
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "admin123":
            st.success("Login successful")
            st.sidebar.title("Navigation")
            pages = ["Farmer Details", "Employee Details", "Equipment Details"]
            page = st.sidebar.selectbox("Choose a page", pages)

            if page == "Farmer Details":
                display_farmer_details()

            elif page == "Employee Details":
                display_employee_details()

            elif page == "Equipment Details":
                display_equipment_details()

        else:
            st.error("Invalid username or password")

def display_farmer_details():
    st.header("Farmer Details")
    farmers = run_query("SELECT * FROM Farmer")
    st.write(farmers)

def display_employee_details():
    st.header("Employee Details")
    employees = run_query("SELECT * FROM Employee")
    st.write(employees)

def display_equipment_details():
    st.header("Equipment Details")
    equipment = run_query("SELECT * FROM Equipment")
    st.write(equipment)

if __name__ == "__main__":
    main()
