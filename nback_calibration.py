#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from psychopy import data, logging, visual, core, event, gui, monitors
import os  # handy system and path functions
import sys  # to get file system encoding
import parallel # for interaction with parallel port
from pyglet.window import key # for keystate handling
import matplotlib.pyplot as plt # for plotting the results

# testing mode or original speed (times written below)
testing_mode = True

# how long should the ttl pulse be?
trigger_dur = 0.01
# How long is the stimulation programmed?
stimulation_dur = 20.5
# How much time the subjects need for rating
time_for_rating = 7

iti_time = 6

#temps = np.array([42, 44, 40, 45, 46, 39, 41, 47, 43])
temps = np.array([42, 44, 40, 45, 46])
ratings = np.empty(len(temps))
ratings[:] = np.nan

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Make data folder
if not os.path.isdir("data"):
    os.makedirs("data")
    
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = thisDir + os.sep + 'data' + os.sep + 'Calibration_plot'

expMonitor = monitors.Monitor('monitor0')
SCREEN_SIZE = (1920,1080)
# window for experimenter
winexp = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    monitor=expMonitor, color=[0.4,0.4,0.4], colorSpace='rgb', waitBlanking = False)
# window for subject
winsub = visual.Window(
    SCREEN_SIZE, fullscr=False, screen=1,
    allowGUI=False, allowStencil=False,
    monitor=expMonitor, color=[0.4,0.4,0.4], colorSpace='rgb', waitBlanking = False)

infotextObjexp = visual.TextStim(win=winexp, text="", color="black", height = 0.06)
textObjsub = visual.TextStim(win=winsub, text="", color="black", height = 0.06)
# fixation cross:
fixObj = visual.ShapeStim(win = winsub, units = 'pix', pos = (0,0),
vertices=((0, -50), (0, 50), (0,0), (-50,0), (50, 0)),
    lineWidth=7,closeShape=False,lineColor="black")
ratingPain = visual.RatingScale(win = winsub, low = 0, high = 100, markerStart = 50, 
marker = 'slider', stretch = 1.5, tickHeight = 1.5, tickMarks = [0,50,100],
labels = [u'not noticable', 'pain threshold', u'not bearable'],
showAccept = False, lineColor='black', textColor='black', textSize=0.8)

keyState=key.KeyStateHandler() # to check the key status when using the keyboard mode
winsub.winHandle.push_handlers(keyState)

timerTrigger = core.Clock() # for duration of messages and triggers to brain amp and thermode
timerRating=core.Clock() #for rating reaction time
timerGetKeys = core.Clock() # when to register another key press for continuous moving of rating scale

# the port for communication with thermode
p_port1 = parallel.Parallel(port = 1)

# define all parts of the experiment as different functions
def itiRoutine():
    # wait before you continue 
    fixObj.draw()
    winsub.flip()
    infotextObjexp.draw() #last rating
    winexp.flip() 
    core.wait(iti_time)

def stimulationRoutine():
    infotextObjexp.setText(u'Stimulation')
    infotextObjexp.draw()
    winexp.flip()
    winsub.flip() # dot disappears
    timerTrigger.reset()
    while timerTrigger.getTime() <= trigger_dur:
        p_port1.setData(int("00000100",2)) # sets pin 4 high
        #p_port1.setData(int("00000001",2)) # sets pin 2 high
    p_port1.setData(0) #set all pins low
    core.wait(stimulation_dur)


def ratingRoutine():
    infotextObjexp.setText('Rating')
    infotextObjexp.draw()
    winexp.flip()
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
    timerRating.reset() # timer set to 0
    keys = None
    # for a certain time check which button has been pressed
    # change image accordingly 
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
                print('Do you use the correct button box / keys?')
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
    infotextObjexp.setText(rating)
    infotextObjexp.draw()
    winexp.flip()
    ratings[temp] = rating


def endRoutine():
    x = temps
    y = ratings
    #x = np.array([46.0, 46.0, 47.0, 44.0, 48.0, 49.5, 47.0])
    #y = np.array([30.0, 30.0, 65.0, 20.0, 83.0, 86.0, 60.0])
    arr1inds = x.argsort()
    x = x[arr1inds[::1]]
    y = y[arr1inds[::1]]
    
    # fit a regression first
    m,b = np.polyfit(x, y, 1) 
    # calculate the temperatures x corresponding to ratings 25 and 75
    temp_25 = (25-b)/m
    temp_75 = (75-b)/m
    print(temp_25)
    print(temp_75)
    
    plt.xlabel('temperature')
    plt.ylabel('ratings')
    plt.plot(x, y, 'yo', x, m*x+b, '--b',temp_25,25,'bo',temp_75,75,'bo') 
    plt.axis([38.5, 50.0, 0, 100])
    
    plt.savefig(filename+'.png',dpi=80,transparent=True)
    
    # for resulting plot
    img = visual.ImageStim(
    win=winexp,
    image=filename+".png",
    units="norm",
    pos = (0,0))

    img.draw()
    winexp.flip()
    textObjsub.setText("Well done! Calibration finished.")
    textObjsub.draw()
    winsub.flip()
    event.waitKeys(keyList=["space"])

##----------Experiment section--------------
# Start experiment with space keys
startText = "Leertaste um zu beginnen\n"
infotextObjexp.setText(startText)
infotextObjexp.draw()
winexp.flip()
event.waitKeys(keyList=["space"])
infotextObjexp.setText("")
infotextObjexp.draw()
winexp.flip()

# run the trials as given in the trial handler
for temp in range(len(temps)):
    itiRoutine()
    stimulationRoutine()
    ratingRoutine()
endRoutine()

winsub.close()
winexp.close()
core.quit()
