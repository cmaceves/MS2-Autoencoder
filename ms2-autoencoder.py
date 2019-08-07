#%%
from keras.layers import Input, Dense
from keras.models import Model

import numpy as numpy
import tensorflow as tf

import extract_mzxml as em

#%%
simpled_dict = em.unpack('simple_dict.json')

