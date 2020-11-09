# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:16:39 2020

@author: DANCEL
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

data = pd.read_csv('../../data/clean_poids.csv')

ipprs = data.IPPR.unique()
ipprs = np.array(ipprs)


c = []
for i in tqdm(ipprs) : 
    d = data[data['IPPR'] == i]
    count = d['count'].iloc[0]
    c.append(count)

plt.hist(c,bins='auto')

# systemRandom = random.SystemRandom()
# rint = systemRandom.randint(1,55498)

# data = data[data['IPPR'] == ipprs[rint]]

# x = np.array(data.age_at_entry)
# y = np.array(data.Poids)

# print(x,y)

# def slope(x1, y1, x2, y2):
#     m = (y2-y1)/(x2-x1)
#     return m

# for i in range(0, len(x)):
#     plt.plot(x[i:i+2], y[i:i+2], 'ro-')
#     sl = slope(x[i], y[i], x[i+1], y[i+1])
#     print(sl)

# plt.show()






