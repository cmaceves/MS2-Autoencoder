from keras.layers import Input, Dense
from keras.models import Model

import numpy as np
import h5py

data_file = '/home/cchen/MS2-Autoencoder/big_data.hdf5'
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
encoding_dim = 100
input_scan = Input(shape=(input_size,))
hidden_1 = Dense(1000, activation='relu')(input_scan)
hidden_2 = Dense(500, activation='relu')(hidden_1)
encoded = Dense(encoding_dim, activation='relu')(hidden_2)
hidden_3 = Dense(500, activation='relu')(encoded)
hidden_4 = Dense(1000, activation='relu')(hidden_3)
decoded = Dense(input_size, activation='relu')(hidden_4)

autoencoder = Model(input_scan, decoded)

autoencoder.compile(optimizer='adadelta', loss='cosine_proximity', metrics=['accuracy'])
autoencoder.summary()

batch_size = 5000
autoencoder.fit_generator(generator=generator(dataset_low, dataset_high, batch_size), 
                          max_queue_size=20, 
                          steps_per_epoch=dataset_low.shape[0] // batch_size, 
                          epochs=50)

#save Model architecture to json
json_model = autoencoder.to_json()
json_file = open('/home/cchen/MS2-Autoencoder/models/deepautoencoder.json', 'w')
json_file.write(json_model)
#saving model architecture to yaml
yaml_model = autoencoder.to_yaml()
yaml_file = open('/home/cchen/MS2-Autoencoder/models/deepautoencoder.yaml', 'w')
yaml_file.write(yaml_model)

#save architeture and weights to hdf5
autoencoder.save('/home/cchen/MS2-Autoencoder/models/deepautoencoder_model.h5')
'''
#loading model
from keras.models import load_model
model1 = load_model('/home/cchen/MS2-Autoencoder/models/deepautoencoder_model.h5')
'''