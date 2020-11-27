# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:36:55 2020

@author: DANCEL
"""

import pandas as pd
import numpy as np



data = pd.read_csv('../all_data.csv')

ipprs = data.IPPR.unique()
