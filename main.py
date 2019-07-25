import extract_mzxml as em
import time

start_time = time.time()

file = 'cholesterol.mzxml'
pair_dict_file = 'C:/Users/CCheny/OneDrive/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output/cholesterol/pair_dict.json'
#directory = 'C:/Users/CCheny/Documents/UC San Diego/Bioinformatics/MS2-Autoencoder/Output/cholesterol' 
directory = 'C:/Users/CCheny/OneDrive/UC San Diego - Junction/Bioinformatics/MS2-Autoencoder/Output/cholesterol'

data = em.read_data(file)
em.count_MS2(data)
id_list_ms2 = em.find_MS2(data, directory)
pair_dict = em.search_MS2_pairs(data, id_list_ms2)
em.output_search_dict(pair_dict, directory, pair=True)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
#pair_dict = em.unpack(pair_dict_file)
processed_dict = em.get_pair_scans(data, pair_dict)
print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
em.output_search_dict(processed_dict, directory, scans=True)
print('operations complete')