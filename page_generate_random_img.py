import streamlit as st
import pickle
import numpy as np
import cv2
import time
import os

from random import randint
from keras.preprocessing.image import load_img

CURRENT_DIR = "/content/gan-app/"

def show_img_random_generation_page():   
    title = "Generating random images"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)    

    st.sidebar.title("Information")
    st.sidebar.markdown("""This page aims to generate random images using several models (StyleGAN2, VAE and NVAE).""", unsafe_allow_html=False)

    # Set left page (sidebar) parameters
    st.sidebar.title("Models")
    option_GAN = st.sidebar.checkbox('GAN (StyleGAN2)', value=True)
    option_VAE = st.sidebar.checkbox('VAE')
    option_NVAE = st.sidebar.checkbox('NVAE')
    known_variables = option_GAN + option_VAE + option_NVAE
    if known_variables == 0:
        st.error('Please select at least one model')
        # st.write('Please select at least one model')
    else:
        col1, col2, col3 = st.sidebar.columns([1,3,1])

        # Set empty space to load images
        img_people = load_img(f"{CURRENT_DIR}/img/people.png")
        if known_variables == 1:
            cols = st.columns([1,2,1])
        elif known_variables == 2:
            cols = st.columns([1,1])
        else:
            cols = st.columns([1,1,1])
        
        # Add default image
        imageLocations = [cols[i].empty() for i in range(len(cols))]
        for i in range(len(imageLocations)):
            if not((i==0 or i==2) and known_variables==1):
                imageLocations[i].image(img_people) 

        # Custom button
        custom_button = st.markdown(""" <style> div.stButton > 
                            button:hover {background-color: white; 
                                        color: #4CAF50; 
                                        border: 2px solid #4CAF50;}
                        </style>""", unsafe_allow_html=True)


        st.sidebar.markdown("""""", unsafe_allow_html=False)                
        ok = col2.button("Generate image")
        models = {'GAN (StyleGAN2)':option_GAN, 'VAE':option_VAE, 'NVAE':option_NVAE}
        if ok:
            # Add progress sidebar
            my_bar = st.sidebar.progress(0)
            time.sleep(1)
            for percent_complete in range(100):
                time.sleep(0.001)
                my_bar.progress(percent_complete + 1)   

            i=0
            img_already_displayed = []
            for model_name, model_used in models.items():
                if model_used == 1:

                    # Generate random image
                    numero = randint(1,5)
                    while numero in img_already_displayed:
                        numero = randint(1,5)
                    img_already_displayed.append(numero)

                    # Load image
                    new_image = load_img(f"{CURRENT_DIR}/img/jpeg/{numero}.jpg")                    

                    # Display image
                    if known_variables == 1:
                        imageLocations[1].image(new_image) 
                        cols[1].markdown(f"<h3 style='text-align: center;'>Generated image with {model_name}", unsafe_allow_html=True)
                    else:
                        imageLocations[i].image(new_image) 
                        cols[i].markdown(f"<h3 style='text-align: center;'>Generated image with {model_name}", unsafe_allow_html=True)
                        i+=1

        # Update session_state dict
        st.session_state['page1'] = {'models':models}



        
