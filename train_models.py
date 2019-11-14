import ms2_model
import numpy as np
import h5py
from os.path import join
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', help='training data')
parser.add_argument('model', help='select the model being trained')
parser.add_argument('path', help='directory path, differs based on user/system')
parser.add_argument('--val_data', help='validation data')

args = parser.parse_args()
data = args.data
model = args.model
path = args.path
val_data = args.val_data

outdir = join(path, 'models/')

f = h5py.File(data, 'r')
dataset_low = f['low_peaks']
dataset_high = f['high_peaks']
if args.val_data:
    g = h5py.File(val_data, 'r')
    X_val = g['low_peaks']
    y_val = g['high_peaks']
else:
    print('no val data')

if model=='conv1d':
    model = ms2_model.model_Conv1D()
    model = ms2_model.fit_model(model, dataset_low, dataset_high)
    ms2_model.save_model(model, join(outdir, 'conv1d.h5'))
    ms2_model.save_history(model.history, 'conv1d_history.pickle') 

elif model=='deepautoencoder':
    autoencoder = ms2_model.model_deep_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
    ms2_model.save_model(autoencoder, join(outdir, 'deepautoencoder.h5'))
    ms2_model.save_history(autoencoder.history, 'deepautoencoder_history.pickle')

elif model=='autoencoder':
    autoencoder = ms2_model.model_autoencoder()
    #autoencoder = ms2_model.fit_val_model2(autoencoder, dataset_low, dataset_high)
    autoencoder = ms2_model.fit_model(autoencoder, dataset_high, dataset_high)
    ms2_model.save_model(autoencoder, join(outdir, 'autoencoder_high.h5'))
    ms2_model.save_history(autoencoder.history, join(outdir, 'autoencoder_high_history.pickle'))

elif model=='variationalautoencoder':
    autoencoder = ms2_model.model_variational_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
    ms2_model.save_model(autoencoder, join(outdir, 'variationalautoencoder.h5'))

print('operations complete')
