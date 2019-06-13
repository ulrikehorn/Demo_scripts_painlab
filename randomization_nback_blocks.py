#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

# number of blocks for one condition (hot/warm):
num_blocks = 20 # must be divisible by 2 for same number of control and nback tasks

conditions = pd.DataFrame({'task': ['control','nback']})
num_conditions = conditions.shape[0]

np.random.seed(16)
result = pd.DataFrame(columns = conditions.columns)

# do the same thing for hot and warm stimuli
for stim_cond in range(2):
    conditions = pd.DataFrame({'task': ['control','nback']})
    conditions = pd.concat([conditions]*(num_blocks/num_conditions),ignore_index=True)
    print(conditions)
    conditions_not_met = True
    for iblock in range(num_blocks):
        sample = conditions.sample(n=1)
        result = result.append(sample, ignore_index = True) # add this sample
        conditions = conditions.loc[~conditions.index.isin(sample.index)]

# add a column for the stimulus condition (first half hot, second half warm)
stim = pd.Series(np.concatenate((np.repeat('hot',num_blocks),np.repeat('warm',num_blocks))))
result = result.assign(stim = stim)

print(result)
# write to file
result.to_csv('nback_run_order_randomized.csv', index = False)
print('saved')