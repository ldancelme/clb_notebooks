# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:45:46 2020

@author: LOX
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

data = pd.read_csv('../data/all_data.csv')
data = pd.read_csv('../data/otls_100_ipprs.csv')

# data = data[data['count'] > 12]
all_data = all_data[all_data['Poids']> 200]
ipprs= np.array(data.IPPR.unique())

# =============================================================================
#                                   Stats
# =============================================================================

prc_otls = len(data[data['otls'] == False])/len(data)

ipprs_patients_otls = []
def patients_avec_otls():
    for ippr in data.IPPR.unique():
        temp = data[data['IPPR'] == ippr]
        otls = np.array(temp.otls)
        if not all(otls):
            ipprs_patients_otls.append(ippr)
    return ipprs_patients_otls
ipprs_patients_otls = patients_avec_otls()

prc_patients_otls = len(ipprs_patients_otls)/len(ipprs)

def moyenne_otls_par_patient():
    moy = []
    for ippr in ipprs_patients_otls:
        temp = data[data['IPPR'] == ippr]
        temp = data[data['otls']==False]
        l    = len(temp)
        moy.append(l)
    return np.mean(moy)
moy = moyenne_otls_par_patient()

patients_otls = data[data['IPPR'].isin(ipprs_patients_otls)]
patients_otls.describe()

    
t=[]
pt = patients_otls.IPPR.unique()
for i in pt:
    temp= patients_otls[patients_otls['IPPR']==i]
    temp = temp[temp['otls']==False]
    a = len(temp)
    t.append(a)


# =============================================================================
#                                   Plotting                                              
# =============================================================================


def plot_otls(ippr):
    print(ippr)
    dplot = data[data['IPPR'] == ippr]
    plt.figure(figsize=[11,6])
    groups = dplot.groupby('otls')
    plt.plot(dplot.age_at_entry, dplot.Poids, 'k--', linewidth=0.5)
    for name, group in groups:
        plt.plot(group["age_at_entry"], group["Poids"], marker='o', linestyle="", label=name)
    plt.title('IPPR: {}'.format(ippr), fontsize=14)
    plt.legend()
    plt.xlabel('Âge (jours)', fontsize=14)
    plt.ylabel('Poids (kg)', fontsize=14)
    
    
    plt.figure(figsize=[11,6])
    plt.plot(dplot.age_at_entry, dplot.Poids, 'k--', linewidth=0.5)
    plt.plot(dplot.age_at_entry, dplot.Poids, marker='o', linestyle="", alpha=0.8, markersize=2)
    x = np.array(dplot.age_at_entry)
    y = np.array(dplot.Poids)
    app = np.array(dplot.Appli)
    print(app)
    for idx, val in enumerate(app):
        plt.text(x[idx], y[idx] , val)


ipprs = random.choices(ipprs_patients_otls, k=3)
for i in ipprs:
    plot_otls(i)

    