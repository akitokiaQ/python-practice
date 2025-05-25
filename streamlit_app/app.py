import streamlit as st
import pandas as pd

st.title('初めてのStreamlitアプリ')

data = pd.DataFrame({
    '名前': ['Alice', 'Bob', 'Charlie'],
    '年齢': [25, 30, 35]
})

st.write("これはサンプルデータです：")
st.dataframe(data)

st.bar_chart(data.set_index('名前'))