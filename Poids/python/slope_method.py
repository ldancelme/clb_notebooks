# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:16:39 2020

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


# c = []
# for i in tqdm(ipprs) : 
#     d = data[data['IPPR'] == i]
#     count = d['count'].iloc[0]
#     c.append(count)

# plt.hist(c,bins='auto')

systemRandom = random.SystemRandom()
rint = systemRandom.randint(1,55498)
# rint=23926

data = data[data['IPPR'] == ipprs[rint]]

x = np.array(data.age_at_entry)
y = np.array(data.Poids)
a = np.array(data.age_at_entry)

print(x,y)

def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m
sl_list = []

cut_off = 0.001


if len(x) > 4:    
    for i in range(0, len(x)-1):
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        sl_list.append(sl)
        
        prc_Poids = abs(1-(y[i]/y[i+1]))
        prc_Poids = abs(1-(np.mean([y[i-2],y[i-1],y[i]])/y[i+1]))
        nb_jours = a[i+1]-a[i]

        if prc_Poids > cut_off*nb_jours:
            otl = 'otl'
            plt.plot(x[i],y[i],marker='o', markeredgecolor = 'white',markerfacecolor='red')
        else:
            otl = 'inl'

        print('['+str(i)+'] '+'Nb de jours : ', x[i+1]-x[i])
        print('['+str(i)+'] '+'DeltaP : ', y[i+1]-y[i])
        print('['+str(i)+'] '+'%Poids : ', prc_Poids)
        print('['+str(i)+'] '+'c_off : ', cut_off*nb_jours)
        print('['+str(i)+'] '+'Slope : ', abs(sl))
        plt.text(x[i]+(x[i+1]-x[i])/2, y[i]+(y[i+1]-y[i])/2, str(np.round(sl,4)))
        print(otl)
        print('-'*10)   
plt.show()

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
    list_p = []
    if idx > 1:
        temp = temp.iloc[:idx-1,:]  

        for j in range(len(temp)):
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
    plt.figure(figsize=[11,6])
    if months >= 6:
        prc = 0.1
    else:
        prc = 0.05
    # prc = 0.1
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






