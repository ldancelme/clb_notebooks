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

# Filter by data sources
lvl4 = pd.read_csv('mean_std_v2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl3 = pd.read_csv('data/priority_lvl/priority_lvl3.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl2 = pd.read_csv('data/priority_lvl/priority_lvl2.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl1 = pd.read_csv('data/priority_lvl/priority_lvl1.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

lvl1_iqr = pd.read_csv('data/outliers_res/lvl1_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl2_iqr = pd.read_csv('data/outliers_res/lvl2_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl3_iqr = pd.read_csv('data/outliers_res/lvl3_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')
lvl4_iqr = pd.read_csv('data/outliers_res/lvl4_IQR_output.csv', dtype={'Taille' : float, 'Appli_origine' : str, 'mean' : float, 'std' : float, 'sem' : float}, na_values = '')

# -----------------------------------------------------------------------------
#                      linear regression model with otl
# -----------------------------------------------------------------------------
data20 = lvl1[lvl1.age_at_entry > 7200]
data20 = data20[data20['age_at_entry'] > 0] # two points < 0

data20.Taille = data20.Taille.apply(lambda x: x*100)
data20 = data20.sample(frac=0.5)
x = data20['age_at_entry']
y = data20['Taille']
# polynomial curve fitting (order=3)
p = np.polyfit(x, y, 3)

# model
predict = np.poly1d(p)
print('coeffs: {}'.format(predict))

# r_square (r2=0.94)
r2 = r2_score(y, predict(x))
print('r2: {}'.format(r2))


sd_cutoff = 3 
Y_hat = predict(x)
delta = y - Y_hat
sd_p = np.std(delta)
ok = abs(delta) < sd_p * sd_cutoff

# plotting
def draw_text(ax):
    at = AnchoredText("r2= {}".format(round(r2,3)),
                      loc='upper left', prop=dict(size=11), frameon=True,
                      )
    ax.add_artist(at)
    
    
figure, ax = plt.subplots(figsize=(6,5))
draw_text(ax)
x_lm = range(0,7200)
ax.scatter(x,y, color=np.where(ok, 'steelblue', 'r'), marker='.', s=25, alpha=0.5)
ax.plot(x_lm, predict(x_lm), c='orange')
ax.set_xlabel('Âge (jours)')
ax.set_ylabel('Taille (cm)')
ax.set_title('Linear Regression Model with outliers, cutoff: 2*std')

# figure.savefig('lm_lvl1_otl+.png', dpi=1080)
figure.savefig('lm_lvl1_otl+.svg')


# # ------------------------------------------------------------- with outliers
# list20_40 = [x for x in lvl1['age_at_entry'] if x > 7200 and x < 14400]
# data20_40 = lvl1[lvl1['age_at_entry'].isin(list20_40)]

# x = data20_40['age_at_entry'] 
# y = data20_40['Taille']

# p = np.polyfit(x,y,1)
# r2 = r2_score(y, np.polyval(p,x))
# print('r2 avec outliers : {}'.format(r2))

# a, b = np.polyfit(x,y,1)

# # plot
# # data20_40 = data20_40.sample(frac=0.1)
# # plt.plot(x,y,'r+')
# # plt.plot(x, a*x+b)

# # ---------------------------------------------------------- without outliers
# list20_40 = [x for x in lvl1_otl['age_at_entry'] if x > 7200 and x < 14400]
# data20_40 = lvl1_otl[lvl1_otl['age_at_entry'].isin(list20_40)]

# x = data20_40['age_at_entry'] 
# y = data20_40['Taille']

# p = np.polyfit(x,y,1)
# r2 = r2_score(y, np.polyval(p,x))
# print('r2 sans outliers : {}'.format(r2))

# a, b = np.polyfit(x,y,1)

# plot
# data20_40 = data20_40.sample(frac=0.1)
# plt.plot(x,y,'r+')
# plt.plot(x, a*x+b)



# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')
