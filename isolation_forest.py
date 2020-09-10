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
import warnings  
warnings.filterwarnings('ignore')

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------
data = pd.read_csv('data/age_interval/all_data.csv')
most = pd.read_csv('data/most_observ/most_data20.csv')

# data20 = data20[data20['std'].notna()]
# data20 = data20[data20['std'] != 0]
# globals().update({'df' + str(ippr): data[data['IPPR'] == ippr] for ippr in ipprs})

# -----------------------------------------------------------------------------
#                                   Modelling
# -----------------------------------------------------------------------------
ipprs = most['IPPR'].unique()
ipprs = np.random.choice(ipprs, size=10)

def isolation_forest(ipprs_iforest):
    for ippr in ipprs:
        print("IPPR: {}".format(ippr))
        data20 = data20[data20['IPPR'] == ippr]
        X_train = data20.Taille
        X_train = np.array(X_train)
        X_train = X_train.reshape(-1, 1)
        
        # iForest model design
        clf = IsolationForest(max_samples='auto', random_state=0)
        # Training
        clf.fit(X_train)
        # Prediction output
        pred = clf.predict(X_train)
        score = clf.score_samples(X_train)
        data20['otl'] = pred                  # Binary (-1 if otl else 1)
        data20['score'] = abs(score)          # -1 < otl score < 0
         
        # Print data20 Taille, otl(bin), otl(score)
        print(data20.iloc[:,np.r_[4, 8:10]])
        print("\nTableau outliers count :\n{}\n{}\n".format(data20['otl'].value_counts(), '-'*35))
        
        
def isolation_forest(df, ippr):
    print("IPPR: {}".format(ippr))
    df = df[df.IPPR == ippr]
    X_train = df.Taille
    X_train = np.array(X_train)
    X_train = X_train.reshape(-1, 1)
    # iForest model design
    clf = IsolationForest(max_samples='auto', random_state=0)
    # Training
    clf.fit(X_train)
    # Prediction output
    otl = clf.predict(X_train)
    score = clf.score_samples(X_train)
    df['otl'] = otl                    # Binary (-1 if otl else 1)
    df['score'] = abs(score)           # -1 < otl score < 0
     
    # Print df Taille, otl(bin), otl(score)
    print(df.iloc[:,np.r_[4, 12:14]])
    print("\nTableau outliers count :\n{}\n{}\n".format(df['otl'].value_counts(), '-'*35))
    
    return otl, score

data = data[data.age_at_entry > 7200]
otl, score = [isolation_forest(data, x) for x in data.IPPR.unique()]
# data20['otl_iForest'] = otl                    # Binary (-1 if otl else 1)
# data20['score_iForest'] = abs(score)           # -1 < otl score < 0

# ------------------------------------------------------------ Plotting        
def plot_iforest(df, ippr):
    X_train = df.Taille # array to df
    age = df.age_at_entry
    otl = df.loc[df['otl'] == -1]
    otl_index=list(otl.index) # index of outliers
    fig, ax = plt.subplots(figsize=(7,4))
    ax.scatter(age[otl_index], X_train[otl_index], marker= 'x', c='r', s=60, label='outliers')
    ax.scatter(age, X_train, c='green', alpha=0.5, s=20, label='inliers')
    ax.set_title('Scatter plot IPPR={} (IsolationForest)'.format(ippr))
    lgd = ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xlabel("Âge (jours)")
    ax.set_ylabel("Taille (cm)")
    
    ## Save figures
    # fig.savefig('plots/iForest/iForest_{}.svg'.format(ippr), bbox_extra_artists=(lgd,))
    # fig.savefig('plots/iForest/iForest_{}.png'.format(ippr), bbox_extra_artists=(lgd,), dpi=1080)
        
    
# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
