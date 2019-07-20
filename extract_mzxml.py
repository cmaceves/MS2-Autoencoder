from pyteomics import mzxml, auxiliary

def read_data(file):
    data = mzxml.MzXML(file)
    print(str(file), 'has been accepted')

    return data

def count_MS2(data):
    tot_ms2 = 0
    tot_ms1 = 0

    for i in range(0, len(data)):
        for k,v in data[i].items():
            if k == 'msLevel':
                if v == 2:
                    tot_ms2 += 1
                else:
                    tot_ms1 += 1
    print('Total %s scans in data' %(str(len(data))))
    print('Count %s MS2 scans in data' %(str(tot_ms2)))

def find_MS2(data, directory):
    id_list_ms1 = []
    id_list_ms2 = []
    
    for i in range(0, len(data)):
        if data[i].get('msLevel') == 2:
            id_list_ms2.append(i) #int
        elif data[i].get('msLevel') == 1:
            id_list_ms1.append(i) #int
        else:
            print('msLevel error: could not sort dict[%s] msLevel' %(str(i)))

        filename1 = directory + '/id_list_ms1.txt'
        filename2 = directory + '/id_list_ms2.txt'
        with open(filename1, 'w') as output:
            output.write(str(id_list_ms1)) #str in txt files for user review
        with open(filename2, 'w') as output:
            output.write(str(id_list_ms2)) #str in txt files for user review
    print('Generated list of indexes containing MS2 scans to "id_list_ms2.txt"')

    return id_list_ms2

def list_retentionTime_MS2(data, id_list_ms2):
    rt_list_ms2 = []

    for i in id_list_ms2:
        rt_list_ms2.append(data[i].get('retentionTime')) #syntax for accessing one particular key of one particular dictionary in the mzxml file

    return rt_list_ms2

def bin_MS2(data, id_list_ms2):
    rt_bin = 30.0



def cast_id_int(id_list_ms2):
    id_list = []

    for num in id_list_ms2:
        id_list.append(int(num))

def search_MS2_pairs(data, id_list_ms2):
    print('Beginning the search')
    pair_dict = {}
    rt_tolerance = 30.0
    mass_tolerance = 0.1

    for i in id_list_ms2:
        rt_save = float(data[i].get('retentionTime'))
        mass_save = float(data[i].get('precursorMz')[0].get('precursorMz'))
        ce_save = float(data[i].get('collisionEnergy'))
        for n in id_list_ms2:
            if n > i:
                rt_dn = data[n].get('retentionTime')
                if rt_dn <= rt_save + rt_tolerance and rt_dn >= rt_save - rt_tolerance: #upperbound and lowerbound
                    mass_dn = data[n].get('precursorMz')[0].get('precursorMz')
                    if mass_dn <= mass_save + mass_tolerance and mass_dn >= mass_save - mass_tolerance:
                        ce_dn = data[n].get('collisionEnergy')
                        if ce_dn == ce_save:
                            pair_dict[i] = n
                            print('Found a match: ', i, ':', n)
        print('finished search for dict[', i, ']')
    return pair_dict

def search_MS2_pairs2(data, id_list_ms2):
    print('Beginning the search')
    pair_dict = {}
    rt_tolerance = 30.0
    mass_tolerance = 0.1

    for k in id_list_ms2:
        if k not in pair_dict.values():
            rt_save = float(data[k].get('retentionTime'))
            mass_save = float(data[k].get('precursorMz')[0].get('precursorMz'))
            
            for v in id_list_ms2:
                v_list = []
                if v != k:
                    rt_dv = data[v].get('retentionTime')
                    if rt_dv <= rt_save + rt_tolerance and rt_dv >= rt_save - rt_tolerance:
                        mass_dv = data[v].get('precursorMz')[0].get('precursorMz')
                        if mass_dv <= mass_save + mass_tolerance and mass_dv >= mass_save - mass_tolerance:
                            v_list.append(v)
                            print('Found a match: %s:%r' %(str(k), str(v)))
                pair_dict[k] = v_list
                print(pair_dict[k].items())
            print('Finished search for dict[%s]' %(str(k)))
    
    return pair_dict