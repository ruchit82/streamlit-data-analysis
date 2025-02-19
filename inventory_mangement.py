# -*- coding: utf-8 -*-
"""Inventory_Mangement.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tL_XZvVhlQcM57r8T5JziIGw-sql3Ph3
"""

import streamlit as st
import pandas as pd
import datetime
import requests
import plotly.express as px
from io import BytesIO

# Google Sheet URLs
SALES_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Jwx4TntDxlwghFn_eC_NgooXlpvR6WTDdvWy4PO0zgk/export?format=csv&gid=2076018430"
FACTORY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1Jwx4TntDxlwghFn_eC_NgooXlpvR6WTDdvWy4PO0zgk/export?format=csv&gid=0"

# Function to load data from Google Sheets
def load_data():
    sales_df = pd.read_csv(SALES_SHEET_URL)
    factory_df = pd.read_csv(FACTORY_SHEET_URL)
    return sales_df, factory_df

# Function to extract category from Design No
def extract_category(design_no):
    categories = ["CM", "CL", "CN", "CZ", "EX", "FR", "FS", "GL", "GT", "OP", "PL", "LN", "LO", "MD", "MV", "NA", "SP", "SPE", "UN"]
    for category in categories:
        if category in design_no:
            return category
    return "Other"

# Load Data
sales_df, factory_df = load_data()

# Convert DATE columns to datetime format
sales_df['DATE'] = pd.to_datetime(sales_df['DATE'], errors='coerce')
factory_df['DATE'] = pd.to_datetime(factory_df['DATE'], errors='coerce')

# Add Category Column
sales_df['CATEGORY'] = sales_df['DESIGN NO'].astype(str).apply(extract_category)
factory_df['CATEGORY'] = factory_df['DESIGN NO'].astype(str).apply(extract_category)

# Exclude items marked as OUT
if 'OUT' in sales_df.columns:
    sales_df = sales_df[sales_df['OUT'] != 'Yes']
if 'OUT' in factory_df.columns:
    factory_df = factory_df[factory_df['OUT'] != 'Yes']

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Aged Stock", "Inventory Data", "Export Data"])

# Home Page
if page == "Home":
    st.title("Welcome to ITAN Jewels Stock Inventory Management")
    st.write("Manage your live stock efficiently with real-time updates, statistics, and visualizations.")
    st.write("### Features:")
    st.markdown("- **Dashboard:** View stock statistics and visualizations.")
    st.markdown("- **Aged Stock:** Monitor inventory older than 15 days.")
    st.markdown("- **Inventory Data:** Access sales and factory stock details.")
    st.markdown("- **Export Data:** Download data as PDF or Excel.")
    st.markdown("- **Refresh Button:** Reload data for real-time updates.")

# Dashboard Page
elif page == "Dashboard":
    st.title("Stock Inventory Dashboard")
    
    total_sales_weight = sales_df['WT'].sum()
    total_factory_weight = factory_df['WT'].sum()
    overall_weight = total_sales_weight + total_factory_weight
    
    st.metric("Total Sales Weight (WT)", total_sales_weight)
    st.metric("Total Factory Stock Weight (WT)", total_factory_weight)
    st.metric("Overall Inventory Weight (WT)", overall_weight)
    
    # Visualizations
    category_weight = sales_df.groupby('CATEGORY')['WT'].sum().reset_index()
    category_weight.columns = ['Category', 'Weight']
    fig = px.bar(category_weight, x='Category', y='Weight', title="Sales Weight by Category")
    st.plotly_chart(fig)

# Aged Stock Page
elif page == "Aged Stock":
    st.title("Aged Stock (More than 15 days old)")
    cutoff_date = datetime.datetime.today() - datetime.timedelta(days=15)
    aged_stock = factory_df[factory_df['DATE'] < cutoff_date]
    st.write(f"### Stock older than 15 days (before {cutoff_date.date()})")
    st.dataframe(aged_stock)
    
    # Aged stock visualization
    aged_category_weight = aged_stock.groupby('CATEGORY')['WT'].sum().reset_index()
    aged_category_weight.columns = ['Category', 'Weight']
    fig = px.pie(aged_category_weight, names='Category', values='Weight', title="Aged Stock Weight by Category")
    st.plotly_chart(fig)

# Inventory Data Page
elif page == "Inventory Data":
    st.title("Inventory Data")
    st.write("### Salesperson Inventory")
    st.dataframe(sales_df)
    
    st.write("### Factory Inventory")
    st.dataframe(factory_df)

# Export Data Page
elif page == "Export Data":
    st.title("Export Data")
    
    # Export to Excel
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        sales_df.to_excel(writer, sheet_name='Sales Inventory', index=False)
        factory_df.to_excel(writer, sheet_name='Factory Inventory', index=False)
        writer.close()
    st.download_button("Download Excel File", data=excel_buffer.getvalue(), file_name="Inventory_Data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    # Export to CSV
    csv_data = sales_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV File", data=csv_data, file_name="Sales_Inventory.csv", mime="text/csv")

# Refresh Button
if st.button("Refresh Data"):
    sales_df, factory_df = load_data()
    st.experimental_rerun()
