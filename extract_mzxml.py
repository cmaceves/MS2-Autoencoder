from pyteomics import mzxml, auxiliary

def read_data(file):
    """
    read mzxml file using pyteomics.mzxml
    """
    data = mzxml.MzXML(file)
    print(str(file), 'has been accepted')

    return data

def count_MS2(data):
    """
    count total number scans and MS2 scans in the data
    """
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
    """
    find MS2 scans from the data
    output to a list of indexes of MS2 scans
    """
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
    """
    list retentionTime for MS2 scans
    used to demonstrate syntax of accessing elements in the parsed mxzml
    """
    rt_list_ms2 = []

    for i in id_list_ms2:
        rt_list_ms2.append(data[i].get('retentionTime')) #syntax for accessing one particular key of one particular dictionary in the mzxml file

    return rt_list_ms2

def search_MS2_pairs(data, id_list_ms2, rt_tol=0.5, mz_tol=0.01):
    """
    search for same molecules in MS2 scans
    same molecules are based on mass ('precursorMz') with a tolerance (mass_tolerance)
    same molecules are found within a bin of retentionTime (rt_tolerance)
    generates a dictionary of scan indexes mapped to a list of matching scan indexes
    outputs a .txt and .json file for review
    """
    print('Beginning the search')
    pair_dict = {} #key is integer from id_list_m2; value is list of integers from id_list_ms2
    rt_tolerance = rt_tol #retentionTime tolerance for half a minute
    mass_tolerance = mz_tol #mass tolerance for 0.01mZ
    intensity_tolerance_low = 2 #greater than 2x precursorIntensity from base molecule
    intensity_tolerance_up = 5 #less than 5x precursorIntensity from base molecule

    for k in id_list_ms2:
        rt_save = float(data[k].get('retentionTime'))
        mass_save = float(data[k].get('precursorMz')[0].get('precursorMz'))
        intensity_save = float(data[k].get('precursorMz')[0].get('precursorIntensity'))
        id_save = int(data[k].get('id'))
        v_list = []
        redun_check = False #initialize redundancy check boolean as not-redundant

        for value in pair_dict.values():
            for index in range(0, len(value)):
                if k == value[index]:
                    redun_check = True              

        if redun_check != True:
            for v in id_list_ms2:
                rt_dv = data[v].get('retentionTime')
                if rt_dv <= rt_save + rt_tolerance and rt_dv >= rt_save - rt_tolerance:
                    mass_dv = data[v].get('precursorMz')[0].get('precursorMz')
                    if mass_dv <= mass_save + mass_tolerance and mass_dv >= mass_save - mass_tolerance:
                        intensity_dv = data[v].get('precursorMz')[0].get('precursorIntensity')
                        if intensity_dv <= intensity_save * intensity_tolerance_up and intensity_dv >= intensity_tolerance_low:
                            v_list.append(v)
                            print('Found a match: %s:%r' %(k, v))
                pair_dict[id_save] = v_list
            print(id_save, pair_dict[id_save])
            print('Finished search for dict[%s]' %k)
            redun_check = False #reset redundancy check boolean
        else:
            redun_check = False #reset redundancy check boolean 
    
    return pair_dict

def output_search_dict(in_dict, directory, pair=None, scans=None, simple=None):
    """
    output the dictionary from search_MS2_pairs and/or get_pair_scans into files
    outputs .txt and .json
    """
    import json

    if pair == True:
        json = json.dumps(in_dict)
        filename = directory + '/pair_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved pair_dict to "pair_dict.json"')

        filename = directory + '/pair_dict.txt'
        with open(filename, 'w') as output:
            output.write(str(in_dict))
        print('saved pair_dict to "pair_dict.txt"')
    elif scans == True:
        json = json.dumps(in_dict)
        filename = directory + '/scan_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved scan_dict to "scan_dict.json"')

        filename = directory + '/scan_dict.txt'
        with open(filename, 'w') as output:
            output.write(str(in_dict))
        print('saved scan_dict to "scan_dict.txt"')
    elif simple == True:
        json = json.dumps(in_dict)
        filename = directory + '/simple_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved scan_dict to "simple_dict.json"')

        filename = directory + '/simple_dict.txt'
        with open(filename, 'w') as output:
            output.write(str(in_dict))
        print('saved scan_dict to "simple_dict.txt"')
    else:
        json = json.dumps(in_dict)
        filename = directory + '/output.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved scan_dict to "output.json"')

        filename = directory + '/output.txt'
        with open(filename, 'w') as output:
            output.write(str(in_dict))
        print('saved scan_dict to "output.txt"') 

def get_pair_scans(data, pair_dict):
    """
    collect the information from the data for the matching molecules
    """
    processed_dict = {}
    for key in pair_dict.keys():
        processed_dict[key] = []
        for index, i in zip(pair_dict[key], range(0, len(pair_dict[key]))):
            scan = data[index].get('id')
            rt = data[index].get('retentionTime')
            intensity = data[index].get('precursorMz')[0].get('precursorIntensity')
            mz = data[index].get('precursorMz')[0].get('precursorMz')
            mz_array = data[index].get('m/z array').tolist()
            intensity_array = data[index].get('intensity array').tolist()
            
            processed_dict[key].append({scan:{}})
            processed_dict[key][i][scan] = {'retentionTime':rt,
                                            'precursorMz':mz,
                                            'precursorIntensity':intensity,
                                            'm/z array':mz_array,
                                            'intensity array':intensity_array}
    
    return processed_dict

def find_max_min(scan_dict):
    """
    find the maximum and minimum precursorIntensity scans for each molecule
    """
    simple_dict = {}
    for mol in scan_dict.keys():
        lst_dict = {}
        for index in range(0, len(scan_dict[mol])):
            for scan in scan_dict[mol][index].keys():
                lst_dict[index] = scan_dict[mol][index][scan].get('precursorIntensity')
                if scan == mol:
                    self_scan = scan_dict[mol][index]
        max_scan = [key for key, val in lst_dict.items() if val == max(lst_dict.values())]
        min_scan = [key for key, val in lst_dict.items() if val == min(lst_dict.values())]

        simple_dict[mol] = [self_scan, scan_dict[mol][min_scan[0]], scan_dict[mol][max_scan[0]]] #[self, min, max]
    return simple_dict

def unpack(input_dict):
    """
    unpack a dictionary that has be save in a .json file
    """
    import json
    with open(input_dict) as f:
        out_dict = json.load(f)

    return out_dict