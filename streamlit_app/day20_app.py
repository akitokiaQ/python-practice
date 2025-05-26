import streamlit as st
import pandas as pd

st.title('GitHub Data from Airbyte')

uploaded_file = st.file_uploader("CSVファイルをここにアップロードしてください", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)