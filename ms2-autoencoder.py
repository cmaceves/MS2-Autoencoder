from keras.layers import Input, Dense
from keras.models import Model

import numpy as np
import tensorflow as tf

data_file = 'concated_data.npz'
file = np.load(data_file, allow_pickle=True)
data = file['arr_0']

normalize = np.amax(data) #for normalizing data
np.random.shuffle(data) #randomize data list
new_list = np.split(data, 2, axis=1) #split data into low peaks and high peaks

low_peaks = new_list[0]
low_peaks = low_peaks.astype('float32') / normalize #normalize by dividing all values by the max value

high_peaks = new_list[1]
high_peaks = high_peaks.astype('float32') / normalize #normalize by dividing all values by the max value

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

encoding_dim = 100
input_scan = Input(shape=(2000,))
encoded = Dense(encoding_dim, activation='relu')(input_scan)
decoded = Dense(2000, activation='sigmoid')(encoded)

autoencoder = Model(input_scan, decoded)

autoencoder.compile(optimizer='adadelta', loss='cosine_proximity')
autoencoder.fit(X_train, y_train,
                epochs=50,
                batch_size=10,
                validation_data=(X_test, y_test))

predict_test = autoencoder.predict(X_test)
#scale everything back 
X_test_norm = X_test * normalize
predict_test_norm = predict_test * normalize
Y_test_norm = y_test * normalize

#plot graph of a predicted and test case
import matplotlib.pyplot as plt
fig, axs = plt.subplots(3, 1, figsize=(20,20))
i = 3
first = X_test_norm[i]
second = predict_test_norm[i]
third = Y_test_norm[i]
top_max = Y_test_norm[i]

axs[0].plot(range(0, 2000), first)
axs[0].set_ylim(bottom=0, top=np.amax(top_max), auto=True)
print(np.amax(first))
axs[1].plot(range(0, 2000), second)
axs[1].set_ylim(bottom=0, top=np.amax(top_max), auto=True)
print(np.amax(second))
axs[2].plot(range(0, 2000), third)
axs[2].set_ylim(bottom=0, top=np.amax(top_max), auto=True)
print(np.amax(third))

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