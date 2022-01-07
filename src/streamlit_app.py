import numpy as np
import os
import pickle
import streamlit as st
import sys
import tensorflow as tf
import urllib
import subprocess
from PIL import Image
import os
import glob
import time
import random

favicons_dir = "/content/GenfaceDemo/Favicon/"


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
    var_name = var.splitlines()[-1]
    file_name = var_name.decode("utf-8")
    with open(file_name, "rb") as file:
        img = Image.open(file_name)
    return img


def main():
    st.set_page_config("GenFace", favicons_dir + "favicon.ico")
    if not os.path.exists("./noise_seed.txt"):
        f = open("./noise_seed.txt", "a+")
        f.write("392")
        f.close()

    f = open("./noise_seed.txt", "r")
    noise_seed = int(float(f.read()))
    f.close()

    st.title("GenFace's StyleGAN generator")
    st.sidebar.title("Facial attributes")

    if st.sidebar.button("Generate a new face"):
        noise_seed = random.randint(0, 1000)  # min:0, max:1000, step:1
        f = open("./noise_seed.txt", "w")
        f.truncate(0)
        f.write(str(noise_seed))  # update noise seed
        f.close()

    age = st.sidebar.slider("Age", -3.0, 3.0, 0.0)
    # st.sidebar.write("Age:", age)
    eyeglasses = st.sidebar.slider("Eyeglasses", -3.0, 3.0, 0.0)
    # st.sidebar.write("Eyeglasses:", eyeglasses)
    gender = st.sidebar.slider("Gender", -3.0, 3.0, 0.0)
    # st.sidebar.write("Gender:", gender)
    pose = st.sidebar.slider("Pose", -3.0, 3.0, 0.0)
    # st.sidebar.write("Pose:", pose)
    smile = st.sidebar.slider("Smile", -3.0, 3.0, 0.0)
    # st.sidebar.write("Smile:", smile)
    st.sidebar.markdown(
        """<style> .css-10y5sf6 { visibility: hidden;} 
    .css-236p07{ visibility: hidden;}
    [data-testid="stTickBarMax"]:after{ value:"Older";   visibility: visible;}
     </style> """,
        unsafe_allow_html=True,
    )
    clear_img_dir()
    image_out = generate_image(age, eyeglasses, gender, pose, smile, noise_seed)
    st.image(image_out, use_column_width=True)

    st.sidebar.write(
        """Playing with the sliders, you _will_ generate new **faces** that never existed before.
        """
    )
    st.sidebar.write(
        """For example, moving the `Smiling` slider can turn a face from grinching to carrying a smile. 
        """
    )
    st.sidebar.caption(f"Streamlit version `{st.__version__}`")

    # Generate a new image from this feature vector (or retrieve it from the cache).


if __name__ == "__main__":
    main()
