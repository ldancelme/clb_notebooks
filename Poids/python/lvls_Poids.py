# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:29:07 2020

@author: LOX
"""
import pandas as pd
import numpy as np
from tqdm import tqdm

data = pd.read_csv('../data/all_data.csv')
applis = data.Appli.unique()

lvl1 = ['DOS', 'BLO']
lvl2 = ['DOS', 'BLO', 'CRC']
lvl3 = ['DOS', 'BLO', 'CRC', 'CRS']
lvl4 = applis

zeros = 0* len(data)
data["priority_lvl"] = zeros

def test_lvl(i): 
    x = 0
    if i in lvl1:
        x = 1
    elif i in lvl2:
        x = 2
    elif i in lvl3:
        x = 3
    elif i in lvl4:
        x = 4
    return x
           
for idx, val in tqdm(enumerate(data.values)):
    x = test_lvl(val[4])
    data.iloc[idx,8] = x
    print('Appli : {}\t priority_lvl:{}'.format(data.iloc[idx, 4], data.iloc[idx, 8]))

# data.to_csv('../data/all_data.csv', index=False)
