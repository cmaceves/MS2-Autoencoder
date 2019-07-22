import extract_mzxml as em
import time

start_time = time.time()

file = 'cholesterol.mzxml'
directory = 'C:/Users/CCheny/OneDrive/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output/cholesterol'

data = em.read_data(file)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
em.count_MS2(data)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
id_list_ms2 = em.find_MS2(data, directory)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
pair_dict = em.search_MS2_pairs(data, id_list_ms2)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
em.output_search_dict(pair_dict, directory)

print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
print('operations complete')