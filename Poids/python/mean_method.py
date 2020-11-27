# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:31:44 2020

@author: DANCEL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import warnings
warnings. filterwarnings('ignore')

txt_out = open("output2.txt","a") 

data = pd.read_csv('../data/all_data.csv')
data_otls = pd.read_csv('../data/otls_555_ipprs.csv')
ipprs_otls = np.array(data_otls.IPPR.unique())

data = data[data['age_at_entry'] > 7300]
ipprs = data.IPPR.unique()
# ipprs = np.array(ipprs)

# ipprs = [x for x in ipprs if x not in ipprs_otls]
# ipprs = random.choices(ipprs, k=5)
# data = data[data['IPPR'].isin(ipprs)]


def mean_next_x_months(temp, idx, months):
    period = months*31
    # print('Period :', period)
    val = {}
    di = temp.iloc[idx,1]
    # print('age_at_entry :', di)
    temp = temp.iloc[idx+1:,:]
    for j in range(len(temp)):
        # print('temp.iloc[j,1] :', temp.iloc[j,1])
        # print('di :', di)
        # print('temp.iloc[j,1] - di :', temp.iloc[j,1] - di)
        if temp.iloc[j,1] - di <= period :
            val.update({temp.iloc[j,1]:temp.iloc[j,3]})
    # print(val)
    txt_out.write('\t\t///// val : {}\n'.format(val))
    
    m = np.array(list(val.values())).mean()
    d = np.array(list(val.keys())).mean()
    p= [d,m]
    return p

def mean_last_x_months(temp, idx, months):
    period = months*31
    # print('Period :', period)
    val = {}
    di = temp.iloc[idx,1]
    # print('age_at_entry :', di)
    new_temp = temp.iloc[:idx-1,:]
    for j in range(len(new_temp)):
        if di - period > min(temp.iloc[:,1]):
           if new_temp.iloc[j,1] >= di-period:
                val.update({new_temp.iloc[j,1]:new_temp.iloc[j,3]})
    # print('val:', val)
    txt_out.write('\t\t///// val : {}\n'.format(val))
    m = np.array(list(val.values())).mean()
    d = np.array(list(val.keys())).mean()
    p= [d,m]
    return p

otls = []
def otl_hugo_crochet(ipprs, months):
    prc  = 0.1
    for idx, ippr in enumerate(ipprs):
        txt_out.write('['+str(idx)+']'+'['+str(ippr)+'] '+'-'*90+'\n')
        d = data[data['IPPR'] == ippr]
        x = np.array(d.age_at_entry)
        y = np.array(d.Poids)
        a = np.array(d.age_at_entry)

        txt_out.write('\t age_at_entry : {}\n'.format(x))
        txt_out.write('\t Poids : {}\n'.format(y))
        for i in range(0, len(x)):
            txt_out.write('\t['+str(i)+']' + '-'*50+'\n')
            
            pl = mean_last_x_months(data, i, months)
            pn = mean_next_x_months(data, i, months)
            
            
            txt_out.write('\t\t/////Méthode Calcul moyenne sur le dernier mois :\n\t\tCoordonnées Moy Dernier Mois: {}\n'.format(pl))
            txt_out.write('\t\t/////Méthode Calcul moyenne sur le prochain mois :\n\t\tCoordonnées Moy Prochain Mois: {}\n'.format(pn))
                        
            prc_Poids_pl = abs(1-(y[i]/pl[1]))
            prc_Poids_pn = abs(1-(y[i]/pn[1]))
            
            txt_out.write('\tprc_Poids_pl >= prc ? {} >= {}\n'.format(prc_Poids_pl, prc))
            txt_out.write('\tprc_Poids_pn >= prc ? {} >= {}\n'.format(prc_Poids_pn, prc))
            
            if prc_Poids_pl >= prc or prc_Poids_pn >= prc:
                otl = True
            else:
                otl = False
            txt_out.write('\totls? {}\n'.format(otl))
            otls.append(otl)



ipprs= [72193145]
# otl_hugo_crochet(ipprs, 1)

def test_niveau_1(d, ippr):
    apps = d.iloc[:,8]
    
    ones = apps[apps==1]
    ones_idx = apps[apps==1].index
    
    lvl = ippr
    

def otl_pascale_roux(ipprs):
    prc  = 0.1
    for idx, ippr in enumerate(ipprs):
        print('['+str(idx)+']'+'['+str(ippr)+'] '+'-'*90+'\n')
        
        d = data[data['IPPR'] == ippr]
        d = data.set_index([pd.Index(range(len(d)))])
        
        niv1 = d[d['priority_lvl'] == 1]
        for i in range(0, len(d)):
            lvl = d.iloc[i,8]
            print('Index :', i)
            print('lvl :', lvl)

otl_pascale_roux(ipprs)

        
# data['otls'] = otls
# print(len(data_otls))
# print(len(data))
# data_otls = data_otls.append(data, ignore_index=True)
# print('Nouveau df : {} lignes'.format(len(data_otls)))
# print('Nombre de patients : {}'.format(len(data_otls.IPPR.unique())))
