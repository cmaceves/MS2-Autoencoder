from pyteomics import mzxml, auxiliary
import numpy as np

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

def search_MS2_matches(data, id_list_ms2, rt_tol=0.5, mz_tol=0.01):
    """
    search for same molecules in MS2 scans
    same molecules are based on mass ('precursorMz') with a tolerance (mass_tolerance)
    same molecules are found within a bin of retentionTime (rt_tolerance)
    generates a dictionary of scan IDs mapped to a list of matching scan indexes
    outputs a .txt and .json file for review
    """
    print('Beginning the search')
    match_index_dict = {} #key is integer from id_list_m2; value is list of integers from id_list_ms2
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

        for value in match_index_dict.values():
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
                match_index_dict[id_save] = v_list
            print(id_save, match_index_dict[id_save])
            print('Finished search for dict[%s]' %k)
            redun_check = False #reset redundancy check boolean
        else:
            redun_check = False #reset redundancy check boolean 
    return match_index_dict

def get_match_scans(data, match_index_dict):
    """
    collect the information from the data for the matching molecules
    hierarchical dictionary
    """
    processed_dict = {}
    for key in match_index_dict.keys():
        processed_dict[int(key)] = []
        for index, i in zip(match_index_dict[key], range(0, len(match_index_dict[key]))):
            scan = int(data[index].get('id'))
            rt = data[index].get('retentionTime')
            intensity = data[index].get('precursorMz')[0].get('precursorIntensity')
            mz = data[index].get('precursorMz')[0].get('precursorMz')
            mz_array = data[index].get('m/z array').tolist()
            intensity_array = data[index].get('intensity array').tolist()
            
            processed_dict[int(key)].append({scan:{}})
            processed_dict[int(key)][i][scan] = {'retentionTime':rt, #retentionTime
                                                'precursorMz':mz, #precursorMz
                                                'precursorIntensity':intensity, #precursorIntensity
                                                'mz array':mz_array, #mz array 
                                                'intensity array':intensity_array} #intensity array
    return processed_dict

def bin_array(processed_dict):
    """
    bin and zip mz array and intensity array
    mz values are binned
    intensity values are summed within the bin
    returns dictionary with binned and zipped array
    """
    from scipy.stats import binned_statistic

    binned_dict = {}
    for key in processed_dict.keys():
        binned_dict[key] = []
        for i in range(0, len(processed_dict[key])):
            for scan in processed_dict[key][i]:
                mz_array = processed_dict[key][i][scan].get('mz array')
                intensity_array = processed_dict[key][i][scan].get('intensity array')
                binned_intensity, binned_mz, bin_index = binned_statistic(mz_array, intensity_array, statistic='sum', bins=2000, range=range(0, 2000)) #bins are integers range(0,2000)
                

                rt = processed_dict[key][i][scan].get('retentionTime')
                mz = processed_dict[key][i][scan].get('precursorMz')
                intensity = processed_dict[key][i][scan].get('precursorIntensity')
                mz_intensity_array = list(zip(binned_mz, binned_intensity)) #zip binned mz array and binned intensity array

                binned_dict[key].append({scan:{}})
                binned_dict[key][i][scan] = {'retentionTime':rt, #retentionTime
                                            'precursorMz':mz, #precursorMz
                                            'precursorIntensity':intensity, #precursorIntensity
                                            'mz_intensity array':mz_intensity_array} #intensity array
    return binned_dict

def create_pairs(binned_dict):
    """
    creates pairs of scans from dict of matched scans
    number of pairs per same molecule is n(n+1)/2 where n is number of scans
    returns dictionary with paired scans
    """
    pairs_dict = {}
    return pairs_dict

