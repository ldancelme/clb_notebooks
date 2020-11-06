
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:18:58 2020

@author: DANCEL
"""
import pandas as pd
import numpy as np
from tqdm import tqdm
import random
from itertools import islice
import warnings


data = pd.read_csv('../../data/clean_poids.csv')
MAD = pd.read_csv('mad_by_ippr.csv')

ipprs = data.IPPR.unique()
ippr = random.choice(ipprs)

def df_mad(df, ippr):
    df = df[df['IPPR'] == ippr]
    poids = np.sort(df.Poids.values)
    M = np.median(poids)
    Q = np.quantile(poids, 0.75)
    b = 1/Q
    Abs = [abs(x-M) for x in poids]
    MedAbs = np.median(Abs)
    MAD = b*MedAbs

    # print('array: ', poids)   
    # print('Median: ', M)
    # print('0.75 Quantile: ', Q)
    # print('1/Q(0.75): ', b)
    # print('Absolute values (M-x) array: ', Abs)
    # print('Median of Absolute Values: ', MedAbs)
    print('MAD: ', MAD)
    
    return ippr, MAD

def list_mad(l):
    l = np.sort(l)
    M = np.median(l)
    Q = np.quantile(l, 0.75)
    b = 1/Q
    Abs = [abs(x-M) for x in l]
    MedAbs = np.median(Abs)
    # MAD = b*MedAbs
    MAD = MedAbs
    return MAD
    
def mad_test(df, ippr):
    df = df[df['IPPR'] == ippr]
    val = df.Poids.values
    mad = MAD[MAD['IPPR'] == ippr]
    mad = mad.MAD
    med = np.median(val)
    lower = med - 3*mad
    upper = med + 3*mad
    print('IPPR: ', ippr)
    print('val:', df.iloc[:,3])
    print('med: ', med)
    print('mad: ', mad)

# mad = mad_test(data, ippr)
# MAD = [mad(data, i) for i in tqdm(ipprs)]
# 29.25% of MAD are equal to 0.0
#            IPPR       MAD
# 22543    720550  0.401786
# 11482   9816644  0.422713
# 36566  36168098  0.426172
# 31408  49178590  0.456216
# 53440   7411656  0.458378
# 12988   4978883  0.654867
# 34872  54157811  0.666667
# 32255  70198457  0.666667
    
# Algo de fenêtre glissante
def window(seq, k):
    i = iter(seq)
    win = []
    for e in range(0, k):
        win.append(next(i))
    yield win
    for e in i:
        win = win[1:] + [e]
        yield win
    
    
# Détection outlier avec MADi sur fenêtre glissante
# k= Taille de la fenêtre
# t0= valeur limit
# deltaT= nombre de jours écoulé entre 2 mesures
def windowed_mad(ippr, k):
    df= data[data['IPPR'] == ippr]
    p= df.Poids.values
    t= df.age_at_entry.values
    a= df.Appli.values
    print(p)
    print(t)
    print(a)
    for i, w in enumerate(window(p,k)):
        print('{} | windowed list (n={}): {}'.format(i, k, w))
        print('{} | MAD: {}'.format(i, list_mad(w)))
    for i, t in enumerate(window(t, k)):
        print('{} | windowed list (n={}): {}'.format(i, k, t[2]-t[0]))

windowed_mad(5418634,3)


# iterable = np.arange(10)
# for value in  window(iterable, 3):       
#     for val in value:
#         print(val)
    
    
    
    
    
    
    
    
    
    
