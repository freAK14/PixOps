# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:27:54 2021

@author: Akash
"""
import numpy as np
import tensorflow as tf

DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255

def normalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return (x - rgb_mean) / 127.5

def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean

def normalize_021(x):
    #Normalizes RGB Images to [0, 1]
    return x / 255.0

def normalize_121(x):
    #Normalizes RGB Images to [-1, 1]
    return x / 127.5 - 1

def denormalize_121(x):
    #Inverse function for normalize_121
    return (x + 1) * 127.5
    
def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)
