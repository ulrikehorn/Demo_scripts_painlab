#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from psychopy import data, logging, visual, core, event, gui, monitors
import os  # handy system and path functions
import sys  # to get file system encoding

# how fast letters are displayed
speed = 0.75

# how many blocks you want to do maximum
num_blocks = 10

# 1back or 2back task
back_n = 2

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Make data folder
if not os.path.isdir("data"):
    os.makedirs("data")

# where are the pictures for the explanation
pathExplanation = 'Pictures/'

filename = thisDir + os.sep + 'data' + os.sep + 'nback_training_result'

# An ExperimentHandler isn't essential but helps with data saving
exp = data.ExperimentHandler(name='Nback', version='',
    runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True,
    dataFileName=filename)

SCREEN_SIZE = (1920,1080)
# window for experimenter
winexp = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    color=[0.5,0.5,0.5], colorSpace='rgb', waitBlanking = False)
# window for subject
winsub = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=1,
    allowGUI=False, allowStencil=False,
    color=[0.5,0.5,0.5], colorSpace='rgb', waitBlanking = False)

textObjexp = visual.TextStim(win=winexp, text="", color="black", height = 0.1, pos=(0.0, 0.0))
textObjexp2 = visual.TextStim(win=winexp, text="", color="black", height = 0.1, pos = (0.0, 0.5))
textObjsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1)
scoreTextsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1, pos = (-0.4, 0.75))
overallscoreTextsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1, pos = (0.4, 0.75))
headlineTextsub = visual.TextStim(win=winsub, color="black", height = 0.15, pos = (0.0, 0.85), bold = True)
if back_n==2:
    imagefile = thisDir + os.sep + pathExplanation + os.sep + '2back_explanation_transp.png'
    headlineTextsub.setText('2-back task')
elif back_n==1:
    imagefile = thisDir + os.sep + pathExplanation + os.sep + '1back_explanation_transp.png'
    headlineTextsub.setText('1-back task')
else:
    print('Only 1 and 2 back tasks are supported')
    winsub.close()
    winexp.close()
    core.quit()
imagesub = visual.ImageStim(win = winsub, image = imagefile, pos = (0, 0.5))

timerResponse=core.Clock() #for reaction time

def taskRoutine(score):
    textObjexp.setText(letter)
    textObjexp.draw()
    textObjexp2.draw()
    winexp.flip()
    scoreTextsub.draw()
    textObjsub.setText(letter)
    textObjsub.draw()
    pressed = False # to track whether subject has pressed a key
    event.clearEvents() # keypresses cleared
    timerResponse.reset() # timer set to 0
    winsub.flip()
    # wait several ms while the letter is shown
    while timerResponse.getTime()<=speed:
        response = event.getKeys(timeStamped=timerResponse)
        if response and not pressed:
            pressed = True
            trials.addData('rt',response[0][1])
            if target==1.0:
                textObjexp2.setText('target hit!')
                trials.addData('response',1)
                score = score + 15
                scoreTextsub.setText('Score:  '+str(score))
                scoreTextsub.draw()
                textObjsub.draw()
                winsub.flip()
            else:
                textObjexp2.setText('incorrectly pressed')
                trials.addData('response',-1)
                score = score - 5
                scoreTextsub.setText('Score:  '+str(score))
                scoreTextsub.draw()
                textObjsub.draw()
                winsub.flip()
    # and then wait a bit more while the letter is not shown anymore
    scoreTextsub.draw()
    winsub.flip()
    while timerResponse.getTime()<= 2*speed:
        response = event.getKeys(timeStamped=timerResponse)
        if response and not pressed:
            pressed = True
            trials.addData('rt',response[0][1])
            if target==1.0:
                textObjexp2.setText('target hit!')
                trials.addData('response',1)
                score = score + 12
                scoreTextsub.setText('Score:  '+str(score))
                scoreTextsub.draw()
                winsub.flip()
                winexp.flip()
            else:
                textObjexp2.setText('incorrectly pressed')
                trials.addData('response',-1)
                score = score - 5
                scoreTextsub.setText('Score:  '+str(score))
                scoreTextsub.draw()
                winsub.flip()
                winexp.flip()
    if not pressed:
        trials.addData('rt',np.nan)
        if target==1.0:
            textObjexp2.setText('target missed!')
            trials.addData('response',-2)
            score = score - 5
            scoreTextsub.setText('Score:  '+str(score))
            scoreTextsub.draw()
            winsub.flip()
            winexp.flip()
        else:
            textObjexp2.setText('no target')
            trials.addData('response',0)
            winexp.flip()
    trials.addData('score',score)
    return score

