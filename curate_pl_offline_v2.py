# Curate-pl-offline implementation
# version: 27-12-21
# --------------------------------------------------------------------
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import os
import numpy, random

from datetime import date

#defining all the functions---------

def tuneRotation(difficultyRotation):
    global clockwise
    global initialAngle
    global changeAngle
    global finalAngle
    clockwise = random.choice([-1,1]) 
    initialAngle = random.randrange(0,90)
    changeAngle = random.randrange(0,(40 - (2 * difficultyRotation)))
    finalAngle = initialAngle + (clockwise * changeAngle)

# setting up noise parameters
def setUpGabor(initialAngle, finalAngle, difficultyNoise):
    global foil
    global target
    opacity = difficultyNoise/20
    foil.setOri(initialAngle)
    noiseFoil = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=initialAngle, opacity=opacity)
        
    target.setOri(finalAngle)
    noiseTarget = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=finalAngle, opacity=opacity)
    return noiseFoil, noiseTarget

# a function to draw the gabor
def drawGabor(fixation, foil, noiseFoil, target, noiseTarget):
    # set point of focus
    fixation.draw()
    win.flip()
    core.wait(0.5)
    # draw first gabor
    foil.draw()
    noiseFoil.draw()
    win.flip()
    core.wait(0.5)
    # draw rotated gabor
    target.draw()
    noiseTarget.draw()
    win.flip()
    core.wait(0.5)

# function to get response 
def getResponse(responseMessage, clockwise):
    global trialClock
    # asking for response
    responseMessage.draw()
    win.flip()
    trialClock.reset()
    # checking response
    reactionTime = 0
    correct=None
    while correct==None:
        allKeys=event.waitKeys()
        reactionTime = trialClock.getTime()
        for thisKey in allKeys:
            if thisKey=='left':
                if clockwise==-1: correct = True  # correct
                else: correct = False             # incorrect
            elif thisKey=='right':
                if clockwise== 1: correct = True  # correct
                else: correct = False            # incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
    return reactionTime, correct
    
def writeData(expInfo, clockwise, correct, reactionTime, trialNo, difficultyRotation, difficultyNoise): 
    global dataFile
    dataFile.write('{dateStr}, {participantId}, {clockwise}, {correct}, {reactionTime}, {sessionNo}, {blockNo}, {trialNo}, {rotation}, {noise}, NA, NA, NA\n'.format( dateStr = expInfo['dateStr'], participantId = expInfo['participantId'], clockwise = (clockwise == 1), correct = correct, reactionTime = reactionTime, sessionNo = expInfo['sessionNo'], blockNo = expInfo['blockNo'], trialNo = trialNo, rotation = difficultyRotation, noise = difficultyNoise))
    print('{dateStr}, {participantId}, {clockwise}, {correct}, {reactionTime}, {sessionNo}, {blockNo}, {trialNo}, {rotation}, {noise}, NA, NA, NA\n'.format(dateStr = expInfo['dateStr'], participantId = expInfo['participantId'], clockwise = (clockwise == 1), correct = correct, reactionTime = reactionTime, sessionNo = expInfo['sessionNo'], blockNo = expInfo['blockNo'], trialNo = trialNo, rotation = difficultyRotation, noise = difficultyNoise))

# getting parameters and other metadata ------------------------------
# getting experiment id
tempId= {'id': 'id'}
expId= ""
dlgId = gui.DlgFromDict(tempId, title='Curate offline Perceptual Learning')
if dlgId.OK:
    expId = tempId['id'].upper()
else:
    core.quit() # the user hit cancel so exit
 
sessType = ""
 
dlgParticipant = gui.Dlg(title = expId + " settings")
dlgParticipant.addField("Session Type", choices = ["Thresholding", "Training"]) #index 0
dlgParticipant.addField("Session: ") #index 1


participantType = dlgParticipant.show()

if dlgParticipant.OK:
    sessType = participantType[0]
    sessNo = participantType[1]
    print(participantType)
    
else:
    core.quit() # the user hit cancel so exit
    
try:
    int(sessNo)
except:
    print("Session number invalid")
    
    dlgParticipant2 = gui.Dlg(title = expId + " settings")
    dlgParticipant2.addText("Session number invalid")
    dlgParticipant2.addFixedField("Session Type: ", sessType)
    dlgParticipant2.addField("Session: ")
    
    participantType2 = dlgParticipant2.show()
    
    if dlgParticipant2.OK:
        sessNo = participantType2[1]
        print(participantType2)
    
    else:
        core.quit() # the user hit cancel so exit
#    
        
# write a function to expect an enter 
def getResponseEnter() : 
    while True:
        response = event.waitKeys()
        print(response[0])
        if response[0] == "return":
            break
        elif response[0] == 'q':
            core.quit()

