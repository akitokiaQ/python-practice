import pandas as pd
import streamlit as st

SHEET_ID = "1LQrN2qYH290SyegvPPHnxRi6-L6XVgRPRWIquwQf0Eo"
GID = "1765704722"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

DATA_DATE = "2024-10-01"

st.title("Population by Age: 18 and Over")

st.caption(f"Source: National Population Survey, {DATA_DATE}")

try:
    df = pd.read_csv(CSV_URL, encoding="utf-8")
    st.subheader("Full Data")
    st.dataframe(df, use_container_width=True)

    age_col = "Age"
    total_col = "Both sexes"

    df = df[[age_col, total_col]].copy()
    df[age_col] = df[age_col].astype(str).str.replace(',', '')
    df[total_col] = df[total_col].astype(str).str.replace(',', '')
    df = df[pd.to_numeric(df[age_col], errors="coerce").notnull()]
    df[age_col] = df[age_col].astype(int)
    df[total_col] = pd.to_numeric(df[total_col], errors="coerce")
    df_adult = df[df[age_col] >= 18].copy()
    df_sorted = df_adult.sort_values(total_col, ascending=False).reset_index(drop=True)
    df_sorted["Rank"] = df_sorted.index + 1

    st.subheader("Ranking (Population by Age, 18+)")
    st.dataframe(df_sorted[["Rank", age_col, total_col]], use_container_width=True)
    st.bar_chart(data=df_sorted.set_index(age_col)[total_col], use_container_width=True)
    st.caption(f"Note: This data is based on the national survey conducted on {DATA_DATE}.")
except Exception as e:
    st.error(f"Data load error: {e}")