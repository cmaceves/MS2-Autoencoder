import extract_mzxml as em
import time

start_time = time.time()

file = 'HNP.mzxml'
directory = 'C:/Users/CCheny/Documents/UC San Diego/Bioinformatics/MS2-Autoencoder/Output/HNP'

data = em.read_data(file)
em.count_MS2(data)
id_list_ms2 = em.find_MS2(data, directory)
pair_dict = em.search_MS2_pairs(data, id_list_ms2)
em.output_search_dict(pair_dict, directory)

print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
print('operations complete')