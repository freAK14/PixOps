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
import cv2

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
        
        pil_img = tf.keras.preprocessing.image.array_to_img(sr)
        pil_img.save('./static/generated/superImage.png')

class colorization:
    def __init__(self):
        pass
    
    def color(self, image_path):
        from skimage.color import rgb2lab, lab2rgb
        from tensorflow.keras.preprocessing import image
        weights_dir = "./weights/colorization_unet/"
        
        model = tf.keras.models.load_model(weights_dir+"U-Net-epoch-100-loss-0.006095.hdf5")
        img = image.img_to_array(image.load_img(image_path))
        h, w = img.shape[0], img.shape[1]
        img_color = []
        img_resize = image.img_to_array(image.load_img(image_path, target_size=(256, 256, 3)))
        image.save_img("./static/generated/bwImage.png", img_resize)
        img_color.append(img_resize)
        img_color = np.array(img_color, dtype=float)
        img_color = rgb2lab(img_color/255.0)[:,:,:,0]
        img_color = img_color.reshape(img_color.shape+(1,))
        output = model.predict(img_color)
        output = output * 128
        result = np.zeros((256, 256, 3))
        result[:, :, 0] = img_color[0][:, :, 0]
        result[:, :, 1:] = output[0]
        final_img = lab2rgb(result)
        image.save_img('./static/generated/colorImage.png', final_img)
        
class style_transfer():
    def __init__(self):
        pass
    def transfer(self, content_imgpath, style_imgpath):
        print(content_imgpath)
        print(style_imgpath)
        print("Tested! OK")
        from models.style_transfer import WCT2
        from models.model_utils import read_img
        model = WCT2()
        model.load_weight('./weights/style_transfer/wct2.h5')
        image_size = 512
        #print("-1-1-1-1-1-1-1-111111111111111111111111111111111111111111111111111111111111111111111111")
        content = read_img(content_imgpath, image_size, expand_dims=True)
        style = read_img(style_imgpath, image_size, expand_dims=True)
        cv2.imwrite('./static/generated/contentImage.png', content[0][...,::-1])
        cv2.imwrite('./static/generated/styleImage.png', style[0][...,::-1])
        #print("22222222222222222222222222222222222222222222222222222222222222222222222")
        gen = model.transfer(content, style)
        cv2.imwrite('./static/generated/genImage.png', gen[0][...,::-1])
        