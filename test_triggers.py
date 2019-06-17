#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, data, visual
import parallel

# how long the trigger signal to the device should be (in s)
trigger_dur = 0.01

# which port to use (default 0)
p_port = parallel.Parallel(port = 1)

# how many pain stimuli you want to send
num_trigger = 20

# of how many trains should one pain stimulus consist
num_trains = 3

# how much time between triggers (in s)
iti = 5.0

# Setup the Window
win = visual.Window(
    size=(1500, 800), fullscr=False, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0.4,0.4,0.4], colorSpace='rgb',
    blendMode='avg', useFBO=True)

dotObj = visual.Circle(win=win, fillColor="white", lineColor="white",radius=[10,10],units="pix")

timerTrigger = core.Clock() # for duration of triggers

# trial handler
trials = data.TrialHandler(nReps=num_trigger, method='random', 
    originPath=-1,
    trialList=[None],
    seed=None, name='trials')

thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

for thisTrial in trials:
    dotObj.setFillColor("white")
    dotObj.setLineColor("white")
    dotObj.draw()
    win.flip()
    core.wait(iti)
    dotObj.setFillColor("red")
    dotObj.setLineColor("red")
    dotObj.draw()
    win.flip()
    for itrain in range(num_trains):
        timerTrigger.reset()
        while timerTrigger.getTime() <= trigger_dur:
            p_port.setData(int("000010000",2)) # sets pin 6 high
        p_port.setData(0) #set all pins low
        core.wait(0.04)

win.close()
core.quit()