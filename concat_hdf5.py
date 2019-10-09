import os
import numpy as np
import h5py

def extract_npz(filename):
    file = np.load(filename, allow_pickle=True)
    data = file['arr_0']
    return data

def normalize_peaks(peaks_array, norm):
    """
    normalizes each array by dividing the array by the max of that array
    """
    from sklearn.preprocessing import normalize

    for i in range(0, len(peaks_array)):
        peaks_array[i] = normalize(peaks_array[i], norm=norm)
    return peaks_array

def split_reshape(data, norm):
    split_data = np.split(data, 2, axis=1)
    low_peaks = split_data[0]
    low_peaks = normalize_peaks(low_peaks, norm) #normalize
    low_peaks = low_peaks.reshape(len(low_peaks), np.prod(low_peaks.shape[1:]))
    high_peaks = split_data[1]
    high_peaks = normalize_peaks(high_peaks, norm) #normalize
    high_peaks = high_peaks.reshape(len(high_peaks), np.prod(high_peaks.shape[1:]))
    return low_peaks, high_peaks

#stitch all data, concatenate, save to compressed
def stitch_npz(file_list):
    data_list = []
    for filename in file_list:
        print('extracting and appending %s' %filename)
        data = extract_npz(filename)
        data_list.append(data)

    big_data = np.concatenate(data_list, axis=0) #concatenate here is going to take the most RAM
    print(big_data.shape)

    np.savez_compressed('concated_data', big_data)

#hdf5 stitching
def stitch_hdf5(file_list, norm):
    """
    concatenate data into hdf5 format for reading from disk
    outputs one hdf5 file with two datasets
    data in datasets will be normalized
    """
    with h5py.File('chemical_split_data.hdf5', 'w') as f: #create empty hdf5 file with two datasets
        dataset = f.create_dataset('low_peaks', shape=(1,2000), maxshape=(None, 2000))
        dataset = f.create_dataset('high_peaks', shape=(1,2000), maxshape=(None, 2000))
        f.close()

    i_prev = 0
    len_total = 0
    for filename in file_list:
        print('extracting and appending %s to hdf5' %filename)
        data = extract_npz(filename)
        size = data.shape
        i_curr = size[0] + i_prev
        len_total += i_curr

        low_peaks, high_peaks = split_reshape(data, norm)

        with h5py.File('chemical_split_data.hdf5', 'a') as f:
            dataset = f['low_peaks'] #append to low_peaks dataset
            dataset.resize((len_total, 2000))
            dataset[i_prev:i_curr, :] = low_peaks

            dataset = f['high_peaks'] #append to high_peaks dataset
            dataset.resize((len_total, 2000))
            dataset[i_prev:i_curr, :] = high_peaks

            f.close()
        i_prev = i_curr
    print('saved all data to chemical_split_data.hdf5')