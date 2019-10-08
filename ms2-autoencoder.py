from keras.layers import Input, Dense
from keras.models import Model

import numpy as np
import tensorflow as tf
data_file = 'concated_data.npz'
file = np.load(data_file, allow_pickle=True)
data = file['arr_0']

np.random.shuffle(data) #randomize data list
new_list = np.split(data, 2, axis=1) #split data into low peaks and high peaks

def normalize_peaks(peaks_array):
    for i in range(0, len(peaks_array)):
        peak_max = np.amax(peaks_array[i])
        if peak_max==0.0:
            peaks_array[i] = peaks_array[i]
        else:
            peaks_array[i] = peaks_array[i] / peak_max
    return peaks_array

low_peaks = new_list[0]
low_peaks = low_peaks.astype('float32')

high_peaks = new_list[1]
high_peaks = high_peaks.astype('float32')

X = normalize_peaks(low_peaks)
y = normalize_peaks(high_peaks)

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

encoding_dim = 100
input_scan = Input(shape=(2000,))
hidden_1 = Dense(1000, activation='relu')(input_scan)
hidden_2 = Dense(500, activation='relu')(hidden_1)
encoded = Dense(encoding_dim, activation='relu')(hidden_2)
hidden_3 = Dense(500, activation='relu')(encoded)
hidden_4 = Dense(1000, activation='relu')(hidden_3)
decoded = Dense(2000, activation='relu')(hidden_4)

autoencoder = Model(input_scan, decoded)

autoencoder.compile(optimizer='adadelta', loss='cosine_proximity', metrics=['accuracy'])
autoencoder.summary()
autoencoder.fit(X_train, y_train,
                epochs=200,
                batch_size=100,
                validation_data=(X_test, y_test))

predicted = autoencoder.predict(X_test)

#save Model architecture to json
json_model = autoencoder.to_json()
json_file = open('autoencoder_json.json', 'w')
json_file.write(json_model)
#saving model architecture to yaml
yaml_model = autoencoder.to_yaml()
yaml_file = open('autoencoder_yaml.yaml', 'w')
yaml_file.write(yaml_model)

#save architeture and weights to hdf5
autoencoder.save('autoencoder_model.h5')
#loading model
from keras.models import load_model
model1 = load_model('autoencoder_model.h5')