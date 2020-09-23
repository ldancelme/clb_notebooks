# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:09:20 2020

@author: DANCEL
"""

# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit
from tqdm import tqdm 

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
# //// Load file
data = pd.read_csv('data/age_interval/all_data.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

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
    x = test_lvl(val[5])
    data.iloc[idx,12] = x
    print('Appli : {}\t priority_lvl:{}'.format(data.iloc[idx, 5], data.iloc[idx, 12]))

# data.to_csv('data/age_interval/all_data.csv', index=False)

# -----------------------------------------------------------------------------
# Temps d'exec pour 447754 lignes = ~50 min
#
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
