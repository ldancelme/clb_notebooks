# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:07:31 2020

@author: LOX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kurtosis
from scipy.stats import skew


data = pd.read_csv('../data/all_data.csv')
data5 = data[data['age_at_entry'] < 1850]
data10 = data[data['age_at_entry'] < 3650]
data20 = data[data['age_at_entry'] < 7300]
data20 = data20[data20['age_at_entry'] > 3650]
# min: 0.525, max: 168.5
#
dataAdult = data[data['age_at_entry'] > 7300]
# min: 0.0, max: 710.0
#
data20_otl = data20[data20['Poids'] > 150]

##_________________________ Scatter Plots (random IPPRs)

# ipprs = data.IPPR
# ipprs = ipprs.sample(n=5)
ipprs = [720550,  9816644, 36168098, 49178590,  7411656,  4978883,
       54157811, 70198457]
for i in ipprs:
    dataplot = data[data['IPPR'] == i]
    x= dataplot.age_at_entry
    y= dataplot.Poids

    plt.figure()
    plt.scatter(x, y, facecolors='none', edgecolors='r', s=20, linewidth=1)
    plt.title('IPPR:{}'.format(i))
    plt.show()


#__________________________ Seaborn Displots

# fig, axes = plt.subplots(2, 2, figsize=[11, 11], dpi=200)
# sns.distplot(data5['Poids'], bins= np.arange(0,100,1), norm_hist = False, color="y", ax=axes[0][0], kde_kws={"bw":15, "kernel":"epa"})
# axes[0][0].set_title('KDE plot des patients entre 0 et 5 ans', fontsize=16)
# sns.distplot(data10['Poids'], bins= np.arange(0,100,1), norm_hist = False, color="r", ax=axes[0][1], kde_kws={"bw":15, "kernel":"epa"})
# axes[0][1].set_title('KDE plot des patients entre 0 et 10 ans', fontsize=16)
# sns.distplot(data20['Poids'], bins= np.arange(0,200,2), norm_hist = False, color="g", ax=axes[1][0], kde_kws={"bw":15, "kernel":"epa"})
# axes[1][0].set_title('KDE plot des patients entre 10 et 20 ans', fontsize=16)
# sns.distplot(dataAdult['Poids'], bins= np.arange(0,700,2), norm_hist = False, color="b", ax=axes[1][1], kde_kws={"bw":15, "kernel":"epa"})
# axes[1][1].set_title('KDE plot des patients > 20 ans', fontsize=16)

# fig, ax = plt.subplots(dpi=200)
# sns.distplot(np.sqrt(data10['Poids']), bins= np.arange(0,10,1), norm_hist = True, color="k", ax=ax, kde_kws={"bw":1, "kernel":"epa"})
# ax.set_title('KDE plot des patients < 20 ans', fontsize=16)

# datasets = [data5, data10, data20, dataAdult]
# datasets_name = ['data5', 'data10', 'data20', 'dataAdult']
# for idx, df in enumerate(datasets):
#     print(datasets_name[idx])
#     print(df.Poids.describe())
#     print("skew         ", np.round(skew(df.Poids.values), 6))
#     print("kurt         ", np.round(kurtosis(df.Poids.values), 6))
#     print('\n')
    
#__________________________ APPLI
# print(data.groupby('Appli').count())
# Appli	count                                               
# BLO	42832
# CRC	366079
# CRS	129226
# DIS	8003
# DOS	139032
# EVO	2935
# ORD	2425
# SAD	26127
# VEN	36236
# XAL	340239

#__________________________ mean, std
mean = data.groupby('IPPR')['Poids'].mean()
zeros = [0] * 1093134
data.insert(5, 'mean', zeros)
mean = mean.to_dict()
data['mean'] = data['IPPR'].map(mean)
    
std = data.groupby('IPPR')['Poids'].std()
data.insert(6, 'std', zeros)
std = std.to_dict()
data['std'] = data['IPPR'].map(std)
    
# data.to_csv('../data/all_data.csv', index=False)
