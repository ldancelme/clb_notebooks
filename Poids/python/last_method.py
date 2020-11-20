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
data = data[data['age_at_entry'] > 7300]
ipprs = data.IPPR.unique()
ipprs = np.array(ipprs)

systemRandom = random.SystemRandom()
rint = systemRandom.randint(1,31481)

# data = data[data['IPPR'] == ipprs[rint]]
data = data[data['IPPR'] == 9012060]

data = data[data['priority_lvl'] == 1]

x = np.array(data.age_at_entry)
y = np.array(data.Poids)
a = np.array(data.age_at_entry)
appl = np.array(data.priority_lvl)

print(x,y)

def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

ind_6mois = 0.000537
ind_1mois = 0.0163
sl_list = []

def mean_next_x_months(temp, idx, months):
    period = months*31
    print('Period :', period)
    val = {}
    di = temp.iloc[idx,1]
    print('age_at_entry :', di)
    temp = temp.iloc[idx+1:,:]  
    list_p = []
    
    for j in range(len(temp)):
        # print('temp.iloc[j,1] :', temp.iloc[j,1])
        # print('di :', di)
        # print('temp.iloc[j,1] - di :', temp.iloc[j,1] - di)
        if temp.iloc[j,1] - di <= period :
            val.update({temp.iloc[j,1]:temp.iloc[j,3]})
    print(val)
    m = np.array(list(val.values())).mean()
    d = np.array(list(val.keys())).mean()
    p= [d,m]
    list_p.append(p)
    return p, list_p

def mean_last_x_months(temp, idx, months):
    period = months*31
    print('Period :', period)
    val = {}
    di = temp.iloc[idx,1]
    print('age_at_entry :', di)
    temp = temp.iloc[:idx-1,:]  
    list_p = []
    print("min: ", min(temp.iloc[:,1]))
    for j in np.arange(2,len(temp)):
        if min(temp.iloc[:,1]) > di-period:
            val.update({temp.iloc[j,1]:temp.iloc[j,3]})
    print(val)
    m = np.array(list(val.values())).mean()
    d = np.array(list(val.keys())).mean()
    p= [d,m]
    list_p.append(p)
    return p, list_p


def outlier_detection(ind_mois):
        durée_passage= a[0]-a[len(data)-1]
         
        for i in range(0, len(x)-1):
            
            
            
            print('['+str(i)+']'+' outlier_detection() loop index')
            plt.plot(x[i:i+2], y[i:i+2], 'ro-')
            sl = slope(x[i], y[i], x[i+1], y[i+1])
            sl_list.append(sl)
            
            p2, list_p2 = mean_next_x_months(data, i, 6)
            print(p2)
            plt.plot(p2[0],p2[1],'bx', markersize=10)
            # plt.text(p2[0],p2[1]+1,str(i),color='blue',fontsize=15)
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
        
def otl_hugo_crochet(months):
    plt.figure(figsize=[7,4], dpi=400)
    if months >= 6:
        prc = 0.1
    else:
        prc = 0.05
        
    for i in range(0, len(x)-1):
        
        p2, list_p2 = mean_last_x_months(data, i, months)
        print(p2)
        plt.plot(p2[0],p2[1],'bx', markersize=5)
        
        if np.isnan(p2).any() == False:
            plt.plot([x[i],p2[0]], [y[i],p2[1]], 'b-', linewidth=0.5)

        
        print('['+str(i)+'] '+'-'*100)
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        new_sl = slope(x[i], y[i], p2[0], p2[1])
        
        print('slope:', abs(sl))
        print('new_slope:', abs(new_sl))
        
        plt.plot(x[i:i+2], y[i:i+2], 'k-', linewidth=0.5)
        plt.plot(x[i:i+2], y[i:i+2], 'ro', markersize=4)
        
                
        prc_Poids = abs(1-(y[i]/p2[1]))
        print('prc_Poids:', prc_Poids)
        if prc_Poids > prc:
            otl = 'otl'
            print(otl)
            plt.text(x[i],y[i]+0.1,'otl')
        else:
            otl = 'inl'
            plt.text(x[i],y[i]+0.2,'inl')        
               
def otl_pascale_roux(months):
    
    if months == 6:
        prc = 0.1
    elif months == 1:
        prc = 0.05
    
    plt.figure(figsize=[13,8])
    for i in range(0, len(x)-1):
        print('['+str(i)+'] '+'-'*100)

        plt.plot(x[i:i+2], y[i:i+2], 'k-', linewidth=0.5)
        plt.plot(x[i:i+2], y[i:i+2], 'ro', markersize=4)
        
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        sl_list.append(sl)
        
        p2, list_p2 = mean_next_x_months(data, i, months)
        print(p2)
        plt.plot(p2[0],p2[1],'bx', markersize=5)
        
        prc_Poids = abs(1-(y[i]/p2[1]))
         
        if prc_Poids > prc:
            otl = 'otl'
            plt.text(x[i],y[i]+0.1,'otl')
        else:
            otl = 'inl'
            plt.text(x[i],y[i]+0.2,'inl')
                
otl_hugo_crochet(3)
# otl_pascale_roux(6)    
