import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
import machine
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Map, Monster, Tile, RoamingMonster, TextForScroller, Item, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, popItOff, buttonInput, noDupAtk, giveName, tameMon, switchActiveMon, save, showMonInfo


def loadGame():
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson')
    bigJson = ujson.load(f)
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
    if bigJson[0]['items'] != [{}]:
        for x in range(0, len(bigJson[0]['items'][0])):
            tempPlayer.inventory.append(Item(bigJson[0]['items'][0]['item' + str(x)]['name'],
                                            bigJson[0]['items'][0]['item' + str(x)]['key'],
                                            bigJson[0]['items'][0]['item' + str(x)]['bonus']))
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
        if playerInfo.friends[0].statBlock['currentHealth'] > 0:
            thingAquired(playerInfo.playerBlock['name']+"'s", playerInfo.friends[0].statBlock['given_name'], "is now",  "Acvtive!", 2)

'''
def refresh(curMon):
    curMon.statBlock['currentHealth'] = curMon.statBlock['Health']
    for attacks in range(0, len(curMon.attackList)):
        curMon.attackList[attacks-1].currentUses = curMon.attackList[attacks-1].numUses
        print(str(curMon['currentHealth']))'''


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
    bottomText = "Pick a Ghost"
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
    
    ghostTitle = getTitle(ghost.playerBlock['worldSeed'])
    #thingAquired(player.playerBlock['name'], "Vs.", ghostTitle, ghost.playerBlock['name'],0,1,1)
    
    t0 = 0
    ct0 = time.ticks_ms()
    x = 10 
    y = 11
    animateCount = 0
    thumby.display.fill(0)
    thumby.display.update()
    time.sleep(1)
    while(t0 - ct0 < 5000):
        t0 = time.ticks_ms()
        randoNumber = random.randint(-1,1)
        randoNumber2 = random.randint(-1,1)
        randoNumber3 = random.randint(-1,1)
        thumby.display.fill(0)
        if(t0 - ct0 > 2800):
            thingAquired(player.playerBlock['name'], "Vs", ghostTitle, ghost.playerBlock['name'],0,1,1)
            thumby.display.blit(bytearray(player.sprite), x+randoNumber-8 , y+randoNumber2, 8, 8, -1, 1, 0)
            thumby.display.blit(bytearray(ghost.sprite), 72-(x+randoNumber2) , y+randoNumber3, 8, 8, -1, ghost.lOrR, 0)
        animateCount = animateCount + 1 
        thumby.display.drawFilledRectangle(-36+animateCount, 0, 36, 40, 1)
        thumby.display.drawFilledRectangle(72-animateCount, 0, 36, 40, 1)
        thumby.display.update()


def getTitle(rSeed):
    random.seed(rSeed)
    titleList=["Eldritch", "Murky", "The Lich", "Elder",
                "Ye Old", "Undead", "Spooky", "Spooky",
                "Spooky", "Gastly", "Haunting", "Just"]
    title = random.randint(0,11)
    return titleList[title]
    
    
def wantToPlayAgain():
    
    battleStartAnimation(0)
    waiting = True
    currentSelect = 0
    t0 = 0
    ct0 = time.ticks_ms()
    while(waiting):
        thingAquired("", "Play", " Again?", "A:Y B:N", 0, 0, 0)
        t0 = time.ticks_ms()
        if(t0 - ct0 >= 10000):
            waiting = False
        if currentSelect == 0:
            currentSelect = buttonInput(currentSelect)
            if currentSelect == 31:
                waiting = False
            elif currentSelect == 30:
                machine.reset()
            else:
                currentSelect = 0



