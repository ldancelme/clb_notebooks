# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 13:17:39 2020

@author: DANCEL
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------

# Filter by data sources
lvl4 = pd.read_csv('mean_std_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl3 = pd.read_csv('data/priority_lvl/priority_lvl3.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl2 = pd.read_csv('data/priority_lvl/priority_lvl2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl1 = pd.read_csv('data/priority_lvl/priority_lvl1.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

def sup20(df):
    df = df[df['age_at_entry'] > 7300]
    return df

def inf20(df):
    df = df[df['age_at_entry'] < 7300]
    return df

lvl4 = inf20(lvl4)
lvl3 = inf20(lvl3)
lvl2 = inf20(lvl2)
lvl1 = inf20(lvl1)

def IQR_outliers(df):
    ippr = df['IPPR'].unique()
    dfs = pd.DataFrame(columns=df.columns)
    tour = 0
    for idx, val in enumerate(ippr):
        dfi = df[df['IPPR'] == val]
        q25, q50, q75 = df['Taille'].quantile([0.25, 0.50, 0.75])
        iqr = q75 - q25
        cut_off = 1.5*iqr
        lower, upper = q25 - cut_off, q75 + cut_off
        
        print('Tour de boucle : {}, IPPR : {}'.format(idx, val))
        # print('IPPR: {}, q25: {}, q75:{}, lower: {}, upper:{}'.format(i, q25, q75, lower, upper))
        # outliers = [x for x in df['Taille'] if x < lower or x > upper]
        # outliers_removed = [x for x in df['Taille'] if x > lower and x < upper ]
        
        dfi['otl'] = [x > lower and x < upper for x in dfi['Taille']]
        dfs = dfs.append(dfi, ignore_index=True)
        tour =+ 1
    return dfs

IQR_outliers(lvl1).to_csv('lvl1_IQR_output_inf20.csv', index=False)
print()
print('=================================================================')
print('                           LVL1 Fini                             ')
print('=================================================================')
print()

IQR_outliers(lvl2).to_csv('lvl2_IQR_output_inf20.csv', index=False)
print()
print('=================================================================')
print('                           LVL2 Fini                             ')
print('=================================================================')
print()

IQR_outliers(lvl3).to_csv('lvl3_IQR_output_inf20.csv', index=False)
print()
print('=================================================================')
print('                           LVL3 Fini                             ')
print('=================================================================')
print()

IQR_outliers(lvl4).to_csv('lvl4_IQR_output_inf20.csv', index=False)
print()
print('=================================================================')
print('                           LVL4 Fini                             ')
print('=================================================================')
print()

# Time:   20174.0035 s
#     	  336.2334 m 
# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
