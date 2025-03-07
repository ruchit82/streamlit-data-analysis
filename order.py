
import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
from io import BytesIO
 
# Function for user authentication
def login(users):
    if "authenticated_user":
        authenticated_user = None
 
    if "authenticated_user":
        authenticated_user = None
 
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}!")
            st.session_state.authenticated_user = username
            return username
        else:
            st.error("Invalid credentials. Please try again.")
    return None
 
# Function to resize image
def resize_image(image, max_width=300):
    if image.width > max_width:
        new_height = int((max_width / image.width) * image.height)
        return image.resize((max_width, new_height))
    return image
 
# Function to combine image and text
def combine_image_with_text(image, details):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Path to system font
    font = ImageFont.truetype(font_path, size=16)  # Set font size to 20, bold
    text_width = 300
    canvas_width = image.width + text_width
    canvas_height = max(image.height, 450)
 
    combined_image = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(combined_image)
 
    # Draw text on the left side
    y_position = 10
    for key, value in details.items():
        draw.text((10, y_position), f"{key}: {value}", fill="black", font=font)
        y_position += 26  # Increased line spacing for larger font
 
    # Paste the image on the right side
    combined_image.paste(image, (text_width, 0))
 
    return combined_image
 
# Function to save data to Excel
def save_to_excel(details, excel_file_path):
    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        new_entry = pd.DataFrame([details])
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = pd.DataFrame([details])
    df.to_excel(excel_file_path, index=False)
 
# Function to generate summary report
def generate_summary_report(excel_file_path):
    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        return df
    else:
        return pd.DataFrame()
 
# Function to delete orders based on date or all data
def delete_orders(excel_file_path, date_to_delete=None):
    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        if date_to_delete:
            df = df[df["Date"] != str(date_to_delete)]  # Keep rows not matching the date
            st.success(f"Orders for {date_to_delete} have been deleted.")
        else:
            df = pd.DataFrame()  # Clear all data
            st.success("All orders have been deleted.")
        df.to_excel(excel_file_path, index=False)
    else:
        st.info("No data exists yet.")
 
# Streamlit app
users = {"user1": "password1", "user2": "password2"}
username = login(users)
 
if username:
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select an option", ["Add New Order", "View Summary Report", "Search Order", "Delete Orders", "Download Data"])
 
    excel_file_path = f"{username}_order_details.xlsx"
 
    if menu == "Add New Order":
        st.title("Add New Order")
 
        image_file = st.file_uploader("Upload Order Image", type=["jpg", "png"])
 
        # Input fields for order details
        Date = st.date_input("Date", value=datetime.today().date())
        Party_code = st.text_input("Party Code")
        Party_name = st.text_input("Party Name")
        Order_no = st.text_input("Order No")
        Weight = st.text_input("Weight")
        Size = st.text_input("Size")
        PCS = st.text_input("PCS")
        Rhodium = st.text_input("Rhodium (Yes/No)")
        Remark = st.text_area("Remark")
 
        if st.button("Submit"):
            image = None
            if image_file:
                image = Image.open(image_file)
                image = resize_image(image)
 
            details = {
              
                "Date": str(Date), 
                "Party Code": Party_code if Party_code else "N/A",
                "Order No": Order_no if Order_no else "N/A",
                "Party Name": Party_name if Party_name else "N/A",
                "Weight": Weight if Weight else "N/A",
                "Size": Size if Size else "N/A",
                "PCS": PCS if PCS else "N/A",
                "Rhodium": Rhodium if Rhodium else "N/A",
                "Remark": Remark if Remark else "N/A",
            }
 
            # Combine image and text if image is provided
            if image:
                combined_image = combine_image_with_text(image, details)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_image_path = f"combined_order_image_{Order_no}_{timestamp}.png"
                combined_image.save(output_image_path)
 
                save_to_excel(details, excel_file_path)
 
                st.image(combined_image, caption="Combined Image")
                st.success(f"Order saved successfully! Combined image saved as {output_image_path}")
 
                img_buffer = BytesIO()
                combined_image.save(img_buffer, format="PNG")
                img_buffer.seek(0)
                st.download_button(
                    label="Download Combined Image",
                    data=img_buffer,
                    file_name=output_image_path,
                    mime="image/png"
                )
            else:
                save_to_excel(details, excel_file_path)
                st.success("Order details have been saved without an image.")
 
    elif menu == "View Summary Report":
        st.title("Summary Report")
        df = generate_summary_report(excel_file_path)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No orders have been entered yet.")
 
    elif menu == "Search Order":
        st.title("Search Order")
        search_by = st.radio("Search By", ["Order No", "Party Name"])
        search_input = st.text_input(f"Enter {search_by}")
        if st.button("Search"):
            df = generate_summary_report(excel_file_path)
            if not df.empty:
                if search_by == "Order No":
                    result = df[df["Order No"] == search_input]
                else:
                    result = df[df["Party Name"].str.contains(search_input, case=False, na=False)]
                if not result.empty:
                    st.write(result)
                else:
                    st.error("Order not found.")
            else:
                st.info("No orders have been entered yet.")
 
    elif menu == "Delete Orders":
        st.title("Delete Orders")
        delete_option = st.radio("Delete Option", ["Delete All Orders", "Delete by Date"])
        if delete_option == "Delete All Orders":
            if st.button("Delete All"):
                delete_orders(excel_file_path)
        elif delete_option == "Delete by Date":
            date_to_delete = st.date_input("Select Date to Delete")
            if st.button("Delete by Date"):
                delete_orders(excel_file_path, date_to_delete)
 
    elif menu == "Download Data":
        st.title("Download Data")
        if os.path.exists(excel_file_path):
            with open(excel_file_path, "rb") as file:
                st.download_button(
                    label="Download Excel File",
                    data=file,
                    file_name=excel_file_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("No data file exists yet.")
