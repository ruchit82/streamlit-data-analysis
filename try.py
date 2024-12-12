# -*- coding: utf-8 -*-
"""try.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y4FxqrB7hFfacWFtSKs746w8OWENfiQG
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit app
st.title("Data Analysis Application")

# File uploader
uploaded_file = st.file_uploader("Upload your data file", type=["xlsx", "csv", "xls"])

if uploaded_file:
    try:
        # Load the data based on file type
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("First 10 rows of the dataset:")
        st.dataframe(data.head(10))

        # Check for required columns
        required_columns = ['DocDate', 'type', 'parName', 'CATEGORY', 'weight', 'noPcs']
        if not all(col in data.columns for col in required_columns):
            st.error(f"The dataset must contain these columns: {required_columns}")
        else:
            # Remove unwanted categories
            excluded_categories = ['ST', 'LOOSE PCS', 'PARA BIDS', 'Langadi', 'PROCESS LOSS',
                                   'SCRAP PCC', 'BALL CHAIN', 'SIGNING TAR', 'Fine']
            df = data[~data['CATEGORY'].isin(excluded_categories)]

            # Party-wise weight summary
            party_weight_summary = df.groupby('parName')['weight'].sum().reset_index()
            party_weight_summary['Rank'] = party_weight_summary['weight'].rank(ascending=False, method='dense')
            party_weight_summary = party_weight_summary.sort_values(by='weight', ascending=False)

            # Dropdown for party selection
            st.write("### Check Party Rank")
            party_name = st.selectbox("Select a party name:", options=party_weight_summary['parName'].unique())

            if party_name:
                party_details = party_weight_summary[party_weight_summary['parName'] == party_name]
                st.write(f"**Rank:** {int(party_details['Rank'].values[0])}")
                st.write(f"**Party Name:** {party_name}")
                st.write(f"**Total Weight:** {party_details['weight'].values[0]:.2f}")

            # Top 10 and bottom 5 parties by weight
            top_10_parties = party_weight_summary.head(10)
            bottom_5_parties = party_weight_summary.tail(5)

            # Category-wise summary
            category_summary = df.groupby('CATEGORY').agg({'weight': 'sum', 'noPcs': 'sum'}).reset_index()
            category_summary_sorted = category_summary.sort_values(by='weight', ascending=False)
            top_10_categories = category_summary_sorted.head(10)
            bottom_5_categories = category_summary_sorted.tail(5)

            # Plots
            st.write("### Top 10 Parties by Weight")
            st.bar_chart(top_10_parties.set_index('parName')['weight'])

            st.write("### Bottom 5 Parties by Weight")
            st.bar_chart(bottom_5_parties.set_index('parName')['weight'])

            st.write("### Top 10 Categories by Weight")
            st.bar_chart(top_10_categories.set_index('CATEGORY')['weight'])

            st.write("### Bottom 5 Categories by Weight")
            st.bar_chart(bottom_5_categories.set_index('CATEGORY')['weight'])

            # Weight over time
            df['DocDate'] = pd.to_datetime(df['DocDate'])
            time_series = df.groupby('DocDate')['weight'].sum().reset_index()
            st.write("### Total Weight Over Time")
            st.line_chart(time_series.set_index('DocDate')['weight'])

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Awaiting file upload...")


    



