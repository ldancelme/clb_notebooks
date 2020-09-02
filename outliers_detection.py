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
from matplotlib.offsetbox import AnchoredText


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

# -----------------------------------------------------------------------------
#                         5 INTERVALS [0,20,40,70,110] 
# -----------------------------------------------------------------------------
# Taille : m -> cm
data["Taille"] = data["Taille"] *100

# //// Intervalles Age
age20 = list(range(20 *365)) # Croissance ~ de 0 à 20 ans
age20_40 = list(range((20 *365), (40 *365))) # Stagnation de 0 à 40 ans 
age40_70 = list(range((40 *365), (70 *365))) # Diminution taille à partir de 40 ans
age70plus = list(range((70 *365) , (110 *365)))

# //// Separation en groupe selon les intervalles d'age
data20 = data[data['age_at_entry'].isin(age20)]
data20.to_csv("data20.csv", index=False)
data20_40 = data[data['age_at_entry'].isin(age20_40)]
data40_70 = data[data['age_at_entry'].isin(age40_70)]
data70 = data[data['age_at_entry'].isin(age70plus)]

# -----------------------------------------------------------------------------
#                         Filter patient w/ 50+ data points 
# -----------------------------------------------------------------------------

most_observ = most_observ[most_observ['len'] > 50]
most_observ_ippr = np.array(most_observ['IPPR'])
data20most = data20[data20['IPPR'].isin(most_observ_ippr)]

# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
