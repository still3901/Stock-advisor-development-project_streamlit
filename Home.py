import streamlit as st
st.set_page_config(page_icon="💸", layout="wide")

import pandas as pd
import numpy as np
import os
from pykrx import stock
import warnings
import datetime as dt
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
import pandas_datareader as pdr
import plotly.graph_objects as go
import yfinance as yf
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
from wordcloud.wordcloud import WordCloud

# 공통 초기화 함수
def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.df_clean = pd.read_csv("df_clean.csv")
        st.session_state.df_clean['Date'] = pd.to_datetime(st.session_state.df_clean['Date'])

def generate_wordcloud_image(date, df_clean, image_path):
    def all_text_combine(df_clean, date):
        date_str = date.strftime('%Y-%m-%d')
        filtered_df = df_clean[df_clean['Date'].dt.strftime('%Y-%m-%d') == date_str]
        grouped_df = filtered_df.groupby('head')['Text'].agg(' '.join).reset_index()
        grouped_df['all'] = grouped_df['head'] + ' ' + grouped_df['Text']
        all_text_combined = ' '.join(grouped_df['all'])
        return all_text_combined

    all_text_combined = all_text_combine(df_clean, date)

    if all_text_combined:
        wordcloud = WordCloud(
            width=1000,
            height=500,
            colormap='nipy_spectral',
            random_state=0,
            max_words=50,
            background_color='white',
            max_font_size=200
        ).generate(all_text_combined)

        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(image_path)
        plt.close()
        return True
    return False

# 페이지 설정
add_page_title()

show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/SOXL stock price list.py", "SOXL stock price list", "💹"),
        Page("pages/test.py", "Present investment opinion", "🎯"),
        Page("pages/If I had bought it then.py", "If I had bought it then...", "💰")
    ]
)

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱) / 데이터 로드 시간과 빈도를 줄이고 애플리케이션 성능 향상. 캐싱된 데이터는 900초(15분) 동안 유지
@st.cache_data(ttl=900)
def load_csv(path):
    return pd.read_csv(path)

# 초기화 함수 호출
initialize_session_state()

# Survey Part
st.title(":green[머신러닝 기술과 소셜데이터를 활용한 주가 어드바이저 개발] :sunglasses:")

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

# def main():
#     st.title("주식 데이터")
#     st.sidebar.title("Stock Chart")
#     ticker = st.sidebar.text_input("Enter a ticker (e.x., SOXL)", value="SOXL")
#     st.sidebar.markdown('Tickers Link: [All Stock Symbols](https://stockanalysis.com/etf/soxl/)')
#     start_date = st.sidebar.date_input("시작 날짜: ", value=pd.to_datetime("2023-05-17"))
#     end_date = st.sidebar.date_input("종료 날짜: ", value=pd.to_datetime("2024-05-23"))

#     if ticker and start_date and end_date:
#         # Download data
#         # data = yf.download(ticker, start=start_date, end=end_date)
#         data = fdr.DataReader(ticker, start=start_date, end=end_date)
#         # st.dataframe(data)

#         # 숫자를 넣을 수 있는 영역 생성
#         num_row = st.sidebar.number_input("Number of Rows", min_value=1, max_value=len(data))
#         # 최근 날짜부터 결과값 보여줌
#         st.dataframe(data[-num_row:].reset_index().sort_index(ascending=False).set_index("Date"))

#         # Chart type selection
#         chart_type = st.sidebar.radio("Select Chart Type", ("Candle_Stick", "Line"))

#         # Create the chart
#         if chart_type == "Candle_Stick":
#             candlestick = go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])
#             fig = go.Figure(candlestick)
#         elif chart_type == "Line":
#             line = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close')
#             fig = go.Figure(line)
#         else:
#             st.error("error")

#         # Update layout and plot
#         fig.update_layout(title=f"{ticker} Stock {chart_type} Chart", xaxis_title="Date", yaxis_title="Price")
#         st.plotly_chart(fig)

# 한국 주식의 경우 'fdr' 대신 'pandas_datareader' 사용
# 기업명으로 티커를 검색하는 함수

def main():
    st.title("주식 데이터")
    st.sidebar.title("Stock Chart")

    # 티커를 입력받는 영역
    ticker = st.sidebar.text_input("Enter a ticker (e.x., SOXL)", value="SOXL")
    st.sidebar.markdown('Tickers Link: [All Stock Symbols](https://stockanalysis.com/etf/soxl/)')

    # 시작 날짜와 종료 날짜를 입력받는 영역
    start_date = st.sidebar.date_input("시작 날짜: ", value=pd.to_datetime("2023-05-17"))
    end_date = st.sidebar.date_input("종료 날짜: ", value=pd.to_datetime("2024-05-23"))

    if ticker and start_date and end_date:
        try:
            # 데이터 다운로드
            data = fdr.DataReader(ticker, start=start_date, end=end_date)

            # 데이터프레임의 행 수를 입력받아 보여주는 영역
            num_row = st.sidebar.number_input("Number of Rows", min_value=1, max_value=len(data), value=min(10, len(data)))
            st.dataframe(data[-num_row:].reset_index().sort_index(ascending=False).set_index("Date"))

            # 차트 타입 선택
            chart_type = st.sidebar.radio("Select Chart Type", ("Candle_Stick", "Line"))

            # 차트 생성
            if chart_type == "Candle_Stick":
                candlestick = go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])
                fig = go.Figure(candlestick)
            elif chart_type == "Line":
                line = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close')
                fig = go.Figure(line)
            else:
                st.error("Invalid Chart Type Selected")

            # 레이아웃 업데이트 및 차트 출력
            fig.update_layout(title=f"{ticker} Stock {chart_type} Chart", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
