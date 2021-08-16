# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:25:10 2021

@author: Akash
"""
from tensorflow.python.keras.layers import Add, BatchNormalization, Conv2D, Dense, Flatten, Input, LeakyReLU, PReLU, Lambda
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.vgg19 import VGG19

from model_utils import pixel_shuffle, normalize_021, normalize_121, denormalize_121

LR_SIZE = 24
HR_SIZE = 96

def upsample(x_in, num_filters):
    x = Conv2D(num_filters, kernel_size = 3, padding = 'same')(x_in)
    x = Lambda(pixel_shuffle(scale = 2))(x)
    return PReLU(shared_axes=[1, 2])(x)

def sr_resnet(num_filters = 64, num_res_blocks = 16):
    x_in = Input(shape=(None, None, 3))
    x = Lambda(normalize_021)(x_in)