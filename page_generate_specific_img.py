import streamlit as st
import pandas as pd
import cv2
import time
import os

from random import randint
from keras.preprocessing.image import load_img



def show_img_specific_generation_page():
    title = "Generating specific images"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)  

    st.sidebar.title("Information")
    st.sidebar.markdown("""This page aims to generate a specific image with StyleGAN2 model by selecting features.""", unsafe_allow_html=False)

    st.sidebar.title("Features")

    # gender_value = 'male' if 'gender' not in st.session_state['page2'] else st.session_state['page2']['gender']
    # gender = st.sidebar.select_slider(
    #     'Gender',
    #     options=['female','',' ','  ','   ','    ','     ','      ','male'],
    #     value=(gender_value)
    # )
    gender_value = 0.0 if 'gender' not in st.session_state['page2'] else float(st.session_state['page2']['gender'])
    gender = st.sidebar.slider("Gender", -3.0, 3.0, gender_value, help="'-3.0' corresponds to 'female' and '+3.0' corresponds to 'male'")

    # age_value = '40' if 'age' not in st.session_state['page2'] else st.session_state['page2']['age']
    # age = st.sidebar.select_slider(
    #     'Age (years)',
    #     options=['10','20','30','40','50','60','70'],
    #     value=(age_value)
    # )
    age_value = 0.0 if 'age' not in st.session_state['page2'] else float(st.session_state['page2']['age'])
    age = st.sidebar.slider("Age (years)", -3.0, 3.0, age_value)

    # smile_value = 'Yes' if 'smile' not in st.session_state['page2'] else st.session_state['page2']['smile']
    # smile = st.sidebar.select_slider(
    #     'Smiling',
    #     options=['No','',' ','  ','   ','    ','     ','      ','Yes'],
    #     value=(smile_value)
    # )
    smile_value = 0.0 if 'smile' not in st.session_state['page2'] else float(st.session_state['page2']['smile'])
    smile = st.sidebar.slider("Smiling", -3.0, 3.0, smile_value, help="'-3.0' corresponds to 'no smiling' and '+3.0' corresponds to 'smiling'")


    # eyeglasses_value = 'Yes' if 'eyeglasses' not in st.session_state['page2'] else st.session_state['page2']['eyeglasses']
    # eyeglasses = st.sidebar.select_slider(
    #     'Eyeglasses',
    #     options=['No','',' ','  ','    ','     ','      ','       ','Yes'],
    #     value=(eyeglasses_value)
    # )
    eyeglasses_value = 0.0 if 'eyeglasses' not in st.session_state['page2'] else float(st.session_state['page2']['eyeglasses'])
    eyeglasses = st.sidebar.slider("Glasses", -3.0, 3.0, eyeglasses_value, help="'-3.0' corresponds to 'no eyeglasses' and '+3.0' corresponds to 'eyeglasses'")

    # Set empty space to load images
    img_people = load_img("img/people.png")
    cols = st.columns([1,4,1])
    imageLocations = [cols[i].empty() for i in range(len(cols))]
    imageLocations[1].image(img_people)

    col1, col2, col3 = st.sidebar.columns([1,3,1])
    ok = col2.button("Generate image")
    custom_button = st.markdown(""" <style> div.stButton > 
                        button:hover {background-color: white; 
                                      color: #4CAF50; 
                                      border: 2px solid #4CAF50;}
                    </style>""", unsafe_allow_html=True)
    if ok:
        # Add progress sidebar
        my_bar = st.sidebar.progress(0)
        time.sleep(1)
        for percent_complete in range(100):
            time.sleep(0.001)
            my_bar.progress(percent_complete + 1)

        # Generate specific image with specified features
        new_image = load_img("gif/generate_specific_img.gif")
        imageLocations[1].image(new_image)

        # Read gif
        # import base64
        # file_ = open(f"gif/generate_specific_img.gif", "rb")
        # contents = file_.read()
        # data_url = base64.b64encode(contents).decode("utf-8")
        # file_.close()
        # imageLocations[1].markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True)

    # Update session_state dict
    st.session_state['page2'] = {'gender':gender,
                                'age':age,
                                'smile':smile,
                                'eyeglasses':eyeglasses,
                                }