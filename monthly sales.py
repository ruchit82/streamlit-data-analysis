import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def main():
    st.title("Sales Analysis")
    
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            st.subheader("First 10 rows of data")
            st.dataframe(data.head(10))
            
            required_columns = ['DocDate', 'type', 'parName', 'CATEGORY', 'CatCd', 'weight', 'noPcs']
            if not all(col in data.columns for col in required_columns):
                st.error("Missing required columns.")
            else:
                data = data[~data['CATEGORY'].isin(['ST', 'LOOSE PCS', 'PARA BIDS', 'Langadi', 'PROCESS LOSS',
                                                    'SCRAP PCC', 'BALL CHAIN', 'SIGNING TAR', 'Fine'])]
                
                party_weight_summary = data.groupby('parName')['weight'].sum().reset_index()
                party_weight_summary = party_weight_summary.sort_values(by='weight', ascending=False)
                
                st.subheader("Summary Statistics")
                st.write(f"Total Parties: {len(party_weight_summary)}")
                st.write(f"Total Categories: {len(data['CatCd'].unique())}")
                st.write(f"Total Weight: {round(data['weight'].sum(), 2)}")
                
                st.subheader("Top 10 Parties by Weight")
                st.dataframe(party_weight_summary.head(10))
                
                st.subheader("Bottom 5 Parties by Weight")
                st.dataframe(party_weight_summary.tail(5))
                
                # Visualization
                st.subheader("Top 10 Parties by Weight - Bar Chart")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(x='weight', y='parName', data=party_weight_summary.head(10), ax=ax)
                ax.set_title('Top 10 Parties by Weight')
                st.pyplot(fig)

if __name__ == "__main__":
    main()
