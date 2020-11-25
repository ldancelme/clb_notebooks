# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:42:30 2020

@author: LOX
"""

import pandas as pd
import numpy as np

data = pd.read_csv('../../data/clean_poids.csv')

data = data.sort_values(by='Poids', ascending=False)

#             IPPR  Poids
# 989224  38529311  710.0
# 119100   9785945  565.0
# 730246  71150564  485.0
# 227424    159753  300.0
# 745075  39166476  220.0
# 745089  39166476  215.0
# 745087  39166476  215.0
# 745084  39166476  215.0
# 182849   3027099  212.0
# 745088  39166476  212.0