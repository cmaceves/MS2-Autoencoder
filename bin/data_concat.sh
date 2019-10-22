#!/bin/sh
#python processing.py '/home/cchen/autoencode_output/' 'ready_array2.npz' --name '/home/cchen/MS2-Autoencoder/big_data.hdf5' --conv1d 'False'
python processing.py '/home/cchen/autoencode_output/' 'ready_array2.npz' --name '/home/cchen/MS2-Autoencoder/big_data_conv1d.hdf5' --conv1d 'True'