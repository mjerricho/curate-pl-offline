# Curate-pl-offline implementation
# version: 08-01-22
# --------------------------------------------------------------------------
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import os
import numpy, random
import pandas as pd
from datetime import date

# defining essential functions ---------------------------------------------
def tuneRotation(difficultyRotation):
    global clockwise
    global initialAngle
    global deltaAngle
    global finalAngle
    clockwise = random.choice([-1,1]) 
    initialAngle = random.randrange(0,90)
    # TODO - deltaAngle needs revision
    deltaAngle = random.randrange(0,(40 - (2 * difficultyRotation)))
    finalAngle = initialAngle + (clockwise * deltaAngle)

# setting up noise parameters
def setUpGabor(initialAngle, finalAngle, difficultyNoise):
    global initialGabor
    global finalGabor
    # TODO - opacity needs revision
    opacity = difficultyNoise/20
    initialGabor.setOri(initialAngle)
    initialNoise = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=initialAngle, opacity=opacity)
    finalGabor.setOri(finalAngle)
    finalNoise = visual.NoiseStim(win, sf = 1, size=4, noiseElementSize=0.05,  mask='gauss', noiseType='uniform', blendmode='avg', ori=finalAngle, opacity=opacity)
    return initialNoise, finalNoise

# a function to draw the gabor
def drawGabor(fixation, initialGabor, initialNoise, finalGabor, finalNoise):
    # set point of focus
    fixation.draw()
    win.flip()
    core.wait(0.5) # TODO - time between gabor needs revision
    # draw first gabor
    initialGabor.draw()
    initialNoise.draw()
    win.flip()
    core.wait(0.5) # TODO - time when initial Gabor is shown needs revision
    # draw rotated gabor
    finalGabor.draw()
    finalNoise.draw()
    win.flip()
    core.wait(0.5) # TODO - time when final Gabor is shown needs revision

# function to get response 
def getResponse(responseMessage, clockwise):
    global trialClock
    # asking for response
    responseMessage.draw()
    win.flip()
    trialClock.reset()
    # checking response
    reactionTime = 0
    correct = None
    while correct == None:
        allKeys = event.waitKeys()
        reactionTime = trialClock.getTime()
        for thisKey in allKeys:
            if thisKey == 'left':
                correct = True if clockwise == -1 else False
            elif thisKey=='right':
                correct = True if clockwise == 1 else False
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
    return reactionTime, correct
    
# write a function to expect an enter 
def getResponseEnter() : 
    while True:
        response = event.waitKeys()
        print(response[0])
        if response[0] == "return":
            break
        elif response[0] == 'q':
            core.quit()
    
def writeData(expInfo, clockwise, correct, reactionTime, trialNo, difficultyRotation, difficultyNoise): 
    global dataFile
    dataFile.write('{dateStr}, {participantId}, {clockwise}, {correct}, {reactionTime}, {sessionNo}, {blockNo}, {trialNo}, {rotation}, {noise}, NA, NA, NA\n'.format(dateStr = expInfo['dateStr'], participantId = expInfo['participantId'], clockwise = (clockwise == 1), correct = correct, reactionTime = reactionTime, sessionNo = expInfo['sessionNo'], blockNo = expInfo['blockNo'], trialNo = trialNo, rotation = difficultyRotation, noise = difficultyNoise))
    print('{dateStr}, {participantId}, {clockwise}, {correct}, {reactionTime}, {sessionNo}, {blockNo}, {trialNo}, {rotation}, {noise}, NA, NA, NA\n'.format(dateStr = expInfo['dateStr'], participantId = expInfo['participantId'], clockwise = (clockwise == 1), correct = correct, reactionTime = reactionTime, sessionNo = expInfo['sessionNo'], blockNo = expInfo['blockNo'], trialNo = trialNo, rotation = difficultyRotation, noise = difficultyNoise))

