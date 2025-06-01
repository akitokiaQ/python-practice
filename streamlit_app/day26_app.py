import pandas as pd
import streamlit as st

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
    ("Full Data", "Age Ranking & Graph", "Population by Age Group"),
    index=0,
    horizontal=True,
)

if mode == "Full Data":
    st.subheader("Full Data (in thousands)")
    st.dataframe(
        df[["Age", "Population_thousands"]].rename(
            columns={"Age": "Age", "Population_thousands": "Population (thousands)"}
        ),
        use_container_width=True
    )

elif mode == "Age Ranking & Graph":
    st.subheader("Population by Age (0-100, in thousands)")
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
        if age == 100:
            return "centenarian"
        return f"{int(age)//10*10}-{int(age)//10*10+9}"

    df["AgeGroup"] = df["Age"].apply(age_group_label)
    age_groups = [
        "0-9", "10-19", "20-29", "30-39", "40-49", "50-59",
        "60-69", "70-79", "80-89", "90-99", "centenarian"
    ]
    pop_by_group = (
        df.groupby("AgeGroup")["Population_thousands"].sum()
        .reindex(age_groups)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    pop_by_group = pop_by_group.rename(
        columns={"AgeGroup": "Age Group", "Population_thousands": "Population (thousands)"}
    )
    st.dataframe(
        pop_by_group,
        use_container_width=True
    )
    # グラフ順序も「centenarian」が必ず最後
    st.bar_chart(pop_by_group.set_index("Age Group")["Population (thousands)"], use_container_width=True)

st.caption("Source: Statistics Bureau of Japan, 'Population Estimates' as of October 1, 2024 | Figures shown in thousands. Age 100 (centenarian) includes all people aged 100 and over.")