#    
if sessType == "Thresholding": 
    
    os.mkdir(str(expId)) #making directory
    
    expInfo = {'participantId': expId, 'sessionNo': sessNo, "blockNo": 0, 'difficultyRotation': 0, 'difficultyNoise': 0}
    
    expInfo['dateStr'] = data.getDateStr()
    print("start session no " + str(expInfo['sessionNo']) + ": " + str(expInfo))
    
    nTrials = 5 #trial number 
    
    cd = os.getcwd()

    # make a text file to save data --------------------------------------
    fileName = expInfo['participantId'] + "_" + date.today().strftime("%d_%m_%Y") + "_sess_" + str(expInfo['sessionNo'])
    dataFile = open(cd + "/" + str(expId) + "/" + fileName + '.csv', 'w')  # a simple text file with 'comma-separated-values'
    
    try: 
        dataFile.write('dateStr, participantId,clockwise,correct, rt, sessionNo, blockNo, trialNo, rotation, noise, triggerTime, responseStart, responseEnd\n')
        
    except:
        print("participant already exists")
        
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
    message3 = visual.TextStim(win, pos=[0,-350], text="Press return/enter key to continue.", units='pix', height=30)
    message1.draw()
    message2.draw()
    message3.draw()
    win.flip()
    getResponseEnter()
        
    # instruction
    instructionText1 = 'In this experiment, you will see a white cross appear on the screen. Please focus your eyes on this circle about 2 feet (60cm) from your screen for the entirety of each session.'
    instructionText2 = 'Two patterns will appear in quick succession over the cross. Your task is to determine whether the second pattern is tilted clockwise or anti-clockwise relative to the first. Move the joystick to the left if the second pattern is tilted anti-clockwise, and the right if it is tilted clockwise.'
    message4 = visual.TextStim(win, pos=[0,+200],text=instructionText1, units='pix', height=19)
    message5 = visual.TextStim(win, pos=[0,-100],text=instructionText2, units='pix', height=19)
    message6 = visual.TextStim(win, pos=[0,-350], text="Press return/enter key to continue.", units='pix', height=30)
    message4.draw()
    message5.draw()
    message6.draw()
    fixation.draw()
    win.flip()
    getResponseEnter()

    # build response message to show when the user can key in response
    responseMessage = visual.TextStim(win, pos=[0,0], text="Type response now.\nanti-clockwise (left) or clockwise (right)", units='pix', height=40)
    
        
    # training/testing phase ---------------------------------------------
    difficultyRotation = expInfo['difficultyRotation']
    difficultyNoise = expInfo['difficultyNoise']
    streak = 0
    
        
    # angle parameters  
    clockwise = 0
    initialAngle = 0
    changeAngle = 0
    finalAngle = 0
        
        
    # warm up
    warmupMessage = visual.TextStim(win, pos=[0,0], text="This is just a warm up trial.", units='pix', height=50)
    warmupMessage.draw()
    win.flip()
    core.wait(1)
    # get the change in angle
    tuneRotation(difficultyRotation)
    # set up the gabor
    noiseFoil, noiseTarget = setUpGabor(initialAngle, finalAngle, difficultyNoise)
    # drawing the gabor
    drawGabor(fixation, foil, noiseFoil, target, noiseTarget)
    # get response
    reactionTime, correct = getResponse(responseMessage, clockwise)
    # check if response is correct
    if correct: 
        correctMessage = visual.TextStim(win, pos=[0,0], text="Correct response.", units='pix', height=50)
        correctMessage.draw()
        win.flip()
        core.wait(1)
    else: 
        falseMessage = visual.TextStim(win, pos=[0,0], text="Wrong response.", units='pix', height=50)
        falseMessage.draw()
        win.flip()
        core.wait(1)
        

    # start session
    startMessage = visual.TextStim(win, pos=[0,0], text="Sesion starts now. Press Enter/Return when you are ready.", units='pix', height=50)
    startMessage.draw()
    win.flip()
    getResponseEnter()
    core.wait(1) #wait for 1 second before beginning next session
    
    expInfo["blockNo"] += 1 #adding 1 to current block
    
    # angle parameters reset 
    clockwise = 0
    initialAngle = 0
    changeAngle = 0
    finalAngle = 0
    
    for trialNo in range(1, nTrials + 1) : 
        # get the change in angle
        tuneRotation(difficultyRotation)
        # set up the gabor
        noiseFoil, noiseTarget = setUpGabor(initialAngle, finalAngle, difficultyNoise)
        # drawing the gabor
        drawGabor(fixation, foil, noiseFoil, target, noiseTarget)
        # get response
        reactionTime, correct = getResponse(responseMessage, clockwise)
        # write data
        writeData(expInfo, clockwise, correct, reactionTime, trialNo, difficultyRotation, difficultyNoise)
        # updating global parameters
        if correct:
            if streak == 2: 
                streak = 0
                difficultyRotation += 1
            else: 
                streak += 1
        else: 
            if difficultyRotation > 1 : 
                difficultyRotation -= 1
    
        
        
    # updating last param ------------------------------------------------
    expInfo['dateStr'] = data.getDateStr()  # add the current time
    expInfo['difficultyRotation'] = difficultyRotation
    expInfo['difficultyNoise'] = difficultyNoise
    
    # save params to file for next time 
    toFile(expId + 'lastParams.pickle', expInfo)  
    print("experiment info updated")
    print("end session no " + str(expInfo['sessionNo']) + ": " + str(expInfo))
        
    

#    .
#    .
#    .
#    
#    
#    elif sessType == "Training":

    #get details from config file given the session number
    #
    
#        .
#        .
#        .
#        
#
#
#