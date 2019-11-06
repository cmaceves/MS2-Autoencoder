from keras.layers import Input, Dense, Conv1D, MaxPooling1D, UpSampling1D
from keras.models import Model

import numpy as np
import h5py

def generator(X_data, y_data, batch_size):
    print('generator initiated')
    steps_per_epoch = X_data.shape[0]
    number_of_batches = steps_per_epoch // batch_size
    i = 0
    
    while True:
        X_batch = X_data[i*batch_size:(i+1)*batch_size]
        y_batch = y_data[i*batch_size:(i+1)*batch_size]
        i += 1
        yield X_batch, y_batch
        print('\ngenerator yielded a batch %s' %i)
        
        if i >= number_of_batches:
            i = 0

def test_generator(X_data, batch_size):
    print('generator initiated')
    steps_per_epoch = X_data.shape[0]
    number_of_batches = steps_per_epoch // batch_size
    i = 0

    while True: 
        X_batch = X_data[i*batch_size:(i+1)*batch_size]
        i += 1
        yield X_batch
        print('\ngenerator yielded a batch %s' %i)

        if i >= number_of_batches:
            i = 0

def fit_model(model, X_data, y_data):
    batch_size = 10000
    model.fit_generator(generator=generator(X_data, y_data, batch_size), 
                        max_queue_size=20, 
                        steps_per_epoch=X_data.shape[0] // batch_size, 
                        epochs=1)
    return model

def predict_model(model, X_data):
    batch_size = 50
    prediction = model.predict_generator(generator=test_generator(X_data, batch_size),
                                            max_queue_size=20,
                                            steps=X_data.shape[0] // batch_size)
    return prediction

def eval_model(model, X_data, y_data):
    batch_size = 50
    evaluation = model.evaluate_generator(generator=generator(X_data, y_data, batch_size),
                                            max_queue_size=20,
                                            steps=X_data.shape[0] // batch_size)
    return evaluation

def save_model(model, name_h5):
    model.save(name_h5)
    print('model has been saved to .h5')

def save_history(history, history_file):
    json.dump(history, open(history_file, 'w'))
    print('training history has been saved to .json')

def load_history(history_file):
    history_dict = json.load(open(history_file, 'r'))

def model_Conv1D():
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

    model = Model(input_scan, decoded)
    model.compile(optimizer='adadelta', loss='cosine_proximity', metrics=['accuracy'])
    return model

def model_deep_autoencoder():
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
    return autoencoder

def model_autoencoder():
    input_size = 2000
    encoding_dim = 100
    input_scan = Input(shape=(input_size,))
    encoded = Dense(encoding_dim, activation='relu')(input_scan)

    decoded = Dense(input_size, activation='relu')(encoded)

    autoencoder = Model(input_scan, decoded)
    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
    return autoencoder

def model_variational_autoencoder():

    return 0