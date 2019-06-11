#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

#num_blocks = 20 # must be divisible by 4 as we have 4 conditions
num_blocks = 21 # must be divisible by 3 as we have 3 conditions

conditions = pd.read_csv('nback_run_order_not_randomized.csv', sep=',', header=0)
num_conditions = conditions.shape[0]
conditions = pd.concat([conditions]*(num_blocks/num_conditions),ignore_index=True)

np.random.seed(16)
result = pd.DataFrame(columns = conditions.columns)
conditions_not_met = True

for iblock in range(num_blocks):
    sample = conditions.sample(n=1)
    result = result.append(sample, ignore_index = True) # add this sample
    conditions = conditions.loc[~conditions.index.isin(sample.index)]

print(result)
# write to file
result.to_csv('nback_run_order_randomized.csv', index = False)
print('saved')