# end message
def showEndMessage(): 
    print("experiment info updated")
    print("end session no " + str(expInfo['sessionNo']) + ": " + str(expInfo))
    endMessage = visual.TextStim(win, pos=[0,0], text="Thank you for participating in this study. Press Enter/Return to end the session.", units='pix', height=50)
    endMessage.draw()
    win.flip()
    getResponseEnter()

########################EXPERIMENT CODE START HERE##########################
# getting parameters and other metadata ------------------------------------
# getting experiment id
tempId= {'id': 'id'}
expId= ""
dlgId = gui.DlgFromDict(tempId, title='Curate offline Perceptual Learning')
if dlgId.OK:
    expId = tempId['id'].upper()
else:
    core.quit() # the user hit cancel so exit
 
sessionType = ""
sessionNo = None
 
# ensure the user inserts an integer for the session number
while True:
    dlgParticipant = gui.Dlg(title = expId + " settings")
    dlgParticipant.addField("Session Type", choices = ["Thresholding", "Training"]) #index 0
    dlgParticipant.addField("Session: ") #index 1
    participantType = dlgParticipant.show()
    # check if user inputs an integer
    if dlgParticipant.OK:
        if participantType[1].isnumeric() : 
            sessionType = participantType[0]
            sessionNo = int(participantType[1])
            print(participantType)
            break
    else:
        core.quit() # the user hit cancel so exit

# initialise experiment info and datafile ----------------------------------
cwd = os.getcwd()
# making directory, returns an error if directory already exists
try: os.mkdir(str(expId)) 
except: pass

expInfo = {'participantId': expId, 'sessionNo': sessionNo, "blockNo": 0, 'difficultyRotation': 0, 'difficultyNoise': 0, 'dateStr': data.getDateStr()}
print("Start session no " + str(expInfo['sessionNo']) + ": " + str(expInfo))

# make a csv file to save data ---------------------------------------------
fileName = expInfo['participantId'] + "_" + date.today().strftime("%d_%m_%Y") + "_sess_" + str(expInfo['sessionNo'])
dataFile = open(cwd + "/" + str(expId) + "/" + fileName + '.csv', 'w')
# add columns header
dataFile.write('dateStr, participantId,clockwise,correct, rt, sessionNo, blockNo, trialNo, rotation, noise, triggerTime, responseStart, responseEnd\n')

