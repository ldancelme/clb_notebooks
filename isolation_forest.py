# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:07:19 2020

@author: LOX
"""

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
from sklearn.ensemble import IsolationForest
# import warnings  
# warnings.filterwarnings('ignore')

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
data = pd.read_csv('data/age_interval/data20_70.csv')
most = pd.read_csv('data/most_observ/most_data20_70_lim50.csv')
ipprs = pd.read_csv('plots/z_score/ippr_zscore.csv')
ipprs = ipprs.IPPR
ipprs_iforest = pd.read_csv('plots/iForest/ippr_iForest.csv')
ipprs_iforest = ipprs_iforest.IPPR

data = data[data['std'].notna()]
data = data[data['std'] != 0]
# ipprs = most['IPPR'].unique()
# ipprs = np.random.choice(ipprs, size=10)
   

def isolation_forest(ipprs_iforest):
    for ippr in ipprs:
        print("IPPR: {}".format(ippr))
        print("PUUUUUTO")
        df = data[data['IPPR'] == ippr]
        X_train = df.Taille
        age = df.age_at_entry
        X_train = np.array(X_train)
        X_train = X_train.reshape(-1, 1)
        
        clf = IsolationForest(max_samples='auto', random_state=0)
        clf.fit(X_train)
        pred = clf.predict(X_train)
        score = clf.score_samples(X_train)
        df['otl'] = pred
        df['score'] = score
        
        print(df.iloc[:,np.r_[4, 8:10]])
        
        otl = df.loc[df['otl'] == -1]
        otl_index=list(otl.index)
        
        print("Tableau outliers count :\n{}".format(df['otl'].value_counts()))
        print('\n\n')
        
        X_train = df.Taille
        
        fig, ax = plt.subplots(figsize=(7,4))
        ax.scatter(age[otl_index], X_train[otl_index], marker= 'x', c='r', s=60, label='outliers')
        ax.scatter(age, X_train, c='green', alpha=0.5, s=20, label='inliers')
        ax.set_title('Scatter plot IPPR={} (IsolationForest)'.format(ippr))
        lgd = ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel("Age (jours)")
        ax.set_ylabel("Taille (cm)")
        fig.savefig('plots/iForest/iForest_{}.svg'.format(ippr), bbox_extra_artists=(lgd,))
        fig.savefig('plots/iForest/iForest_{}.png'.format(ippr), bbox_extra_artists=(lgd,), dpi=1080)

isolation_forest(ipprs)











# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
