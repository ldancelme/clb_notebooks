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
most = pd.read_csv('data/most_observ/most_data20_70_lim50.csv')
ipprs_iforest = pd.read_csv('plots/iForest/ippr_iForest.csv')
ipprs_iforest = ipprs_iforest.IPPR

ipprs = most['IPPR']
ipprs.to_csv("ipprs_index.csv", index=True)

# data = data[data['std'] > 0.001]
print(len(data))

ipprs = most['IPPR'].unique()
ipprs = np.random.choice(ipprs, size=15)

# calculating Z-score
def z_score(df, ippr):
    df = df[df['IPPR'] == ippr]
    x = df['Taille']
    z = zscore(x)
    return z
    
# plotting
def zscore_plots(ipprs):
    for ippr in ipprs:
        print(ippr)
        df = data[data['IPPR'] == ippr]
        x = df.age_at_entry
        y = df.Taille
        print(x)
        
        z = z_score(df, ippr)
        if z.any() > 0:
            print('z : {}'.format(z))
            fig, ax = plt.subplots()
            
            # mean, std
            mu = np.mean(y)
            theta = np.std(y)
            
            col = np.where((z<=1.0) & (z>=-1.0), 'c', 'r')
            
            ax.scatter(x, y, color=col, alpha=0.5, s=40)
            ax.hlines(mu, x.iloc[0], x.iloc[len(x)-1],'k', linewidth=2)
            ax.hlines(mu+theta, x.iloc[0], x.iloc[len(x)-1],'r', linestyles='dashed')
            ax.hlines(mu-theta, x.iloc[0], x.iloc[len(x)-1], 'r', linestyles='dashed')
            ax.set_title('Scatter plot IPPR={}, (z >= 1)'.format(ippr))
            ax.set_xlabel("Âge (jours)")
            ax.set_ylabel("Taille (cm)")
            # fig.savefig('plots/z_score/zscore_{}.svg'.format(ippr))
            # fig.savefig('plots/z_score/zscore_{}.png'.format(ippr), dpi=400)
           


zscore_plots(ipprs_iforest)

# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
