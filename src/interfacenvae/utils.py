# import and utils for nvae

#########################################################
#this script downloads the model checkpoint loads it in cuda and stores it in pickle 
#format for future use and speed considerations
# this script should be executed before calling the streamlit app
import sys
import torch
import os
import pickle

#check if folder /content/downloaded_imgs exists
tmp_download_folder = "/content/downloaded_imgs"
CODE_DIR = "/content/gan-app/src/interfacenvae"
model_path = "/content/gan-app/src/model.pkl" #storing model once loaded

if not os.path.exists(tmp_download_folder):
    os.mkdir(tmp_download_folder)


# use GPU for computation if possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# make sure that files in local directory can be imported
sys.path.insert(0, ".")
os.chdir("/content/gan-app/src")

# try to import nvae module and download it if it fails
import urllib

# load code for NVAE
try:
    import nvae
except ImportError:
    urllib.request.urlretrieve("https://uu-sml.github.io/course-apml-public/lab/nvae.py", "nvae.py")

# load nvae model celeba_256
model = nvae.load_pretrained_model("celeba_256a", CODE_DIR+"/")
model.to(device)
with open(model_path, 'wb') as model_storage:
    pickle.dump(model, model_storage)