# if sessionType is Training, check whether the user wants default or custom setting
if sessionType == "Training":
    dlgParticipant2 = gui.Dlg(title = expId + " settings")
    dlgParticipant2.addFixedField("Session Type: ", sessionType)
    dlgParticipant2.addFixedField("Session Number: ", sessionNo)
    dlgParticipant2.addField("Default Training Setting?", choices = ["Yes", "No"]) #index 2
    participantType2 = dlgParticipant2.show()
    if dlgParticipant2.OK:
        default = participantType2[2]
        print("user chose: " + str(participantType2))
        
        # set up parameters for Training ------------------
        # check whether previous profile is present
        try:
            df = pd.read_csv(cwd + "/" + str(expId) + "/" + str(expId) + "_profile.csv") #read participant profile 
        except:
            print("wrong participant id or threshold profile does not exist")
            dlgParticipant5 = gui.Dlg(title="Error in getting profile")
            dlgParticipant5.addText("ID " + expId + " does not exist. Please re-enter ID at the start.")
            participantType5 = dlgParticipant5.show()
                
        # difficulty setting values for L, M, H ------------
        # [0] is rotation threshold
        # [1] is noise threshold
        L = [df["low"][0], df["low"][1]]
        M = [df["medium"][0], df["medium"][1]]
        H = [df["high"][0], df["high"][1]]
        
        print("level, rot, noise")
        print("low = " + str(L))
        print("medium = " + str(M))
        print("high = " + str(H))
            
        # initialising the sequence based on default or custom input -----------
        sequence = []
        # user selected to custom input
        if default =="No":
            #getting custom sequence if default is no
            dlgParticipant4 = gui.Dlg(title = expId + " custom sequence")
            dlgParticipant4.addText("Please input sequence below e.g L,M,H,L,M,H")
            dlgParticipant4.addField("Sequence")
            participantType4 = dlgParticipant4.show()
            
            #need to code try and except depend on how u use it
            if dlgParticipant4.OK:
                tempSequence = participantType4[0]
                print(str(tempSequence))
                print(str(type(tempSequence)))
                for letter in tempSequence.split(","):
                    if letter == "L": sequence.append(L)
                    elif letter == "M": sequence.append(M)
                    elif letter == "H": sequence.append(H)
                    else: 
                        print("Wrong input.")
                        core.quit()
            else:
                core.quit() # the user hit cancel so exit
        # user selected default option
        else:  
            runs = {
                    "run_A": [L, M, H, M, H, L, H, L, M], 
                    "run_B": [M, L, H, L, H, M, H, M, L], 
                    "run_C": [M, H, L, H, L, M, L, M, H],
                    "run_D": [L, H, M, H, M, L, M, L, H], 
                    "run_E": [H, L, M, L, M, H, M, H, L],
                    "run_F": [H, M, L, M, L, H, L, H, M]
                    }
            if sessionNo == 2 or sessionNo == 12: sequence = runs["run_A"]
            elif sessionNo == 3 or sessionNo == 11: sequence = runs["run_B"]
            elif sessionNo == 4 or sessionNo == 10: sequence = runs["run_C"]
            elif sessionNo == 5 or sessionNo == 9: sequence = runs["run_D"]
            elif sessionNo == 6 or sessionNo == 8: sequence = runs["run_E"]
            elif sessionNo == 7 or sessionNo == 13: sequence = runs["run_F"]
            elif sessionNo == 8 or sessionNo == 14: sequence = runs["run_E"]
        print("sequence is " + str(sequence))
    else:
        core.quit() # the user hit cancel so exit

# setting up parameters and instructions -----------------------------------
# create window and stimuli
win = visual.Window([1500,900],allowGUI=True, monitor='testMonitor', units='deg')
initialGabor = visual.GratingStim(win, sf=1, size=4, mask='gauss')
finalGabor = visual.GratingStim(win, sf=1, size=4, mask='gauss')
fixation = visual.GratingStim(win, color=1, colorSpace='rgb', tex=None, mask='cross', size=0.2)
                              
# clocks to keep track of time
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
        
