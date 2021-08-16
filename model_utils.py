# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:27:54 2021

@author: Akash
"""
import numpy as np
import tensorflow as tf

def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)
