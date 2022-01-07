# import numpy as np
# import os
# import pickle
# import streamlit as st
# import sys
# import tensorflow as tf
# import urllib
# import subprocess
# from PIL import Image
# import os
# import glob
# import time
# import random

# favicons_dir = "/content/gan-app/src/Favicon/"


# def clear_img_dir():
#     files = glob.glob("/content/downloaded_imgs/*.jpg")
#     for f in files:
#         os.remove(f)


# def generate_image(age, eyeglasses, gender, pose, smile, noise_seed):
#     var = subprocess.check_output(
#         [
#             "python",
#             "ganface_gen.py",
#             str(age),
#             str(eyeglasses),
#             str(gender),
#             str(pose),
#             str(smile),
#             str(noise_seed),
#         ]
#     )

#     # Lit + récupère img générée
#     var_name = var.splitlines()[-1] 
#     file_name = var_name.decode("utf-8")

#     with open(file_name, "rb") as file:
#         img = Image.open(file_name)
#     return img


# def main():
#     st.set_page_config("GenFace", favicons_dir + "favicon.ico")
#     if not os.path.exists("./noise_seed.txt"):
#         f = open("./noise_seed.txt", "a+")
#         f.write("392")
#         f.close()

#     f = open("./noise_seed.txt", "r")
#     noise_seed = int(float(f.read()))
#     f.close()

#     st.title("GenFace's StyleGAN generator")
#     st.sidebar.title("Facial attributes")

#     # if st.sidebar.button("Generate a new face"):
#     #     noise_seed = random.randint(0, 1000)  # min:0, max:1000, step:1
#     #     f = open("./noise_seed.txt", "w")
#     #     f.truncate(0)
#     #     f.write(str(noise_seed))  # update noise seed
#     #     f.close()

#     age = st.sidebar.slider("Age", -3.0, 3.0, 0.0)
#     # st.sidebar.write("Age:", age)
#     eyeglasses = st.sidebar.slider("Eyeglasses", -3.0, 3.0, 0.0)
#     # st.sidebar.write("Eyeglasses:", eyeglasses)
#     gender = st.sidebar.slider("Gender", -3.0, 3.0, 0.0)
#     # st.sidebar.write("Gender:", gender)
#     pose = st.sidebar.slider("Pose", -3.0, 3.0, 0.0)
#     # st.sidebar.write("Pose:", pose)
#     smile = st.sidebar.slider("Smile", -3.0, 3.0, 0.0)
#     # st.sidebar.write("Smile:", smile)
#     st.sidebar.markdown(
#         """<style> .css-10y5sf6 { visibility: hidden;} 
#     .css-236p07{ visibility: hidden;}
#     [data-testid="stTickBarMax"]:after{ value:"Older";   visibility: visible;}
#      </style> """,
#         unsafe_allow_html=True,
#     )
#     clear_img_dir()
#     st.write(age, eyeglasses, gender, pose, smile, noise_seed)
#     image_out = generate_image(age, eyeglasses, gender, pose, smile, noise_seed)
#     st.image(image_out, use_column_width=True)

#     st.sidebar.write(
#         """Playing with the sliders, you _will_ generate new **faces** that never existed before.
#         """
#     )
#     st.sidebar.write(
#         """For example, moving the `Smiling` slider can turn a face from grinching to carrying a smile. 
#         """
#     )
#     st.sidebar.caption(f"Streamlit version `{st.__version__}`")

#     # Generate a new image from this feature vector (or retrieve it from the cache).


# if __name__ == "__main__":
#     main()


###########################################################################################



import streamlit as st
from streamlit.elements.form import current_form_id
from page_home import show_home_page
from page_generate_random_img import show_img_random_generation_page
from page_generate_specific_img import show_img_specific_generation_page
from page_user import show_user_page
from keras.preprocessing.image import load_img

import base64


if 'status' not in st.session_state:
    st.session_state['status'] = True
    st.session_state['nb_loaded_pages'] = 0
    st.session_state['page1'] = dict()
    st.session_state['page2'] = dict()
    st.session_state['page3'] = dict()

# main_bg = "img/logoEMMK.png"
# main_bg_ext = "png"

# img_logo = load_img(main_bg)
# st.sidebar.image(img_logo)

pages = ["Home 🏠", "Generate random images 🎲", "Generate specific images 🎯", "Who would you look like.. ? 🔮"]

# new_page_sidebar = st.sidebar.selectbox("Choose your page:", (pages[0], pages[1], pages[2], pages[3]))
sidebar_page = st.sidebar.selectbox("Choose your page:", (pages[1], pages[2], pages[3]))
if st.session_state['status']:
    st.session_state['current_page'] = sidebar_page
    st.session_state['nb_loaded_pages'] += 1
    # st.write(st.session_state)


if st.session_state['current_page'] == pages[1]:
    data = show_img_random_generation_page()
elif st.session_state['current_page'] == pages[2]:
    show_img_specific_generation_page()
elif st.session_state['current_page'] == pages[3]:
    show_user_page()
