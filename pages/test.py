
import streamlit as st
from PIL import Image
import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
import time 

# pip install scikit-learn==1.2.2 로 설치.

def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.df_clean = pd.read_csv("df_clean.csv")
        st.session_state.df_clean['Date'] = pd.to_datetime(st.session_state.df_clean['Date'])

def generate_wordcloud_image(date, df_clean, image_path):
    filtered_df = df_clean[df_clean['Date'] == pd.to_datetime(date)]
    if not filtered_df.empty:
        cleaned_reviews = filtered_df['all']
        if not cleaned_reviews.empty:
            cleaned_review = cleaned_reviews.iloc[0]
            if cleaned_review:
                wordcloud = WordCloud(
                    width=1000,
                    height=500,
                    colormap='nipy_spectral',
                    random_state=0,
                    max_words=50,
                    background_color='white',
                    max_font_size=200
                ).generate(cleaned_review)
                plt.figure(figsize=(12, 8))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.savefig(image_path)
                plt.close()
                return True
    return False

@st.cache_data(persist="disk")

def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

def prepare_data_for_prediction(date):
    df = pd.read_csv('df_0123.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    date = pd.to_datetime(date)
    
    train_data = df[df['Date'] < date]
    test_data = df[df['Date'] == date]
    
    if test_data.empty:
        return None, None, None, None

    columns_list = [col for col in df.columns if col != 'soxl_Signal' and col != 'Date']
    X_train = train_data[columns_list].astype(float)
    y_train = train_data['soxl_Signal'].astype(int)
    X_test = test_data[columns_list].astype(float)
    y_test = test_data['soxl_Signal'].astype(int)
    return X_train, y_train, X_test, y_test

def main():
    st.title("예측 결과!! 🎯")

    initialize_session_state()

    DATA_PATH = "./"
    IMAGE_PATH = os.path.join(DATA_PATH, 'wordcloud.png')
    
    IMAGE_PATH1 = os.path.join(DATA_PATH, 'up.png')
    IMAGE_PATH2 = os.path.join(DATA_PATH, 'middle.png')
    IMAGE_PATH3 = os.path.join(DATA_PATH, 'down.png')

    date = st.date_input("예측할 날짜를 입력하세요")

    if st.button("Generate WordCloud", use_container_width=True):
        if generate_wordcloud_image(date, st.session_state.df_clean, IMAGE_PATH):
            st.image(IMAGE_PATH, use_column_width=True)
        else:
            st.write("선택한 날짜에 해당하는 데이터가 없습니다.")
    
    if st.button("Predict", use_container_width=True):
        model_path = './gradient_boosting_model_label_count.pkl'
        model = load_model(model_path)
        # my_bar = st.progress(0)

        # for percent_complete in range(100):
        #     time.sleep(0.5)
        #     my_bar.progress(percent_complete + 0.1)
        

        X_train, y_train, X_test, y_test = prepare_data_for_prediction(date)
        if X_train is not None and X_test is not None:
            model.fit(X_train, y_train)
            prediction = model.predict(X_test)
            
            st.balloons()
            if prediction[0] == 0:
                st.title("강력 매도!!")
                st.image(IMAGE_PATH3, use_column_width=True)
            elif prediction[0] == 1:
                st.title("매도!!")
                st.image(IMAGE_PATH3, use_column_width=True)
            elif prediction[0] == 2:
                st.title("중립!!")
                st.image(IMAGE_PATH2, use_column_width=True)
            elif prediction[0] == 3:
                st.title("매수!!")
                st.image(IMAGE_PATH1, use_column_width=True)
            elif prediction[0] == 4:
                st.title("강력 매수!!")
                st.image(IMAGE_PATH1, use_column_width=True)
            else:
                result = "알 수 없는 값"
            
            st.subheader(f"Prediction for {date}: {prediction[0]}")
        else:
            st.subheader("선택한 날짜에 해당하는 데이터가 없습니다.")

if __name__ == "__main__":
    main()

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
