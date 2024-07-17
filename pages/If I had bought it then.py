import streamlit as st
from PIL import Image
import os
import pandas as pd

st.header("시그널을 따라 매매했더라면..! 💰")
st.write("")
st.subheader(" 4/22일에 시그널에 따라 1000달러를 매매했더라면??")
st.subheader(" 5/22일엔 1435.20달러!! ")

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가


DATA_PATH = "./"
IMAGE_PATH = os.path.join(DATA_PATH, 'if.png')
st.image(IMAGE_PATH, use_column_width=True)