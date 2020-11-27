# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 17:28:31 2020

@author: LOX
"""

import pandas as pd
import numpy as np
import timeit

# Timer, file exec
start = timeit.default_timer()

# -----------------------------------------------------------------------------
# load data file (à partir de data_taille.csv)
taille = pd.read_csv('data_taille.csv', dtype={'Taille' : float, 'Appli_origine' : str})
uniq = pd.read_csv('mean_std_uniq.csv', dtype={'Taille' : float, 'Appli_origine' : str})

# //// On conserve toutes les colonnes du df taille en ajoutant mean, std
# //// On répète les mean, std, sem par IPPR sur cq ligne pour le meme IPPR

zeros = [0] * 447754

taille.insert(6, 'mean',zeros)
taille.insert(7, 'std',zeros)

mean_uniq = uniq.set_index('IPPR')['mean'].to_dict()
std_uniq = uniq.set_index('IPPR')['std'].to_dict()

taille['mean'] = taille['IPPR'].map(mean_uniq)
taille['std'] = taille['IPPR'].map(std_uniq)

# taille.to_csv('mean_std.csv', index=False)

# End timer -------------------------------------------------------------------
stop = timeit.default_timer()
print('Time: \t', str(round(stop - start, 3)), 's \n \t\t ' + str(round((stop - start) / 60, 5)) + ' m')