# Thresholding case --------------------------------------------------------
if sessionType == "Thresholding": 
    # training/testing phase ---------------------------------------------
    difficultyRotation = expInfo['difficultyRotation']
    difficultyNoise = expInfo['difficultyNoise']
    streak = 0
    
    # angle parameters  
    clockwise = 0
    initialAngle = 0
    deltaAngle = 0
    finalAngle = 0
        
    # warm up TODO - should we do more than one? we can use for-loop
    warmupMessage = visual.TextStim(win, pos=[0,0], text="This is just a warm up trial.", units='pix', height=50)
    warmupMessage.draw()
    win.flip()
    core.wait(1)
    # get the change in angle
    tuneRotation(difficultyRotation)
    # set up the gabor
    initialNoise, finalNoise = setUpGabor(initialAngle, finalAngle, difficultyNoise)
    # drawing the gabor
    drawGabor(fixation, initialGabor, initialNoise, finalGabor, finalNoise)
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
        
    # start session -----
    # TODO - EDIT N PARAMETER
    nTrials = 5 
    startMessage = visual.TextStim(win, pos=[0,0], text="Sesion starts now. Press Enter/Return when you are ready.", units='pix', height=50)
    startMessage.draw()
    win.flip()
    getResponseEnter()
    core.wait(1) #wait for 1 second before beginning next session
    
    expInfo["blockNo"] += 1 #adding 1 to current block
    
    # only changing the difficultyRotation
    for trialNo in range(1, nTrials + 1) : 
        # get the change in angle
        tuneRotation(difficultyRotation)
        # set up the gabor
        initialNoise, finalNoise = setUpGabor(initialAngle, finalAngle, difficultyNoise)
        # drawing the gabor
        drawGabor(fixation, initialGabor, initialNoise, finalGabor, finalNoise)
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
                
    rot_threshold = difficultyRotation
    
    #signifying the end of block 1 
    message7 = visual.TextStim(win, pos=[0,0], text="End of block 1. Press enter to continue", units='pix', height=30)
    message7.draw()
    win.flip()
    getResponseEnter()
    
    message8 = visual.TextStim(win, pos=[0,0], text="Starting Block 2", units='pix', height=30)
    message8.draw()
    core.wait(1)
    win.flip()
    
    #starting block 2/ thresholding for noise --------
    
    #setting rotation for noise thresholding
    difficultyRotation = rot_threshold - 3 if rot_threshold > 3 else 0

    expInfo["blockNo"] += 1 #adding 1 to current block
    
    # only changing the difficultyNoise
    # TODO - do we need to reset streak for the other block?
    streak = 0
    for trialNo in range(1, nTrials + 1) : 
        # get the change in angle
        tuneRotation(difficultyRotation)
        # set up the gabor
        initialNoise, finalNoise = setUpGabor(initialAngle, finalAngle, difficultyNoise)
        # drawing the gabor
        drawGabor(fixation, initialGabor, initialNoise, finalGabor, finalNoise)
        # get response
        reactionTime, correct = getResponse(responseMessage, clockwise)
        # write data
        writeData(expInfo, clockwise, correct, reactionTime, nTrials + trialNo, difficultyRotation, difficultyNoise)
        # updating global parameters
        if correct:
            if streak == 2: 
                streak = 0
                difficultyNoise += 1
            else: 
                streak += 1
        else: 
            if difficultyNoise > 1 : 
                difficultyNoise -= 1
                
    noise_threshold = difficultyNoise
    low_rot_threshold = 0 if rot_threshold < 6 else rot_threshold - 6
    low_noise_threshold = 0 if noise_threshold < 6 else noise_threshold - 6
    
    # creating and saving curate profile
    # rotation = first row, noise = second row
    profile = {"low": [low_rot_threshold,low_noise_threshold], "medium": [rot_threshold,noise_threshold], "high": [rot_threshold + 6,noise_threshold + 6]}
    df = pd.DataFrame.from_dict(profile) 
    df.to_csv(cwd + "/" + str(expId) + "/" + str(expId) + "_profile.csv", index = False, header = True)
    
# backup
# dataFile2 = open(cwd + "/" + str(expId) + "/" + fileName2 + '.csv', 'w')  # a simple text file with 'comma-separated-values'
# dataFile2.write("{low}, {medium}, {high}".format(low = profile["low"], medium = profile["medium"], high = profile["high"]))
    
# Training case ------------------------------------------------------------
elif sessionType == "Training":
    # TODO EDIT PARAMETERS
    nBlocks = 6
    nTrials = 5
    # only changing the difficultyNoise
    for blockNo in range(nBlocks):
        expInfo["blockNo"] += 1 # updating current block
        # getting the parameter based on the sequence
        difficultyRotation = sequence[blockNo][0]
        difficultyNoise = sequence[blockNo][1]
        for trialNo in range(1, nTrials + 1) : 
            # get the change in angle
            tuneRotation(difficultyRotation)
            # set up the gabor
            initialNoise, finalNoise = setUpGabor(initialAngle, finalAngle, difficultyNoise)
            # drawing the gabor
            drawGabor(fixation, initialGabor, initialNoise, finalGabor, finalNoise)
            # get response
            reactionTime, correct = getResponse(responseMessage, clockwise)
            # write data
            writeData(expInfo, clockwise, correct, reactionTime, ((blockNo * nTrials) + trialNo), difficultyRotation, difficultyNoise)
            
showEndMessage()