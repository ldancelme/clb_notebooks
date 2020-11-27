# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 16:00:52 2020

@author: DANCEL
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


taille = [1.8, 1.8, 1.8, 20, 1.81, 1.81, 1.8, 20, 1.8, 1.8, 1.8]
otly = [1.72,1.89]
otlx = [23,27]
age = np.arange(20,31,1)


fig, ax = plt.subplots()
ax.scatter(age,taille)
ax.scatter(otlx, otly, c='r')
ax.set_ylim(1.7,1.9)
ax.legend(['inliers', 'outliers'])
ax.set_xlabel('Âge (ans)')
ax.set_ylabel('Taille (m)')
ax.set_title('Taille du patient XXX en fonction de son âge')
plt.show

fig.savefig('ex_plot_outlier.svg')

