import gc
gc.enable()
import time
import thumby
import math
import sys
import ujson
sys.path.append("/Games/Tiny_Monster_Trainer/")
from classes import TextForScroller
#from wilderness import battleStartAnimation


#remember this for later ---->   machine.unique_id

def openScreen():
    gc.collect()
    thumby.display.setFPS(40)
    f = open('/Games/Tiny_Monster_Trainer/Curtian/Other.ujson')
    images = ujson.load(f)
    myScroller = TextForScroller("Welcome! Press A/B to start!")
    while(1):
        whatDo = 0
        thumby.display.fill(0)
        thumby.display.blit(bytearray(images["introTail"]), 0, 0, 25, 30, 0, 0, 0)
        thumby.display.blit(bytearray(images["introHead"]), 47, 0, 25, 30, 0, 1, 0)
        thingAquired("Tiny", "Monster", "Trainer!", "", 0, 1, 1)
        thumby.display.drawLine(0, 28, 72, 28, 1)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        thumby.display.update()
        whatDo = buttonInput(whatDo)
        if whatDo >= 30:
            battleStartAnimation(0)
            f.close()
            try:
                p = open("/Games/Tiny_Monster_Trainer/Curtian/tmt.ujson", "r")
                p.close()
                p = open("/Games/Tiny_Monster_Trainer/here_be_monsters.ujson", "r")
                p.close()
                break
            except OSError:
                import CreateWorld
                del sys.modules["CreateWorld"]
                break 

 
def thingAquired(word1, word2, itemName, word4 ="", setSleep=1, skipUpdate=0, skipFill=0):
    if skipFill == 0:
        thumby.display.fill(0)
    thumby.display.drawText(word1, math.floor(((72-(len(word1))*6))/2), 1, 1)
    thumby.display.drawText(word2, math.floor(((72-(len(word2))*6))/2), 10, 1)
    thumby.display.drawText(itemName, math.floor(((72-(len(itemName))*6))/2), 19, 1)
    thumby.display.drawText(word4, math.floor(((72-(len(word4))*6))/2), 28, 1)
    if skipUpdate == 0:
        thumby.display.update()
    time.sleep(setSleep)

            
def battleStartAnimation(color):
    thumby.display.setFPS(0)
    for x in range(0,72):
        for y in range (0, 40):
            thumby.display.drawLine(x, 0, 0, y, color)
            thumby.display.drawLine(72, 40-y, 72-x, 40, color)
        thumby.display.update()
    thumby.display.fill(0)
    thumby.display.update()
    thumby.display.setFPS(40)
    
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
    thumby.display.drawFilledRectangle(0, 12, 72, 9, 1)
    thumby.display.drawText(options[currentSelect - 1], math.floor(((72-(len(options[currentSelect - 1]))*6))/2), 4, 1) # prints top opt
    thumby.display.drawText(options[currentSelect], math.floor(((72-(len(options[currentSelect]))*6))/2), 13, 0) # prints center opt
    thumby.display.drawText(options[currentSelect+1],  math.floor(((72-(len(options[currentSelect + 1]))*6))/2), 22, 1) #prints bottom opt
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
    thumby.display.fill(0)
    curSelect = 1
    tempSelect = curSelect
    cancelCheck = 0
    optionList = ["Place Holder", "Single",  "Versus"]
    while cancelCheck != 1:
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        tempSelect = curSelect
        curSelect = showOptions(optionList, curSelect, "Choose Mode")
        if curSelect == 31:
            curSelect = tempSelect
            if optionList[curSelect] == optionList[0]:
                pass
            if optionList[curSelect] == optionList[1]:
                thingAquired("Entering", "the", "Wilderness!", ":)", 0, 0, 0)
                import wilderness
            if optionList[curSelect] == optionList[2]:
                pass
        if curSelect == 30:
            cancelCheck = 1
            thumby.display.fill(0)
        thumby.display.update()

while(1):
    openScreen()
    print("in While")
    optionScreen()
