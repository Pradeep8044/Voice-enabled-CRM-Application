import streamlit as st
import speech_recognition as sr
import sqlite3
from datetime import datetime

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('customers.db')
    return conn

# Function to create customer table if not exists
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            points INTEGER NOT NULL,
            enrollment_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
create_table()

# Streamlit UI
st.set_page_config(page_title="Customer Management App", layout="wide")
st.title("🎤 Customer Management Application")

# Sidebar for navigation
st.sidebar.header("Navigation")
app_mode = st.sidebar.selectbox("Choose App Mode", ["Add Customer", "Search Customer"])

if app_mode == "Add Customer":
    st.header("➕ Add New Customer")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth", datetime.now())
    phone = st.text_input("Phone Number")
    points = st.number_input("Reward Points", min_value=0)

    if st.button("Add Customer"):
        enrollment_date = datetime.now().strftime("%Y-%m-%d")
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, dob, phone, points, enrollment_date) VALUES (?, ?, ?, ?, ?)', (name, dob.strftime("%Y-%m-%d"), phone, points, enrollment_date))
        conn.commit()
        conn.close()
        st.success("✅ Customer added successfully!")

elif app_mode == "Search Customer":
    st.header("🔍 Search Existing Customer")
    st.write("Press the button and speak the customer's name to search.")

    if st.button("Start Voice Search"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎤 Listening...")
            audio = r.listen(source)

        try:
            customer_name = r.recognize_google(audio)
            st.success(f"You said: **{customer_name}**")

            # Search for the customer in the database (case-sensitive)
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE name = ?', (customer_name,))
            customer = cursor.fetchone()
            conn.close()

            if customer:
                # Display customer details
                st.write("### Customer Details:")
                st.write(f"**Name:** {customer[1]}")
                st.write(f"**DOB:** {customer[2]}")
                st.write(f"**Phone:** {customer[3]}")
                st.write(f"**Existing Points:** {customer[4]}")
                st.write(f"**Enrollment Date:** {customer[5]}")

                # Add options to add or deduct points
                add_points = st.number_input("Add Points", min_value=0)
                deduct_points = st.number_input("Deduct Points", min_value=0)

                if st.button("Update Points"):
                    new_points = customer[4] + add_points - deduct_points
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE customers SET points = ? WHERE id = ?', (new_points, customer[0]))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Updated points for **{customer[1]}** to **{new_points}**.")
            else:
                st.error("❌ Customer not found.")

        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError:
            st.error("❌ Could not request results from Google Speech Recognition service.")

# Footer
st.markdown("---")
st.write("### Developed by [Pradeep Lakkam](https://www.linkedin.com/in/pradeep2023/) | Connect with me!")
