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

def bin_MS2(data, id_list_ms2):
    """
    create bins of data based on retentionTime param
    """
    rt_bin = 30.0

def search_MS2_pairs(data, id_list_ms2):
    """
    search for same molecules in MS2 scans
    same molecules are based on mass ('precursorMz') with a tolerance (mass_tolerance)
    same molecules are found within a bin of retentionTime (rt_tolerance)
    generates a dictionary of scan indexes mapped to a list of matching scan indexes
    outputs a .txt and .json file for review
    """
    print('Beginning the search')
    pair_dict = {} #key is integer from id_list_m2; value is list of integers from id_list_ms2
    rt_tolerance = 30.0 #retentionTime tolerance for half a minute
    mass_tolerance = 0.01 #mass tolerance for 0.01mZ

    for k in id_list_ms2:
        rt_save = float(data[k].get('retentionTime'))
        mass_save = float(data[k].get('precursorMz')[0].get('precursorMz'))
        v_list = []
        redun_check = False #initialize redundancy check boolean as not-redundant

        for value in pair_dict.values():
            for index in range(0, len(value)):
                if k == value[index]:
                    redun_check = True              

        if redun_check != True:
            for v in id_list_ms2:
                if v != k:
                    rt_dv = data[v].get('retentionTime')
                    if rt_dv <= rt_save + rt_tolerance and rt_dv >= rt_save - rt_tolerance:
                        mass_dv = data[v].get('precursorMz')[0].get('precursorMz')
                        if mass_dv <= mass_save + mass_tolerance and mass_dv >= mass_save - mass_tolerance:
                            v_list.append(v)
                            print('Found a match: %s:%r' %(k, v))
                pair_dict[k] = v_list
            print(k, pair_dict[k])
            print('Finished search for dict[%s]' %k)
            redun_check = False #reset redundancy check boolean
        else:
            redun_check = False #reset redundancy check boolean 
    
    return pair_dict

def output_search_dict(pair_dict, directory):
    """
    output the dictionary from search_MS2_pairs into files
    outputs .txt and .json
    """
    import json
    json = json.dumps(pair_dict)
    filename = directory + '/pair_dict.json'
    with open(filename, 'w') as output:
        output.write(json)
    print('saved pair_dict to "pair_dict.json"')

    filename = directory + '/pair_dict.txt'
    with open(filename, 'w') as output:
        output.write(str(pair_dict))
    print('saved pair_dict to "pair_dict.txt"')