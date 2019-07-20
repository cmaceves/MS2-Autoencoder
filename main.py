import extract_mzxml as em
import time

start_time = time.time()

file = 'cholesterol.mzxml'
data = em.read_data(file)
em.count_MS2(data)
id_list_ms2 = em.find_MS2(data)
#rt_list_ms2 = em.list_retentionTime_MS2(data, id_list_ms2)
pair_dict = em.search_MS2_pairs2(data, id_list_ms2)

import csv
w = csv.writer(open('pair_dict3.csv', 'w'))
for k, v in pair_dict.items():
    w.writerow([k, v])

import json
json = json.dumps(pair_dict)
with open('pair_dict3.json', 'w') as output:
    output.write(json)

with open('pair_dict3.txt', 'w') as output:
    output.write(str(pair_dict))

print('--- %s runtime ---' %(str(time.time() - start_time)))
print('operations complete')