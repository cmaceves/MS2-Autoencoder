import os
import numpy as np
import h5py

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

#stitch all data, concatenate, save to compressed
def stitch_npz(file_list):
    data_list = []
    for filename in file_list:
        print('extracting and appending %s' %filename)
        data = extract_npz(filename)
        data_list.append(data)

    big_data = np.concatenate(data_list, axis=0)
    print(big_data.shape)

    np.savez_compressed('concated_data', big_data)

#hdf5 stitching
def stitch_hdf5(file_list):
    #create and initialize empty hdf5 dataset
    with h5py.File('large_split_data.hdf5', 'w') as f:
        dataset = f.create_dataset('low_peaks', shape=(1,1,2000), 
                                    maxshape=(None, 1, 2000))
        dataset = f.create_dataset('high_peaks', shape=(1,1,2000), 
                                    maxshape=(None, 1, 2000))
        f.close()

    i_prev = 0
    len_total = 0
    for filename in file_list:
        print('extracting and appending %s' %filename)
        data = extract_npz(filename)
        size = data.shape
        i_curr = size[0] + i_prev
        len_total += i_curr

        split_data = np.split(data, 2, axis=1)
        low_peaks = split_data[0]
        high_peaks = split_data[1]

        with h5py.File('large_split_data.hdf5', 'a') as f:
            dataset = f['low_peaks']
            dataset.resize((len_total, 1, 2000))
            dataset[i_prev:i_curr, :, :] = low_peaks

            dataset = f['high_peaks']
            dataset.resize((len_total, 1, 2000))
            dataset[i_prev:i_curr, :, :] = high_peaks

            f.close()
        i_prev = i_curr
    print('saved all data to large_data.hdf5')

stitch_hdf5(file_list)

'''
#save low peaks and high peaks to datasets inside one hdf5 file
new_list = np.split(big_data, 2, axis =1)
low_peaks = new_list[0]
low_peaks = low_peaks.astype('float32')
high_peaks = new_list[1]
high_peaks = high_peaks.astype('float32')
'''