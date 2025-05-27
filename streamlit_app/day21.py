import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証設定（Google Sheets）
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# スプレッドシート名とシート名を指定
spreadsheet = gc.open('Git Trending→google spreadsheets')  # Googleシートのタイトルを正確に記入
stargazers_sheet = spreadsheet.worksheet('stargazers')    # スターゲイザーシートを指定

stargazers_data = pd.DataFrame(stargazers_sheet.get_all_records())

# datetime型に変換
stargazers_data['starred_at'] = pd.to_datetime(stargazers_data['starred_at'])

# Streamlitに表示
st.title('GitHub Stargazers Data')
st.write("データのプレビュー：")
st.dataframe(stargazers_data)

# 日付ごとのスター数を集計
daily_counts = stargazers_data['starred_at'].dt.date.value_counts().sort_index()

# Streamlitで日付ごとのスター数を表示
st.write("日付ごとのスター獲得数")
st.bar_chart(daily_counts)