import os
import argparse
import concat_hdf5 as ch5

parser = argparse.ArgumentParser()
parser.add_argument('data_path', help='path to the data being concatenated')
parser.add_argument('data_name', help='name of the data file being concatenated')
parser.add_argument('--norm', default='l2', help='the norm to use to normalize data')

args = parser.parse_args()
path = args.data_path
data_name = args.data_name
norm = args.norm

#'/home/cchen/autoencode_output/'
#'C:/Users/CCheny/Documents/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output'
file_list = []
for i in os.listdir(path):
    for filename in os.listdir(os.path.join(path, i)):
        if filename == data_name:
            file_list.append(os.path.join(path, i, filename))
            print(os.path.join(path, i, filename))

ch5.stitch_hdf5(file_list, norm=norm)