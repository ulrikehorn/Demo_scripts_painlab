#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from psychopy import data, logging, visual, core, event, gui, monitors
from pyglet.window import key # for keystate handling
import os  # handy system and path functions
import sys  # to get file system encoding
import parallel # for interaction with parallel port
#import matplotlib.pyplot as plt # for plotting the results

#----------------settings--------------------
# how long letters are displayed (in s)
speed = 0.75
# how long the fixation cross is shown in between (5s)
iti_time = 5
# how long the time for the rating scale is (8s)
rating_time = 8

# overall number of blocks, from which first half will be with pain
# second half only with warm stimulation (therefore provide value divisible by 2)
# max number possible: 40
num_blocks = 10

# for testing at a computer without parallel port change this:
parallel_port_mode = True

# pin to Thermode: 6
# how long the signal should be (in s)
thermode_trigger_dur = 0.01

#--------------------------------------------

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Make data folder
if not os.path.isdir("data"):
    os.makedirs("data")

# where are the pictures for the explanation
pathExplanation = 'Pictures/'

# Store info about the experiment session
expName = 'N-Back experiment'
expInfo = {'Subject':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['expName'] = expName

filename = thisDir + os.sep + 'data' + os.sep + 'nback_result_' + '%s' % (expInfo['Subject'])

# An ExperimentHandler isn't essential but helps with data saving
exp = data.ExperimentHandler(name=expName, version='',
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

# text for experimenter screen:
textObjexp = visual.TextStim(win=winexp, text="", color="black", height = 0.1, pos=(0.0, 0.0))
textObjexp2 = visual.TextStim(win=winexp, text="", color="black", height = 0.1, pos = (0.0, 0.5))
# text for subject (letter, score, overall_score, headline to display which task is upcoming)
textObjsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1)
scoreTextsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1, pos = (-0.4, 0.75))
overallscoreTextsub = visual.TextStim(win=winsub, text="", color="black", height = 0.1, pos = (0.4, 0.75))
headlineTextsub = visual.TextStim(win=winsub, color="black", height = 0.15, pos = (0.0, 0.65), bold = True)
# fixation cross:
fixObj = visual.ShapeStim(win = winsub, units = 'pix', pos = (0,0),
vertices=((0, -50), (0, 50), (0,0), (-50,0), (50, 0)),
    lineWidth=7,closeShape=False,lineColor="black")
# had a dot before:
#dotObj = visual.Circle(win=winsub, fillColor="white", lineColor="white",radius=[10,10],units="pix")
ratingPain = visual.RatingScale(win = winsub, low = 0, high = 100, markerStart = 50, 
marker = 'slider', stretch = 1.5, tickHeight = 1.5, tickMarks = [0,50,100],
labels = [u'not noticable', 'pain threshold', u'not bearable'],
showAccept = False, lineColor='black', textColor='black', textSize=0.8)
imagefile = thisDir + os.sep + pathExplanation + os.sep + '2back_explanation_transp.png'
imagesub = visual.ImageStim(win = winsub, image = imagefile, pos = (0, 0.35))

# to check the key status during rating
keyState = key.KeyStateHandler() 
winsub.winHandle.push_handlers(keyState)

timerRating = core.Clock() #for rating time
timerResponse = core.Clock() #for reaction time
timerTrigger = core.Clock() # for sending trigger to thermode

#initialize parallel port for communication with thermode
if parallel_port_mode:
    p_port1 = parallel.Parallel(port = 1)

# Inter trial interval with fixation cross
def itiRoutine():
    fixObj.draw()
    winsub.flip()
    # Save screenshot
    #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
    #winsub.saveMovieFrames('screenshot_iti.png')  # save with a descriptive and unique filename.     
    core.wait(iti_time)

# control task: show only letters
# and rating
def controlRoutine():
    # Start block with space keys
    #imagesub.draw() --> maybe make a control image as well?
    headlineTextsub.setText('control task')
    headlineTextsub.draw()
    winsub.flip()
    # Save screenshot
    #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
    #winsub.saveMovieFrames('screenshot_control_start.png')  # save with a descriptive and unique filename.     
    core.wait(2.5)
    winsub.flip()
    core.wait(0.5)
    timerTrigger.reset() # timer set to 0
    # begin heat/warm stimulation (send trigger to brainamp and thermode)
    if parallel_port_mode:
        while timerTrigger.getTime() <= thermode_trigger_dur:
            #p_port1.setData(int("00000001",2)) # sets pin 2 high
            #p_port1.setData(int("00010100",2)) # sets pin 4 and 6 high
            p_port1.setData(int("00010000",2)) # sets pin 6 high
        p_port1.setData(0) #set all pins low
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
        # Save screenshot
        #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
        #winsub.saveMovieFrames('screenshot_control_letter.png')  # save with a descriptive and unique filename.     
        core.wait(speed)
        winexp.flip()
        winsub.flip()
        core.wait(speed)
        #trials.addData('response',np.nan)
        #trials.addData('score',np.nan)
        #trials.addData('rt',np.nan)
        exp.nextEntry()
    rating = ratingRoutine()
    return rating

