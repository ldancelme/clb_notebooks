# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pandas as pd 
import numpy as np
from tqdm import tqdm

data = pd.read_csv("../data/all_data.csv")
data20 = data[data['age_at_entry'] <= 7300]
data20plus = data[data['age_at_entry'] > 7300]

def med_count(data):
    ipprs = data.IPPR.unique()
    c = []
    for i in tqdm(ipprs):
        x = data[data['IPPR']==i]
        count = np.array(x['count'])[0]
        c.append(count)
    med = np.median(c)
    return med

med = med_count(data)
med20 = med_count(data20)
med20plus = med_count(data20plus)

print('\n\n\nmed : {}\nmed20 : {}\nmed20plus: {}'.format(med, med20, med20plus))
    