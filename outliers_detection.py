# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:55:32 2020

@author: DANCEL
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit
import matplotlib.pyplot as plt
import scipy.stats as st


# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
# //// Load file
data = pd.read_csv('mean_std_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float}, na_values = '')
most_observ = pd.read_csv('most_observ.csv')

# //// Sort IPPR by the most observations
# most_observ = pd.DataFrame([i, len(data[data['IPPR'] == i])] for i in ipprs) 
# most_observ.columns = ['IPPR','len']
# most_observ = most_observ.sort_values(by='len', ascending=False)

data = pd.read_csv('mean_std_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
# //// Groupe selon les intervalles d'age
data20 = pd.read_csv('data/age_interval/data20.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
data20_40 = pd.read_csv('data/age_interval/data20_40.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
data20_70 = pd.read_csv('data/age_interval/data20_70.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
data40_70 = pd.read_csv('data/age_interval/data40_70.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
data70 = pd.read_csv('data/age_interval/data70.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

# -----------------------------------------------------------------------------
#                         5 INTERVALS [0,20,40,70,110] 
# -----------------------------------------------------------------------------
# Taille : m -> cm
data["Taille"] = data["Taille"] *100

# Find the patient w/ the most height data points
def most_observ(df, lim):
    ipprs = df['IPPR'].unique()
    most_observ = pd.DataFrame([i, len(df[df['IPPR'] == i])] for i in ipprs) 
    most_observ.columns = ['IPPR','len']
    most_observ = most_observ.sort_values(by='len', ascending=False)
    most_observ = most_observ[most_observ['len'] >= lim]
    return most_observ
    # file_name = "most_observ_" + str(df) + ".csv"
    # most_observ.to_csv(file_name, index=False)

# ex, to find 50 patient w/ the most data points : 
# most_observ20 = most_observ(data20, 50)
# most_observ = most_observ[most_observ['len'] > 50]
# most_observ_ippr = np.array(most_observ['IPPR'])
# data20most = data20[data20['IPPR'].isin(most_observ_ippr)]

# -----------------------------------------------------------------------------
#                               Fonctions Utiles
# -----------------------------------------------------------------------------

# Filtre les patients dont l'IPPR appartient à la liste entrée en argument
def filter_ippr(df, ippr_list):
    df = df[df['IPPR'].isin(ippr_list)]
    return df.reset_index(drop=True)


# Supprime les patients dont l'IPPR appartient à la liste entrée en argument
def suppr_ippr(df, ippr_list):
    df = df.drop(df[df['IPPR'].isin(ippr_list)].index)
    return df.reset_index(drop=True)

# Retourne la première date de saisie de poids d'un patient
def get_first_date(df, ippr):
    df = df[df['IPPR'] == ippr]
    first = df['age_at_entry'].min()
    return first

# Retourne la dernière date de saisie de poids d'un patient
def get_last_date(df, ippr):
    df = df[df['IPPR'] == ippr]
    last = df['age_at_entry'].max()
    return last

# Retourne le nb de jours entre la 1ère et denière date de saisie de poids
def get_period(df , ippr):
    first = get_first_date(df, ippr)
    last = get_last_date(df, ippr)
    return last - first

# Retourne le nombre de taille saisie pour un patient
def count_observ(df, ippr):
    count = len(df[df['IPPR'] == ippr])
    return count


# -----------------------------------------------------------------------------
#                           Outliers Detect° Fct°
# -----------------------------------------------------------------------------

def IQR_outliers(df, ippr):
    df = df[df['IPPR'] == ippr]
    q25, q50, q75 = df['Taille'].quantile([0.25, 0.50, 0.75])
    iqr = q75 - q25
    cut_off = 1.5*iqr
    lower, upper = q25 - cut_off, q75 + cut_off
    outliers = [x for x in df['Taille'] if x < lower or x > upper]
    outliers_removed = [x for x in df['Taille'] if x > lower and x < upper ]
    # for x in df: 
    #     outliers
    return outliers, outliers_removed


# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
