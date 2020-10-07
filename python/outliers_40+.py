# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 09:49:25 2020

@author: LOX
"""
import pandas as pd 
import numpy as np
from tqdm import tqdm

data = pd.read_csv('../data/age_interval/all_data.csv')

by_ippr = data.groupby('IPPR', sort=False)
sup40 = by_ippr['age_at_entry'].min() > 18250
sup40 = sup40[sup40 == True]
idx = np.array(sup40.index)

data40 = data[data['IPPR'].isin(idx)]

evo10ans = 1
evo1ans = evo10ans / 10
evo1jour = evo1ans / 365

def isDescending(df):
    arr = np.array(df)
    previous = arr[0]
    for item in arr:
        if item > previous:
            return False
        previous = item
    return True
        
def ippr_isDescending(ippr):
    df = data40[data40['IPPR'] == ippr]
    desc = isDescending(df['Taille'])
    return ippr, desc

desc_list = []
for index, ippr in tqdm(enumerate(idx)):
    desc_list.append(ippr_isDescending(ippr))
    
desc_True = [x for x in desc_list if x[1] == True]
desc_False = [x for x in desc_list if x[1] == False]

def test_evo():
    for ippr in idx[15966:15991]:
        
        df = data40[data40['IPPR'] == ippr]
        df =  df.iloc[:,[1,4,12]]
        
        if len(df) > 1 and isDescending(df['Taille']):        
            print('='*40, 'IPPR: {} (len(df)={})'.format(ippr,len(df)))
            for i in range(1, len(df)): 
                imoins = i-1
                
                duree = df.iloc[i,0] - df.iloc[imoins,0]
                deltaT = df.iloc[i,1] - df.iloc[imoins,1]
                deltaOK = duree*evo1jour

                if deltaT != 0 and abs(deltaT) <= deltaOK:
                    OK = True
                else:
                    OK = False
                
                taille = df.iloc[i,1]
                lvl = df.iloc[i,2]
                
                print('{}> age: {}, duree: {}, taille: {}, deltaOK: {}, OK: {}, lvl: {}'.format(i, df.iloc[i,0], duree, df.iloc[i,1], deltaOK, OK, df.iloc[i,2]))
                
# test_evo()