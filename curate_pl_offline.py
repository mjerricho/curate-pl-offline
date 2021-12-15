# Curate-pl-offline implementation
# version: 14-12-21
# --------------------------------------------------------------------
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random

# getting parameters and other metadata ------------------------------
# getting experiment id
tempId= {'id': 'id'}
expId= ""
dlgId = gui.DlgFromDict(tempId, title='Curate offline Perceptual Learning')
if dlgId.OK:
    expId = tempId['id'].upper()
else:
    core.quit() # the user hit cancel so exit

# try to get a previous parameters file, create new one if it does not exist
try:  
    expInfo = fromFile(expId + 'lastParams.pickle')
except:  # if not there then use a default set
    expInfo = {'participantId': expId, 'sessionNo': 0, 'absRotation': 0, 'absNoise': 0}
    print("new experiment info created")

expInfo['dateStr'] = data.getDateStr()
expInfo['sessionNo'] = expInfo['sessionNo'] + 1 # increase the session number
#print(expInfo['sessionNo'])

# start updating parameters for training and testing -----------------
nTrials = 0
testType = ""
if expInfo['sessionNo'] < 2 or expInfo['sessionNo'] > 8 : 
    nTrials = 98
    testType = "3d1u"
else : 
    nTrials = 150
    testType = "scanner"
    
# make a text file to save data --------------------------------------
fileName = expInfo['participantId'] + "_" + expInfo['dateStr'] + "_sess_" + str(expInfo['sessionNo'])
dataFile = open(fileName + '.csv', 'w')  # a simple text file with 'comma-separated-values'
dataFile.write('dateStr, participantId,clockwise,correct, rt, sessionNo, trialNo, rotation, noise, triggerTime, responseStart, responseEnd\n')

# setting up parameters and instructions -------------------------------
# create window and stimuli
win = visual.Window([1500,900],allowGUI=True,
                    monitor='testMonitor', units='deg')
foil = visual.GratingStim(win, sf=1, size=4, mask='gauss')
target = visual.GratingStim(win, sf=1, size=4, mask='gauss')
fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                              tex=None, mask='cross', size=0.2)
                              
# and some handy clocks to keep track of time
globalClock = core.Clock()
trialClock = core.Clock()

# Introduction and reminder to read the instructions
message1 = visual.TextStim(win, pos=[0,+3],text='Hello, {}'.format(expInfo['participantId']), bold=True)
message2 = visual.TextStim(win, pos=[0,0], text="Please read the following instructions carefully.", units='pix', height=30)
message3 = visual.TextStim(win, pos=[0,-350], text="Press any key to continue.", units='pix', height=30)
message1.draw()
message2.draw()
message3.draw()
win.flip()
event.waitKeys() #pause until there's a keypress

# instruction
instructionText1 = 'In this experiment, you will see a white cross appear on the screen. Please focus your eyes on this circle about 2 feet (60cm) from your screen for the entirety of each session.'
instructionText2 = 'Two patterns will appear in quick succession over the cross. Your task is to determine whether the second pattern is tilted clockwise or anti-clockwise relative to the first. Move the joystick to the left if the second pattern is tilted anti-clockwise, and the right if it is tilted clockwise.'
message4 = visual.TextStim(win, pos=[0,+200],text=instructionText1, units='pix', height=19)
message5 = visual.TextStim(win, pos=[0,-100],text=instructionText2, units='pix', height=19)
message6 = visual.TextStim(win, pos=[0,-350], text="Press any key to continue.", units='pix', height=30)
message4.draw()
message5.draw()
message6.draw()
fixation.draw()
win.flip()
##pause until there's a keypress
event.waitKeys()

responseMessage = visual.TextStim(win, pos=[0,0], text="anti-clockwise (left) or clockwise (right)", units='pix', height=50)

# warm up  ----------------------------------------------------------
warmupMessage = visual.TextStim(win, pos=[0,0], text="This is just a warm up trial.", units='pix', height=50)
warmupMessage.draw()
win.flip()
core.wait(4)

# set up parameters
initialOri = 20
finalOri = 30
foil.setOri(initialOri)
target.setOri(finalOri)

# draw stimuli
fixation.draw()
win.flip()
core.wait(2)

foil.draw()
win.flip()
core.wait(2)
target.draw()
win.flip()
core.wait(2)

responseMessage.draw()
win.flip()
result = event.waitKeys()
print(result[0])
if result[0] == 'right':
    correctMessage = visual.TextStim(win, pos=[0,0], text="Correct! It was clockwise (right).", units='pix', height=50)
    correctMessage.draw()
    win.flip()
    core.wait(3)
else : 
    falseMessage = visual.TextStim(win, pos=[0,0], text="Wrong! It was clockwise (right).", units='pix', height=50)
    falseMessage.draw()
    win.flip()
    core.wait(3)

# training/testing phase ---------------------------------------------
targetSide = 0
difficultyRotation = 0
difficultyNoise = 0
streak = 0

# angle parameters

# first session
if expInfo['sessionNo'] == 1 : 
    for trialNo in range(nTrials) : 
        # get the change in angle
        targetSide = random.choice([-1,1]) 
        initialAngle = random.randrange(0,90)
        changeAngle = random.randrange(0,(40 - (2 * difficultyRotation)))
        finalAngle = initialAngle + (targetSide * changeAngle)
        
        # set up the gabor
        foil.setOri(initialAngle)
        noiseFoil = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=initialAngle, opacity=0)
        
        target.setOri(finalAngle)
        noiseTarget = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=finalAngle, opacity=0)

        # drawing the gabor
        fixation.draw()
        win.flip()
        core.wait(1)

        foil.draw()
        noiseFoil.draw()
        win.flip()
        core.wait(1)
        target.draw()
        noiseTarget.draw()
        win.flip()
        core.wait(1)
        
        responseMessage.draw()
        win.flip()
        trialClock.reset()
        
        reactionTime = 0
        thisResp=None
        while thisResp==None:
            allKeys=event.waitKeys()
            reactionTime = trialClock.getTime()
            for thisKey in allKeys:
                if thisKey=='left':
                    if targetSide==-1: thisResp = 1  # correct
                    else: thisResp = -1              # incorrect
                elif thisKey=='right':
                    if targetSide== 1: thisResp = 1  # correct
                    else: thisResp = -1              # incorrect
                elif thisKey in ['q', 'escape']:
                    core.quit()  # abort experiment
        
        dataFile.write('{dateStr}, {participantId}, {clockwise}, {correct}, {reactionTime}, {sessionNo}, {trialNo}, {rotation}, {noise}, NA, NA, NA\n'.format(dateStr = expInfo['dateStr'], participantId = expInfo['participantId'], clockwise = targetSide, correct = thisResp, reactionTime = reactionTime, sessionNo = expInfo['sessionNo'], trialNo = trialNo, rotation = difficultyRotation, noise = difficultyNoise))
        core.wait(1)

# updating last param ------------------------------------------------
expInfo['dateStr'] = data.getDateStr()  # add the current time
toFile(expId + 'lastParams.pickle', expInfo)  # save params to file for next time 
print("experiment info updated")