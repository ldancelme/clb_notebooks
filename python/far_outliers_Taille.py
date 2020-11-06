# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:39:24 2020

@author: DANCEL
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

taille = pd.read_csv('../data/age_interval/all_data.csv')

taille = taille[taille['Appli'] == 'DOS']
ipprs = taille.IPPR.unique()

def limit_test(x, mean, liminf, limsup):
    if x > np.round(limsup,2):
        return 1
    elif x < np.round(liminf,2):
        return 1
    return 0
    

z = 0*125046
taille['otl'] = z

otls = []
for i in tqdm(ipprs):
    data = taille[taille['IPPR'] == i]
    tai = np.array(data['Taille'])
    mean = np.array(data["mean"])[0]
    std = np.array(data["std"])[0]
    liminf = mean - std*1
    limsup = mean + std*1
    otl = [limit_test(x,mean,liminf, limsup) for x in tai]
    [otls.append(x) for x in otl]



# def far_outliers(ipprs, k):
     
    # print('data : ', data)
    # print('tai\t', tai)
    # print('Appli : ', np.array(data['Appli']))
    # print('liminf\t', liminf)
    # print('limsup\t', limsup)
    # print('mean\t', mean)
    # print('std\t', std)
    # print('otl\t', otl)
    
# far_outliers(ipprs, 1)