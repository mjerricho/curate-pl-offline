from psychopy import core, visual, gui, data, event
import numpy
from random import random

# create window and stimuli
win = visual.Window([1500,900],allowGUI=True,
                    monitor='testMonitor', units='deg')
foil = visual.GratingStim(win, sf=1, size=4, mask='gauss')
target = visual.GratingStim(win, sf=1, size=4, mask='gauss')
fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                              tex=None, mask='cross', size=0.2)
noise = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg')

target.draw()
noise.draw()
win.flip()
event.waitKeys()
               
               