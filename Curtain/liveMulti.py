import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Monster, TextForScroller, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, switchActiveMon, showMonInfo
#from wilderness import loadGame


'''
    need to figure out who is the S & R
    need to check if switches happen
    need to make it so you can only switch once
    need to get attack name from R
    need to have S calculate damage
    need to send the results to R 
    need to animate attack
    repeat as needed
'''
    
'''
    while in the battle look check for switches and check for attacks
    after picking an attack it goes back to the menu and waits
    check if a switch happened after an attack was picked and undo the attack
    
    i think i need to send over a ujson file with:
    the monster's name (need to figure out a way to deal with duplicate names - probably do a check in wilderness and make them rename one)
    attack name
    something to keep track of a switch that happened
    maybe one more thing to keep track of a switch that happened
    
    then need another thing to send over damage/miss that happened
'''


def loadGame():
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson')
    bigJson = ujson.load(f)
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
    for x in range(0, len(bigJson[0]['monsterInfo'][0])):
        tempMon = Monster()
        tempMon.statBlock = bigJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat'].copy()
        tempMon.bodyBlock = bigJson[0]['monsterInfo'][1]['mon' + str(x) + 'body'].copy()
        tempMon.mutateSeed = bigJson[0]['monsterInfo'][3]['mon' + str(x) + 'mutate'].copy()
        for y in range(0, len(bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
            tempAttackMove = AttackMove(bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'], 
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType'])
            tempAttackMove.currentUses = bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['currentUses']
            tempMon.attackList.append(tempAttackMove) 
        tempMon.attackList = tempMon.attackList.copy()
        tempPlayer.friends.append(tempMon)
        tempPlayer.friends = tempPlayer.friends.copy()
    f.close()
    del bigJson
    return tempPlayer


def waitingForResponse(loadingStr, whatDoing):                
    thingAquired(whatDoing, "", "othr trainer!", loadingStr,0,0,0)
    loadingStr = loadingStr + "."
    if loadingStr == "...":
        loadingStr = ""
    return loadingStr



def findWhoSendsFirst():
    t0 = 02
    handshakeTimer = 0
    random.seed(time.ticks_ms())
    whoSendsFirst = bytearray([0]) 
    whoSendsFirst[0] = random.randint(1, 255)
    whoSendsFirstRcvd = bytearray([0]) 
    loadingStr = ""
    
    thingAquired("Send / Rcv", str(whoSendsFirst[0]), "", "",1,0,0)
    timerTrigger = 0
    #uncomment to test on actual thumby
    while(t0 - handshakeTimer < 30):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Contacting")
    
        thumby.link.send(whoSendsFirst)
        received = thumby.link.receive()
        
        if received != None:
            if handshakeTimer == 0:
                whoSendsFirstRcvd = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
                '''if whoSendsFirst[0] == whoSendsFirstRcvd[0]:
                    whoSendsFirst[0] = random.randint(1, 255)'''
                    
    
    if whoSendsFirst[0] > whoSendsFirstRcvd[0]:
        sOr = 1
    else:
        sOr = 0
    return sOr


def loadGhost(ghostFile):
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Ghosts/'+ghostFile+'.ujson')
    bigGhostJson = ujson.load(f)
    tempPlayer.playerBlock = bigGhostJson[0]['player'].copy()
    for x in range(0, len(bigGhostJson[0]['monsterInfo'][0])):
        tempMon = Monster()
        tempMon.statBlock = bigGhostJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat'].copy()
        tempMon.bodyBlock = bigGhostJson[0]['monsterInfo'][1]['mon' + str(x) + 'body'].copy()
        for y in range(0, len(bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
            tempAttackMove = AttackMove(bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'], 
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType'])
            tempAttackMove.currentUses = bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['currentUses']
            tempMon.attackList.append(tempAttackMove) 
        tempMon.attackList = tempMon.attackList.copy()
        tempPlayer.friends.append(tempMon)
        tempPlayer.friends = tempPlayer.friends.copy()
    tempPlayer.lOrR = 0
    f.close()
    del bigGhostJson
    return tempPlayer


def autoSwitchMon(playerInfo):
    if playerInfo.friends[0].statBlock['currentHealth'] < 1:
        x = 0
        for monsters in playerInfo.friends:
            if playerInfo.friends[x].statBlock['currentHealth'] > 0:
                switchActiveMon(playerInfo, playerInfo.friends[0], playerInfo.friends[x], x)
            x = x + 1
        #if playerInfo.friends[0].statBlock['currentHealth'] > 0:
        #    thingAquired(playerInfo.playerBlock['name']+"'s", playerInfo.friends[0].statBlock['given_name'], "is now",  "Acvtive!", 2)


def attackAnimation(playerBod, nmeBod, whoFirst, sOr, playerHP, playerAfterDmg, nmeHP, nmeAfterDmg, playerAtkElm, nmeAtkElm, nmeOos, playerOos):
    # BITMAP: width: 8, height: 8
    sidewaySkull = bytearray([0,42,62,119,127,107,107,62]) # ethereal
    darkness = bytearray([0,36,66,8,16,66,36,0]) # darkness
    maybeFireball = bytearray([20,42,62,99,69,89,99,62]) # fire
    maybeWaterball = bytearray([16,68,16,40,68,76,56,0]) # water
    windBlow = bytearray([68,85,85,34,8,138,170,68]) # wind
    rock = bytearray([20,65,28,42,66,86,36,56]) # earth
    punch =  bytearray([189,165,36,116,148,180,132,120])  # physical
    spiral = bytearray([124,130,57,69,149,153,66,60]) # mind
    fourFlowers = bytearray([32,82,37,2,64,164,74,4]) # light
    heart = bytearray([28,62,126,252,252,126,62,28]) # cute
    arrow = bytearray([4,60,39,114,90,78,120,0]) # mystic
    basic = bytearray([56,108,130,162,138,154,130,124]) #basic
    
    BoltArray = [basic, rock, windBlow, maybeWaterball, maybeFireball, fourFlowers, darkness, heart, spiral, punch, arrow, sidewaySkull]
    playerAttackTypeNum = typeAsNum(playerAtkElm)
    nmeAttackTypeNum = typeAsNum(nmeAtkElm)
    playerAtked = 0
    playerAtkedChk = 0
    nmeAtked = 0
    nmeAtkedChk = 0
    combatText = ""
    #thingAquired("","in atk", "animation","",1,0,0)
    playGo = 0
    nmeGo = 0
    showPlayerHP = playerHP
    showNmeHP = nmeHP
    if sOr == 0:
        if whoFirst == 1:
            whoFirst = 0
        else: # whoFirst == 0:
            whoFirst = 1
    
    if whoFirst == 1:
        playGo = 1
    else:
        nmeGo = 1
    while((playerAtkedChk + nmeAtkedChk) <= 1):
        t0 = 0
        ct0 = time.ticks_ms()
        bobRate = 250
        bobRange = 5
        animateX = 0
        playerAttacking = 0
        
        thumby.display.setFPS(40)
        while(t0 - ct0 < 4000):
            t0 = time.ticks_ms()
            bobOffset = math.sin(t0 / bobRate) * bobRange
            if(t0 - ct0 >= 4000):
                combatText = ""
            playerX = 8
            nmeX = 42
            y = 0
            nmeY = 0
            if (t0 - ct0 >= 2000) and (t0 - ct0 <= 3000) and playerAttacking == 1:
                y = 5
            elif (t0 - ct0 >= 2000) and (t0 - ct0 <= 3000) and playerAttacking == 2:
                nmeY = 5
            else:
                pass
            thumby.display.fill(0) 
            printMon(playerBod, playerX + y, 1, 0)
            printMon(nmeBod, nmeX - nmeY, 1, 1)
            thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
            thumby.display.drawText(str(showPlayerHP), 2, 30, 0)
            thumby.display.drawText(str(showNmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
            thumby.display.drawText(combatText, math.ceil(((72-(len(combatText))*6))/2)+1, 30, 0)
            if nmeHP == nmeAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and playerAtkedChk == 0 and playGo == 1: # player misses
                combatText = "Miss"
                playerAtked = 1
                playerAttacking = 1
            elif nmeHP != nmeAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and playerAtkedChk == 0 and playGo == 1 : # player hits
                thumby.display.blit(BoltArray[playerAttackTypeNum], (30 + animateX), math.floor(10+bobOffset), 8, 8, 0, 0, 0) #, flippy, 0)
                showNmeHP = nmeAfterDmg
                combatText = "Hit!"
                playerAtked = 1
                playerAttacking = 1
            elif playerHP == playerAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and nmeAtkedChk == 0 and nmeGo == 1: # nme misses
                #thumby.display.drawText("Miss", 25, 30, 0)
                combatText = "Miss"
                nmeAtked = 1
                playerAttacking = 2
            elif playerHP != playerAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and nmeAtkedChk == 0 and nmeGo == 1: # nme hits
                thumby.display.blit(BoltArray[nmeAttackTypeNum], (36 - animateX), math.floor(10+bobOffset), 8, 8, 0, 1, 0) #, flippy, 0)
                showPlayerHP = playerAfterDmg
                combatText = "Hit!"
                nmeAtked = 1
                playerAttacking = 2
            else:
                pass
                #thumby.display.drawText("Pass"+str(playerAtkedChk + nmeAtkedChk), 25, 30, 0)
            thumby.display.update()
            y = 0
            nmeY = 0
            if (t0 - ct0) % 2 == 0 and (t0 - ct0) > 2000:
                animateX = animateX + 1 
        if nmeAtked == 1:
            nmeGo = 0
            playGo = 1
            nmeAtkedChk = 1
        if playerAtked == 1:
            nmeGo = 1
            playGo = 0
            playerAtkedChk = 1
            
        if nmeAfterDmg <= 0 or playerAfterDmg <= 0:
            break


def isTypeWeak(mon1Type, mon2Type): 
    typeList = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    offsetList = ["Fire", "Earth", "Wind", "Water", "Mind", "Light", "Darkness",
                "Cute", "Ethereal", "Physical", "Mystical"]
    x = 0
    bonus = 0
    if mon1Type != "":
        while mon1Type != offsetList[x]:
            x = x + 1
        if mon2Type == typeList[x]:
            bonus = 1
    return bonus
    

def isTypeStrong(mon1Type, mon2Type): 
    typeList = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    offsetList = ["Wind", "Water", "Fire", "Earth", "Darkness", "Cute", "Mind",
                "Light", "Mystical", "Ethereal", "Physical"]
    x = 0
    bonus = 0
    if mon1Type != "":
        while mon1Type != typeList[x]:
            x = x + 1
        if mon2Type == offsetList[x]:
            bonus = 1
    return bonus


def typeAsNum(moveType):
    typeList = ["", "Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    typeNumber = 0
    for i in range(0,12):
        if moveType == typeList[i]:
            typeNumber = i
    return typeNumber


def attackOptionMenu(monInfo):  
    currentSelect = 1
    tempSelect = currentSelect
    playerOptionList = []
    
    for attacksKnown in range(0, len(monInfo)):
        playerOptionList.append(monInfo[attacksKnown].name)
        
    while(currentSelect < 29):
        thumby.display.fill(0)
        tempSelect = currentSelect
        if currentSelect == len(monInfo):
            currentSelect = currentSelect - 1
        if currentSelect == -abs(len(monInfo)):
            currentSelect = currentSelect + 1
        currentSelect = showOptions(playerOptionList, currentSelect, "Stamina: " + str(monInfo[currentSelect].currentUses))
        thumby.display.update()
        if currentSelect == 31:
            return tempSelect 
        elif currentSelect == 30:
            return 30 
        elif currentSelect == 28 or currentSelect == 29:
            currentSelect = tempSelect


def drawArrowsGhost(d, u): # x, y):
    #arrowLR = [4,4,4,31,14,4] # 6 x 5
    arrowUD = [8,24,63,24,8] # 5 x 6    # last three are: key, mirrorX, mirrorY

    thumby.display.blit(bytearray(arrowUD), 66, 20, 5, 6, d, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 3, 5, 6, u, 0, 1)


def pickGhost():
    import os
    curSelect = 0
    cancelCheck = 0
    tempSelect = curSelect
    bottomText = "You vs Who"
    files = os.listdir("/Games/Tiny_Monster_Trainer/Ghosts/")
    for x in range(len(files)):
        files[x] = files[x].replace('.ujson', '')
    while cancelCheck != 1:
        curSelect = showOptions(files, curSelect, bottomText)
        drawArrowsGhost(0, 0)
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        if curSelect == 31:
            curSelect = tempSelect
            return files[curSelect] 
        if curSelect == 30:
            cancelCheck = 1
            thumby.display.fill(0)
            return ""
        tempSelect = curSelect
        thumby.display.update()


def drawIntro(player, ghost):
    thingAquired(player.playerBlock['name'], "Vs.", "Spooky", ghost.playerBlock['name'],0,1,1)
    
    t0 = 0
    ct0 = time.ticks_ms()
    x = 10 
    y = 11
    animateCount = 0
    '''while(1):
        t0 = 0
        ct0 = time.ticks_ms()  '''
    animateCount = 0
    thumby.display.fill(0)
    thumby.display.update()
    time.sleep(1)
    while(t0 - ct0 < 5000):
        t0 = time.ticks_ms()
        randoNumber = 0 #random.randint(-1,1)
        randoNumber2 = 0 #random.randint(-1,1)
        randoNumber3 = 0 #random.randint(-1,1)
        thumby.display.fill(0)
        if(t0 - ct0 > 2800):
            thingAquired(player.playerBlock['name'], "Vs", ghost.playerBlock['name'], "",0,1,1)
            thumby.display.blit(bytearray(player.sprite), x+randoNumber-8 , y+randoNumber2, 8, 8, -1, 1, 0)
            thumby.display.blit(bytearray(ghost.sprite), 72-(x+randoNumber2) , y+randoNumber3, 8, 8, -1, ghost.lOrR, 0)
        #if (t0%10==0):
        animateCount = animateCount + 1 
        thumby.display.drawFilledRectangle(-36+animateCount, 0, 36, 40, 1)
        thumby.display.drawFilledRectangle(72-animateCount, 0, 36, 40, 1)
        
        thumby.display.update()
 
 
def sendCheckAndGetCheck(checkCheckNum):
    t0 = 0
    handshakeTimer = 0
    timerTrigger = 0
    loadingStr = ""
    checkCheckOther = bytearray([0])
    while(t0 - handshakeTimer < 300):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Attack")
    
        thumby.link.send(checkCheckNum)
        received = thumby.link.receive()
        
        if received != None:
            if handshakeTimer == 0:
                checkCheckOther = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
    return checkCheckOther
   

def multiPlayerDodge(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    try:
        dodgeBonus = 0
        attackAmnt = 0
        if activeAttack.magic == 1:
            attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
            dodgeBonus = defenceMon.statBlock['Tinfoil'] + random.randint(-1, 5)
        else:
            attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
            dodgeBonus = defenceMon.statBlock['Endurance'] + random.randint(-1, 5)
        dodge = defenceMon.statBlock['Agility'] + dodgeBonus 
        hit = 1
        if defTrainLevel > 99: #temp fix ---- change this to be something like if the dif of both trainer lvls is greater than 100 then make only 99 more or something like that
            defTrainLevel = 99
        if (dodge + random.randint(-abs(attackTrainLevel),(100 - defTrainLevel)))+200 > (90 - defTrainLevel)+200: # check for dodge
            glanceCheck = random.randint(-20, 20)
            if ((math.ceil(attackAmnt/2) + attackMon.statBlock['Agility']) + glanceCheck) >= dodge+defTrainLevel: # check for glance
                hit = 2
            else:
                hit = 0
        return hit
    except Exception as e:
        print(e)
        f = open("/Games/Tiny_Monster_Trainer/liveMulti789.log", "w")
        f.write(str(e) + " on Line 564. ish " )
        f.close() 
        
        
def multiPlayerAttack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    attackAmnt = 0
    defence = 0
    defBonus = 0
    if activeAttack.magic == 1:
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2) 
        defBonus = defenceMon.statBlock['Tinfoil'] + random.randint(-1, 5)
        defence =  defTrainLevel + defBonus
    else:
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
        defBonus = defenceMon.statBlock['Endurance'] + random.randint(-1, 5)
        defence = defTrainLevel + defBonus
    damage = 0
    atkTypeBonus = 1
    defTypeBonus = 1

    for x in range(1,3):
        atkTypeBonus = isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
    for x in range(1,3):
        defTypeBonus = isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
    damage = math.ceil((attackAmnt * atkTypeBonus)/3) - math.ceil((defence * defTypeBonus)/3)
    if damage <= 0:
        damage = 1
    return damage


def MultiPlayerBattleScreen(player, nmePlayer, sOr): 
    #print("Hi, you are in a fight!")
    random.seed(time.ticks_ms())
    myScroller = TextForScroller(player.friends[0].statBlock['given_name'] + " has entered into battle with " + nmePlayer.friends[0].statBlock['given_name'] + "! Their trainer's level is " + str(nmePlayer.playerBlock['trainerLevel']) +"!" )
    currentSelect = 1
     
    tempSelect = currentSelect
    nmeActiveInfo = [{"sAndrKey" : "", "given_name" : nmePlayer.friends[0].statBlock['given_name'], "attackNameStr" : ""}]
    swapCheck = 0
    myMoveOutOfStam = 0
    oppMoveOutOfStam = 0
    options = ["Info", "Atk", "Swap"] 
    nmeAttackRdy = 0
    mySelectedAttackName = ""
    mySelectedAttackNum = 0
    myAttackRdy = 0
    nmeAtkToUse = 0
    attackResultsKeep =  [{'nmeMonHP' : 0, 'OppMooS' : oppMoveOutOfStam, 'myMonHP': player.friends[0].statBlock['currentHealth'], 'myMooS' : myMoveOutOfStam, 'sAndrKey' : "test4"}]
    playerB4hp = player.friends[0].statBlock['currentHealth']
    nmeB4hp = nmePlayer.friends[0].statBlock['currentHealth']
    

    while((player.friends[0].statBlock['currentHealth'] >= 1) and (nmePlayer.friends[0].statBlock['currentHealth'] >= 1)):
        thumby.display.fill(0)
        
        myDmg = 0
        oppDmg = 0
        whoWentFirst = 0

        tempSelect = currentSelect
        currentSelect = showOptions(options, currentSelect, "", 47)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
        if currentSelect == 31: 
            currentSelect = tempSelect
            if options[currentSelect] == "Atk" and myAttackRdy == 0: 
                selectCheck = attackOptionMenu(player.friends[0].attackList)
                if selectCheck < 30:
                    mySelectedAttackName = player.friends[0].attackList[selectCheck].name
                    mySelectedAttackNum = selectCheck
                    myAttackRdy = 1
            elif options[currentSelect] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmePlayer.friends[0])
                tempPlayer.friends.append(player.friends[0])
                showMonInfo(tempPlayer, 0 , 1)
                del tempPlayer
            elif options[currentSelect] == "Swap":
                if swapCheck == 1:
                    pass #make something to say already swapped
                tempCurrentMon = player.friends[0].statBlock['given_name']
                showMonInfo(myGuy, 0, 2)
                if tempCurrentMon != player.friends[0].statBlock['given_name']:
                    swapCheck = 1
                    myAttackRdy = 0
                    #might need to do auto switch here
        if currentSelect == 30 or currentSelect == 28 or currentSelect == 29 :
            currentSelect = tempSelect    

        try:        
            if nmeActiveInfo != None:
                if nmeActiveInfo[0]['given_name'] != nmePlayer.friends[0].statBlock['given_name'] or (nmeActiveInfo[0]['given_name'] != None and nmeActiveInfo[0]['given_name'] != nmePlayer.friends[0].statBlock['given_name']):
                    for x in range(0, len(nmePlayer.friends)): 
                        if nmePlayer.friends[x].statBlock['given_name'] == nmeActiveInfo[0]['given_name']:
                            tempName = nmePlayer.friends[0].statBlock['given_name']
                            switchActiveMon(nmePlayer, nmePlayer.friends[0], nmePlayer.friends[x], x) #y'know i think some of this looks redundant now? but it works
                            nmeAttackRdy = 0
                            myAttackRdy = 0
                            thingAquired(nmePlayer.playerBlock['name'], "told", tempName, "to retreat!", 1,0,0)
                            thingAquired(nmePlayer.playerBlock['name'], "told", nmePlayer.friends[0].statBlock['given_name'], "to attack!", 1,0,0)
        except Exception as e:
            print(e)
            f = open("/Games/Tiny_Monster_Trainer/liveMulti56.log", "w")
            f.write(str(e) + " on Line 679. ish " )
            f.close() 
                
            
        try:
            if nmeActiveInfo != None:
                if nmeAttackRdy == 0:
                    if nmeActiveInfo[0]['attackNameStr'] != "" or (nmeActiveInfo[0]['attackNameStr'] != None and nmeActiveInfo[0]['attackNameStr'] != "") :
                        for x in range(0, len(nmePlayer.friends[0].attackList)): 
                            if nmePlayer.friends[0].attackList[x].name == nmeActiveInfo[0]['attackNameStr']:
                                tempName = nmePlayer.friends[0].attackList[x].name
                                #thingAquired(nmePlayer.playerBlock['name'], "told", nmePlayer.friends[0].statBlock['given_name'], "to attack!", 1,0,0)#Set switch check to 1 in case I try to change mon after I picked an attack, actually should make it so they have to wait after attack is made
                                #thingAquired(nmePlayer.friends[0].statBlock['given_name'], "uses", nmePlayer.friends[0].attackList[x].name, "", 1,0,0)
                                nmeAtkToUse = x 
                                nmeAttackRdy = 1
                    else:
                        nmeAttackRdy = 0
        except Exception as e:
            print(e)
            f = open("/Games/Tiny_Monster_Trainer/liveMulti4.log", "w")
            f.write(str(e) + " on Line 675. ish " )
            f.close() 
        
        nmeActiveInfo = sAndrCheckActiveMon(player.friends[0].statBlock['given_name'], mySelectedAttackName, nmeActiveInfo, ("test"+str(myAttackRdy)))
        if nmeActiveInfo != None:
            if nmeActiveInfo[0]['sAndrKey'] == "test1" and myAttackRdy == 1 and nmeAttackRdy == 1:
                for x in range(0,50):
                    nmeActiveInfo = sAndrCheckActiveMon(player.friends[0].statBlock['given_name'], mySelectedAttackName, nmeActiveInfo, ("test"+str(myAttackRdy)))
                time.sleep(1)
        

        printMon(player.friends[0].bodyBlock, 0, 1, 0)
        printMon(nmePlayer.friends[0].bodyBlock, 25, 1, 1)
        thumby.display.update()
        
        playerB4hp = player.friends[0].statBlock['currentHealth']
        nmeB4hp = nmePlayer.friends[0].statBlock['currentHealth']    
        
        try:
            if sOr == 1 and myAttackRdy == 1 and nmeAttackRdy == 1 and player.friends[0].statBlock['currentHealth'] >= 1 and nmePlayer.friends[0].statBlock['currentHealth'] >= 1 :
                myDodge = multiPlayerDodge(player.friends[0], nmePlayer.friends[0], player.friends[0].attackList[mySelectedAttackNum], player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel']) 
                oppDodge = multiPlayerDodge(nmePlayer.friends[0], player.friends[0], nmePlayer.friends[0].attackList[nmeAtkToUse], nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
                myDmg = multiPlayerAttack(player.friends[0], nmePlayer.friends[0], player.friends[0].attackList[mySelectedAttackNum], player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel'])
                if oppDodge > 0: #"what's oppDodge? Not much, what's up with you?" 
                    myDmg = math.floor(myDmg / oppDodge) 
                oppDmg = multiPlayerAttack(nmePlayer.friends[0], player.friends[0], nmePlayer.friends[0].attackList[nmeAtkToUse], nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
                if myDodge > 0:
                    oppDmg = math.floor(oppDmg / myDodge)
                agileTie = 0
                if (player.friends[0].statBlock['Agility'] + player.playerBlock['trainerLevel']) == (nmePlayer.friends[0].statBlock['Agility'] + nmePlayer.playerBlock['trainerLevel']):
                        agileTie = random.randint(-2,1)
                if (player.friends[0].statBlock['Agility'] + player.playerBlock['trainerLevel'] + agileTie) >= (nmePlayer.friends[0].statBlock['Agility'] + nmePlayer.playerBlock['trainerLevel']):
                    whoWentFirst = 1
                    if player.friends[0].attackList[mySelectedAttackNum].currentUses <= 0:
                        player.friends[0].statBlock['currentHealth'] = math.floor(player.friends[0].statBlock['currentHealth'] * 0.7)
                        myMoveOutOfStam = 1
                    player.friends[0].attackList[mySelectedAttackNum].currentUses = player.friends[0].attackList[mySelectedAttackNum].currentUses -1                            
                    if player.friends[0].attackList[mySelectedAttackNum].currentUses < 0:
                        player.friends[0].attackList[mySelectedAttackNum].currentUses = 0
                    if player.friends[0].statBlock['currentHealth'] > 0:
                        nmePlayer.friends[0].statBlock['currentHealth'] = nmePlayer.friends[0].statBlock['currentHealth'] - myDmg 
                        if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                            if nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses <= 0:
                                nmePlayer.friends[0].statBlock['currentHealth'] = math.floor(nmePlayer.friends[0].statBlock['currentHealth'] * 0.7)
                                oppMoveOutOfStam = 1
                            if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                                nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses = nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses -1 
                            if nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses < 0:
                                nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses = 0
                            if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                                player.friends[0].statBlock['currentHealth'] = player.friends[0].statBlock['currentHealth'] - oppDmg
                else:
                    whoWentFirst = 0
                    if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                        if nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses <= 0:
                            nmePlayer.friends[0].statBlock['currentHealth'] = math.floor(nmePlayer.friends[0].statBlock['currentHealth'] * 0.7)
                            oppMoveOutOfStam = 1
                    nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses = nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses - 1 
                    if nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses < 0:
                        nmePlayer.friends[0].attackList[nmeAtkToUse].currentUses = 0
                    if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                        player.friends[0].statBlock['currentHealth'] = player.friends[0].statBlock['currentHealth'] - oppDmg 
                        if player.friends[0].statBlock['currentHealth'] > 0:
                            if player.friends[0].attackList[mySelectedAttackNum].currentUses <= 0:
                                player.friends[0].statBlock['currentHealth'] = math.floor(player.friends[0].statBlock['currentHealth'] * 0.7)
                                myMoveOutOfStam = 1
                            player.friends[0].attackList[mySelectedAttackNum].currentUses = player.friends[0].attackList[mySelectedAttackNum].currentUses -1                            
                            if player.friends[0].attackList[mySelectedAttackNum].currentUses < 0:
                                player.friends[0].attackList[mySelectedAttackNum].currentUses = 0
                            if player.friends[0].statBlock['currentHealth'] > 0:
                                nmePlayer.friends[0].statBlock['currentHealth'] = nmePlayer.friends[0].statBlock['currentHealth'] - myDmg 
                attackResultsSend = [{'nmeMonHP' : nmePlayer.friends[0].statBlock['currentHealth'], 'OppMooS' : oppMoveOutOfStam, 'myMonHP': player.friends[0].statBlock['currentHealth'], 'myMooS' : myMoveOutOfStam, 'whoGoesFirst' : whoWentFirst, 'sAndrKey' : 'test4'}]
                del attackResultsKeep
                attackResultsKeep = attackResultsSend.copy()
                try:                    
                    while attackResultsSend[0]['sAndrKey'] == "test4":
                        attackResultsSend = sAndrAfterDmg(attackResultsKeep)
                    if attackResultsSend[0]['sAndrKey'] == "test5" or attackResultsSend[0]['sAndrKey'] == "test6" :
                        for x in range(0,15):
                            attackResultsSend = sAndrAfterDmg(attackResultsKeep)
                        #time.sleep(1) 11-6-22 tried to lower to .2, try it out and see how it goes
                        #maybe clear screen here?
                        time.sleep(.2)
                    del attackResultsSend
                except Exception as e:
                    print(e)
                    f = open("/Games/Tiny_Monster_Trainer/liveMulti29.log", "w")
                    f.write(str(e) + " on Line 781. ish " )
                    f.close() 
                    

                
                if player.friends[0].statBlock['currentHealth'] < 0:
                    player.friends[0].statBlock['currentHealth'] = 0
                if nmePlayer.friends[0].statBlock['currentHealth'] < 0:
                    nmePlayer.friends[0].statBlock['currentHealth'] = 0
                    
                myScroller = TextForScroller(player.friends[0].statBlock['given_name'] + " has " + str(player.friends[0].statBlock['currentHealth']) + " HP. " + nmePlayer.friends[0].statBlock['given_name'] + " has " + str(nmePlayer.friends[0].statBlock['currentHealth']) + " HP.")

        except Exception as e:
            print(e)
            f = open("/Games/Tiny_Monster_Trainer/liveMulti464.log", "w")
            f.write(str(e) + " on Line 806. ish " )
            f.close()    
        
        if sOr == 0 and myAttackRdy == 1 and nmeAttackRdy == 1 and player.friends[0].statBlock['currentHealth'] >= 1 and nmePlayer.friends[0].statBlock['currentHealth'] >= 1:
            try:
                attackResultsKeep[0]['sAndrKey'] = "test4"
                while attackResultsKeep[0]['sAndrKey'] == "test4":
                    attackResultsKeep = sAndrAfterDmg(attackResultsKeep) 
                if attackResultsKeep[0]['sAndrKey'] == "test5" or attackResultsKeep[0]['sAndrKey'] == "test6" :
                    for x in range(0,15):
                        attackResultsKeep = sAndrAfterDmg(attackResultsKeep)
                        #thingAquired("in sor 0", "for", str(x), attackResultsKeep[0]['sAndrKey'] + " " + str(attackResultsKeep[0]['nmeMonHP']) + " " + str(attackResultsKeep[0]['myMonHP']), 0,0,0)
                    #time.sleep(1) changed this to .2 on 11*6*22, trying it out might go back to 1 and clear screen
                    time.sleep(.2)
                player.friends[0].statBlock['currentHealth'] = attackResultsKeep[0]['nmeMonHP']
                nmePlayer.friends[0].statBlock['currentHealth'] = attackResultsKeep[0]['myMonHP'] 
                
                if player.friends[0].statBlock['currentHealth'] < 0:
                    player.friends[0].statBlock['currentHealth'] = 0
                if nmePlayer.friends[0].statBlock['currentHealth'] < 0:
                    nmePlayer.friends[0].statBlock['currentHealth'] = 0
                    
                myScroller = TextForScroller(player.friends[0].statBlock['given_name'] + " has " + str(player.friends[0].statBlock['currentHealth']) + " HP. " + nmePlayer.friends[0].statBlock['given_name'] + " has " + str(nmePlayer.friends[0].statBlock['currentHealth']) + " HP.")
                
            except Exception as e:
                print(e)
                f = open("/Games/Tiny_Monster_Trainer/liveMulti24.log", "w")
                f.write(str(e) + " on Line 797. ish " )
                f.close()         
    

        if player.friends[0].statBlock['currentHealth'] < 0:
            player.friends[0].statBlock['currentHealth'] = 0
        if nmePlayer.friends[0].statBlock['currentHealth'] < 0:
            nmePlayer.friends[0].statBlock['currentHealth'] = 0
        
        if myAttackRdy == 1 and nmeAttackRdy == 1:
            # need to print if out off stamina and if HP was lost
            attackAnimation(player.friends[0].bodyBlock, nmePlayer.friends[0].bodyBlock, attackResultsKeep[0]['whoGoesFirst'], sOr, playerB4hp, player.friends[0].statBlock['currentHealth'], nmeB4hp, nmePlayer.friends[0].statBlock['currentHealth'], player.friends[0].attackList[mySelectedAttackNum].moveElementType, nmePlayer.friends[0].attackList[nmeAtkToUse].moveElementType, attackResultsKeep[0]['OppMooS'], attackResultsKeep[0]['myMooS'])
            if player.friends[0].statBlock['currentHealth'] == 0:
                thingAquired(player.friends[0].statBlock['given_name'], "was", "knocked", " out!", 1, 0, 0)
            if nmePlayer.friends[0].statBlock['currentHealth'] == 0:
                thingAquired(nmePlayer.friends[0].statBlock['given_name'], "was", "knocked", " out!", 1, 0, 0)
            myAttackRdy = 0
            mySelectedAttackName = ""
            nmeAttackRdy = 0
            nmeActiveInfo[0]['attackNameStr'] = ""
        
        #maybe move this auto switch stuff to the if above, but i forget if autoswitch needs to constantly be checked in the loop
        checkAutoSwitch = nmePlayer.friends[0].statBlock['given_name']
        autoSwitchMon(ghost)
        autoSwitchMon(myGuy)
        if nmePlayer.friends[0].statBlock['given_name'] != checkAutoSwitch:
            nmeActiveInfo = None

    #thingAquired("at end", "of", "function", "", 5,0,0)
    return 0



def sAndrCheckActiveMon(playerCurMonGName, activeAttack, theirPrevInfo, testKey):
    thingToSend = [{"sAndrKey" : testKey, "given_name" : str(playerCurMonGName), "attackNameStr" : str(activeAttack)}]
    #theirName = ""
    #print(thingToSend)
    thumby.link.send(ujson.dumps(thingToSend).encode())
    received = thumby.link.receive()

    if received != None:
        theirStuff = ujson.loads(received.decode())
        if theirStuff[0]['sAndrKey'] == "test1" or theirStuff[0]['sAndrKey'] == "test0":
            thumby.link.send(ujson.dumps(thingToSend).encode())
            return theirStuff
    else:
        return theirPrevInfo 



def sAndrAfterDmg(resultInfoList): ###########
        
    thumby.link.send(ujson.dumps(resultInfoList).encode())
    received = thumby.link.receive()

    if received != None:
        theirStuff = ujson.loads(received.decode())
        if theirStuff[0]['sAndrKey'] == "test5":
            theirStuff[0]['sAndrKey'] = "test6"
            return theirStuff
        elif theirStuff[0]['sAndrKey'] == "test4":
            theirStuff[0]['sAndrKey'] = "test5"
            return theirStuff
        else:
            return resultInfoList #might need to return a junk value or something, dunno yet
    else:
        return resultInfoList 

        
ghostFile = pickGhost()
thumby.display.fill(0)
thumby.display.update()
sendOrReceive = findWhoSendsFirst()
if ghostFile != "":
    myGuy = Player()
    myGuy = loadGame()
    ghost = Player()
    ghost = loadGhost(ghostFile)
    
    
    playAgain = 1
    
    while(playAgain == 1):
        drawIntro(myGuy, ghost)
        
        victory=0
        activeMon=0
        battle=1
        
        random.seed(time.ticks_ms())
       
        for x in range(0,len(myGuy.friends)):
            myGuy.friends[x].statBlock['currentHealth'] = myGuy.friends[x].statBlock['Health']
            for attacks in range(0, len(myGuy.friends[x].attackList)):
                myGuy.friends[x].attackList[attacks-1].currentUses = myGuy.friends[x].attackList[attacks-1].numUses
        for x in range(0,len(ghost.friends)):
            ghost.friends[x].statBlock['currentHealth'] = ghost.friends[x].statBlock['Health']
            for attacks in range(0, len(ghost.friends[x].attackList)):
                ghost.friends[x].attackList[attacks-1].currentUses = ghost.friends[x].attackList[attacks-1].numUses
        
        while(battle == 1):
            victory = 0
            thumby.display.fill(0)
            try:
                victory = MultiPlayerBattleScreen(myGuy, ghost, sendOrReceive)
            except Exception as e:
                print(e)
                f = open("/Games/Tiny_Monster_Trainer/liveMulti1.log", "w")
                f.write(str(e) + " on Line 837. ish " )
                f.close() 
    
            if myGuy.friends[activeMon].statBlock['currentHealth'] <= 0:
                battle = 0
            if ghost.friends[activeMon].statBlock['currentHealth'] <= 0:
                battle = 0
                victory = 1
            thumby.display.update()
    
            thingAquired("M:"+str(myGuy.friends[activeMon].statBlock['currentHealth'])+" E:"+str(ghost.friends[x].statBlock['currentHealth']),"out of","battle",str(victory),1,0,0)
                
        if victory == 1:        
            battleStartAnimation(0)
            thingAquired("****************", "You", " Win!", "****************", 4, 0, 0)
        else:
            battleStartAnimation(0)
            thingAquired("................", "You", "Lost!", "................", 4, 0, 0)
