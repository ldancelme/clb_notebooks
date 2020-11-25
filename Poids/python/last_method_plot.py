# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:45:46 2020

@author: LOX
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

data = pd.read_csv('otls_100_ipprs.csv')
ipprs= np.array(data.IPPR.unique())

len(data[data['otls'] == True])

ipprs = random.choices(ipprs, k=5)
ip = random.choices(ipprs, k=1)

def plot_otls(ippr):
    print(ippr)
    dplot = data[data['IPPR'] == ippr]
    plt.figure(figsize=[11,6])
    groups = dplot.groupby('otls')
    plt.plot(dplot.age_at_entry, dplot.Poids, 'k--', linewidth=0.5)
    for name, group in groups:
        plt.plot(group["age_at_entry"], group["Poids"], marker='o', linestyle="", label=name)
    plt.title('IPPR: {}'.format(ippr))
    plt.legend()
    
for i in ipprs:
    plot_otls(i)