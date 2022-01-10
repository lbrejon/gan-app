import os
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_probability as tfp
import matplotlib.pyplot as plt
import pandas as pd
import zipfile 
import gdown
from tensorflow.keras import Sequential, Model
from tensorflow.keras.layers import (Dense, Flatten, Reshape, Conv2D, 
                                     UpSampling2D, BatchNormalization)
tfd = tfp.distributions
tfb = tfp.bijectors
tfpl = tfp.layers

DIR = "/content/gan-app/src/interfacevae"

DIR_CHECKPOINTS = f"{DIR}/checkpoints2"
tmp_download_dir = "/content/downloaded_imgs"

###################################################""
### VAE Model and config 
###################################################""
def get_prior(num_modes, latent_dim):
    probs = [1./num_modes] * num_modes
    mixture = tfd.Categorical(probs=probs)

    prior = tfd.MixtureSameFamily(
        mixture_distribution=mixture,
        components_distribution=tfd.MultivariateNormalDiag(
            loc=tf.Variable(
                tf.random.normal((num_modes, latent_dim)),
                trainable=True, 
                dtype=tf.float32
                ),
            scale_diag=tfp.util.TransformedVariable(
                initial_value=tf.ones((num_modes, latent_dim)),
                bijector=tfb.Softplus()
                )
            )
        )
    
    return prior




# KLD is calculated using Monte-Carlo Estimate of 3 samples

def get_kl_regularizer(prior):
    regularizer = tfpl.KLDivergenceRegularizer(
        prior,
        use_exact_kl=False,
        weight=1.0, 
        test_points_fn=lambda q: q.sample(3),
        test_points_reduce_axis=(0, 1)
    )

    return regularizer



def get_encoder(latent_dim, kl_regularizer):
    encoder = Sequential([
        Conv2D(32, 4, input_shape=(64, 64, 3), strides=2, padding='SAME', activation='relu'),
        BatchNormalization(),
        Conv2D(64, 4, strides=2, padding='SAME', activation='relu'),
        BatchNormalization(),
        Conv2D(128, 4, strides=2, padding='SAME', activation='relu'),
        BatchNormalization(),
        Conv2D(256, 4, strides=2, padding='SAME', activation='relu'),
        BatchNormalization(),
        Flatten(),
        Dense(tfpl.MultivariateNormalTriL.params_size(latent_dim)),
        tfpl.MultivariateNormalTriL(latent_dim, activity_regularizer=kl_regularizer)
    ])

    return encoder



def get_decoder(latent_dim):
    decoder = Sequential([
        Dense(4096, input_shape=(latent_dim,), activation='relu'),
        Reshape((4, 4, 256)),
        UpSampling2D(2),
        Conv2D(128, 3, padding='SAME', activation='relu'),
        UpSampling2D(2),
        Conv2D(64, 3, padding='SAME', activation='relu'),
        UpSampling2D(2),
        Conv2D(32, 3, padding='SAME', activation='relu'),
        UpSampling2D(2),
        Conv2D(128, 3, padding='SAME', activation='relu'),
        Conv2D(3, 3, padding='SAME'),
        Flatten(),
        tfpl.IndependentBernoulli((64, 64, 3))
    ])

    return decoder


# blocks
 
# prior = get_prior(num_modes=2, latent_dim=100)
# kl_regularizer = get_kl_regularizer(prior)
# encoder = get_encoder(latent_dim=100, kl_regularizer=kl_regularizer)
# decoder = get_decoder(latent_dim=100)



# ########################################################
# # Load model from checkpoints folder (only thing that takes time (250Mb) )  
# ########################################################



# # define model
# vae = Model(inputs=encoder.inputs, outputs=decoder(encoder.outputs))

# # Include the epoch in the file name (uses `str.format`)
# DIR_CHECKPOINTS = f"{DIR}/checkpoints"
# checkpoint_path = f"{DIR_CHECKPOINTS}/cp-{epoch:04d}.ckpt"
# checkpoint_dir = os.path.dirname(checkpoint_path)
# if not os.path.exists(checkpoint_dir):
#     os.makedirs(checkpoint_dir)

