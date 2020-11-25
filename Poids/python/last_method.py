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

data = pd.read_csv('../../data/clean_poids.csv')

data_otls = pd.read_csv('otls_100_ipprs.csv')
ipprs_otls = np.array(data_otls.IPPR.unique())

# data = data[data['age_at_entry'] > 7300]
ipprs = data.IPPR.unique()
ipprs = np.array(ipprs)

ipprs = [x for x in ipprs if x not in ipprs_otls]
ipprs = random.choices(ipprs, k=100)
# data = data[data['IPPR'].isin(ipprs)]

# systemRandom = random.SystemRandom()
# rint = systemRandom.randint(1,31481)

# test = pd.read_csv('test_poids.csv')
# test2 = pd.read_csv('test_poids2.csv')
# test3 = pd.read_csv('test_poids3.csv')
# data = test3

# data = data[data['IPPR'] == ipprs[rint]]
# data = data[data['IPPR'] == 9012060]
# data = data[data['IPPR'] == 53180334]
# data = data[data['priority_lvl'] == 1]

# x = np.array(data.age_at_entry)
# y = np.array(data.Poids)
# a = np.array(data.age_at_entry)
# appl = np.array(data.priority_lvl)


def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

ind_6mois = 0.000537
ind_1mois = 0.0163

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
    m = np.array(list(val.values())).mean()
    d = np.array(list(val.keys())).mean()
    p= [d,m]
    return p

otls = []
zeros = []
zeros = np.zeros(len(data))
data['otl'] = zeros
def otl_hugo_crochet(ipprs, months):
    prc  = 0.1
    for ippr in tqdm(ipprs):
        d = data[data['IPPR'] == ippr]
        x = np.array(d.age_at_entry)
        y = np.array(d.Poids)
        a = np.array(d.age_at_entry)
        for i in range(0, len(x)):
            pl = mean_last_x_months(data, i, months)
            pn = mean_next_x_months(data, i, months)
            
            prc_Poids_pl = abs(1-(y[i]/pl[1]))
            prc_Poids_pn = abs(1-(y[i]/pn[1]))
            
            if prc_Poids_pl > prc and prc_Poids_pn > prc:
                otl = True
            else:
                otl = False
            
            otls.append(otl)
            print(len(otls))

otl_hugo_crochet(ipprs, 1)
    
def otl_hugo_crochet(months):
    plt.figure(figsize=[11,6])
    # if months >= 6:
    #     prc = 0.1
    # else:
    #     prc = 0.05
    prc = 0.1
    for i in range(0, len(x)-1):
        print('['+str(i)+'] '+'-'*90)
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        print('slope:', abs(sl))
        
        pl = mean_last_x_months(data, i, months)
        pn = mean_next_x_months(data, i, months)
        
        print('pl:',pl)
        print('pn:',pn)
        
        plt.plot(pn[0],pn[1],'bx', markersize=5)
        plt.plot(pl[0],pl[1],'rx', markersize=5)
        plt.text(pn[0],pn[1]+0.08, i, fontsize=7, fontstyle='oblique', c='b')
        plt.text(pl[0],pl[1]+0.08, i, fontsize=7, fontstyle='oblique', c='r')
        
        plt.plot(x[i:i+2], y[i:i+2], 'kD-', markersize=2, linewidth=0.5)
        prc_Poids_pl = abs(1-(y[i]/pl[1]))
        prc_Poids_pn = abs(1-(y[i]/pn[1]))
        print('prc_Poids_pl:', prc_Poids_pl)
        print('prc_Poids_pn:', prc_Poids_pn)
        if prc_Poids_pl > prc and prc_Poids_pn > prc:
            otl = 'otl'
            o = True
            print(otl)
            plt.text(x[i],y[i]+0.4,'otl')
        else:
            o = False
            otl = 'inl'
            plt.text(x[i],y[i]-0.4,'inl')     
        
    plt.savefig('otl5_02.png',figsize=[11,6], dpi=800)
            
def outlier_detection(ind_mois):
    durée_passage= a[0]-a[len(data)-1]
     
    for i in range(0, len(x)-1):
        
        
        
        print('['+str(i)+']'+' outlier_detection() loop index')
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        
        pl, list_pl = mean_next_x_months(data, i, 6)
        print(pl)
        plt.plot(pl[0],pl[1],'bx', markersize=10)
        # plt.text(pl[0],pl[1]+1,str(i),color='blue',fontsize=15)
        print('-'*100)
        
        prc_Poids = abs(1-(y[i]/y[i+1]))
        prc_Poids = abs(1-(np.mean([y[i-2],y[i-1],y[i]])/y[i+1]))
        nb_jours = a[i+1]-a[i]

        if prc_Poids > ind_mois*nb_jours:
            otl = 'otl'
            plt.plot(x[i],y[i],marker='o', markeredgecolor = 'white',markerfacecolor='red')
        else:
            otl = 'inl'
            
        # print('['+str(i)+'] '+'Nb de jours : ', x[i+1]-x[i])
        # print('['+str(i)+'] '+'DeltaP : ', y[i+1]-y[i])
        # print('['+str(i)+'] '+'%Poids : ', prc_Poids)
        # print('['+str(i)+'] '+'c_off : ', ind_mois*nb_jours)
        # print('['+str(i)+'] '+'Slope : ', abs(sl))
        # print('['+str(i)+'] '+'Appli : ', appl[i])
        # plt.text(x[i]+(x[i+1]-x[i])/2, y[i]+(y[i+1]-y[i])/2, str(np.round(sl,4)))
        # print(otl)
        # print('-'*10)
            
    # plt.text(min(x),max(y)+0.4,'ippr: ' +str(ipprs[rint]))
        
def otl_pascale_roux(months):
    
    if months == 6:
        prc = 0.01
    elif months == 1:
        prc = 0.05
    
    plt.figure(figsize=[13,8])
    for i in range(0, len(x)-1):
        print('['+str(i)+'] '+'-'*100)

        plt.plot(x[i:i+2], y[i:i+2], 'k-', linewidth=0.5)
        plt.plot(x[i:i+2], y[i:i+2], 'ro', markersize=4)
        
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        
        pl, list_pl = mean_next_x_months(data, i, months)
        print(pl)
        plt.plot(pl[0],pl[1],'bx', markersize=5)
        
        prc_Poids = abs(1-(y[i]/pl[1]))
         
        if prc_Poids > prc:
            otl = 'otl'
            plt.text(x[i],y[i]+0.1,'otl')
        # else:
        #     otl = 'inl'
        #     plt.text(x[i],y[i]+0.2,'inl')
                
# otl_hugo_crochet(1)
# otl_pascale_roux(6)    
