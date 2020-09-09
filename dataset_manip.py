# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:55:32 2020

@author: DANCEL
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit


# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
# //// Load file
data20 = pd.read_csv('data/age_interval/data20.csv')
most = pd.read_csv('data/most_observ/most_data20.csv')

# Taille : m -> cm
data20["Taille"] = data20["Taille"]

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
# first_date = [get_first_date(data20, x) for x in data20.IPPR]
# data20['first_date'] = first_date


# Retourne la dernière date de saisie de poids d'un patient
def get_last_date(df, ippr):
    df = df[df['IPPR'] == ippr]
    last = df['age_at_entry'].max()
    return last
# last_date = [get_last_date(data20, x) for x in data20.IPPR]
# data20['last_date'] = last_date



# Retourne le nb de jours entre la 1ère et denière date de saisie de poids
def get_period(df, ippr):
    first = get_first_date(df, ippr)
    last = get_last_date(df, ippr)
    return last - first
# period = [get_period(data20, x) for x in data20.IPPR]
# data20['period'] = period

# Retourne le nombre de taille saisie pour un patient
def count_observ(df, ippr):
    count = len(df[df['IPPR'] == ippr])
    return count

# zeros = [0] * 105239
# data20.insert(11, 'count', zeros)
# most_uniq = most.set_index('IPPR')['len'].to_dict()
# data20['count'] = data20['IPPR'].map(most_uniq)


# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
