# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:31:57 2020

@author: DANCEL
"""

import pandas as pd
import numpy as np
import xlwings as xw

wb = xw.Book("../../Projet IMC v2.xlsx")


general_sheet = wb.sheets['Général']
general_max_letter = 'N'
general_max_row = 172791


# Fonction de conversion du format sheet vers des dataframes
# On est obligé de convertir par groupe de 100 000 lignes
# car sinon cela prend trop de temps et une erreur time out empêche la convertion

def transform_sheet_to_df(sheet, max_letter, max_row):
    q = max_row // 100000
    list_of_df = []
    for ind in range(q):
        subsheet_range = 'A' + str(int(ind)*100000 + 1) + ':' + max_letter + str(int(ind+1)*100000)
        print(subsheet_range)
        df = sheet[subsheet_range].options(pd.DataFrame, index=False, header=False).value
        list_of_df.append(df)
    if q*100000 != max_row:
        last_subsheet_range = 'A' + str(q*100000 + 1) + ':' + max_letter + str(max_row)
        print(last_subsheet_range)
        df = sheet[last_subsheet_range].options(pd.DataFrame, index=False, header=False).value
        list_of_df.append(df)
    df = pd.concat(list_of_df, axis=0, ignore_index=True)
    # On enlève les points des noms de colonnes et on met des _ à la place des espaces
    new_header = [name.replace(' ', '_').replace('.', '') for name in df.iloc[0]]
    df = df[1:]
    df.columns = new_header
    return df


# Conversion des sheets en dataframe --> celles qu'on va utiliser pour nettoyer et traiter les données

general = transform_sheet_to_df(general_sheet, general_max_letter, general_max_row)


# Différentes valeurs trouvées pour les colonnes T, N et M de l'onglet Général
# T = NULL,X,0,1,2,3,4
# N = NULL,X,0,1,2,3
# M = 0, 1
# Autres valeurs bizarres de T: 17 'a'
# Autres valeurs bizarres de N: 3327 '+', 1 '°', 1 '_', 2 'B', 2 '=', 1 '4', 1 '6'
# Pas d'autres valeurs bizarres pour M

def fix_last_weird_values(df):
    df.loc[df['T'] == 'a', 'T'] = 'NULL'
    df.loc[df['N'].isin(['°', '_', 'B', '=', '4', '6']), 'N'] = 'NULL'
    return df


egal = general[general['N'] == '=']
