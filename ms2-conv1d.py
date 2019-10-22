from keras.layers import Input, Dense, Conv1D, MaxPooling1D, UpSampling1D
from keras.models import Model

import numpy as np
import h5py

data_file = '/home/cchen/MS2-Autoencoder/big_data_conv1d.hdf5'
f = h5py.File(data_file, 'r')
dataset_low = f['low_peaks']
dataset_high = f['high_peaks']
print(dataset_low.shape)
print(dataset_high.shape)

def generator(X_data, y_data, batch_size):
    print('generator initiated')
    steps_per_epoch = X_data.shape[0]
    number_of_batches = steps_per_epoch // batch_size
    i = 0
    
    while True:
        X_batch = dataset_low[i*batch_size:(i+1)*batch_size]
        y_batch = dataset_high[i*batch_size:(i+1)*batch_size]
        i += 1
        yield X_batch, y_batch
        print('\ngenerator yielded a batch %s' %i)
        
        if i >= number_of_batches:
            i = 0

input_size = 2000
input_scan = Input(shape=(input_size, 1))
print(input_scan.shape)
hidden_1 = Conv1D(1, (5, ), activation='relu', padding='same')(input_scan)
print(hidden_1.shape)
hidden_2 = MaxPooling1D()(hidden_1)
hidden_3 = Conv1D(1, (5, ), activation='relu', padding='same')(hidden_2)
print(hidden_3.shape)
hidden_4 = MaxPooling1D()(hidden_3)
hidden_5 = Conv1D(1, (5, ), activation='relu', padding='same')(hidden_4)
print(hidden_5.shape)
encoded = MaxPooling1D((5, ))(hidden_5)
print(encoded.shape)

hidden_6 = Conv1D(1, (5, ), activation='relu', padding='same')(encoded)
print(hidden_6.shape)
hidden_7 = UpSampling1D(5)(hidden_6)
hidden_8 = Conv1D(1, (5, ), activation='relu', padding='same')(hidden_7)
print(hidden_7.shape)
hidden_9 = UpSampling1D()(hidden_8)
hidden_10 = Conv1D(1, (5, ), activation='relu', padding='same')(hidden_9)
print(hidden_10.shape)
hidden_11 = UpSampling1D()(hidden_10)
decoded = Conv1D(1, (5, ), activation='relu', padding='same')(hidden_11)
print(decoded.shape)

autoencoder = Model(input_scan, decoded)
autoencoder.compile(optimizer='adadelta', loss='cosine_proximity', metrics=['accuracy'])

batch_size = 5000
autoencoder.fit_generator(generator=generator(dataset_low, dataset_high, batch_size), 
                          max_queue_size=20, 
                          steps_per_epoch=dataset_low.shape[0] // batch_size, 
                          epochs=50)

#save Model architecture to json
json_model = autoencoder.to_json()
json_file = open('/home/cchen/MS2-Autoencoder/models/conv1d.json', 'w')
json_file.write(json_model)
#saving model architecture to yaml
yaml_model = autoencoder.to_yaml()
yaml_file = open('/home/cchen/MS2-Autoencoder/models/conv1d.yaml', 'w')
yaml_file.write(yaml_model)

#save architeture and weights to hdf5
autoencoder.save('/home/cchen/MS2-Autoencoder/models/conv1d_model.h5')
'''
#loading model
from keras.models import load_model
model1 = load_model('/home/cchen/MS2-Autoencoder/models/conv1d_model.h5')
'''