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






