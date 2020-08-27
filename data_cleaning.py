#!/usr/bin/env python
# coding: utf-8

# # Nettoyage des données de Taille
# ----------------------
# ### PRETRAITEMENT et NETTOYAGE à partir des méthodes des élèves Centrale
# 
# `Import` de packages Python et démarrage du `timer` sur l'execution du script. Installation du package `xlwings` pour lire les fichier Excel (`.xlsx`).

# In[1]:


get_ipython().system('python -m pip install xlwings')

import pandas as pd
import numpy as np
import xlwings as xw
import matplotlib.pyplot as plt
import timeit
import os

start = timeit.default_timer()


# Importation du fichier et récupération de chaque onglet avec leurs infos pour pouvoir convertir.
# On est obligé de procéder de cette manière pour obtenir des dataframes à cause de la protection par mot de passe

# In[2]:


PATH = os.path.join('C:/Users/LOX/Desktop/CLB/test', 'Projet IMC v2.xlsx')
wb = xw.Book(PATH)

# La lettre correspond à la dernière colonne de l'onglet
# Le nombre correspond à la dernière ligne de l'onglet

taille_sheet = wb.sheets['Données evol - Taille ']
taille_max_letter = 'E'
taille_max_row = 571950

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
taille = transform_sheet_to_df(taille_sheet, taille_max_letter, taille_max_row)


# ### CONTRÔLE DE QUALITÉ ET DÉFINITION DES FONCTIONS
# 
# Tableau Récapitulatif de toutes les fonctions de Prétraitement et Nettoyage codées par les élèves de Centrale.
# _________
# | Processus | Définition | Fonction | Validation | Commentaires |
# |:-:|:-:|:-:|:-:|:-:|
# | *Suppression des doublons* | Supprime les lignes identiques dans le tableau | `pandas.DataFrame.drop_duplicates` | Fonctionne (ex : -23488   données de taille) | 0 général, 359 tabagisme, 43748 poids, 23902   taille, 1043 avis nutritionnel, 4 apa. Applicable à toute les données. |
# | *Suppression des lignes sans identifiant* | Supprime les lignes sans id patient (IPPR) | `Pandas.DataFrame.dropna` | Fonctionne | 2 général, 1 tabagisme,   1 poids, 1 taille, 1 avis nutritionnel, 1 apa. Applicable à toute les données. |
# | *Remplacement des champs vides* | Ajout de la valeur 'NULL' par défaut dans les champs vides et les champs avec uniquement des espaces | `replace_missing()` `fix_space_only()` | Fonctionne | Applicable à toute les données. |
# | *Suppression des espaces autours des valeurs* | Utilise la fonction strip pour éliminer les espaces superflus autour des valeurs | `remove_spaces_around()`   |     Fonctionne    | Applicable à toute les données. |
# | *Remplacement des virgules par des points* | Utilise la fonction replace change toutes les valeurs décimales avec virgule par des points | `put_dot()` |     Fonctionne    | S’applique à toute donnée numérique décimale. |
# | *Ajout du zéro absent sur les valeurs décimales* | Pour les nombres   décimaux < 1 sans 0. *,5 devient 0,5*    | `add_zero()` `correct_missing_zero()` | Fonctionne | S’applique à toute donnée numérique décimale. |
# | *Passage des valeurs négatives et positives* | Les valeurs numériques   négatives deviennent positives | `to_positive()`   `change_negative_value()` | Fonctionne | Uniquement pour   certaines données. Ex : l’âge d’un patient ne peut pas être en négatif. |
# | *Passage X en Majuscule* | X =  'non déterminé' ou 'non évaluable' *x devient X* | `put_maj_x()` `standardize_x()` | Fonctionne | S'applique aux données TNM uniquement. |
# | *Remplacement de certaines valeurs aberrantes* | Détail : **T** : 'is' devient 0 ; 'IS' devient 0 ; '9' devient 0 ; 'a' et 'T' deviennent ; NULL. **N** : '-' devient 0 ; '+', '°', '_', 'B', '4' et '6' deviennent NULL. **M** : Valeurs > 1 deviennent 1 | `fix_M()` `fix_TNM()` `fix_last_weird_values()` | Fonctionne | Vérifier que ces valeurs n’ont aucun intérêt médical et peuvent être remplacées. S'applique aux données TNM uniquement. |
# | *Simplification de la valeur du TNM* | Simplification de chaque lettre du TNM pour obtenir un TNM à 3 chiffres.    *Pour T : 2a devient 2* | `get_first_char()` `simplify_TNM()` | Fonctionne | Vérifier que ces   valeurs n’ont aucun intérêt médical et peuvent être remplacées. |
# | *Standardisation du format de taille* | Passage en m des tailles exprimées cm    *180 (cm) devient 1.80 (m)* | `add_dot()` `check_format()` | Fonctionne | S'applique aux données de taille uniquement. |
# 
# 
# *Note* : Dans ce Notebook on traite uniquement les données de taille

