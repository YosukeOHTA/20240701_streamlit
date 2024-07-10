# https://qiita.com/Gyutan/items/1cbff90d31828b25c05d

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

df1 = pd.read_csv('./data/data.csv', encoding="shift-jis", skiprows=5, index_col='Unnamed: 0')
df1 = df1[['Unnamed: 1', 'Unnamed: 4',]]
df1.rename(columns={'Unnamed: 1':'平均気温', 'Unnamed: 4':'最高気温', }, inplace=True)


code1 = '''
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
'''
st.code(code1, language='python')


st.subheader('AgGrid - scroll')
AgGrid(df1)
code2 = '''
AgGrid(df1)
'''
st.code(code2, language='python')


st.subheader('AgGrid - page')
gb = GridOptionsBuilder.from_dataframe(df1)
gb.configure_pagination()
gridOptions = gb.build()
AgGrid(df1, gridOptions=gridOptions)
code3 = '''
gb = GridOptionsBuilder.from_dataframe(df1)
gb.configure_pagination()
gridOptions = gb.build()
AgGrid(df1, gridOptions=gridOptions)
'''
st.code(code3, language='python')


st.subheader('AgGrid - func')
gb = GridOptionsBuilder.from_dataframe(df1)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()
AgGrid(df1, gridOptions=gridOptions, enable_enterprise_modules=True)
code4 = '''
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.subheader('AgGrid - func')
gb = GridOptionsBuilder.from_dataframe(df1)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()
AgGrid(df1, gridOptions=gridOptions, enable_enterprise_modules=True)
'''
st.code(code4, language='python')

st.subheader('st.dataframe')
st.dataframe(df1)