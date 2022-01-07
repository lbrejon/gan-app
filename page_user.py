import streamlit as st
import pandas as pd
import cv2
from keras.preprocessing.image import load_img
from tempfile import NamedTemporaryFile
import base64

import os

CURRENT_DIR = "/content/gan-app/"


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


def show_user_page():
    title = "Who would you look like.. ?"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)

    st.sidebar.title("Information")
    st.sidebar.markdown("""This page aims to visualize an image generation with a GAN model.""", unsafe_allow_html=False)
    
    st.sidebar.title("Help")
    st.sidebar.markdown("""**Step 1:** Upload an image to be generated with a StyleGAN2 model """, unsafe_allow_html=False)
    st.sidebar.markdown("""**Step 2:** Click on the "**Generate image**" button to see the image generation""", unsafe_allow_html=False)
    st.sidebar.markdown("""**Step 3:** If you like the result, you can download the result in gif format by clicking on the "**Download GIF** 📥" button""", unsafe_allow_html=False)


    # Select an image
    uploaded_file = st.file_uploader("Select a picture:", accept_multiple_files=False)
    temp_file = NamedTemporaryFile(delete=False)

    if uploaded_file:
        col1, col2, col3 = st.sidebar.columns([1,3,1])
        ok = col2.button("Generate image")
        custom_button = st.markdown(""" <style> div.stButton > 
                            button:hover {background-color: white; 
                                        color: #4CAF50; 
                                        border: 2px solid #4CAF50;}
                        </style>""", unsafe_allow_html=True)

        # Read buffer
        temp_file.write(uploaded_file.getvalue())

        # Display loaded image
        img = load_img(temp_file.name)
        img_people = load_img(f"{CURRENT_DIR}/img/people.png")
        cols = st.columns([1, 1]) 
        imageLocations = [cols[i].empty() for i in range(len(cols))]       
        imageLocations[0].image(img, use_column_width=True)
        imageLocations[1].image(img_people, use_column_width=True)


        if ok:
            filename_gif = f"{CURRENT_DIR}/gif/alphonse_generated.gif"
            file_ = open(filename_gif, "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            
            imageLocations[1].markdown(f'<img src="data:image/gif;base64,{data_url}" width=345 alt="cat gif">', unsafe_allow_html=True,)

            colAA, colBB, colCC, colDD = st.columns([1,1,2,1])
            colCC.download_button(label="Download GIF 📥", 
                                  data=file_,
                                  file_name=filename_gif.replace("gif/","gif/downloaded/"),
                                  mime="image/gif")
            file_.close()

    
