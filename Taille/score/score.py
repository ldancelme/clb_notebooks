# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:41:29 2020

@author: DANCEL
"""

import numpy as np
import pandas as pd

data = pd.read_csv('../data/age_interval/all_data.csv')
data_ippr = data.sample(n=5) # SELECT 10 RANDOM PATIENTS
ipprs = data_ippr.IPPR.unique()
print('IPPRS: {}\n'.format(ipprs))

def score_appli():
    print('='*25+' SCORE APPLI ORIGINE '+'='*25)
    for i in ipprs:
        print('*'*15)
        print('IPPR: {}'.format(i))
        curr = data[data['IPPR'] == i]
        lvl = curr.priority_lvl
        print('lvl: {}'.format(lvl.values))
        four_pct = len(lvl[lvl == 1])/len(curr)
        three_pct = len(lvl[lvl == 2])/len(curr)
        two_pct = len(lvl[lvl == 3])/len(curr)
        one_pct = len(lvl[lvl == 4])/len(curr)
        print('%fours: {}\n%threes: {}\n%twos: {}\n%ones: {}'.format(np.round(four_pct,3), np.round(three_pct,3), np.round(two_pct,3), np.round(one_pct,3)))
        score_sur_4 = 4*four_pct + 3*three_pct + 2*two_pct + 1*one_pct
        print('score (/4): {}/4'.format(np.round(score_sur_4,3)))
        score = score_sur_4/4
        print('score (%): {}%\n'.format(np.round(score*100,2)))

# score_appli()


def calculate_weights(dimensions, method):
    N = len(dimensions)
    
    if method == 'sr':
        denom = np.array([ ((1 / (i + 1)) + ((N + 1 - (i + 1)) / N)) for i, x in enumerate(dimensions) ]).sum()
        weights = [ ((1 / (i + 1)) + ((N + 1 - (i + 1)) / N)) / denom for i, x in enumerate(dimensions) ]
    elif method == 'rs':
        denom = np.array([ (N + 1 - (i + 1)) for i, x in enumerate(dimensions)]).sum()
        weights = [ (N + 1 - (i + 1)) / denom for i, x in enumerate(dimensions) ]
    elif method == 'rr':
        denom = np.array([ 1 / (i + 1) for i, x in enumerate(dimensions) ]).sum()
        weights = [ (1 / (i + 1)) / denom for i, x in enumerate(dimensions) ]
    elif method == 're':
        exp = 0.2
        denom = np.array([ (N + 1 - (i + 1)) ** exp for i, x in enumerate(dimensions) ]).sum()
        weights = [ (N + 1 - (i + 1)) ** exp / denom for i, x in enumerate(dimensions) ]
    else:
        raise Exception('Invalid weighting method provided')
    
    return weights

dim = ['Appli', 'Dim', 'OtlPercentage']
dim2 = ['Appli1', 'Appli2']
dim4= ['Appli1', 'Appli2', 'Appli3','Appli4']
dim5= ['Appli1', 'Appli2', 'Appli3','Appli4','Appli5']




weights_sr = calculate_weights(dim5, 'sr')
weights_rs = calculate_weights(dim5, 'rs')
weights_rr = calculate_weights(dim5, 'rr')
weights_re = calculate_weights(dim5, 're')

    