# # get latest checkpoint files (training can be done separately and checkpoint updated)
# url1="https://drive.google.com/uc?id=1ikqdP9EsTM_1AoTUz0D0PAmD1AUj9Ktx" #ckpt
# url2="https://drive.google.com/uc?id=1fjrS4dnytmZk1Uz14UV0qHs5DEuPgKx0" #
# url3="https://drive.google.com/uc?id=1fH7KRS9vWge6U6Ufwh8nL9Pns9KSReFv" #idx

# gdown.download(url1, f"{DIR_CHECKPOINTS}/cp-0018.ckpt.data-00000-of-00001", quiet=False)
# gdown.download(url2, f"{DIR_CHECKPOINTS}/checkpoint", quiet=False)
# gdown.download(url3, f"{DIR_CHECKPOINTS}/cp-0018.ckpt.index", quiet=False)

# latest = tf.train.latest_checkpoint(checkpoint_dir)
# vae.load_weights(latest)



# ########
# # Generate img 
# #######

def generate_images(prior, decoder, n_samples):
  z = prior.sample(n_samples)

  return decoder(z).mean()

###########
# use example
###########

#sampled_images = generate_images(prior, decoder, 10)
#imshow(sampled_images[1])

def generate_model():
    prior = get_prior(num_modes=2, latent_dim=100)
    kl_regularizer = get_kl_regularizer(prior)
    encoder = get_encoder(latent_dim=100, kl_regularizer=kl_regularizer)
    decoder = get_decoder(latent_dim=100)

    # define model
    vae = Model(inputs=encoder.inputs, outputs=decoder(encoder.outputs))

    # Include the epoch in the file name (uses `str.format`)
    # checkpoint_path = f"{DIR_CHECKPOINTS}/cp-{epoch:04d}.ckpt"
    # checkpoint_dir = os.path.dirname(checkpoint_path)
    # if not os.path.exists(checkpoint_dir):
    #     os.makedirs(checkpoint_dir)

    # get latest checkpoint files (training can be done separately and checkpoint updated)
    # url1="https://drive.google.com/uc?id=1ikqdP9EsTM_1AoTUz0D0PAmD1AUj9Ktx" #ckpt
    # url2="https://drive.google.com/uc?id=1fjrS4dnytmZk1Uz14UV0qHs5DEuPgKx0" #
    # url3="https://drive.google.com/uc?id=1fH7KRS9vWge6U6Ufwh8nL9Pns9KSReFv" #idx

    # gdown.download(url1, f"{DIR_CHECKPOINTS}/cp-0018.ckpt.data-00000-of-00001", quiet=False)
    # gdown.download(url2, f"{DIR_CHECKPOINTS}/checkpoint", quiet=False)
    # gdown.download(url3, f"{DIR_CHECKPOINTS}/cp-0018.ckpt.index", quiet=False)

    latest = tf.train.latest_checkpoint(DIR_CHECKPOINTS)
    vae.load_weights(latest)
    return prior, decoder


if __name__ == "__main__":
    prior = get_prior(num_modes=2, latent_dim=100)
    kl_regularizer = get_kl_regularizer(prior)
    encoder = get_encoder(latent_dim=100, kl_regularizer=kl_regularizer)
    decoder = get_decoder(latent_dim=100)

    # define model
    vae = Model(inputs=encoder.inputs, outputs=decoder(encoder.outputs))
    latest = tf.train.latest_checkpoint(DIR_CHECKPOINTS)
    vae.load_weights(latest)

    n_samples = 10

    z = prior.sample(n_samples)
    sampled_images = decoder(z).mean()

    # prior, decoder = generate_model(model_path, CODE_DIR)
    # n_samples = 1
    # sampled_images = generate_images(prior, decoder, n_samples)
    img_name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    output_img = sampled_images[0]

    tmp_download_dir = "/content/downloaded_imgs/"

    plt.imsave(tmp_download_dir + img_name + ".jpg", output_img)
    print("\n" + tmp_download_dir + img_name + ".jpg")


    # print("/content/downloaded_imgs/init/MB809G.jpg")


    # inference_vae(model, tmp_download_dir)
