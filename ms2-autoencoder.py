#%%
from keras.layers import Input, Dense
from keras.models import Model

import numpy as np
import tensorflow as tf

import extract_mzxml as em
#%%
data_file = 'C:/Users/CCheny/Documents/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output/cholesterol/ready_array2.npz'
file = np.load(data_file, allow_pickle=True)
data = file['arr_0']
#%%
normalize = np.amax(data) #for normalizing data
np.random.shuffle(data) #randomize data list
new_list = np.split(data, 2, axis=1) #split data into low peaks and high peaks

low_peaks = new_list[0]
low_peaks = low_peaks.astype('float32') / normalize #normalize by dividing all values by the max value

high_peaks = new_list[1]
high_peaks = high_peaks.astype('float32') / normalize #normalize by dividing all values by the max value
#%%
X = low_peaks
y = high_peaks

Xsplit = int(0.8*len(X))
X_train = X[:Xsplit, :, :] #80% of the low peaks data
X_test = X[Xsplit:, :, :] #20% of the high peaks data
X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:])) #reshape to 2D
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:])) #reshape to 2D

ysplit = int(0.8*len(y))
y_train = y[:ysplit, :, :] #80% of the high peaks data
y_test = y[ysplit:, :, :] #20% of the high peaks data
y_train = y_train.reshape(len(y_train), np.prod(y_train.shape[1:])) #reshape to 2D
y_test = y_test.reshape(len(y_test), np.prod(y_test.shape[1:])) #reshape to 2D
#%%
encoding_dim = 100
input_scan = Input(shape=(2000,))
encoded = Dense(encoding_dim, activation='relu')(input_scan)
decoded = Dense(2000, activation='sigmoid')(encoded)

autoencoder = Model(input_scan, decoded)
encoder = Model(input_scan, encoded)

encoded_input = Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = Model(encoded_input, decoder_layer(encoded_input))
#%%
autoencoder.compile(optimizer='adadelta', loss='poisson')
autoencoder.fit(X_train, y_train,
                epochs=50,
                bathc_size=10,
                validation_data=(X_test, y_test))
#%%
encoded_scans = encoder.predict(X_test)
decoded_scans = decoder.predict(encoded_scans)