def feedbackRoutine(overall_score):
    hits = sum(trials.data['response']==1)[0]
    missed = sum(trials.data['response']==-2)[0]
    incorrect = sum(trials.data['response']==-1)[0]
    if missed==0 and incorrect ==0:
        result_text = "You made no mistakes!\nVery good!"
    elif missed==0 and incorrect>0:
        result_text = "You detected all {} targets but incorrectly pressed {} times.".format(hits, incorrect)
    elif missed>0 and hits>0 and incorrect==0:
        result_text = "You missed {} targets!\nYou detected {} target(s).".format(missed,hits)
    elif missed>0 and hits>0 and incorrect>0:
        result_text = "You missed {} targets!\nYou detected {} target(s).\nYou incorrectly pressed the key {} times.".format(missed,hits,incorrect)
    else:
        result_text = "You missed {} targets!\nYou incorrectly pressed the key {} times.".format(missed,incorrect)
    textObjsub.setText(result_text)
    textObjsub.draw()
    scoreTextsub.draw()
    overallscoreTextsub.setText('Overall score:  '+str(overall_score))
    overallscoreTextsub.draw()
    winsub.flip()
    event.waitKeys()


##----------Experiment section--------------
overall_score = 0
for iblock in range(num_blocks):

    # set up handler to deal with trials
    # trials have the correct randomized order, so just read them sequentially
    trial_file = str(back_n)+'back_randomized_training.csv'
    blockdf = pd.read_csv(trial_file, sep=',', header=0)
    indices = blockdf[blockdf['block'] == iblock].index.tolist()
    # selected to many blocks
    if not indices:
        textObjsub.setText('Overall score:  '+str(overall_score)+'\nGoodbye!')
        textObjsub.draw()
        winsub.flip()
        core.wait(2)
        winsub.close()
        winexp.close()
        core.quit()
    # otherwise add these trials 
    trials = data.TrialHandler(nReps=1.0, method='sequential',
        trialList=data.importConditions(trial_file,selection = indices),
        name='Trials')
    # add this structure to the experiment
    exp.addLoop(trials)
    
    # Start block with space keys
    imagesub.draw()
    headlineTextsub.draw()
    startText = "Press space to start, escape to exit\n"
    textObjsub.setText(startText)
    textObjsub.draw()
    winsub.flip()
    startkey = event.waitKeys(keyList=["space","escape"])
    if startkey[0]=='escape':
        textObjsub.setText('Overall score:  '+str(overall_score)+'\nGoodbye!')
        textObjsub.draw()
        winsub.flip()
        core.wait(2)
        winsub.close()
        winexp.close()
        core.quit()
    else:
        score = 0
        scoreTextsub.setText('Score:  '+str(score))
        scoreTextsub.draw()
        winsub.flip()
        # run the trials as given in the trial handler
        for trial in trials:
            # abbreviate parameter names if possible (e.g. letter = trial.letter)
            if trial != None:
                for paramName in trial.keys():
                    exec(paramName + '= trial.' + paramName)
            score = taskRoutine(score)
            exp.nextEntry()
        overall_score = overall_score + score
        feedbackRoutine(overall_score)

textObjsub.setText('Overall score:  '+str(overall_score)+'\nGoodbye!')
textObjsub.draw()
winsub.flip()
core.wait(2)
winsub.close()
winexp.close()
core.quit()
