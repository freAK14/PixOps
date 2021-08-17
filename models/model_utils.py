# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:27:54 2021

@author: Akash
"""
import numpy as np
import tensorflow as tf

DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255

'''#######################
      Utility Functions
   #######################'''

def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch

def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]

def evaluate(model, dataset):
    psnr_values = []
    for lr, hr in dataset:
        sr = resolve(model, lr)
        psnr_value = psnr(hr, sr)[0]
        psnr_values.append(psnr_value)
    return tf.reduce_mean(psnr_values)

def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)

'''#######################
   Normalization Functions
   #######################'''

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

'''#######################
           Metrics
   #######################'''
def psnr(x1, x2):
    return tf.image.psnr(x1, x2, max_val=255)
