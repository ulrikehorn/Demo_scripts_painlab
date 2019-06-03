#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

num_blocks = 10
num_trials = 15
letter_list = ['A','B','C','D','E']
back_n = 1

np.random.seed(722)

result = pd.DataFrame(columns = ['letter','target','block'])
print(result)

for iblock in range(num_blocks):
    trial_seq = pd.DataFrame(columns = result.columns)
    rand_letters = np.array([])
    target = np.zeros(num_trials)
    for itrial in range(num_trials):
        rand_letters = np.append(rand_letters,np.random.choice(letter_list))
        if (itrial>= back_n) and (rand_letters[itrial] == rand_letters[itrial-back_n]):
            target[itrial] = 1
    trial_seq = trial_seq.assign(letter = rand_letters)
    trial_seq = trial_seq.assign(target = target)
    # add a column for the block number
    block_num = pd.Series(np.repeat(iblock,num_trials))
    trial_seq = trial_seq.assign(block = block_num)
    # add the trial sequence to the result structure
    result = result.append(trial_seq, ignore_index = True)

print(result)
file_name = str(back_n)+'back_randomized.csv'
result.to_csv(file_name, index = False)

