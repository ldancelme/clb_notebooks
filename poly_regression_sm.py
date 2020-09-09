# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:51:42 2020

@author: LOX
"""

# ---------------------------------- imports ----------------------------------
import pandas as pd
import numpy as np
import timeit
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.sandbox.regression.predstd import wls_prediction_std

    

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------

# Import data by data sources
lvl1 = pd.read_csv('data/priority_lvl/priority_lvl1.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

# Set DataFrame
data20 = lvl1[lvl1.age_at_entry < 7200]
data20 = data20[data20['age_at_entry'] > 0] # two points < 0
data20.Taille = data20.Taille.apply(lambda x: x*100)

# p = 0.5 # Keep p % of observations
# data20 = data20.sample(frac= p)

# -----------------------------------------------------------------------------
#                                   Modelling
# -----------------------------------------------------------------------------
data = data20
x = data['age_at_entry']
y = data['Taille']

# Process polynomial coeffs
x = np.array(x)
x = x.reshape(-1, 1)
        
polynomial_features= PolynomialFeatures(degree=3)
xp = polynomial_features.fit_transform(x)

model = sm.OLS(y, xp).fit()
ypred = model.predict(xp) 


figure, ax = plt.subplots(figsize=(6,5))
ax.scatter(x,y, color='b', marker='x', s=25, alpha=0.5, linewidth=1)

x = np.sort(x, axis=0)
ypred = np.sort(ypred, axis=0)

_, upper,lower = wls_prediction_std(model)

upper = np.sort(upper, axis=0)
lower = np.sort(lower, axis=0)

ax.plot(x, ypred, c='orange',linewidth=1)
ax.plot(x, upper, 'g', '--',label="Lower") # confid. intrvl
ax.plot(x, lower, color='orange', linestyle=':',label="Upper")
ax.legend(loc='upper left')

ax.set_xlabel('Âge (jours)')
ax.set_ylabel('Taille (cm)')
















# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')