# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:34:05 2020

@author: Bhavyadeep Purswani
"""

import pandas as pd
df = pd.read_csv("train.csv")
print(df.mode())