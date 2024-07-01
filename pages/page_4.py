import streamlit as st
import pandas as pd
import numpy as np

st.header('Plot map')
df3 = pd.DataFrame(
    np.random.rand(100, 2)/[50, 50]+ [35.69, 139.70],
    columns=['lat', 'lon',]
)
st.map(df3)


