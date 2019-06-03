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

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Make data folder
if not os.path.isdir("data"):
    os.makedirs("data")

filename = thisDir + os.sep + 'data' + os.sep + 'nback_experiment_result'

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
dotObj = visual.Circle(win=winsub, fillColor="white", lineColor="white",radius=[10,10],units="pix")
ratingPain = visual.RatingScale(win = winsub, low = 0, high = 100, markerStart = 50, 
marker = 'slider', stretch = 1.5, tickHeight = 1.5, tickMarks = [0,50,100],
labels = [u'nicht spürbar', 'Schmerzgrenze', u'unerträglich'],
showAccept = False, lineColor='black', textColor='black', textSize=0.8)
imagefile = thisDir + os.sep + '2back_explanation_transp.png'
imagesub = visual.ImageStim(win = winsub, image = imagefile, pos = (0, 0.5))

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

def controlRoutine():
    # Start block with space keys
    #imagesub.draw() --> control image
    headlineTextsub.setText('control task')
    headlineTextsub.draw()
    startText = "Press space to start\n"
    textObjsub.setText(startText)
    textObjsub.draw()
    winsub.flip()
    startkey = event.waitKeys(keyList=["space"])
    # run the trials as given in the trial handler
    for trial in trials:
        # abbreviate parameter names if possible (e.g. letter = trial.letter)
        if trial != None:
            for paramName in trial.keys():
                exec(paramName + '= trial.' + paramName)
        textObjexp.setText(letter)
        textObjexp.draw()
        winexp.flip()
        textObjsub.setText(letter)
        textObjsub.draw()
        winsub.flip()
        core.wait(speed)
        winexp.flip()
        winsub.flip()
        core.wait(speed)
        exp.nextEntry()
    rating = ratingRoutine()
    return rating

def taskRoutine():
    # Start block with space keys
    imagesub.draw()
    headlineTextsub.setText('2-back task')
    headlineTextsub.draw()
    startText = "Press space to start\n"
    textObjsub.setText(startText)
    textObjsub.draw()
    winsub.flip()
    startkey = event.waitKeys(keyList=["space"])
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
        textObjexp.setText(letter)
        textObjexp.draw()
        textObjexp2.draw()
        winexp.flip()
        textObjsub.setText(letter)
        textObjsub.draw()
        scoreTextsub.setText('Score:  '+str(score))
        scoreTextsub.draw()
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
        exp.nextEntry()
    rating = ratingRoutine()
    return score, rating

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
    textObjexp.setText(rating)
    textObjexp.draw()
    winexp.flip()
    return rating
    

##----------Experiment section--------------
# create lists to store subject's ratings and performance
overall_score = 0
ratings = np.empty(num_blocks)
for iblock in range(num_blocks):
    # set up handler to deal with trials
    # trials have the correct randomized order, so just read them sequentially
    blockdf = pd.read_csv('2back_randomized.csv', sep=',', header=0)
    indices = blockdf[blockdf['block'] == iblock].index.tolist()
    # add these trials 
    trials = data.TrialHandler(nReps=1.0, method='sequential',
        trialList=data.importConditions('2back_randomized.csv',selection = indices),
        name='Trials')
    
    # add this structure to the experiment
    exp.addLoop(trials)
    
    # alternate between control condition and task condition
    # TO DO: do that with another randomization file 
    if iblock % 2:
        rating = controlRoutine()
    else:
        score, rating = taskRoutine()
    ratings[iblock] = rating
    overall_score = overall_score + score
    itiRoutine()

# TO DO: analysis of ratings depending on condition

print(ratings)
winsub.close()
winexp.close()
core.quit()


