# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:15:15 2020

@author: LOX
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest



ipprs = pd.read_csv('sctr_moins5_01.csv')
ipprs = list(ipprs.IPPR)

ippr = 90243940

data = pd.read_csv("../data/age_interval/all_data.csv")
# data = data[data.IPPR.isin(ipprs)]


data = data[data['IPPR'] == ippr]
data.age_at_entry = data.age_at_entry / 365
x = data.age_at_entry
y = data.Taille
data = data.iloc[:,[1,4]]
X = data.values
# X = X.reshape(-1,1)

# <<<<<<<<<<<<< K-means Clustering >>>>>>>>>>>>>
#
km = KMeans(
    n_clusters=3, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(X)

df = pd.DataFrame({'age':x.values,'Taille':y.values,'cluster':y_km})
def plot_clusters():
    # plot the 3 clusters

    plt.scatter(
        X[y_km == 0, 0], X[y_km == 0, 1],
        s=50, facecolor='none', 
        edgecolor='lightgray', marker='o',
        label='cluster 1'
    )
    
    plt.scatter(
        X[y_km == 1, 0], X[y_km == 1, 1],
        s=50, facecolor='none', 
        edgecolor='orange', marker='o', 
        label='cluster 2'
    )
    
    plt.scatter(
        X[y_km == 2, 0], X[y_km == 2, 1],
        s=50, facecolor='none', 
        edgecolor='lightblue', marker='o', 
        label='cluster 3'
    )
    
    # plot the centroids
    plt.scatter(
        km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
        s=50, marker='*',
        c='red', alpha=0.5,
        label='centroids'
    )
    plt.show()
    plt.legend()
    plt.title('K-means Clustering (IPPR:{})'.format(ippr))

# plot_clusters()

def plot_linreg(cluster):
    fig, ax = plt.subplots()
    X = cluster[:,0].reshape(-1,1)
    Y = cluster[:,1].reshape(-1,1)
    # regression
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    
    # plot
    ax.scatter(X, Y, facecolor='none', edgecolor='b')
    ax.plot(X, Y_pred, color='red')

cluster0 = X[y_km == 0, :]
cluster1 = X[y_km == 1, :]
cluster2 = X[y_km == 2, :]



plot_linreg(cluster0)
plot_linreg(cluster1)
plot_linreg(cluster2)



def isolation_forest(df, cluster):
    df = df[df['cluster'] == cluster]
    print("IPPR: {}".format(ippr))
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
    
    # plot
    age = df.age
    otl = df.loc[df['otl'] == -1]
    otl_index=list(otl.index) # index of outliers
    X_train = df.Taille
    fig, ax = plt.subplots(figsize=(7,4))
    ax.scatter(age[otl_index], X_train[otl_index], marker= 'x', c='r', s=60, label='outliers')
    ax.scatter(age, X_train, c='green', alpha=0.5, s=20, label='inliers')
    ax.set_title('Scatter plot IPPR={} (IsolationForest)'.format(ippr))
    ax.set_xlabel("Âge (jours)")
    ax.set_ylabel("Taille (cm)")

isolation_forest(df,0)
isolation_forest(df,1)
isolation_forest(df,2)

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10, 10], dpi=200)
# ax.scatter(X, y_km, facecolor='none', edgecolor='b', linewidth=0.5)
# plt.show()



