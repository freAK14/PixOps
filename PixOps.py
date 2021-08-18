# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 01:44:43 2021

@author: Akash
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image

class super_resolution:
    def __init__(self):
        pass
        
    def gen_sr(self, image_path):
        from models.model_utils import resolve_single
        from models.srgan import generator
        weights_dir = "weights/srgan"
        weights_file = lambda filename: os.path.join(weights_dir, filename)
        gan_generator = generator()
        gan_generator.load_weights(weights_file('gan_generator.h5'))
        
        img = np.array(Image.open(image_path))
        sr = resolve_single(gan_generator, img)
        
        #plt.imshow(sr)
        #plt.savefig("./demo_images/op.png")
        pil_img = tf.keras.preprocessing.image.array_to_img(sr)
        pil_img.save('./demo_images/op.png')