#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from psychopy import data, logging, visual, core, event, gui, monitors
from pyglet.window import key # for keystate handling
import os  # handy system and path functions
import sys  # to get file system encoding

# how fast letters are displayed
speed = 0.75

num_blocks = 3

# An ExperimentHandler isn't essential but helps with data saving
exp = data.ExperimentHandler(name='Nback', version='',
    runtimeInfo=None, originPath=None)

SCREEN_SIZE = (1920,1080)
# window for experimenter
winexp = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    color=[0,0,0], colorSpace='rgb', waitBlanking = False)
# window for subject
winsub = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=1,
    allowGUI=False, allowStencil=False,
    color=[0,0,0], colorSpace='rgb', waitBlanking = False)

textObjexp = visual.TextStim(win=winexp, text="", color="black", height = 0.06, pos=(0.0, 0.0))
textObjexp2 = visual.TextStim(win=winexp, text="", color="black", height = 0.06, pos = (0.0, 0.5))
textObjsub = visual.TextStim(win=winsub, text="", color="black", height = 0.06)
dotObj = visual.Circle(win=winsub, fillColor="white", lineColor="white",radius=[10,10],units="pix")
ratingPain = visual.RatingScale(win = winsub, low = 0, high = 100, markerStart = 50, 
marker = 'slider', stretch = 1.5, tickHeight = 1.5, tickMarks = [0,50,100],
labels = [u'nicht spürbar', 'Schmerzgrenze', u'unerträglich'],
showAccept = False)

keyState=key.KeyStateHandler() # to check the key status when using the keyboard mode
winsub.winHandle.push_handlers(keyState)

timerRating=core.Clock() #for rating time
timerResponse=core.Clock() #for reaction time

def itiRoutine():
    dotObj.pos = (0,0)
    dotObj.setFillColor("white")
    dotObj.setLineColor("white")
    dotObj.draw()
    winsub.flip()
    core.wait(5)

def taskRoutine():
    textObjexp.setText(letter)
    textObjexp.draw()
    textObjexp2.draw()
    winexp.flip()
    textObjsub.setText(letter)
    textObjsub.draw()
    timerResponse.reset() # timer set to 0
    winsub.flip()
    core.wait(speed)
    winsub.flip()
    core.wait(speed)
    response = event.getKeys(timeStamped=timerResponse)
    trials.addData('response',response) # and save it
    if target==1.0:
        if not response:
            textObjexp2.setText('target missed!')
        else:
            textObjexp2.setText('target hit!')
    else:
        if not response:
            textObjexp2.setText('no target')
        else:
            textObjexp2.setText('incorrectly pressed')
        textObjexp2.draw()
        winexp.flip()

def ratingRoutine():
    textObjsub.setText("Wie stark war dieser \n Schmerz?\n")
    textObjsub.draw()
    winsub.flip()
    ratingPain.reset()
    timeRating = 'NaN'
    # start in the middle of the scale
    currentPos = 50
    ratingPain.markerPlacedAt = currentPos
    ratingPain.draw()
    textObjsub.draw()
    winsub.flip()
    timerRating.reset() # timer set to 0
    keys = None
    # for a certain time check which button has been pressed
    # change image accordingly 
    time_for_rating = 8
    while timerRating.getTime() <= time_for_rating:
        # getKeys only checks where it has been pressed down once
        # use key state handler or implement timer how long you will want to
        # wait to count it as another press --> this does not work as we would want
        # to stop the timer when the key is released but getkeys does not track this!
        # problem with keystate in pyglet is that it is somehow related to a particular window
        # and therefore dependent on win flips?
        if keyState[key.LEFT]:
            keys = [(1, timerRating.getTime())]
        if keyState[key.RIGHT]:
            keys = [(2, timerRating.getTime())]
        if not keyState[key.LEFT] and not keyState[key.RIGHT]:
            keys = None
        if keys:
            timeRating = keys[0][1]
            # move left
            if keys[0][0] == 1:
                currentPos = currentPos - 1
                # move right
            elif keys[0][0] == 2:
                currentPos = currentPos + 1
            else:
                print('Do you use the correct keys?')
            # do not cross the borders of the scale
        if currentPos > 100:
            currentPos = 100
        elif currentPos < 0:
            currentPos = 0
        ratingPain.markerPlacedAt = currentPos
        ratingPain.draw()
        textObjsub.draw() 
        winsub.flip()
    rating = ratingPain.getRating() # get final rating 
    trials.addData('rating',rating) # and save it
    trials.addData('timeRating',timeRating) # save time of final rating
    textObjexp.setText(rating)
    textObjexp.draw()
    winexp.flip()
    ratings[trials.thisTrialN] = rating

##----------Experiment section--------------
for iblock in range(num_blocks):

    # set up handler to deal with trials
    # trials have the correct randomized order, so just read them sequentially
    blockdf = pd.read_csv('nback_randomized.csv', sep=',', header=0)
    indices = blockdf[blockdf['block'] == iblock].index.tolist()
    trials = data.TrialHandler(nReps=1.0, method='sequential',
        trialList=data.importConditions('nback_randomized.csv',selection = indices),
        name='Trials')
    
    # add this structure to the experiment
    exp.addLoop(trials)
    
    # Start experiment with space keys
    startText = "Press space to start\n"
    textObjsub.setText(startText)
    textObjsub.draw()
    winsub.flip()
    event.waitKeys(keyList=["space"])
    winsub.flip()
    
    # create lists to store subject's ratings
    ratings = np.empty(len(trials.trialList))
    
    # run the trials as given in the trial handler
    for trial in trials:
        # abbreviate parameter names if possible (e.g. letter = trial.letter)
        if trial != None:
            for paramName in trial.keys():
                exec(paramName + '= trial.' + paramName)
        taskRoutine()
        exp.nextEntry()
    
    ratingRoutine()
    itiRoutine()

winsub.close()
winexp.close()
core.quit()