# In[3]:


# Delete duplicate data
# Formula: taille = taille.drop_duplicates().reset_index(drop=True)

# Replace all other missing values by "NULL"
def replace_missing(df):
    for name in df.columns:
        df.loc[df[name].isnull(), name] = 'NULL'
    return df
# Formula: taille = replace_missing(taille)

    
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

# Change ',50' to '0.50'
def put_dot(df):
    for col_name in df.columns:
        df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].astype(str).apply(lambda x: x.replace(',','.'))
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

def add_dot(value):
    if len(value) > 1:
        if value[1] == '.':
            return value
        else:
            return value[0] + '.' + value[1:]
    else:
        return value

def add_dot_73_5(value):
    if len(value) == 4 and value[2] == '.':
        return '0.' + value[0] + value[1]
    else:
        return value

def check_format73_5(df):
    # df['Taille'] = df['Taille'].apply(add_dot1)
    df['Taille'] = df['Taille'].apply(add_dot_73_5)
    return df

def check_format(df):
    # df['Taille'] = df['Taille'].apply(add_dot1)
    df['Taille'] = df['Taille'].apply(add_dot)
    return df

# Change les ages négatifs pour les passer en positif
def to_positive(age):
    if float(age) < 0:
        return str(-float(age))
    else:
        return age
    
def change_negative_value(df, col_name):
    df.loc[df[col_name] != 'NULL', col_name] = df.loc[df[col_name] != 'NULL', col_name].apply(to_positive)
    return df

# Patients sans mesure de taille (impossible de calculer un IMC sans taille)
def get_ippr_sans_taille():
    return taille.loc[(taille['Taille'] == 'NULL') & (taille['Age_patient_à_la_saisie_de_la_taille'] == 'NULL'), 'IPPR']


# Fonction qui sert à supprimer les patients dont l'IPPR appartient à la liste entrée en argument
def suppr_ippr(df, ippr_list):
    df = df.drop(df[df['IPPR'].isin(ippr_list)].index)
    return df.reset_index(drop=True)

ippr_list_sans_taille = get_ippr_sans_taille()


# ### Nettoyage du dataset
# Enregistrement du tableau des données de taille dans un fichier *clean_taille.csv* au format `.csv`.
# Trop de ligne dans le dataset pour enregister au format `.xlsx`.
# Taille du tableau final = 571949x5

# In[4]:


def cleaning_taille(df):
    print('Execution des fonctions de nettoyage et prétraitement \n=====================================================')
    df = df.drop_duplicates()
    print('Duplicates dropped')
    df = df.dropna(subset=['IPPR'])
    print('Missing IPPR removed')
    df = replace_missing(df)
    print('Missing value treated')
    df = remove_spaces_around(df)
    print('Spaces in value removed')
    df = correct_missing_zero(df, 'Taille')
    print('Missing zero added')
    df = put_dot(df)    
    print('Dot put instead of coma')
    df = suppr_ippr(df, ippr_list_sans_taille)
    print('Patient without height removed')
    df = change_negative_value(df, 'Age_patient_à_la_saisie_de_la_taille')
    print('Negatives values changed to positive')

    return df.reset_index(drop=True)

taille = cleaning_taille(taille)

# Special cleaning taille
taille = check_format73_5(taille)
print('taille format73_5 check')

taille = check_format(taille)
print('taille format check')

print()
print('APRES LE NETTOYAGE DES DONNÉES, IL Y A :')
print(' -', (taille['Taille'] != 'NULL').sum(), 'données de taille saisies sur', taille.shape[0], 'lignes dans la table')
print(' -', taille.loc[taille['Taille'] != 'NULL', 'IPPR'].nunique(), 'patients dans la table "Taille"')

taille.to_csv('clean_taille.csv', index=False)

# --------------------------------------------------------------------------------
print()
stop = timeit.default_timer()
print('Time:  ', str(round(stop - start, 4)), 's\n\t' + str(round((stop - start) / 60, 4)) + ' m ')

