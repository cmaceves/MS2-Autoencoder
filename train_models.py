import ms2_model
import numpy as np
import h5py 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', help='training data')
parser.add_argument('model', help='select the model being trained')

args = parser.parse_args()
data = args.data
model = args.model

f = h5py.File(data, 'r')
dataset_low = f['low_peaks']
dataset_high = f['high_peaks']

if model=='conv1d':
    model = ms2_model.model_Conv1D()
    model = ms2_model.fit_model(model, dataset_low, dataset_high)

elif model=='deepautoencoder':
    autoencoder = ms2_model.model_deep_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)

elif model=='autoencoder':
    autoencoder = ms2_model.model_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)

elif model=='variationalautoencoder':
    autoencoder = ms2_model.model_variational_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
