import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import plotly.express as px
import warnings
import datetime as dt
# import to_upward
from streamlit_extras.switch_page_button import switch_page
# from prophet import Prophet
# from prophet.plot import add_changepoints_to_plot
import yfinance as yf
import plotly.graph_objects as go

# 페이지 설정: 넓은 레이아웃
st.set_page_config(layout="wide")

# 스트림릿 애플리케이션 내용
st.write("""
# SOXL주가표  💹
Shown are the stock closing price and volume of Soxl!
""")
st.write("* train data -> 2023-05-01 ~ 2024-01-23")
st.write("* test data -> 2024-01-24 ~ 2024-05-17")  

st.markdown("<hr>", unsafe_allow_html=True)	#구분선 추가

# 날짜 입력 받기
date = st.date_input('예측할 날짜를 입력하세요')
st.write(f"선택한 날짜: {date}")


st.header("예측을 위한 SOXL 주가(예측 전 후)")
st.write("예측 확인하기")
    
ticker = st.sidebar.text_input("Enter a ticker (e.x.SOXL)", value="SOXL")
st.sidebar.markdown('Tickers Link: [All Stock Symbols](https://stockanalysis.com/etf/soxl/)')
start_date = st.sidebar.date_input("시작 날짜: ", value=pd.to_datetime("2024-01-23"))
end_date = st.sidebar.date_input("종료 날짜: ", value=pd.to_datetime("2024-05-17"))  

if ticker and start_date and end_date:
    # Download data
    data = yf.download(ticker, start=start_date, end=end_date)
    st.dataframe(data)

        
    line = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close')
    fig = go.Figure(line)

    # Update layout and plot
    fig.update_layout(title=f"{ticker} Stock line Chart", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)
    
    


