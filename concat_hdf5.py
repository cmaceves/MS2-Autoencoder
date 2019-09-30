import os
import numpy as np
#import h5py

path = '/home/cchen/autoencode_output/'
file_list = []
for i in os.listdir(path):
    for filename in os.listdir(os.path.join(path, i)):
        if filename == 'ready_array2.npz':
            file_list.append(os.path.join(path, i, filename))
            print(os.path.join(path, i, filename))

def extract_npz(filename):
    file = np.load(filename, allow_pickle=True)
    data = file['arr_0']
    return data

data_list = []
for filename in file_list:
    print('extracting and appending %s' %filename)
    data = extract_npz(filename)
    data_list.append(data)

big_data = np.concatenate(data_list, axis=0)
print(big_data.shape)

np.savez_compressed('concated_data', big_data)