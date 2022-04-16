import gc
gc.enable()
import time
import thumby
import math
import random
import sys
sys.path.append("/Games/Tiny_Monster_Trainer/")

#title

#select die

#roll

#theme


def rollDice(sides, amount):
    print("in rollDice")
    for int in range(0, amount):
        print(random.randint(1,sides))


def buttonInput(selectPos):                
    selectionBoxPos = selectPos
    while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
        pass
    if(thumby.buttonU.pressed() == True):
        while(thumby.buttonU.pressed() == True): 
            pass
        selectionBoxPos = selectionBoxPos - 1
    elif(thumby.buttonD.pressed() == True):
        while(thumby.buttonD.pressed() == True): 
            pass
        if (selectionBoxPos <= 26):
            selectionBoxPos = selectionBoxPos + 1
    elif(thumby.buttonL.pressed() == True):
        while(thumby.buttonL.pressed() == True): 
            pass
        selectionBoxPos = 29
    elif(thumby.buttonR.pressed() == True):
        while(thumby.buttonR.pressed() == True): 
            pass
        selectionBoxPos = 28
    elif(thumby.buttonA.pressed() == True):
        while(thumby.buttonA.pressed() == True):
            pass
        selectionBoxPos = 31
    elif(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
        selectionBoxPos = 30
    return selectionBoxPos

def currentSelectCheckRange(optionAmount, currentSelect):
    if currentSelect > optionAmount - 2 :
        currentSelect = currentSelect - optionAmount
    if currentSelect < -abs(optionAmount) + 2:
        currentSelect = currentSelect + optionAmount
    return currentSelect    

def showOptions(options, currentSelect, bottomText):
    optionAmount = len(options)
    currentSelect = currentSelectCheckRange(optionAmount, currentSelect)
    thumby.display.fill(0)
    thumby.display.drawFilledRectangle(23, 12, 25, 9, 1)
    thumby.display.drawText(options[currentSelect - 1], math.floor(((72-(len(options[currentSelect - 1]))*6))/2), 4, 1) # prints top opt
    thumby.display.drawText(options[currentSelect], math.floor(((72-(len(options[currentSelect]))*6))/2), 13, 0) # prints center opt
    thumby.display.drawText(options[currentSelect+1],  math.floor(((72-(len(options[currentSelect + 1]))*6))/2), 22, 1) #prints bottom opt
    thumby.display.drawLine(22, 0, 22, 30, 1)# line for left bar
    thumby.display.drawLine(48, 0, 48, 30, 1)# line for right bar
    thumby.display.drawLine(22, 2, 48, 2, 1) #line for top bar
    thumby.display.drawLine(0, 30, 72, 30, 1) #line for bottom text
    if bottomText != "":
        thumby.display.drawText(bottomText,  math.floor(((72-(len(bottomText))*6))/2), 32, 1) # prints other info on bottom of screen
    currentSelect = buttonInput(currentSelect)
    if optionAmount <= 1:
        if currentSelect == 31:
            return currentSelect
        elif currentSelect == 30:
            return currentSelect
        elif currentSelect > 0 or currentSelect < 0:
            return 0
    return currentSelect
    

def optionScreen():
    #if(thumby.buttonB.pressed() == True):
    #    while(thumby.buttonB.pressed() == True):
    #        pass
    thumby.display.fill(0)
    curSelect = 1
    tempSelect = curSelect
    cancelCheck = 0
    optionList = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]
    while cancelCheck != 1:
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        tempSelect = curSelect
        curSelect = showOptions(optionList, curSelect, "Select Die")
        if curSelect == 31:
            curSelect = tempSelect
            if optionList[curSelect] == optionList[0]:
                #import DVD_Corner_Remix
                import Tiny_Monster_Trainer
                rollDice(4,1)
                #del sys.modules["DVD_Corner_Remix"]
            if optionList[curSelect] == optionList[1]:
                rollDice(6,1)
            if optionList[curSelect] == optionList[2]:
                rollDice(8,1)
            if optionList[curSelect] == optionList[3]:
                rollDice(10,1)
            if optionList[curSelect] == optionList[4]:
                rollDice(12,1)
            if optionList[curSelect] == optionList[5]:
                rollDice(20,1)
            if optionList[curSelect] == optionList[6]:
                rollDice(100,1)
        if curSelect == 30:
            cancelCheck = 1
            thumby.display.fill(0)
        thumby.display.update()

while(1):
    random.seed(time.ticks_ms())
    print("in While")
    optionScreen()
