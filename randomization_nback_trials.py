#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

num_blocks = 30
num_trials = 15
letter_list = ['A','B','C','D','E']
back_n = 2

np.random.seed(722) # seed for task file 
#np.random.seed(723) # seed for training file

result = pd.DataFrame(columns = ['letter','target','block'])
conditions_met = False

for iblock in range(num_blocks):
    trial_seq = pd.DataFrame(columns = result.columns)
    rand_letters = np.array([])
    target = np.zeros(num_trials)
    for itrial in range(num_trials):
        conditions_met = False
        while not conditions_met:
            letter = np.random.choice(letter_list)
            if (itrial>= back_n) and (letter == rand_letters[itrial-back_n]):
                target[itrial] = 1
            else:
                target[itrial] = 0
            # not more than 3 times the same letter
            if (itrial>=3) and (letter == rand_letters[itrial-1] and letter == rand_letters[itrial-2] and letter == rand_letters[itrial-3]):
                conditions_met = False
            # not more than two targets in a row
            elif (itrial>=2) and (target[itrial]==1 and target[itrial-1]==1 and target[itrial-2]==1):
                conditions_met = False
            else:
                conditions_met = True
        rand_letters = np.append(rand_letters,letter)
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

