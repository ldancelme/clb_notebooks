# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:42:39 2020

@author: DANCEL
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import timeit


# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
# //// Load file
data = pd.read_csv('data/age_interval/data20_70.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float}, na_values = '')
data20 = pd.read_csv('data/age_interval/data20.csv')

# Taille : m -> cm
data["Taille"] = data["Taille"] *100

# Return df name as str
def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name

# Find the patient w/ the most height data points
def most_observ(df, lim):
    ipprs = df['IPPR'].unique()
    most_observ = pd.DataFrame([i, len(df[df['IPPR'] == i])] for i in ipprs) 
    most_observ.columns = ['IPPR','len']
    most_observ = most_observ.sort_values(by='len', ascending=False)
    most_observ = most_observ[most_observ['len'] >= lim]
    
    df.name = get_df_name(df)
    file_name = "most_{}_lim{}.csv".format(df.name,lim)

    most_observ.to_csv(file_name, index=False)
    
    return most_observ

# Find the patient w/ the most height data points
def most_observ(df):
    ipprs = df['IPPR'].unique()
    most_observ = pd.DataFrame([i, len(df[df['IPPR'] == i])] for i in ipprs) 
    most_observ.columns = ['IPPR','len']
    most_observ = most_observ.sort_values(by='len', ascending=False)
    
    df.name = get_df_name(df)
    file_name = "most_{}.csv".format(df.name)

    most_observ.to_csv(file_name, index=False)
    
    return most_observ


# //// Sort IPPR by the most observations
# most = pd.DataFrame([i, len(data[data['IPPR'] == i])] for i in ipprs) 
# most.columns = ['IPPR','len']
# most = most.sort_values(by='len', ascending=False)

# ex, to find 50 patient w/ the most data points : 
most = most_observ(data20)
most.to_csv('data/most_observ/most_data20.csv', index=False)
# most = most[most['len'] > 50]
# most_ippr = np.array(most['IPPR'])
# data20most = data20[data20['IPPR'].isin(most_ippr)]