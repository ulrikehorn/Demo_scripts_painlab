#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import data, logging, visual, core, event, gui, monitors
from numpy import random
import pandas as pd
import os  # handy system and path functions
import sys  # to get file system encoding
import parallel # for interaction with parallel port
import pylink # for eyelink communication
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy # for eyelink routine configuration
 # the file EyeLinkCoreGraphicsPsychoPy.py has to be in the same folder!

# used computer has a parallel port (for sending triggers to digitimer and brainamp)
parallel_port_mode = False
# testing mode or original speed (times written below)
testing_mode = T
# connect with a real eye tracker or not?
dummyMode = True # Simulated connection to the tracker; press ESCAPE to skip calibration/validataion

# how long the trigger signal to digitimer and brainamp should be
trigger_dur = 0.01

# waiting times
iti_test = 1.5
#iti_orig = 10 ~8 (jittered)
cue_time = 3.5
stim_time = 0.5

# establish a link to the tracker
if not dummyMode: 
    tk = pylink.EyeLink('100.1.1.1')
else:
    tk = pylink.EyeLink(None)
    
# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Make data folder
if not os.path.isdir("data"):
    os.makedirs("data")

# where are the cue pictures
pathCues = 'Pictures/'

# Store info about the experiment session
expName = 'Conditioning_task'
expInfo = {'Subject':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr(format='%Y%m%d_%H%M')  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = thisDir + os.sep + 'data' + os.sep + '%s_%s_%s' % (expInfo['Subject'], expInfo['expName'], expInfo['date'])

# in the DOS system you can only store up to 8 characters for the file name 
edf_running_name = expInfo['Subject'] + '.EDF'
# save on the other PC with a proper file name like all the other file types
edf_save_filename = filename + '.edf'

tk.openDataFile(edf_running_name)
# add personalized data file header (preamble text)
tk.sendCommand("add_file_preamble_text 'Conditioning task IMPRS workshop'") 

# An ExperimentHandler isn't essential but helps with data saving
exp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

trials = data.TrialHandler(nReps=1.0, method='sequential',
    trialList=data.importConditions('conditioning_randomized.csv'),
    name='Trials')

# add this structure to the experiment
exp.addLoop(trials)

# set screen properties
scnWidth, scnHeight = (1920, 1080)

# define monitor for correct eye tracking
mon = monitors.Monitor('basement', width=53.0, distance=46.0)
mon.setSizePix((scnWidth, scnHeight))

# experimenter monitor
winexp = visual.Window((1500, 800), fullscr=False, screen = 0, color=[0.4,0.4,0.4], units='pix', allowStencil=True,autoLog=False, waitBlanking = False)

# subject monitor
win = visual.Window((scnWidth, scnHeight), fullscr=False, monitor=mon, screen = 1, color=[0.4,0.4,0.4], units='pix', allowStencil=True,autoLog=False, waitBlanking = False, allowGUI=False)

# call the custom calibration routine "EyeLinkCoreGraphicsPsychopy.py", instead of the default
# routines that were implemented in SDL
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# create all objects: text, image, dot, clock, rating scale
textObj = visual.TextStim(win, units = "pix", text="", color="black", height=30)
textObjExp = visual.TextStim(winexp, units = "pix", text="", color="black", height=20)
imageObj = visual.ImageStim(win, units = "pix")
dotObj = visual.Circle(win=win, fillColor="white", lineColor="white",radius=[10,10],units="pix")

timerAttention = core.Clock() #for reaction time in attention trials
timerTrigger = core.Clock() # for duration of messages and triggers to digitimer

if parallel_port_mode:
    # the port for communication with digitimer and brainamp
    p_port1 = parallel.Parallel(port = 1)

## Set up the tracker
tk.setOfflineMode() # we need to put the tracker in offline mode before we change its configurations
tk.sendCommand('sample_rate 500') #250, 500, 1000
# inform the tracker the resolution of the subject display
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))
# save display resolution in EDF data file for Data Viewer integration purposes
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))
# specify the calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical), 
tk.sendCommand("calibration_type = HV9") 
# specify the proportion of subject display to calibrate/validate (OPTIONAL, useful for wide screen monitors)
#tk.sendCommand("calibration_area_proportion 0.85 0.83")
#tk.sendCommand("validation_area_proportion  0.85 0.83")
# the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (1000/1000Plus/DUO)
eyelinkVer = tk.getTrackerVersion()
# Set the tracker to parse Events using "GAZE" (or "HREF") data
tk.sendCommand("recording_parse_type = GAZE")
# Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
# [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
if eyelinkVer>=2: tk.sendCommand('select_parser_configuration 0')
# get Host tracking software version
hostVer = 0
if eyelinkVer == 3:
    tvstr  = tk.getTrackerVersionString()
    vindex = tvstr.find("EYELINK CL")
    hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
# specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
if hostVer>=4: 
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
    tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
else:          
    tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

## define all parts of the experiment as different functions
def itiRoutine(iti_time):
    dotObj.pos = (0,0)
    dotObj.setFillColor("white")
    dotObj.setLineColor("white")
    dotObj.draw()
    win.flip()
    # send message to tracker when ITI begins
    tk.sendMessage('iti_onset')
    if testing_mode:
        core.wait(iti_test)
    else:
        core.wait(iti_time)

## pain as argument
def cueRoutine(pain):
    if (pain == 'pain'):
        file = pathCues + 'pain.jpg'
    elif (pain == 'no pain'):
        file = pathCues + 'no_pain.jpg'
    else:
        print('Something went wrong with the pain coding in the conditions file')
    try:
        imageObj.setImage(file)
    except FileNotFoundError:
        print('The image could not be found!')
    imageObj.draw()
    dotObj.draw()
    win.flip()
    textObjExp.setText(pain)
    textObjExp.draw()
    winexp.flip()
    # send message to tracker
    if (pain == 'pain'):
        tk.sendMessage('pain_cue')
    else:
        tk.sendMessage('no_pain_cue')
    # send trigger to BrainAmp and then wait
    if parallel_port_mode:
        timerTrigger.reset()
        while timerTrigger.getTime() <= trigger_dur:
            p_port1.setData(int("000000001",2)) # sets pin 2 high
        p_port1.setData(0) #set all pins low
        core.wait(cue_time - trigger_dur)
    else:
        print('now I would send a trigger to the brainamp')
        core.wait(cue_time)
    # after anticipation there comes the attention/stimulation phase
    # still showing the image
    imageObj.draw()
    dotObj.draw()
    win.flip()
    winexp.flip()
    if (pain == 'pain'):
        # send message to tracker
        tk.sendMessage('trigger_onset')
        # begin heat/warm stimulation (send trigger to brainamp and digitimer)
        if parallel_port_mode:
            timerTrigger.reset()
            while timerTrigger.getTime() <= trigger_dur:
                p_port1.setData(int("00010100",2)) # sets pin 4 and 6 high
            p_port1.setData(0) #set all pins low
            core.wait(stim_time - trigger_dur)
        else:
            print('now I would send a trigger to the brainamp and digitimer')
            core.wait(stim_time)
    else:
        core.wait(stim_time)


##----------Experiment section--------------
# Start experiment with space keys, later: trigger start by scanner
textObjExp.setText("Space to start experiment\n")
textObjExp.setHeight(20)
textObjExp.draw()
winexp.flip()
event.waitKeys(keyList=["space"])

textObjExp.setText("Enter to start calibration, \ncontinue with C, V and Esc")
textObjExp.draw()
winexp.flip()

if not dummyMode:
    # set up the camera and calibrate the tracker at the beginning of each block
    tk.doTrackerSetup()

# give start signal to thermode here to run a particular block
# give signal to brain amp when a new block starts
# give signal to eyetracker when a new block starts
# take the tracker offline
tk.setOfflineMode()
pylink.pumpDelay(50)

# send the standard "TRIALID" message to mark the start of a trial
# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
tk.sendMessage('TRIALID')

# start recording, parameters specify whether events and samples are
# stored in file, and available over the link
error = tk.startRecording(1,1,1,1)
pylink.pumpDelay(100) # wait for 100 ms to make sure data of interest is recorded

textObjExp.setText("Started recording")
textObjExp.draw()
winexp.flip()

# run the trials as given in the trial handler
for trial in trials:
    # abbreviate parameter names if possible (e.g. attention = trial.attention)
    if trial != None:
        for paramName in trial.keys():
            exec(paramName + '= trial.' + paramName)
        itiRoutine(iti_time)
        cueRoutine(pain)
        exp.nextEntry()

itiRoutine(iti_time)

# send a message to mark the end of trial
# [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
tk.sendMessage('TRIAL_RESULT')
pylink.pumpDelay(100)
tk.stopRecording() # stop recording
    
# close the EDF data file
tk.setOfflineMode()
tk.closeDataFile()
pylink.pumpDelay(50)

# Get the EDF data and say goodbye
textObjExp.setText("Transfer data")
textObjExp.draw()
winexp.flip()
textObj.setText('The experiment is over.')
textObj.draw()
win.flip()
tk.receiveDataFile(edf_running_name, edf_save_filename)

# close the link to the tracker
tk.close()

# close the graphics
pylink.closeGraphics()
win.close()
core.quit()
