#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import numpy as np
import timeit
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from scipy import stats
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats import weightstats as st
from sklearn.neighbors import KernelDensity


start = timeit.default_timer()

# Load data
data = pd.read_csv('../data/age_interval/all_data.csv', na_values = '')


# //// Intervalles Âge 
# Taille : m -> cm
data["Taille"] = data["Taille"] *100

# //// Intervalles Age
age20 = list(range(20 *365))                    # Croissance ~ de 0 à 20 ans
age20_40 = list(range((20 *365), (40 *365)))    # Stagnation de 0 à 40 ans 
age40_70 = list(range((40 *365), (70 *365)))    # Diminution taille à partir de 40 ans
age70plus = list(range((70 *365) , (110 *365)))
age20_70 = list(range((20 *365), (70 *365))) 

# //// Separation en groupe selon les intervalles d'age
data20 = data[data['age_at_entry'].isin(age20)]
data20.to_csv("data20.csv", index=False)
data20_40 = data[data['age_at_entry'].isin(age20_40)]
data20_40.to_csv("data20_40.csv", index=False)
data40_70 = data[data['age_at_entry'].isin(age40_70)]
data40_70.to_csv("data40_70.csv", index=False)
data70 = data[data['age_at_entry'].isin(age70plus)]
data70.to_csv("data70.csv", index=False)
data20_70 = data[data['age_at_entry'].isin(age20_70)]
data20_70.to_csv("data20_70.csv", index=False)


m20, s20 = stats.norm.fit(data20['Taille'])
m20_40, s20_40 = stats.norm.fit(data20_40['Taille'])
m40_70, s40_70 = stats.norm.fit(data40_70['Taille'])
m70, s70 = stats.norm.fit(data70['Taille'])

# //// Groups stats: mean, std
groups_mean = [m20, m20_40, m40_70, m70]
groups_std = [s20, s20_40, s40_70, s70]


# Distribution des patients dans les différents groupes

# |Période             |  Age   |Effectif| mean | std |
# |:-                  |:-:     |:-:     |:-:   |:-:  |
# |Enfant / Adolescent |[0-20]  |105239  |128.51|32.75|
# |Jeune Adulte        |[20-40] |35848   |170.23|9.92 |
# |Adulte              |[40-70] |229963  |167.53|8.93 |
# |Seniors             |[70-110]|76693   |165.48|9.02 |
# 
# Total : 447 743 lignes. 


# //// Some weird values
data_outliers00 = data[data['age_at_entry'] < 0] # age < 0
data_outliers01 = data[data['Taille'] > 220]     # Taille > 2.5 m
data_outliers02 = data20[data20["Taille"] > 300] # age < 20 && Taille > 300
data_outliers03 = data20_70[data20_70['Taille'] > 21] # 
# data_outliers02.to_csv("ols_ageinf20_taillesup300.csv", index=False)

print('Outliers : age < 0, n = 11, 5 premières valeurs :\n')
print(data_outliers00.iloc[:5, [1, 4, -2]])
print('\nOutliers : Taille > 250, n = 13, 5 premières valeurs :\n')
print(data_outliers01.iloc[:5, [1, 4, -2]])


# # //// Boxplots : Taille du patient ~ Tranche d'Âge [(^)](#up)
# # Data used for the boxplpots
# plt.figure(figsize=(6, 5))
# data_bxplt = [data20["Taille"], data20_40["Taille"], data40_70["Taille"], data70["Taille"]]
# labels={'0-20', '70+', '40-70', '20-40'}

# # boxplot w/o ylim (outliers are visible)
# plt.boxplot(data_bxplt, labels=labels)
# plt.ylabel("Taille (cm)")
# plt.xlabel("Âge")
# plt.title("Taille du patient ~ Tranche d'Âge", fontsize=16)



# # On recommence en supprimant les valeurs de taille > 300 cm
# # boxplot w/o outliers
# data20 = data20[data20["Taille"] < 300]
# data_bxplt = [data20["Taille"], data20_40["Taille"], data40_70["Taille"], data70["Taille"]]
# plt.figure(figsize=(6, 5))
# plt.boxplot(data_bxplt, labels=labels)
# plt.xlabel("Âge")
# plt.ylabel("Taille (cm)")
# plt.title("Boxplot sans les outliers", fontsize=16)


# # //// Kernel Density Estimation plots

# # plot a kernel density estimation over a stacked barchart
# fig, axes = plt.subplots(2, 2, figsize=[11, 11], dpi=200)

# # Affichage quantiles
# iqr20 = stats.mstats.mquantiles(data20['Taille'])
# iqr20_40 = stats.mstats.mquantiles(data20_40['Taille'])
# iqr40_70 = stats.mstats.mquantiles(data40_70['Taille'])
# iqr70 = stats.mstats.mquantiles(data70['Taille'])
# iqrs = [iqr20, iqr20_40, iqr40_70, iqr70]

