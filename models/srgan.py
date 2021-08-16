# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:25:10 2021

@author: Akash
"""
from tensorflow.python.keras.layers import Add, BatchNormalization, Conv2D, Dense, Flatten, Input, LeakyReLU, PReLU, Lambda
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.vgg19 import VGG19


LR_SIZE = 24
HR_SIZE = 96