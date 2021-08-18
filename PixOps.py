# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 01:44:43 2021

@author: Akash
"""
import os
import matplotlib.pyplot as plt

class super_resolution:
    def __init__(self):
        from models.srgan import generator
        from models.model_utils import resolve_single
        from utils import load_image
        weights_dir = "weights/srgan"
        weights_file = lambda filename: os.path.join(weights_dir, filename)
        
    def gen_sr(self, image_path):
        gan_generator = self.generator()
        gan_generator.load_weights(self.weights_file('gan_generator.h5'))
        
        img = self.load_image(image_path)
        sr = self.resolve_single(gan_generator, img)
        
        plt.imshow(sr)