def find_max_min(pairs_dict):
    """
    find the maximum and minimum precursorIntensity scans for each pair
    rearrange pair according to minimum scan then maximum scan
    input is a dict
    """
    simple_dict = {}
    for mol in pairs_dict.keys():
        lst_dict = {}
        for index in range(0, len(pairs_dict[mol])):
            for scan in pairs_dict[mol][index].keys():
                lst_dict[index] = pairs_dict[mol][index][scan].get('precursorIntensity')
                if scan == mol:
                    self_scan = pairs_dict[mol][index]
        max_scan = [key for key, val in lst_dict.items() if val == max(lst_dict.values())]
        min_scan = [key for key, val in lst_dict.items() if val == min(lst_dict.values())]

        simple_dict[mol] = [self_scan, pairs_dict[mol][min_scan[0]], pairs_dict[mol][max_scan[0]]] #[self, min, max]
    return simple_dict

def convert_to_list(simple_dict):
    """
    converts simple_dict into a list of structured arrays
    """
    mol_list = []
    pair_list = []
    for mol in simple_dict.keys():
        self_list = []
        match_list = []
        for key in simple_dict[mol][0].keys():
            scan = key
            rt = simple_dict[mol][0][key].get('retentionTime')
            intensity = simple_dict[mol][0][key].get('precursorIntensity')
            mz = simple_dict[mol][0][key].get('precursorMz')
            mz_intensity_array = simple_dict[mol][0][key].get('mz_intensity_array')

            self_array = np.array([(scan, rt, mz, intensity, mz_intensity_array)],
                                    dtype=[('id', 'S10'), ('rt', 'f8'), ('mz', 'f8'), ('intensity', 'f8'), ('mz_intensity_array', zip, len(mz_intensity_array))])
            self_list.append(self_array)

        for index in range(1, len(simple_dict[mol])):
            for key in simple_dict[mol][index].keys():
                scan = key
                rt = simple_dict[mol][index][key].get('retentionTime')
                intensity = simple_dict[mol][index][key].get('precursorIntensity')
                mz = simple_dict[mol][index][key].get('precursorMz')
                mz_intensity_array = simple_dict[mol][index][key].get('mz_intensity_array')
                
                scan_array = np.array([(scan, rt, mz, intensity, mz_intensity_array)],
                                        dtype=[('id', 'S10'), ('rt', 'f8'), ('mz', 'f8'), ('intensity', 'f8'), ('mz_intensity_array', zip, len(mz_intensity_array.shape))])
                match_list.append(scan_array)
        mol_list.append(self_list)
        pair_list.append(match_list)
        simple_list = [mol_list, pair_list]
    return simple_list

def output_dict(in_dict, directory, pair=None, scans=None, simple=None):    
    """
    output the dictionary from search_MS2_pairs, get_pair_scans, find_max_min into files
    outputs .txt and .json
    """
    import json

    if pair == True:
        json = json.dumps(in_dict)
        filename = directory + '/pair_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved pair_dict to %s' %filename)

    elif scans == True:
        json = json.dumps(in_dict)
        filename = directory + '/processed_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved processed_dict to %s' %filename)

    elif simple == True:
        json = json.dumps(in_dict)
        filename = directory + '/simple_dict.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved simple_dict to %s' %filename)

    else:
        json = json.dumps(in_dict)
        filename = directory + '/output.json'
        with open(filename, 'w') as output:
            output.write(json)
        print('saved dict to "output.json"')

def output_list(in_list, directory, scans=None, simple=None):
    import numpy as np

    if scans == True:
        filename = directory + '/scan_list.txt'
        np.savetxt(filename, in_list, fmt='%s')

        filename = directory + '/scan_list.npy'
        np.save(filename, in_list)

    elif simple == True:
        '''
        filename = directory + '/simple_list.txt'
        np.savetxt(filename, in_list, fmt='%s')
        '''
        filename = directory + '/simple_list.npy'
        np.save(filename, in_list)

def unpack(input_dict):
    """
    unpack a dictionary that has be save in a .json file
    """
    import json
    with open(input_dict) as f:
        out_dict = json.load(f)
    return out_dict