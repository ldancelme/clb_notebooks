"""
Created on Thu Jun 18 17:15:41 2020

@author: loicdancelme
"""

import pandas as pd
import numpy as np
import xlwings as xw
import timeit

start = timeit.default_timer()


# ---------------------------------------------------------------------------

# Importation du fichier et récupération de chaque onglet avec leurs infos pour pouvoir convertir
# On est obligé de procéder de cette manière pour obtenir des dataframes à cause de la protection par mot de passe

wb = xw.Book("Projet IMC v2.xlsx")

# La lettre correspond à la dernière colonne de l'onglet
# Le nombre correspond à la dernière ligne de l'onglet

poids1_sheet = wb.sheets['Données évol - Poids - Part 1']
poids1_max_letter = 'E'
poids1_max_row = 600001

poids2_sheet = wb.sheets['Données évol - Poids - Part 2']
poids2_max_letter = 'E'
poids2_max_row = 660429

# Fonction de conversion du format sheet vers des dataframes
# On est obligé de convertir par groupe de 100 000 lignes
# car sinon cela prend trop de temps et une erreur time out empêche la conversion


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
poids1 = transform_sheet_to_df(poids1_sheet, poids1_max_letter, poids1_max_row)
poids2 = transform_sheet_to_df(poids2_sheet, poids2_max_letter, poids2_max_row)
poids = pd.concat([poids1, poids2], axis=0, ignore_index=True)


# ---------------------------- QUALITY CHECK & FUNCTION DEFINITION --------------------------------

print()
print('AVANT LE NETTOYAGE DES DONNÉES, IL Y A :')
print(' -', (poids['Poids'] != 'NULL').sum(), 'données de poids saisies sur', poids.shape[0], 'lignes dans la table')
print(' -', poids.loc[poids['Poids'] != 'NULL', 'IPPR'].nunique(), 'patients dans la table "Poids"')
print()


# Delete duplicate data 
poids = poids.drop_duplicates().reset_index(drop=True)

# Drop lines with NA values
poids = poids.dropna(subset=['IPPR']).reset_index(drop=True)


# Remove spaces around values
def fix_space_only(value):
    if value == '':
        return 'NULL'
    else:
        return value

def remove_spaces_around(df):
    for col_name in df.columns:
        df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].apply(lambda x: x.strip())
        df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].apply(fix_space_only)
    return df


# replace ',' with a '.'
def put_dot(df):
    for col_name in df.columns:
        df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].apply(lambda x: x.replace(',','.'))
    return df


# Change ',50' to '0,50'
def add_zero(value):
    if value[0] == ',':
        return '0' + value
    else:
        return value

def correct_missing_zero(df, col_name):
    df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].apply(add_zero)
    return df


# Replace all other missing values by "NULL"
def replace_missing(df):
    for name in df.columns:
        df.loc[df[name].isnull(), name] = 'NULL'
    return df


# Patients sans mesure de poids (impossible de calculer un IMC sans poids)
def get_ippr_sans_poids():
    return poids.loc[(poids['Poids'] == 'NULL') & (poids['Age_patient_à_la_saisie_du_poids'] == 'NULL'), 'IPPR']

# Si on cherche uniquement à travailler sur la variation de l'IMC, il faut minimum deux messures de poids
# Donc les patients avec une seule mesure de poids sont inutiles
def get_ippr_one_poids():
    return poids.groupby('IPPR').filter(lambda x: len(x) == 1)['IPPR']


# Fonction qui sert à supprimer les patients dont l'IPPR appartient à la liste entrée en argument
def suppr_ippr(df, ippr_list):
    df = df.drop(df[df['IPPR'].isin(ippr_list)].index)
    return df.reset_index(drop=True)


ippr_list_sans_poids = get_ippr_sans_poids()
ippr_list_one_poids = get_ippr_one_poids()


# <//////////////////////////////////// CLEANING ////////////////////////////////////>
    
def cleaning_poids(df):
    df = replace_missing(df)
    df = remove_spaces_around(df)
    df = put_dot(df)
    df = replace_missing(df)
    df = suppr_ippr(df, ippr_list_sans_poids)
    df = suppr_ippr(df, ippr_list_one_poids)
    df = correct_missing_zero(df, 'Poids')
    return df.reset_index(drop=True)

poids = cleaning_poids(poids)

poids.to_csv('clean_poids.csv', index=False)


print()
print('APRÈS UN PREMIER NETTOYAGE DES DONNÉES, IL RESTE :')
print(' -', poids.loc[poids['Poids'] != 'NULL', 'IPPR'].nunique(), 'patients dans la table "Poids"')
print()
# --------------------------------------------------------------------------------
stop = timeit.default_timer()
print()
print('Time: ', stop - start, 's')  
