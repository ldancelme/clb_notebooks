# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:55:02 2020

@author: LOX
"""
# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit
import matplotlib.pyplot as plt

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
data = pd.read_csv('data/age_interval/data20_70.csv')
most = pd.read_csv('data/most_observ/most_data20_70_lim50.csv')


def knn():
    ipprs = most['IPPR'].unique()
    ipprs = np.random.choice(ipprs, size=15)
    for ippr in ipprs:
        df = data[data['IPPR'] == ippr]
        x = df.age_at_entry
        y = df.Taille











# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