class Battle:
    def __init__(self):                                           
        self.battleBlock = {'myMon' : "", #maybe just have an empty dict here
                            'nmeMon' : "",
                            'myTL' : 0,
                            'nmeTL' : 0,
                            'myDmg' : 0,
                            'nmeDmg' : 0,
                            'myB4hp' : 0,
                            'nmeB4hp' : 0,
                            'textScroll' : "",
                            'curAtkSlct' : 15,
                            'prvAtkSlct': 0,
                            'nmeAtkSlct': 0,
                            }
        self.options = ["Info", "Atk", "Swap"] #add tame
    
    
    def setBattle(self, player, nmePlayer):
        self.battleBlock = {'myMon' : player.friends[0].statBlock['given_name'],
                            'nmeMon' : nmePlayer.friends[0].statBlock['given_name'],
                            'myTL' : player.playerBlock['trainerLevel'],
                            'nmeTL' : nmePlayer.playerBlock['trainerLevel'],
                            'myDmg' : 0,
                            'nmeDmg' : 0,
                            'myB4hp' : 0,
                            'nmeB4hp' : 0,
                            'textScroll' : player.friends[0].statBlock['given_name'] + " has entered into battle with " + nmePlayer.friends[0].statBlock['given_name'] + "!",
                            'curAtkSlct' : 15,
                            'prvAtkSlct': 0,
                            'nmeAtkSlct': 0,
                            }
    

    def attackOptionMenu(self, monAtkList, prvSlct):  
        currentSelect = prvSlct
        tempSelect = currentSelect
        playerOptionList = []
        
        for attacksKnown in range(0, len(monAtkList)):
            playerOptionList.append(monAtkList[attacksKnown].name)
            
        while(currentSelect < 29):
            thumby.display.fill(0)
            tempSelect = currentSelect
            if currentSelect == len(monAtkList):
                currentSelect = currentSelect - 1
            if currentSelect == -abs(len(monAtkList)):
                currentSelect = currentSelect + 1
            currentSelect = showOptions(playerOptionList, currentSelect, "Stamina: " + str(monAtkList[currentSelect].currentUses))
            thumby.display.update()
            if currentSelect == 31:
                return tempSelect 
            elif currentSelect == 30:
                return 30 
            elif currentSelect == 28 or currentSelect == 29:
                currentSelect = tempSelect
                
    def typeAsNum(self, moveType):
        typeList = ["", "Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                    "Mind", "Physical", "Mystical", "Ethereal"]
        typeNumber = 0
        for i in range(0,12):
            if moveType == typeList[i]:
                typeNumber = i
        return typeNumber
    
    
    def isTypeWeak(self, mon1Type, mon2Type): 
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
    

    def isTypeStrong(self, mon1Type, mon2Type): 
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
        
    
    def attack(self, attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
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
            atkTypeBonus = self.isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
        for x in range(1,3):
            defTypeBonus = self.isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
        damage = math.ceil((attackAmnt * atkTypeBonus)/3) - math.ceil((defence * defTypeBonus)/3)
        if damage <= 0:
            damage = 1
        return damage
        
        
    def dodge(self, attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    
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
    
    
    def staChk(self, mon2Chk, atkSel):
        watMon = 0
        if mon2Chk.statBlock['currentHealth'] == self.battleBlock['myB4hp'] and self.battleBlock['myB4hp'] != self.battleBlock['nmeB4hp']:
            watMon = 1
        elif mon2Chk.statBlock['currentHealth'] == self.battleBlock['nmeB4hp'] and self.battleBlock['myB4hp'] != self.battleBlock['nmeB4hp']:
            watMon = 2
        else:
            print("in else")
            #pass
        if mon2Chk.attackList[atkSel].currentUses <= 0:
            outStaHP = math.floor(mon2Chk.statBlock['currentHealth'] * 0.7)
            print(str(outStaHP))
            thingAquired(mon2Chk.statBlock['given_name'], "doesn't have", "enough", "stamina!", 2, 0, 0)
            thingAquired(mon2Chk.statBlock['given_name'], "hurt itself", "and goes down", "to "+str(outStaHP)+" HP!", 2, 0, 0)
            mon2Chk.statBlock['currentHealth'] = outStaHP
        mon2Chk.attackList[atkSel].currentUses = mon2Chk.attackList[atkSel].currentUses -1                            
        if mon2Chk.attackList[atkSel].currentUses < 0:
            mon2Chk.attackList[atkSel].currentUses = 0
        if watMon == 1:
            self.battleBlock['myB4hp'] = mon2Chk.statBlock['currentHealth'] 
        elif watMon == 2:
            self.battleBlock['nmeB4hp'] = mon2Chk.statBlock['currentHealth']
        else:
            print("Butts")
            
            
    def damageTxt(self, player, nme):
        damage = btl.battleBlock['nmeB4hp'] - nme.friends[0].statBlock['currentHealth']
        sOrNo = ""
        if damage > 0:
            if damage > 1:
                sOrNo = "s"
            self.battleBlock['textScroll'] = player.friends[0].statBlock['given_name']+" hit "+nme.friends[0].statBlock['given_name']+" for "+str(damage)+" point"+sOrNo+" of damage!"
        else:
            self.battleBlock['textScroll'] = player.friends[0].statBlock['given_name']+" missed "+nme.friends[0].statBlock['given_name']+"!"


    def battleCrunch(self, firstMon, secMon, firstAtk, SecAtk, firstTL, secTL): #(should be able to use self.battleBlock['curAtkSlct']) and not send firstAtk
        #firstMonHP = firstMon.statBlock['currentHealth']
        #secMonHP = secMon.statBlock['currentHealth']
        
        firstDodge = self.dodge(secMon, firstMon, secMon.attackList[SecAtk]) #, player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel'])  ########### remember to look at this to see if i'm doing the right mon's attack
        secDodge = self.dodge(firstMon, secMon, firstMon.attackList[firstAtk]) #, nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
        firstDmg = self.attack(firstMon, secMon, firstMon.attackList[firstAtk]) #, btl.battleBlock['myTL'], btl.battleBlock['nmeTL'])
        secDmg = self.attack(secMon, firstMon, secMon.attackList[SecAtk]) #, nmePlayer.playerBlock['trainerLevel'], firstMon.playerBlock['trainerLevel'])

        if firstDodge > 0:
            secDmg = math.floor(secDmg / firstDodge)      
        if secDodge > 0: 
            firstDmg = math.floor(firstDmg / secDodge)
        self.staChk(firstMon, firstAtk)
        if firstMon.statBlock['currentHealth'] > 0:
            secMon.statBlock['currentHealth'] = secMon.statBlock['currentHealth'] - firstDmg 
            self.staChk(secMon, SecAtk)
            self.chkBlw0(secMon)
            if secMon.statBlock['currentHealth'] > 0:
                firstMon.statBlock['currentHealth'] = firstMon.statBlock['currentHealth'] - secDmg
         # something is happening around here that makes it so a monster goes to 1 hp from 2 then attacks and just dies?
        self.chkBlw0(firstMon)
        
        
    def chkBlw0(self, monster):
        if monster.statBlock['currentHealth'] < 0:
            monster.statBlock['currentHealth'] = 0
            
    
    def makeSlct(self, player, nmeFrens, CS, PS):
        if CS == 31: # 31 = selection made so go on to see what happens
            CS = PS #reset curSelect to prevSelect so it's not 31 anymore
            if self.options[CS] == "Atk": # and myAttackRdy == 0: <-ignore comment
                self.battleBlock['curAtkSlct'] = self.attackOptionMenu(player.friends[0].attackList, self.battleBlock['prvAtkSlct']) #get the attack's number from user
                if self.battleBlock['curAtkSlct'] < 30: # < 30 = an attack is selected, make prvAtkSlct = curAtkSlct
                    self.battleBlock['prvAtkSlct'] = self.battleBlock['curAtkSlct']
                else:
                    self.battleBlock['curAtkSlct'] = 15 # 15 = no attack selected
                     
            elif self.options[CS] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmeFrens[0])
                tempPlayer.friends.append(player.friends[0])
                showMonInfo(tempPlayer, 0, 1)
                del tempPlayer
            elif self.options[CS] == "Swap":
                showMonInfo(player, 0, 2)
        if CS == 30 or CS == 28 or CS == 29 :
            CS = PS   
        return CS

    
    def drawScreen(self, myScroller, player, nme, CS, PS): 
        thumby.display.setFPS(40)
        CS = showOptions(self.options, curSelect, "", 47)
        if CS  > 27:
            CS = btl.makeSlct(myGuy, ghost.friends, CS, PS)
        printMon(player.friends[0].bodyBlock, 0, 1, 0)
        printMon(nme.friends[0].bodyBlock, 25, 1, 1)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)

        return CS


    def npcAtkSel(self, npcAtkList):
        self.battleBlock['nmeAtkSlct'] = random.randint(0,len(npcAtkList)) - 1


    def attackAnimation(self, playerBod, nmeBod, whoFirst, sOr, playerHP, playerAfterDmg, nmeHP, nmeAfterDmg, playerAtkElm, nmeAtkElm): #, nmeOos, playerOos):
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
        playerAttackTypeNum = self.typeAsNum(playerAtkElm)
        nmeAttackTypeNum = self.typeAsNum(nmeAtkElm)
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
        
        



while(1):
    ghostFile = pickGhost()
    thumby.display.fill(0)
    thumby.display.update()

    
    if ghostFile != "":
        myGuy = Player()
        myGuy = loadGame()
        ghost = Player()
        ghost = loadGhost(ghostFile)
        
        drawIntro(myGuy, ghost)
        
        victory=0
        activeMon=0
        btl = Battle()
        
        battle=1
        
        for x in range(0,len(myGuy.friends)):
            myGuy.friends[x].statBlock['currentHealth'] = myGuy.friends[x].statBlock['Health']
            for attacks in range(0, len(myGuy.friends[x].attackList)):
                myGuy.friends[x].attackList[attacks-1].currentUses = myGuy.friends[x].attackList[attacks-1].numUses
        for x in range(0,len(ghost.friends)):
            ghost.friends[x].statBlock['currentHealth'] = ghost.friends[x].statBlock['Health']
            for attacks in range(0, len(ghost.friends[x].attackList)):
                ghost.friends[x].attackList[attacks-1].currentUses = ghost.friends[x].attackList[attacks-1].numUses

        btl.setBattle(myGuy, ghost)
        myScroller = TextForScroller(btl.battleBlock['textScroll'])
        
        curSelect = 1
        prevSelect = 1
        while(battle == 1):
            victory = 0
            #thumby.display.fill(0)

            prevSelect = curSelect
            curSelect = btl.drawScreen(myScroller, myGuy, ghost, curSelect, prevSelect)

            whoGoesFirst = 0
            sOr = 0
            btl.battleBlock['myB4hp'] = myGuy.friends[0].statBlock['currentHealth'] - 0
            btl.battleBlock['nmeB4hp'] = ghost.friends[0].statBlock['currentHealth'] - 0

            #ok, make an equation with - 0 to try to copy something

            if btl.battleBlock['curAtkSlct'] != 15:
                agileTie = random.randint(-2,1)
                if (myGuy.friends[0].statBlock['Agility'] + myGuy.playerBlock['trainerLevel'] + agileTie) >= (ghost.friends[0].statBlock['Agility'] + ghost.playerBlock['trainerLevel']):
                    btl.npcAtkSel(ghost.friends[0].attackList)
                    btl.battleCrunch(myGuy.friends[0], ghost.friends[0], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['myTL'], btl.battleBlock['nmeTL'])
                    whoGoesFirst = 0
                else:
                    btl.npcAtkSel(ghost.friends[0].attackList)
                    btl.battleCrunch(ghost.friends[0], myGuy.friends[0], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeTL'], btl.battleBlock['myTL'])
                    whoGoesFirst = 1

                btl.attackAnimation(myGuy.friends[0].bodyBlock,
                                ghost.friends[0].bodyBlock,
                                whoGoesFirst,
                                sOr,
                                btl.battleBlock['myB4hp'],
                                myGuy.friends[0].statBlock['currentHealth'],
                                btl.battleBlock['nmeB4hp'],
                                ghost.friends[0].statBlock['currentHealth'],
                                myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].moveElementType,
                                ghost.friends[0].attackList[btl.battleBlock['nmeAtkSlct']].moveElementType) # need to actually get a monster attack
                
                #reminder to reset scroller starting pos after an attack
                #out of sta not removing hp
                #
                btl.battleBlock['prvAtkSlct'] = btl.battleBlock['curAtkSlct']
                btl.damageTxt(myGuy, ghost)
                if myScroller.scrollingText != btl.battleBlock['textScroll']:
                    myScroller = TextForScroller(btl.battleBlock['textScroll'])
            btl.battleBlock['curAtkSlct'] = 15

            autoSwitchMon(ghost)
            autoSwitchMon(myGuy)
            if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
            if ghost.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
                victory = 1

            thumby.display.update()

            if victory == 1:
                battle = 0

        if victory == 1:        
            battleStartAnimation(0)
            thingAquired("","You Win!","","",4,0,0)
        else:
            battleStartAnimation(0)
            thingAquired("","You Lost!","","",4,0,0)
    
    wantToPlayAgain()
