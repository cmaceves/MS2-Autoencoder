#%%
from keras.layers import Input, Dense
from keras.models import Model

import numpy as np
import tensorflow as tf

import extract_mzxml as em

#%%
simple_list_file = 'C:/Users/CCheny/Documents/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output/cholesterol/simple_list.npy'
simple_list = np.load(simple_list_file, allow_pickle=True)

X_train = simple_list[1] #features
y_train = simple_list[0] #labels

#%%
num_inputs = 
num_hid1 = 
num_hid2 = 
num_hid3 = 
num_output = num_inputs
learning_rate = 0.01
activation_function = tf.nn.relu 

#%%
X = tf.placeholder(tf.float64)
initializer = tf.variance_scaling_initializer()

w1 = tf.Variable(initializer([num_inputs, num_hid1]), dtype = tf.float64)
w2 = tf.Variable(initializer([num_hid1, num_hid2]), dtype = tf.float64)
w3 = tf.Variable(initializer([num_hid2, num_hid3]), dtype=tf.float64)
w4 = tf.Variable(initializer([num_hid3, num_output]), dtype=tf.float64)

b1 = tf.Variable(tf.zeros(num_hid1))
b2 = tf.Variable(tf.zeros(num_hid2))
b3 = tf.Variable(tf.zeros(num_hid3))
b4 = tf.Variable(tf.zeros(num_output))

hid_layer1 = activation_function(tf.matmul(X, w1) + b1)
hid_layer2 = activation_function(tf.matmul(hid_layer1, w2) + b2)
hid_layer3 = activation_function(tf.matmul(hid_layer2, w3) + b3)
output_layer = activation_function(tf.matmul(hid_layer3, w4) + b4)

#%%
loss = tf.reduce_mean(tf.square(output_layer - X))
optimizer = tf.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

num_epoch = 5
batch_size = 

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(num_epoch):
        