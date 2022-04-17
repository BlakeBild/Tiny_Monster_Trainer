import gc
gc.enable()
#import time
import thumby
#import math
import sys
import ujson
sys.path.append("/Games/Tiny_Monster_Trainer/Curtian/")
from classLib import TextForScroller
from funcLib import thingAquired, battleStartAnimation, buttonInput, showOptions
#import micropython


#remember this for later ---->   machine.unique_id

def openScreen():
    gc.collect()
    #micropython.mem_info()
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
                p = open("/Games/Tiny_Monster_Trainer/Curtian/here_be_monsters.ujson", "r")
                p.close()
                break
            except OSError:
                gc.collect()
                import createPlayer
                del sys.modules["createPlayer"]
                break 

 
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
                thingAquired("Entering", "the", "Wilderness!", "^^^^^^^^^^^^", 0, 0, 0)
                gc.collect()
                #micropython.mem_info()
                import wilderness
            if optionList[curSelect] == optionList[2]:
                pass
        if curSelect == 30:
            cancelCheck = 1
            thumby.display.fill(0)
        thumby.display.update()


while(1):
    openScreen()
    #micropython.mem_info()
    #print("in While")
    optionScreen()
