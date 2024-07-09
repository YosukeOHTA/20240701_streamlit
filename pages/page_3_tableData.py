import streamlit as st
import pandas as pd

df1 = pd.read_csv('./data/data.csv', encoding="shift-jis", skiprows=5, index_col='Unnamed: 0')
df1 = df1[['Unnamed: 1', 'Unnamed: 4',]]
df1.rename(columns={'Unnamed: 1':'平均気温', 'Unnamed: 4':'最高気温', }, inplace=True)
# st.table(df1)

st.subheader('Raw Table')
st.dataframe(df1)

st.subheader('Line chart')
st.line_chart(df1)

st.subheader('Area chart')
st.area_chart(df1)

st.subheader('Bar chart')
st.bar_chart(df1)