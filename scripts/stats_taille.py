#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:36:22 2020

@author: loicdancelme
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit

# Timer, file exec
start = timeit.default_timer()

# -----------------------------------------------------------------------------
# //// Load à partir de clean_csv
# load data file
# # taille = pd.read_csv('clean_taille.csv',dtype={'Taille' : float, 'Appli_origine' : str})
taille = pd.read_csv('data_taille.csv',dtype={'Taille' : float, 'Appli_origine' : str})
uniq = pd.read_csv('mean_std_uniq_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str})

# -----------------------------------------------------------------------------
# <///////////////////////////// years <=> days //////////////////////////////>
# -----------------------------------------------------------------------------
# Transform age in days to in years
def to_years(age):
    age = age / 365
    return age

# Transform age in years to in days
def to_days(age):
    age = age * 365
    return age

# Add a 'age_at_diag' column to the df
# taille.columns = ['IPPR', 'age_at_entry', 'diff_entry_diag', 'Taille', 'Appli']
# taille.insert(2,'age_at_diag', taille['age_at_entry'] - taille['diff_entry_diag'])

# Copy df and set 'age_at_entry','age_at_diag' to years
taille_yrs = taille.copy()
taille_yrs[['age_at_entry','age_at_diag']] = taille[['age_at_entry','age_at_diag']] .apply(lambda x: round(to_years(x)))

# -----------------------------------------------------------------------------
# <//////////////////////////// Slice dataframe //////////////////////////////>
# -----------------------------------------------------------------------------
# n : chunk row size
# Access the chunks with: list_df[0], list_df[1] etc...
# Assemble back into one df using pd.concat.
# -----------------------------------------------------------------------------
def slice_df(df, n):
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    return list_df

taille_chunks = slice_df(taille, 200)

# -----------------------------------------------------------------------------
# </////////////////////////// Stats descriptives ////////////////////////////>
# -----------------------------------------------------------------------------
#                                mean_std.csv
# -----------------------------------------------------------------------------
# //// On conserve toutes les colonnes du df taille en ajoutant mean, std
# //// On répète les mean, std par IPPR sur cq ligne pour le meme IPPR

zeros = [0] * 447754

taille.insert(6, 'mean',zeros)
taille.insert(7, 'std',zeros)

mean_uniq = uniq.set_index('IPPR')['mean'].to_dict()
std_uniq = uniq.set_index('IPPR')['std'].to_dict()

taille['mean'] = taille['IPPR'].map(mean_uniq)
taille['std'] = taille['IPPR'].map(std_uniq)

taille.to_csv('mean_std_v2.csv', index=False)

# -----------------------------------------------------------------------------
#                              mean_std_uniq.csv
# -----------------------------------------------------------------------------
# //// On retire les tailles de la df 
# //// On conserve une seule mean, std par IPPR
ippr_uniq = pd.Series(taille['IPPR'].unique(), index=taille['IPPR'].unique(), name='IPPR')
mean_uniq = taille.groupby('IPPR')['Taille'].mean()
std_uniq = taille.groupby('IPPR')['Taille'].std()
ippr_mean = pd.merge(ippr_uniq, mean_uniq, on='IPPR')
pre_mean_std_uniq = pd.merge(ippr_mean, std_uniq, on='IPPR')
mean_std_uniq = pre_mean_std_uniq.rename(columns={'Taille_x':'mean', 'Taille_y':'std'})

# Obsolete
# -----------------------------------------------------------------------------
# def stats_taille_unique(ippr):
#     # On conserve IPPR et Taille pour cq ippr
#     list_taille = taille.loc[taille['IPPR'] == ippr, ['IPPR', 'Taille']].reset_index(drop=True)
#     list_taille['Taille'] = list_taille['Taille'].apply(lambda x: float(x))
    
#     # mean
#     list_taille['mean'] = list_taille['Taille'].mean(axis=0)
    
#     # std
#     list_taille['std'] = list_taille['Taille'].std(axis=0)
    
#     # lists 
#     ipprs = list_taille['IPPR'].values.tolist()
#     mean = list_taille['mean'].values.tolist()
#     std = list_taille['std'].values.tolist()
    
#     return ipprs, mean, std

# # liste des ippr
# ippr_list_uniq = taille['IPPR'].unique()

# mean_std_uniq = [stats_taille_unique(i) for i in ippr_list_uniq]
# mean_std_uniq_df = pd.DataFrame(mean_std_uniq, columns = ['IPPR', 'mean', 'std'])
# mean_std_uniq_df['IPPR'] = mean_std_uniq_df['IPPR'].apply(lambda x : x[0])
# mean_std_uniq_df['mean'] = mean_std_uniq_df['mean'].apply(lambda x : x[0])
# mean_std_uniq_df['std'] = mean_std_uniq_df['std'].apply(lambda x : x[0]) 
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# </////////////////////// Interpretation des résultats //////////////////////>
# -----------------------------------------------------------------------------
# std = nan => 1 seule taille
# std = 0   => toutes les tailles sont les mêmes 
# -----------------------------------------------------------------------------

# export DF en .csv
# taille.to_csv('data_taille.csv', index=False)
# taille_yrs.to_csv('data_taille_yrs.csv', index=False)
#mean_std_uniq.to_csv('mean_std_uniq_v2.csv', index=False)


# End timer -------------------------------------------------------------------
stop = timeit.default_timer()
print('Time: ', stop - start, 's')
