# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:18:58 2020

@author: DANCEL
"""
import pandas as pd
import numpy as np
from tqdm import tqdm
import random

data = pd.read_csv('../../data/clean_poids.csv')
MAD = pd.read_csv('mad_by_ippr.csv')

data = data[data['std'] > 30]
ipprs = data.IPPR.unique()
ippr = random.choice(ipprs)

def mad(df, ippr):
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
    print('lower: ', lower)
    print('upper', upper)

mad = mad_test(data, ippr)
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
