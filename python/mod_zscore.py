# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:31:43 2020

@author: DANCEL
"""
########################## Modified Z-Score ##########################
import pandas as pd
import numpy as np
import random
from tqdm import tqdm

taille = pd.read_csv('../data/age_interval/all_data.csv')
taille = taille[taille['Appli'] == 'DOS']


def outliers_modified_z_score(ys):
    threshold = 3.5

    median_y = np.median(ys)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in ys])
    modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y
                         for y in ys]
    return np.where(np.abs(modified_z_scores) > threshold)


ipprs = np.array(taille.IPPR.unique())
# systemRandom = random.SystemRandom()
# rint = systemRandom.randint(1,13904)
# ippr = ipprs[rint]


z = 0*13904
taille['otl_index'] = z

otls = []
for i in tqdm(ipprs):
    
    data = taille[taille['IPPR']== i]
    data = np.array(data.Taille)
        
    otl = outliers_modified_z_score(data)
    
    [otls.append(x) for x in otl]

# otls = outliers_modified_z_score(taille)