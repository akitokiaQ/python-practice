import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

SHEET_ID = "1LQrN2qYH290SyegvPPHnxRi6-L6XVgRPRWIquwQf0Eo"
GID = "1765704722"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

DATA_DATE = "2024-10-01"

st.title("Population by Age (Japan, 2024)")
st.caption(f"Source: National Population Survey, {DATA_DATE}")
st.caption("All population figures are displayed in thousands.")
st.caption("Note: Age 100 (centenarian) includes all people aged 100 and over.")

@st.cache_data
def load_and_prepare_data():
    df = pd.read_csv(CSV_URL, encoding="utf-8")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Population_thousands"] = pd.to_numeric(df["Both sexes"].str.replace(",", ""), errors="coerce")
    df = df[(df["Age"] >= 0) & (df["Age"] <= 100)]
    df = df.sort_values("Age")
    return df

df = load_and_prepare_data()

mode = st.radio(
    "View Mode",
    (
        "Full Data",
        "Age Ranking & Graph",
        "Population by Age Group",
        "Elderly and Working-age Population"
    ),
    index=0,
    horizontal=True,
)

if mode == "Full Data":
    st.subheader("Full Data (in thousands)")
    st.dataframe(
        df[["Age", "Population_thousands"]].rename(
            columns={"Population_thousands": "Population (thousands)"}
        ),
        use_container_width=True
    )

elif mode == "Age Ranking & Graph":
    st.subheader("Population by Age (0–100, in thousands)")
    st.bar_chart(df.set_index("Age")["Population_thousands"], use_container_width=True)
    rank_df = df.copy().sort_values("Population_thousands", ascending=False).reset_index(drop=True)
    rank_df["Rank"] = rank_df.index + 1
    st.dataframe(
        rank_df[["Rank", "Age", "Population_thousands"]].rename(
            columns={"Population_thousands": "Population (thousands)"}
        ),
        use_container_width=True
    )

elif mode == "Population by Age Group":
    st.subheader("Population by Age Group (in thousands)")

    def age_group_label(age):
        return "centenarian" if age == 100 else f"{(age // 10) * 10}s"

    df["Age Group"] = df["Age"].apply(age_group_label)
    group_df = df.groupby("Age Group")["Population_thousands"].sum().reset_index()
    st.bar_chart(group_df.set_index("Age Group"), use_container_width=True)
    st.dataframe(
        group_df.rename(columns={"Population_thousands": "Population (thousands)"}),
        use_container_width=True
    )

elif mode == "Elderly and Working-age Population":
    total_population = df["Population_thousands"].sum()
    seniors_65 = df[df["Age"] >= 65]["Population_thousands"].sum()
    seniors_75 = df[df["Age"] >= 75]["Population_thousands"].sum()
    working_population = df[(df["Age"] >= 15) & (df["Age"] < 65)]["Population_thousands"].sum()
    children_population = df[df["Age"] < 15]["Population_thousands"].sum()

    st.subheader("Japan's Population Structure (2024)")

    st.metric("Total Population (thousands)", f"{total_population:,}")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Population 65+ (Aging Rate)",
        f"{seniors_65:,}",
        f"{seniors_65 / total_population:.2%}"
    )
    col2.metric(
        "Population 75+ (Super Aging Rate)",
        f"{seniors_75:,}",
        f"{seniors_75 / total_population:.2%}"
    )
    col3.metric(
        "Working-age Population (15–64)",
        f"{working_population:,}",
        f"{working_population / total_population:.2%}"
    )

    st.subheader("Population Proportions (Pie Chart)")
    labels = ["Children (0–14)", "Working-age (15–64)", "Seniors (65+)"]
    sizes = [children_population, working_population, seniors_65]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Ensures pie chart is drawn as a circle

    st.pyplot(fig)