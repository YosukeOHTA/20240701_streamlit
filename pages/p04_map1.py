import streamlit as st
import pandas as pd
import numpy as np
from   streamlit_folium import st_folium      # streamlitでfoliumを使う
import folium                               # folium

st.header('Plot map')
# df3 = pd.DataFrame(
#     np.random.rand(100, 2)/[50, 50]+ [35.69, 139.70],
#     columns=['lat', 'lon',])


st.subheader('folium.Map')
m = folium.Map(
    # 地図の中心位置の指定(今回は栃木県の県庁所在地を指定)
    location=[43.07076877001753, 141.35328401349244], 
    # タイル、アトリビュートの指定
    tiles='https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
    attr='都道府県庁所在地、人口、面積(2016年)',
    # ズームを指定
    zoom_start=15)

pop = 'test1'
folium.Marker(
    location=[43.07076877001753, 141.35328401349244],
    popup=folium.Popup(pop, max_width=300),
    icon=folium.Icon(icon='home', icon_color='white', color='red')
).add_to(m)
st_data = st_folium(m, width=1200, height=800)


st.subheader('st.map')
history = np.zeros((0,2))
item = np.array([43.07076877001753, 141.35328401349244])
history = np.vstack((history, item))
df3 = pd.DataFrame(history, columns=['lat', 'lon',])
st.map(df3)