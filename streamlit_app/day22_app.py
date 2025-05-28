import streamlit as st
import pandas as pd

# タイトルを設定
st.title('GitHubリポジトリの観測数・フォーク数分析')

# Google Sheetsを公開リンク経由で読み込む
sheet_url = "https://docs.google.com/spreadsheets/d/1tteVL-iuwnrKlxcoJ-LCxuQlx2EznbKKMTzC0rqdLKc/export?format=csv"
df = pd.read_csv(sheet_url)

# 必要な列のみ抽出（name, watchers_count, forks_count）
df_display = df[['name', 'watchers_count', 'forks_count']]

# リポジトリ名をインデックスに設定
df_display.set_index('name', inplace=True)

# 観測数とフォーク数を横並びで表示
st.subheader("各リポジトリの観測数・フォーク数")

st.bar_chart(df_display)

# 上位5つのリポジトリをランキング形式で表示
st.subheader("観測数・フォーク数 上位5つのリポジトリ")

# 観測数のトップ5
top_watchers = df_display.sort_values(by='watchers_count', ascending=False).head(5)
st.write("🔍 観測数 Top5")
st.bar_chart(top_watchers['watchers_count'])

# フォーク数のトップ5
top_forks = df_display.sort_values(by='forks_count', ascending=False).head(5)
st.write("🔗 フォーク数 Top5")
st.bar_chart(top_forks['forks_count'])