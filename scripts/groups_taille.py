# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 09:20:36 2020

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
data = pd.read_csv('mean_std.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')


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


# //// Some weird values
data_outliers00 = data[data['age_at_entry'] < 0] # age < 0
data_outliers01 = data[data['Taille'] > 220]     # Taille > 2.5 m

# //// Boxplots
plt.figure(1, dpi=400)
plt.title("Taille du patient ~ Tranche d'Âge")
data_bxplt = [data20["Taille"], data20_40["Taille"], data40_70["Taille"], data70["Taille"]]
data_bxplt = data_bxplt[::-1]
plt.boxplot(data_bxplt, labels={'0-20', '20-40', '40-70', '70+'})
plt.ylabel("Taille (cm)")
plt.xlabel("Âge")
plt.ylim(0, 250)


# //// Scatter plots



# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print('\n|======== exec time|')
print('|Time:', str(round(stop - start, 3)), '\t s  |\n| \t ' + str(round((stop - start) / 60, 5)) + ' m |')
print('|==================|')