# show nback task with score for current run and overall score 
# collect any key presses while the letter is still visible (score +15)
# and also when the letter disappeared (score +12)
# also show rating 
def taskRoutine():
    # Start block with space keys
    imagesub.draw()
    headlineTextsub.setText('2-back task')
    headlineTextsub.draw()
    winsub.flip()
    # Save screenshot
    #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
    #winsub.saveMovieFrames('screenshot_task_start.png')  # save with a descriptive and unique filename.     
    core.wait(2.5)
    winsub.flip()
    core.wait(0.5)
    score = 0
    scoreTextsub.setText('Score:  '+str(score))
    scoreTextsub.draw()
    winsub.flip()
    timerTrigger.reset() # timer set to 0
    # begin heat/warm stimulation (send trigger to brainamp and thermode)
    if parallel_port_mode:
        while timerTrigger.getTime() <= thermode_trigger_dur:
            #p_port1.setData(int("00000001",2)) # sets pin 2 high
            #p_port1.setData(int("00010100",2)) # sets pin 4 and 6 high
            p_port1.setData(int("00010000",2)) # sets pin 6 high
        p_port1.setData(0) #set all pins low
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
        # Save screenshot
        #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
        #winsub.saveMovieFrames('screenshot_task_letter.png')  # save with a descriptive and unique filename.     
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
                    textObjexp2.draw()
                    winexp.flip()
                else:
                    textObjexp2.setText('incorrectly pressed')
                    trials.addData('response',-1)
                    score = score - 5
                    scoreTextsub.setText('Score:  '+str(score))
                    scoreTextsub.draw()
                    textObjsub.draw()
                    winsub.flip()
                    textObjexp2.draw()
                    winexp.flip()
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
                    textObjexp2.draw()
                    winexp.flip()
                else:
                    textObjexp2.setText('incorrectly pressed')
                    trials.addData('response',-1)
                    score = score - 5
                    scoreTextsub.setText('Score:  '+str(score))
                    scoreTextsub.draw()
                    winsub.flip()
                    textObjexp2.draw()
                    winexp.flip()
        if not pressed:
            if target==1.0:
                textObjexp2.setText('target missed!')
                trials.addData('response',-2)
                score = score - 5
                scoreTextsub.setText('Score:  '+str(score))
                scoreTextsub.draw()
                winsub.flip()
                textObjexp2.draw()
                winexp.flip()
            else:
                textObjexp2.setText('no target')
                trials.addData('response',0)
                textObjexp2.draw()
                winexp.flip()
        trials.addData('score',score)
        exp.nextEntry()
    rating = ratingRoutine()
    return score, rating

def ratingRoutine():
    textObjsub.setText("How intense \nwas this stimulation?\n")
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
    # Save screenshot
    #winsub.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
    #winsub.saveMovieFrames('screenshot_rating.png')  # save with a descriptive and unique filename.     
    timerRating.reset() # timer set to 0
    keys = None
    # for a certain time check which button has been pressed
    # change image accordingly 
    while timerRating.getTime() <= rating_time:
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

# read table with randomized task order
# in there are task and stimulation values
# (first half is hot, second half is warm)
# nback and control task are randomly distributed
taskdf = pd.read_csv('nback_run_order_randomized.csv', sep=',', header=0)
warm_task_index = taskdf[taskdf['stim']=='warm'].index[0]
task_bool_indices = np.concatenate((np.repeat(True,num_blocks/2),
    np.repeat(False,warm_task_index-num_blocks/2),np.repeat(True,num_blocks/2),
    np.repeat(False,warm_task_index-num_blocks/2)))

# start experiment with space key 
startText = "Press space to start\n"
textObjsub.setText(startText)
textObjsub.draw()
winsub.flip()
event.waitKeys(keyList=["space"])
itiRoutine()
score = 0
overall_score = 0
ratings = np.empty(num_blocks)
for iblock in range(num_blocks/2):
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
    
    # switch between control condition and task condition
    if taskdf['task'][iblock] == 'control':
        rating = controlRoutine()
    else:
        score, rating = taskRoutine()
    ratings[iblock] = rating
    overall_score = overall_score + score
    itiRoutine()

# after one half of the experiment switch stimulation to warm instead of painful
headlineTextsub.setText('Short break')
headlineTextsub.draw()
startText = "Next stimuli will not be painful.\nPress space to start this next block\n"
textObjsub.setText(startText)
textObjsub.draw()
winsub.flip()
event.waitKeys(keyList=["space"])

itiRoutine()
for iblock in range(num_blocks/2,num_blocks):
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
    
    # switch between control condition and task condition
    if taskdf['task'][warm_task_index] == 'control':
        rating = controlRoutine()
    else:
        score, rating = taskRoutine()
    ratings[iblock] = rating
    overall_score = overall_score + score
    itiRoutine()
    warm_task_index = warm_task_index+1


    #trials.addData('rating',rating)
    #print(trials.thisIndex)
    #print(trials.thisTrialN)
    #trials.data['score'][trials.thisIndex:trials.thisTrialN] = 5.0
    #print(trials.data['rating'])

ratingdf = pd.DataFrame({'Task':taskdf['task'][task_bool_indices], 'Rating':ratings, 'Stim':taskdf['stim'][task_bool_indices]})
ratingdf.to_csv(filename+'_ratings.csv', index = False)
#print(ratings)
# plot of ratings depending on condition
#data = np.transpose(np.array([ratings[::2],ratings[1::2]]))
#labels = list(['Control','Task'])
#fs = 10  # fontsize
#fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), sharey=True)
#axes.boxplot(data, labels=labels, showfliers=False)
#axes.set_title('Ratings', fontsize=fs)
#plt.ylim(0, 100)     # set the ylim to left, right
# add more plots by changing the nrows number and then accessing
# axes via axes[0].boxplot(data, labels=labels, showmeans=True) and axes[1]
#
#fig.subplots_adjust(hspace=0.4)
#plt.show()

winsub.close()
winexp.close()
core.quit()


