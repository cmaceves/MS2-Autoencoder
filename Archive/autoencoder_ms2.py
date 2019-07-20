
#open mzXML file
from simple_load_mzXML import load_mzxml_file
import xmltodict
import pandas as pd

file = 'Cholesterol_130uM_GB1_01_6914.mzXML'

with open(file) as fd:
    mzxml = xmltodict.parse(fd.read())
df = pd.DataFrame.from_dict(mzxml)
items = list(mzxml.items())
print(items[0][1])

'''
mzXML_list = load_mzxml_file(file)

#autoencoder
from keras.layers import Input, Dense
from keras.models import Model
from keras import backend as K

encoding_dim = 
'''