# def iqr_plot(iqr, ax, y, y2):
#     for xc in iqr:
#         ax.axvline(x=xc, ymin= 0, ymax = 0.05, c ='m', linewidth = 1)
#     for i in iqr:
#         ax.text(iqr[0]-4, y,'Q1', fontsize = 8)
#         ax.text(iqr[1]-4, y2,'Q2', fontsize = 8)
#         ax.text(iqr[2]-4, y,'Q3', fontsize = 8)

# # Labels def
# def lbl_box(i):
#     lbl = "mean : " + str(round(groups_mean[i],2)) + "\nstd : " + str(round(groups_std[i],3)) + "\nQ1 : "  
#     lbl += str(iqrs[i][0]) + "\nQ2 : "  + str(iqrs[i][1]) + "\nQ3 : "  + str(iqrs[i][2])
#     return lbl
                                                                      
# lbl20 = lbl_box(0)
# lbl20_40 = lbl_box(1)
# lbl40_70 = lbl_box(2)
# lbl70 = lbl_box(3)

# # Display mean, std, IQR
# def mean_std_box(lbl, x, y):
#     at = AnchoredText(lbl,
#               prop=dict(size=10), frameon=True,
#               loc='upper left',
#               )
#     at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
#     axes[x][y].add_artist(at)


# # //// [00-20] range Kernel 
# sns.distplot(data20['Taille'], bins= np.arange(0,220,2), norm_hist = False, color="g", ax=axes[0, 0], kde_kws={"bw":15, "kernel":"epa"})
# iqr_plot(iqr20, axes[0][0], 0.001, 0.001)
# axes[0][0].set_title('KDE plot des patients entre 0 et 20 ans', fontsize=16)
# mean_std_box(lbl20, 0, 0)

# # //// [20-40] range histogram
# sns.distplot(data20_40['Taille'], bins= np.arange(70,260,2), color="b", ax=axes[1, 0], kde_kws={"bw":15, "kernel":"epa"})
# iqr_plot(iqr20_40, axes[0][1], 0.003, 0.0045)
# axes[0][1].set_title('KDE plot des patients entre 20 et 40 ans', fontsize=16)
# mean_std_box(lbl20_40, 1, 0)

# # //// [40-70] range histogram
# sns.distplot(data40_70['Taille'], bins= np.arange(70,260,2), color="r", ax=axes[0, 1], kde_kws={"bw":15, "kernel":"epa"})
# iqr_plot(iqr40_70, axes[1][0], 0.003, 0.0045)
# axes[1][0].set_title('KDE plot des patients entre 40 et 70 ans', fontsize=16)
# mean_std_box(lbl40_70, 0, 1)

# # //// [70-110] range histogram
# sns.distplot(data70['Taille'], bins= np.arange(70,260,2), color="k", ax=axes[1, 1], kde_kws={"bw":15, "kernel":"epa"})
# iqr_plot(iqr70, axes[1][1], 0.003, 0.0045)
# axes[1][1].set_title('KDE plot des patients de plus de 70 ans', fontsize=16)
# mean_std_box(lbl70, 1, 1)

# plt.suptitle("KDE plots (Bandwith: Silverman, Kernel: Epanechnikov)", fontsize = 22, y = 0)
# plt.tight_layout(pad=1)


# # //// KDE Plots (Méthode 2)
# # https://jakevdp.github.io/PythonDataScienceHandbook/05.13-kernel-density-estimation.html#Kernel-Density-Estimation-in-Practice)
# def kde_fit(data):
#     fig = plt.figure()    
#     x = np.array(data['Taille'])
#     xmax = x.max()
#     xs = x.size
#     x_d = np.linspace(0, xmax, xs)
    
#     # instantiate and fit the KDE model
#     kde = KernelDensity(bandwidth=15.0, kernel='gaussian')
#     kde.fit(x[:, None])

#     # score_samples returns the log of the probability density
#     logprob = kde.score_samples(x_d[:, None])

#     plt.fill_between(x_d, np.exp(logprob), alpha=0.5)
#     plt.plot(x, np.full_like(x, -0.01), '|k', markeredgewidth=1)
#     plt.show()

# kde_fit(data20)
# kde_fit(data20_40)
# kde_fit(data40_70)
# kde_fit(data70)

# //// Z-test
# ztest, pval = st.ztest(data20_40['Taille'], x2=None, value=170.23)
# print(ztest)
# print(float(pval))


# //// Q-Q plots | Probplots
# theo = np.random.normal(170.23, 9.92, 358498)
# sm.qqplot(theo)
# sm.qqplot_2samples(data20_40['Taille'], theo)

# stats.probplot(data20['Taille'], dist="norm", plot=pylab)
# pylab.show()

# stats.probplot(data20_40['Taille'], dist="norm", plot=pylab)
# pylab.show()

# stats.probplot(data40_70['Taille'], dist="norm", plot=pylab)
# pylab.show()

# stats.probplot(data70['Taille'], dist="norm", plot=pylab)
# pylab.show()

# probscale.probplot(data20['Taille'], plottype='pp', bestfit=True,
#                    problabel='Percentile', datalabel='Taille (cm)',
#                    line_kws=dict(label='Best-fit line'))
# -----------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')

