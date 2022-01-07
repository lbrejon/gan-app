import numpy as np
import torch
import random
import string
import matplotlib.pyplot as plt
import os
import pickle
import nvae
# before executing this file, please execute ./interfacenvae/utils.py to load the model
# this file should be in the same folder with nvae.py for speed reasons

CODE_DIR = "/content/GenfaceDemo/interfacenvae"

tmp_download_dir = "/content/downloaded_imgs/"

model_path = "/content/GenfaceDemo/model.pkl"

os.chdir(".")
if not os.path.exists(tmp_download_dir):
  os.mkdir(tmp_download_dir)

def generate_model(model_path, code_dir):
  if os.path.exists(model_path):
    #if the model pickle exists
    with open(model_path, 'rb') as model_storage:
      model = pickle.load(model_storage)
  #else:
    #model = nvae.load_pretrained_model("celeba_256a", CODE_DIR+"/")
    #model.to(device)
  return model

def inference_nvae(model, download_dir):
    #generate random temperature value in 0.7 0.75
    t= 0.75# random value around 0.75 (tested and gives good resulst)
    with torch.no_grad():
        logits = model.sample(1, t)
        output = model.decoder_output(logits)
        output_img = output.sample()    
        output_img = output_img.permute(0, 2, 3, 1).squeeze().cpu().numpy()
        img_name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        plt.imsave(tmp_download_dir + img_name + ".jpg", output_img)
        print("\n" + tmp_download_dir + img_name + ".jpg")

if __name__ == "__main__":
    print("CURRENT DIRECTORY: ", os.getcwd())
    # model = generate_model(model_path, CODE_DIR)
    # inference_nvae(model, tmp_download_dir)