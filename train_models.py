import ms2_model
import numpy as np
import h5py 
from os.path import join
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', help='training data')
parser.add_argument('model', help='select the model being trained')
parser.add_argument('path', help='directory path, differs based on user/system')

args = parser.parse_args()
data = args.data
model = args.model
path = args.path

outdir = join(path, 'models/')

f = h5py.File(data, 'r')
dataset_low = f['low_peaks']
dataset_high = f['high_peaks']

if model=='conv1d':
    model = ms2_model.model_Conv1D()
    model = ms2_model.fit_model(model, dataset_low, dataset_high)
    save_model(model, join(outdir, 'conv1d.json'), join(outdir, 'conv1d.h5'))    

elif model=='deepautoencoder':
    autoencoder = ms2_model.model_deep_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
    save_model(model, join(outdir, 'deepautoencoder.json'), join(outdir, 'deepautoencoder.h5'))

elif model=='autoencoder':
    autoencoder = ms2_model.model_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
    save_model(model, join(outdir, 'autoencoder.json'), join(outdir, 'autoencoder.h5'))

elif model=='variationalautoencoder':
    autoencoder = ms2_model.model_variational_autoencoder()
    autoencoder = ms2_model.fit_model(autoencoder, dataset_low, dataset_high)
    save_model(model, join(outdir, 'variationalautoencoder.json'), join(outdir, 'variationalautoencoder.h5'))

print('operations complete')
