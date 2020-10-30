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
from sklearn.metrics import r2_score
from matplotlib.offsetbox import AnchoredText
    

# //// Timer, file exec
start = timeit.default_timer()
# -----------------------------------------------------------------------------

# Import data by data sources
lvl4 = pd.read_csv('../data/age_interval/all_data.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl3 = pd.read_csv('../data/priority_lvl/priority_lvl3.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl2 = pd.read_csv('../data/priority_lvl/priority_lvl2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl1 = pd.read_csv('../data/priority_lvl/priority_lvl1.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

# lvl1_iqr = pd.read_csv('data/outliers_res/lvl1_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
# lvl2_iqr = pd.read_csv('data/outliers_res/lvl2_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
# lvl3_iqr = pd.read_csv('data/outliers_res/lvl3_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
# lvl4_iqr = pd.read_csv('data/outliers_res/lvl4_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

# -----------------------------------------------------------------------------
#                           Linear regression model
# -----------------------------------------------------------------------------
data = lvl1
data20 = data[data.age_at_entry < 7200]
data20 = data20[data20['age_at_entry'] > 0] # two points < 0
data20.Taille = data20.Taille.apply(lambda x: x*100)
# Keep x % of observations
# per = 0.1
# data20 = data20.sample(frac= per)

# -----------------------------------------------------------------------------
#                                   Modelling
# -----------------------------------------------------------------------------
data = data20
x = data['age_at_entry']
y = data['Taille']

x= x /365


# polynomial curve fitting
p = np.polyfit(x, y, 5)

# model
predict = np.poly1d(p)
print('coeffs: {}'.format(predict))

# r_square (r2=0.94)
r2 = r2_score(y, predict(x))
print('r2: {}'.format(r2))

sd_cutoff = 2
pred = predict(x)
delta = y - pred
sd_p = np.std(delta)
ok = abs(delta) < sd_p * sd_cutoff


# -----------------------------------------------------------------------------
#                                   Plotting
# -----------------------------------------------------------------------------
def draw_text(ax):
    at = AnchoredText("r2= {}\ncut_off = 2*std".format(round(r2,3)),
                      loc='upper left', prop=dict(size=11), frameon=True,
                      )
    ax.add_artist(at)
    

figure, ax = plt.subplots(figsize=(10,6))
draw_text(ax)
x_lm = range(0,20)
ax.scatter(x,y, color=np.where(ok, 'steelblue', 'r'), marker='x', s=25, alpha=0.5, linewidth=1)
ax.plot(x_lm, predict(x_lm), c='orange')
ax.set_xlabel('Âge (jours)')
ax.set_ylabel('Taille (cm)')
ax.set_title("Regression Polynomiale d'ordre 5 (<20 ans)", fontsize=16)

figure.savefig('lm_lvl1.png', dpi=1080)
# figure.savefig('lm_lvl1.svg')


# -----------------------------------------------------------------------------
#                                   Validation
# -----------------------------------------------------------------------------
# y -> y
# y_hat -> pred
# residuals -> e
e = y - pred 




# # Scatter Plot
# figure, ax_s = plt.subplots(nrows=1, ncols=2, figsize=(15,8))
# def scatter_plt(x, y, col):
#     ax_s[col].scatter(x, y, color='c', marker='x', linewidth=1, alpha = 0.5)
#     ax_s[col].set_xlabel('Taille Prédite (cm)')
#     ax_s[col].set_ylabel('Résidus')
    
#     p = np.polyfit(x, y, 1)
#     predict = np.poly1d(p)
#     r2 = r2_score(y, predict(x))
    
#     corr = np.corrcoef(x, y)
    
#     minx = round(int(min(x)), 1)
#     maxx = round(int(max(x)) ,1)
#     x_lm = range(minx, maxx)
    
#     if col == 0:
#         ax_s[col].plot(x_lm, predict(x_lm), c='orange', label='$r^2$: {}'.format(np.round(r2, 3)))
#         ax_s[col].set_xlabel('Taille (cm)')
#         ax_s[col].legend()
        
#     ax_s[1].set_title('ScatterPlot : e ~ y_hat (corr: {})'.format("{:e}".format(corr[1][0])))
#     ax_s[0].set_title('ScatterPlot : y ~ y_hat')
    
# # scatter_plt(y, pred, 0)
# # scatter_plt(pred, e, 1)


# # # -----------------------------------------------------------------------------
# # Hist2d 
# figure, ax_h = plt.subplots(nrows=1, ncols=2, figsize=(15,8))
# def hist_2d(x, y, col):
#     h = ax_h[col].hist2d(x, y, bins=75, cmap=plt.cm.jet)

#     ax_h[col].set_xlabel('Taille')
#     ax_h[col].set_ylabel('Taille Prédite')
    
#     p = np.polyfit(x, y, 1)
#     predict = np.poly1d(p)
#     r2 = r2_score(y, predict(x))
    
#     minx = round(int(min(x)), 1)
#     maxx = round(int(max(x)) ,1)
#     x_lm = range(minx, maxx)    
    
#     ax_h[col].plot(x_lm, predict(x_lm), c='orange', label='$r^2$: {}'.format(np.round(r2, 3)))
#     ax_h[col].legend()
#     ax_h[col].set_xticks(np.arange(min(x), max(x)+1, 10.0))
#     ax_h[col].set_yticks(np.arange(min(y), max(y)+1, 10.0))
    
#     ax_h[col].grid()
#     ax_h[0].set_title('ScatterPlot : y ~ y_hat')
#     ax_h[1].set_title('ScatterPlot : e ~ y_hat')
    
# # hist_2d(y, pred, 0)
# # hist_2d(e, pred, 1)


# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
