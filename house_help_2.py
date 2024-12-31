# -*- coding: utf-8 -*-
"""House Helper Management System"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File Paths and User Credentials
EXCEL_FILE = 'house_helps.xlsx'
UPLOADS_DIR = 'uploads'
USER_CREDENTIALS = {"admin": "admin1"}  # Simple dictionary for authentication

# Ensure the uploads directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Create the Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[ 
        'name', 'age', 'gender', 'address', 'contact', 
        'experience', 'photo_path', 'rate', 'registration_date'
    ])
    df.to_excel(EXCEL_FILE, index=False)

# Function: Register Helper
def register_helper():
    st.subheader("🔄 Register New Helper")

    name = st.text_input("👤 Enter Name:", key="name")
    age = st.number_input("📅 Enter Age:", min_value=18, max_value=100)
    gender = st.selectbox("⚥ Select Gender:", ['Male', 'Female', 'Other'])
    address = st.text_area("📍 Enter Address:")
    contact = st.text_input("📞 Enter Contact Number:")
    experience = st.number_input("💼 Enter Experience (in years):", min_value=0)
    rate = st.number_input("💵 Enter Rate per day:", min_value=0.0)
    photo = st.file_uploader("🖼️ Upload Photo", type=["jpg", "png", "jpeg"])

    if st.button("✅ Register Helper", key="register_button"):
        try:
            # Load existing data
            df = pd.read_excel(EXCEL_FILE)

            # Check for duplicate phone number
            if contact in df['contact'].values:
                st.warning("⚠️ A helper with this contact number already exists!")
                return

            # Save photo if uploaded
            if photo is not None:
                photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.name}"
                photo_path = os.path.join(UPLOADS_DIR, photo_filename)
                with open(photo_path, "wb") as f:
                    f.write(photo.getbuffer())
            else:
                photo_path = "No photo uploaded"

            # Add new helper data
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_data = {
                'name': name, 'age': age, 'gender': gender, 'address': address,
                'contact': contact, 'experience': experience, 'rate': rate,
                'photo_path': photo_path, 'registration_date': registration_date
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)

            st.success("✅ Registration successful!")
        except Exception as e:
            st.error(f"❌ Error during registration: {str(e)}")

# Function: Search Helper
def search_helper():
    st.subheader("🔍 Search Helper")

    search_term = st.text_input("🔎 Enter Name or Contact Number to Search:")

    if st.button("✅ Search Helper"):
        try:
            # Load the data
            df = pd.read_excel(EXCEL_FILE)

            # Search for helpers matching the search term
            search_results = df[df['contact'].str.contains(search_term, case=False) | df['name'].str.contains(search_term, case=False)]

            if search_results.empty:
                st.warning("⚠️ No helper found with that name or contact number.")
            else:
                st.dataframe(search_results[['name', 'age', 'gender', 'rate', 'contact', 'registration_date']])
        except Exception as e:
            st.error(f"❌ Error during search: {str(e)}")

# Function: Admin Use (Overview, Deletion, and Download)
def admin_use():
    st.subheader("👨‍💻 Admin Panel")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("✅ Login", key="login_button"):
        # Debug message to display entered username and password
        st.write(f"Entered username: {username}, Entered password: {password}")
        
        # Compare entered credentials with predefined credentials
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success("✅ Login successful!")

            # Load the data
            df = pd.read_excel(EXCEL_FILE)

            menu = st.selectbox(
                "Choose an Admin Action:",
                ["Overview of Helpers", "Delete Helper", "Download Excel File"]
            )

            # Overview of Helpers
            if menu == "Overview of Helpers":
                st.dataframe(df[['name', 'age', 'gender', 'rate', 'registration_date']])

            # Delete Helper
            elif menu == "Delete Helper":
                contact_to_delete = st.text_input("Enter the contact number of the helper to delete:")
                if st.button("Delete Helper"):
                    if contact_to_delete in df['contact'].values:
                        df = df[df['contact'] != contact_to_delete]
                        df.to_excel(EXCEL_FILE, index=False)
                        st.success("✅ Helper deleted successfully!")
                    else:
                        st.warning("⚠️ Helper not found with this contact number.")

            # Download Excel File
            elif menu == "Download Excel File":
                try:
                    file_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📂 Download Excel File",
                        data=file_data,
                        file_name="house_helps.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"❌ Error while preparing the file for download: {str(e)}")
        else:
            st.error(f"❌ Invalid username or password. You entered username: {username} and password: {password}")

# Main Streamlit Application
def main():
    st.set_page_config(
        page_title="House Helper Management System",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS Styling
    st.markdown("""<style>
    .main { background-color: #f8f9fa; }
    .css-18e3th9 { background-color: #ffffff; }
    .css-1d391kg { color: #007bff; font-size: 24px; font-weight: bold; }
    .stButton > button { background-color: #007bff; color: white; border-radius: 8px; padding: 12px 24px; font-size: 16px;}
    .stButton > button:hover { background-color: #0056b3;}
    .stTextInput input { background-color: #f1f1f1; border: 1px solid #007bff; border-radius: 8px;}
    .stTextArea textarea { background-color: #f1f1f1; border: 1px solid #007bff; border-radius: 8px;}
    .stSelectbox select { background-color: #f1f1f1; border: 1px solid #007bff; border-radius: 8px;}
    .stNumberInput input { background-color: #f1f1f1; border: 1px solid #007bff; border-radius: 8px;}
    .stFileUploader { background-color: #f1f1f1; border: 1px solid #007bff; border-radius: 8px;}
    .stFileUploader:hover { background-color: #e2e6ea;}
    .stTextInput input:focus { border: 2px solid #007bff;}
    .stSelectbox select:focus { border: 2px solid #007bff;}
    .stTextArea textarea:focus { border: 2px solid #007bff;}
    .stButton > button { background-color: #28a745;}
    .stButton > button:hover { background-color: #218838;}
    </style>""", unsafe_allow_html=True)

    st.title("🏠 House Helper Management System")
    st.sidebar.header("📋 Navigation")

    menu = st.sidebar.radio(
        "Choose an Option:",
        ["Register Helper", "Search Helper", "Admin Use"]
    )

    if menu == "Register Helper":
        register_helper()
    elif menu == "Search Helper":
        search_helper()
    elif menu == "Admin Use":
        admin_use()

# Run the Streamlit App
if __name__ == '__main__':
    main()
