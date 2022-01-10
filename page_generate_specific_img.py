import streamlit as st
import pandas as pd
import cv2
import time
import os
import shutil

from random import randint
from keras.preprocessing.image import load_img

import glob
import subprocess
from PIL import Image
import random

CURRENT_DIR = "/content/gan-app/"


def update_dict(gender, age, pose, smile, eyeglasses):
    st.session_state['page2'].update({'gender':gender,
                                'age':age,
                                'pose':pose,
                                'smile':smile,
                                'eyeglasses':eyeglasses,
                                })

def create_sliders():
    gender_value = 0.0 if 'gender' not in st.session_state['page2'] else float(st.session_state['page2']['gender'])
    gender = st.sidebar.slider("Gender", -3.0, 3.0, gender_value, help="'-3.0' corresponds to 'female' and '+3.0' corresponds to 'male'")

    age_value = 0.0 if 'age' not in st.session_state['page2'] else float(st.session_state['page2']['age'])
    age = st.sidebar.slider("Age (years)", -3.0, 3.0, age_value)

    smile_value = 0.0 if 'smile' not in st.session_state['page2'] else float(st.session_state['page2']['smile'])
    smile = st.sidebar.slider("Smiling", -3.0, 3.0, smile_value, help="'-3.0' corresponds to 'no smiling' and '+3.0' corresponds to 'smiling'")

    pose_value = 0.0 if 'pose' not in st.session_state['page2'] else float(st.session_state['page2']['pose'])
    pose = st.sidebar.slider("Pose", -3.0, 3.0, pose_value, help="'-3.0' corresponds to '??' and '+3.0' corresponds to '??'")

    eyeglasses_value = 0.0 if 'eyeglasses' not in st.session_state['page2'] else float(st.session_state['page2']['eyeglasses'])
    eyeglasses = st.sidebar.slider("Eyeglasses", -3.0, 3.0, eyeglasses_value, help="'-3.0' corresponds to 'no eyeglasses' and '+3.0' corresponds to 'eyeglasses'")

    update_dict(gender, age, pose, smile, eyeglasses)



def clear_img_dir(dir2clear):
    files = glob.glob(dir2clear)
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

    # Read image generated path
    var_name = var.splitlines()[-1] 
    file_name = var_name.decode("utf-8")

    # Load image
    with open(file_name, "rb") as file:
        img = Image.open(file_name)
    return file_name, img



def show_img_specific_generation_page():
    title = "Generating specific images"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)  

    st.sidebar.title("Information")
    st.sidebar.markdown("""This page aims to generate a specific image with StyleGAN2 model by selecting features.""", unsafe_allow_html=False)
    col1, col2, col3 = st.sidebar.columns([1,3,1])
    
    st.sidebar.title("Features")

    # Create sliders
    create_sliders()
    age = st.session_state['page2']['age']
    gender = st.session_state['page2']['gender']
    pose = st.session_state['page2']['pose']
    smile = st.session_state['page2']['smile']
    eyeglasses = st.session_state['page2']['eyeglasses']

    # Images path
    img_people_path = f"{CURRENT_DIR}/img/people.png"
    noise_seed_path = f"{CURRENT_DIR}/noise_seed.txt"

    # Set empty space to load images
    cols = st.columns([1,1])
    imageLocations = [cols[i].empty() for i in range(len(cols))]
    img_people = load_img(img_people_path)
    imageLocations[0].image(img_people)
    imageLocations[1].image(img_people)

    # Display initial generated img (on the left)
    if 'img_init_generated_path' in st.session_state['page2']:
        img_init_generated_path = st.session_state['page2']['img_init_generated_path']
        img_init_generated = load_img(img_init_generated_path)
        imageLocations[0].image(img_init_generated)

    # Create button for new img generation
    col1, col2, col3 = st.sidebar.columns([1,3,1])
    new_img_button = col2.button("Generate new image")
    custom_button = st.markdown(""" <style> div.stButton > 
                        button:hover {background-color: white; 
                                      color: #4CAF50; 
                                      border: 2px solid #4CAF50;}
                    </style>""", unsafe_allow_html=True)

    if new_img_button:
        # Display unknown img logo
        imageLocations[0].image(img_people)
        imageLocations[1].image(img_people)

        # Remove existing generated img (initial img -> on the left)
        clear_img_dir("/content/downloaded_imgs/init/*.jpg")        

        # Generate new noise seed
        noise_seed = random.randint(0, 1000)
        f = open(f"{CURRENT_DIR}/noise_seed.txt", "w")
        f.truncate(0)
        f.write(str(noise_seed))  # update noise seed
        f.close()

        # Reset dictionary
        st.session_state['page2'] = dict()

    # Check if 'noise_seed.txt' file exists else create a file (for initialization)
    if not 'noise_seed' in st.session_state['page2']:
        f = open(f"{CURRENT_DIR}/noise_seed.txt", "w")
        noise_seed = random.randint(0, 1000)
        st.session_state['page2']['noise_seed'] = noise_seed # Add noise seed value in dictionary
        f.write(str(noise_seed))
        f.close()
    else:
        noise_seed = st.session_state['page2']['noise_seed']

    # Remove existing generated img (processed img -> on the right)
    clear_img_dir("/content/downloaded_imgs/*.jpg")

    # Generate processed img
    img_generated_path, img_generated = generate_image(age, eyeglasses, gender, pose, smile, noise_seed)
    
    # Display generated img (on the right)
    imageLocations[1].image(img_generated)
    if not 'img_generated_path' in st.session_state['page2']:
        imageLocations[0].image(img_generated)
        imageLocations[1].image(img_generated)
    else:
        imageLocations[1].image(image_out)
    
    # Save img generated path as img initial generated
    if not 'img_init_generated_path' in st.session_state['page2']:
        img_init_generated_path = img_generated_path

        # Create directory to save initial img
        img_init_dir = "/content/downloaded_imgs/init"
        if not os.path.exists(img_init_dir):
            os.mkdir(img_init_dir)

        # Remove existing img initial
        clear_img_dir("{img_init_dir}/*.jpg")

        # Copy img initial in specific directory for future loading
        img_name = os.path.basename(img_init_generated_path)
        img_generated_path = f"{img_init_dir}/{img_name}"
        shutil.copyfile(img_init_generated_path, img_generated_path)
        
        # Add 'img_init_generated_path' in dictionary to save image initial path
        st.session_state['page2'].update({'img_init_generated_path': img_generated_path})


        # Read gif
        # import base64
        # file_ = open(f"gif/generate_specific_img.gif", "rb")
        # contents = file_.read()
        # data_url = base64.b64encode(contents).decode("utf-8")
        # file_.close()
        # imageLocations[1].markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True)

    st.write(st.session_state['page2'])
