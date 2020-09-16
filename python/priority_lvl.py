# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:09:20 2020

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
data = pd.read_csv('mean_std_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')


priority_lvl3 = data[data['Appli'] != 'EVO']
priority_lvl3 = priority_lvl3[priority_lvl3['Appli'] != 'VEN']
priority_lvl3 = priority_lvl3[priority_lvl3['Appli'] != 'ORD']
priority_lvl3 = priority_lvl3[priority_lvl3['Appli'] != 'XAL']
priority_lvl2 = priority_lvl3[priority_lvl3['Appli'] != 'CRS']
priority_lvl1 = priority_lvl2[priority_lvl2['Appli'] != 'CRC']

print("priority_lvl4 : {}, taille : {}".format(data['Appli'].unique(), len(data)))
print("priority_lvl3 : {}, taille : {}".format(priority_lvl3['Appli'].unique(), len(priority_lvl3)))
print("priority_lvl2 : {}, taille : {}".format(priority_lvl2['Appli'].unique(), len(priority_lvl2)))
print("priority_lvl1 : {}, taille : {}".format(priority_lvl1['Appli'].unique(), len(priority_lvl1)))


# priority_lvl1.to_csv('priority_lvl1.csv', index=False)
# priority_lvl2.to_csv('priority_lvl2.csv', index=False)
# priority_lvl3.to_csv('priority_lvl3.csv', index=False)



# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
