# -*- coding: utf-8 -*-
import os
import string
import subprocess
import sys
import os.path
import io
import IPython.display
import numpy as np
import cv2
import PIL.Image
import torch
import matplotlib.pyplot as plt
import random

# constants and paths
if not os.path.exists("interfacegan/models/pretrain/stylegan_celebahq.pth"):
    bashCommand = "wget https://www.dropbox.com/s/nmo2g3u0qt7x70m/stylegan_celebahq.pth?dl=1 -O interfacegan/models/pretrain/stylegan_celebahq.pth --quiet"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
os.chdir("/content")
CODE_DIR = "interfacegan"
os.chdir(f"./{CODE_DIR}")
tmp_download_dir = "/content/downloaded_imgs/"

from interfacegan.models.model_settings import MODEL_POOL
from interfacegan.models.stylegan_generator import StyleGANGenerator
from interfacegan.utils.manipulator import linear_interpolate

def build_generator(model_name):
    """Builds the generator by model name."""
    generator = StyleGANGenerator(model_name)
    return generator


def sample_codes(generator, num, latent_space_type="Z", seed=0):
    """Samples latent codes randomly."""
    np.random.seed(seed)
    codes = generator.easy_sample(num)
    if latent_space_type == "W":
        codes = torch.from_numpy(codes).type(torch.FloatTensor).to(generator.run_device)
        codes = generator.get_value(generator.model.mapping(codes))
    return codes


"""# Select a Model"""


def select_model(model_name, generator, latent_space_type):
    boundaries = {}
    for i, attr_name in enumerate(ATTRS):
        boundary_name = f"{model_name}_{attr_name}"
        if generator.gan_type == "stylegan" and latent_space_type == "W":
            boundaries[attr_name] = np.load(
                f"boundaries/{boundary_name}_w_boundary.npy"
            )
        else:
            boundaries[attr_name] = np.load(f"boundaries/{boundary_name}_boundary.npy")
    return boundaries


"""# Sample latent codes"""


def sample_latentcodes(generator, latent_space_type,noise_seed):
    num_samples = 1   
    latent_codes = sample_codes(generator, num_samples, latent_space_type, noise_seed)
    if generator.gan_type == "stylegan" and latent_space_type == "W":
        synthesis_kwargs = {"latent_space_type": "W"}
    else:
        synthesis_kwargs = {}

    return latent_codes, synthesis_kwargs


"""# Edit facial attributes"""

if __name__ == "__main__":
    model_name = "stylegan_celebahq"  # @param ['pggan_celebahq','stylegan_celebahq', 'stylegan_ffhq']
    latent_space_type = "WP"  # @param ['Z', 'W']
    ATTRS = ["age", "eyeglasses", "gender", "pose", "smile"]
    generator = build_generator(model_name)
    boundaries = select_model(model_name, generator, latent_space_type)
    
    # parse arguments from command line
    age = float(sys.argv[1])  # @param {type:"slider", min:-3.0, max:3.0, step:0.1}
    eyeglasses = float(sys.argv[2])  # @param {type:"slider", min:-3.0, max:3.0, step:0.1}
    gender = float(sys.argv[3])  # @param {type:"slider", min:-3.0, max:3.0, step:0.1}
    pose = float(sys.argv[4])  # @param {type:"slider", min:-3.0, max:3.0, step:0.1}
    smile = float(sys.argv[5])  # @param {type:"slider", min:-3.0, max:3.0, step:0.1}
    noise_seed=int(sys.argv[6])  # @param changes when 
    # define latent_codes
    latent_codes, synthesis_kwargs = sample_latentcodes(generator, latent_space_type,noise_seed)
    new_codes = latent_codes.copy()
    for i, attr_name in enumerate(ATTRS):
        new_codes += boundaries[attr_name] * eval(attr_name)
    new_images = generator.easy_synthesize(new_codes, **synthesis_kwargs)["image"]
    img_name = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )
    plt.imsave(tmp_download_dir + img_name + ".jpg", new_images.squeeze(0))

    # do not change this line, this is the last print and the line parsed by the streamlit to show the resulting image
    print("\n" + tmp_download_dir + img_name + ".jpg")