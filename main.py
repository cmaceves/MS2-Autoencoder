import extract_mzxml as em
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('data_file', help='data')
parser.add_argument('directory', help='directory for output files')
parser.add_argument('--match_index_file', action='store')
parser.add_argument('--processed_dict_file', action='store')
parser.add_argument('--binned_dict_file', action='store')
parser.add_argument('--pairs_dict_file', action='store')

args = parser.parse_args()
file = args.data_file
directory = args.directory
match_index_file = args.match_index_file
processed_dict_file = args.processed_dict_file
binned_dict_file = args.binned_dict_file
pairs_dict_file = args.pairs_dict_file

start_time = time.time()

data = em.read_data(file)

if args.binned_dict_file: # tests the create_pairs() function
    binned_dict = em.unpack(binned_dict_file)
    pairs_dict = em.create_pairs(binned_dict)
    em.output_dict(pairs_dict, directory, pairs=True)
    print('operations complete')

elif args.processed_dict_file: #tests the bin_array() function
    processed_dict = em.unpack(processed_dict_file)
    binned_dict = em.bin_array(processed_dict)
    print('--- %s seconds runtime --- ' %(str(time.time() - start_time)))
    em.output_dict(binned_dict, directory, binned=True)
    print('operations complete')

elif args.match_index_file: #tests the get_match_scans() function
    match_index_dict = em.unpack(match_index_file)
    processed_dict = em.get_match_scans(data, match_index_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_dict(processed_dict, directory, processed=True)
    print('operations complete')

else: #complete run through
    em.count_MS2(data)
    id_list_ms2 = em.find_MS2(data, directory)
    match_index_dict = em.search_MS2_matches(data, id_list_ms2)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_dict(match_index_dict, directory, match_index=True)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    processed_dict = em.get_match_scans(data, match_index_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_dict(processed_dict, directory, processed=True)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    binned_dict = em.bin_array(processed_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_dict(binned_dict, directory, binned=True)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    print('operations complete')