# Curate-pl-offline implementation
# version: 27-12-21
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
    expInfo = {'participantId': expId, 'sessionNo': sessNo, "blockNo": 0, 'difficultyRotation': 0, 'difficultyNoise': 0}
    
    expInfo['dateStr'] = data.getDateStr()
    print("start session no " + str(expInfo['sessionNo']) + ": " + str(expInfo))
    
    nTrials = 98 #trial number 
    

    # make a text file to save data --------------------------------------
    fileName = expInfo['participantId'] + "_" + expInfo['dateStr'] + "_sess_" + str(expInfo['sessionNo'])
    dataFile = open(fileName + '.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('dateStr, participantId,clockwise,correct, rt, sessionNo, blockNo, trialNo, rotation, noise, triggerTime, responseStart, responseEnd\n')
        
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