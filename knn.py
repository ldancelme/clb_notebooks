# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 09:29:04 2020

@author: DANCEL
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit
from scipy.stats import zscore

import matplotlib.pyplot as plt

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
data = pd.read_csv('data/age_interval/data20_70.csv')
clean = pd.read_csv('data/outliers_res/lvl1_IQR_output.csv')
clean = clean[clean['otl'] == True]
clean = clean[clean['age_at_entry'] < 25550]
most = pd.read_csv('most_observ.csv')

# calculating Z-score
def z_score(df, ippr):
    df = df[df['IPPR'] == ippr]
    x = df['Taille']
    z = zscore(x)
    return z
    

data = data[data['std'] > 0.1]
print(len(data))
ipprs = data['IPPR'].unique()
ipprs = np.random.choice(ipprs, size=5)
for ippr in ipprs:
    df = data[data['IPPR'] == ippr]
    x = df.age_at_entry
    y = df.Taille
    
    z = z_score(df, ippr)
    print('z : {}'.format(z))
    
    # ok = [x for x in z if x <= 1 and x >= -1]
    # print('ok : {}'.format(ok))
    # print()
    col = np.where((z<=1.0) & (z>=-1.0), 'c', 'r')
    
    plt.figure()
    plt.scatter(x, y, color=col)
    plt.title('Scatter plot IPPR={}'.format(ippr))
    

# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
