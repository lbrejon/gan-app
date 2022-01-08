import streamlit as st
import pandas as pd
import cv2
import time
import os

from random import randint
from keras.preprocessing.image import load_img

import glob
import subprocess
from PIL import Image
import random

CURRENT_DIR = "/content/gan-app/"

def clear_img_dir():
    files = glob.glob("/content/downloaded_imgs/*.jpg")
    for f in files:
        os.remove(f)


def generate_image(age, eyeglasses, gender, pose, smile, noise_seed):
    var = subprocess.check_output(
        [
            "python",
            "ganface_gen.py",
            str(age),
            str(eyeglasses),
            str(gender),
            str(pose),
            str(smile),
            str(noise_seed),
        ]
    )

    # Lit + récupère img générée
    var_name = var.splitlines()[-1] 
    file_name = var_name.decode("utf-8")

    with open(file_name, "rb") as file:
        img = Image.open(file_name)
    return img

def show_img_specific_generation_page():
    title = "Generating specific images"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)  

    st.sidebar.title("Information")
    st.sidebar.markdown("""This page aims to generate a specific image with StyleGAN2 model by selecting features.""", unsafe_allow_html=False)

    st.sidebar.title("Features")

    gender_value = 0.0 if 'gender' not in st.session_state['page2'] else float(st.session_state['page2']['gender'])
    gender = st.sidebar.slider("Gender", -3.0, 3.0, gender_value, help="'-3.0' corresponds to 'female' and '+3.0' corresponds to 'male'")

    age_value = 0.0 if 'age' not in st.session_state['page2'] else float(st.session_state['page2']['age'])
    age = st.sidebar.slider("Age (years)", -3.0, 3.0, age_value)

    smile_value = 0.0 if 'smile' not in st.session_state['page2'] else float(st.session_state['page2']['smile'])
    smile = st.sidebar.slider("Smiling", -3.0, 3.0, smile_value, help="'-3.0' corresponds to 'no smiling' and '+3.0' corresponds to 'smiling'")

    pose_value = 0.0 if 'pose' not in st.session_state['page2'] else float(st.session_state['page2']['pose'])
    pose = st.sidebar.slider("Pose", -3.0, 3.0, pose_value, help="'-3.0' corresponds to '??' and '+3.0' corresponds to '??'")

    eyeglasses_value = 0.0 if 'eyeglasses' not in st.session_state['page2'] else float(st.session_state['page2']['eyeglasses'])
    eyeglasses = st.sidebar.slider("Glasses", -3.0, 3.0, eyeglasses_value, help="'-3.0' corresponds to 'no eyeglasses' and '+3.0' corresponds to 'eyeglasses'")

    # Set empty space to load images
    img_people = load_img(f"{CURRENT_DIR}/img/people.png")
    cols = st.columns([1,4,1])
    imageLocations = [cols[i].empty() for i in range(len(cols))]

    try:
        noise_seed = st.session_state['page2']['noise_seed']
    except:
        imageLocations[1].image(img_people)

    # imageLocations[1].image(img_people) if not hasattr(st.session_state['page2'], 'noise_seed')


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
        # new_image = load_img(f"{CURRENT_DIR}/gif/generate_specific_img.gif")
        # imageLocations[1].image(new_image)
        if not os.path.exists("./noise_seed.txt"):
            f = open("./noise_seed.txt", "a+")
            f.write("392")
            f.close()

        f = open("./noise_seed.txt", "r")
        noise_seed = int(float(f.read()))
        f.close()

        noise_seed = random.randint(0, 1000)  # min:0, max:1000, step:1
        f = open("./noise_seed.txt", "w")
        f.truncate(0)
        f.write(str(noise_seed))  # update noise seed
        f.close()


    if not os.path.exists("./noise_seed.txt"):
        f = open("./noise_seed.txt", "a+")
        # noise_seed = random.randint(0, 1000)  # min:0, max:1000, step:1
        noise_seed = 300
        f.write(noise_seed)
        f.close()
    else:
        f = open("./noise_seed.txt", "r")
        noise_seed = int(float(f.read()))
        f.close()


    clear_img_dir()
    st.write(age, eyeglasses, gender, pose, smile, noise_seed)
    image_out = generate_image(age, eyeglasses, gender, pose, smile, noise_seed)
    imageLocations[1].image(image_out)

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
                                'pose':pose,
                                'smile':smile,
                                'eyeglasses':eyeglasses,
                                'noise_seed':noise_seed,
                                }
