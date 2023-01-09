import gc
gc.enable()
import time
import thumby
import math
import random
import math
import sys
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player
from funcLib import thingAquired, printMon, showOptions, showMonInfo

class Battle:
    def __init__(self):                                           
        self.battleBlock = {}
        self.options = ["Info", "Atk", "Swap", "Tame", "Run"] 
    
    
    def setBattle(self, player, nmePlayer, mode=0):
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
                            'whoFirst': 0,
                            'myText' : "",
                            'nmeText' : "",
                            'othrOpt' : 0
                            }
                            
        if mode == 1:
            self.options.pop(-1)
            self.options.pop(-1)
            self.battleBlock.pop('othrOpt')


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
            pass
        if mon2Chk.attackList[atkSel].currentUses <= 0:
            outStaHP = math.floor(mon2Chk.statBlock['currentHealth'] * 0.7)
            thingAquired(mon2Chk.statBlock['given_name'], "doesn't have", "enough", "stamina!", 2, 0, 0)
            thingAquired(mon2Chk.statBlock['given_name'], "hurt itself", "& goes down", "to "+str(outStaHP)+" HP!", 2, 0, 0)
            mon2Chk.statBlock['currentHealth'] = outStaHP
        mon2Chk.attackList[atkSel].currentUses = mon2Chk.attackList[atkSel].currentUses -1                            
        if mon2Chk.attackList[atkSel].currentUses < 0:
            mon2Chk.attackList[atkSel].currentUses = 0
        if watMon == 1:
            self.battleBlock['myB4hp'] = mon2Chk.statBlock['currentHealth'] 
        elif watMon == 2:
            self.battleBlock['nmeB4hp'] = mon2Chk.statBlock['currentHealth']
        else:
            pass
            
            
    def damageTxt(self, player, nme):
        damage = self.battleBlock['nmeB4hp'] - nme.friends[0].statBlock['currentHealth']
        sOrNo = ""
        if damage > 0:
            if damage > 1:
                sOrNo = "s"
            self.battleBlock['textScroll'] = player.friends[0].statBlock['given_name']+" hit "+nme.friends[0].statBlock['given_name']+" for "+str(damage)+" point"+sOrNo+" of damage!"
        else:
            self.battleBlock['textScroll'] = player.friends[0].statBlock['given_name']+" missed "+nme.friends[0].statBlock['given_name']+"!"

    
    def getComTxt(self, dodge, damage):
        if damage > 0 and dodge > 0:
            if dodge == 1: 
                return "Hit!"
            elif dodge == 2:
                return "Glance"
        elif dodge != 0 and damage == 0:
            return "Block"
        else:
            return "Miss"


    def battleCrunch(self, firstMon, secMon, firstAtk, SecAtk, firstTL, secTL): #(should be able to use self.battleBlock['curAtkSlct']) and not send firstAtk
        firstDmg = 0
        secDmg = 0
        firstDodge = self.dodge(secMon, firstMon, secMon.attackList[SecAtk]) #, player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel'])  ########### remember to look at this to see if i'm doing the right mon's attack
        secDodge = self.dodge(firstMon, secMon, firstMon.attackList[firstAtk]) #, nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
        if firstDodge > 0:
            secDmg = self.attack(secMon, firstMon, secMon.attackList[SecAtk]) #, nmePlayer.playerBlock['trainerLevel'], firstMon.playerBlock['trainerLevel'])
            secDmg = math.floor(secDmg / firstDodge)   
        if secDodge > 0: 
            firstDmg = self.attack(firstMon, secMon, firstMon.attackList[firstAtk]) #, btl.battleBlock['myTL'], btl.battleBlock['nmeTL'])
            firstDmg = math.floor(firstDmg / secDodge)
        self.staChk(firstMon, firstAtk)
        if firstMon.statBlock['currentHealth'] > 0:
            self.staChk(secMon, SecAtk)
            secMon.statBlock['currentHealth'] = secMon.statBlock['currentHealth'] - firstDmg 
            self.chkBlw0(secMon)
            if secMon.statBlock['currentHealth'] > 0:
                firstMon.statBlock['currentHealth'] = firstMon.statBlock['currentHealth'] - secDmg
        self.chkBlw0(firstMon)
        if self.battleBlock['whoFirst'] == 0: 
            self.battleBlock['myText'] = self.getComTxt(secDodge, firstDmg)
        else:
            self.battleBlock['nmeText'] = self.getComTxt(secDodge, firstDmg)
        if self.battleBlock['whoFirst'] == 1: 
            self.battleBlock['myText'] = self.getComTxt(firstDodge, secDmg)
        else:
            self.battleBlock['nmeText'] = self.getComTxt(firstDodge, secDmg)
        
            
    def chkBlw0(self, monster):
        if monster.statBlock['currentHealth'] < 0:
            monster.statBlock['currentHealth'] = 0
            
    
    def makeSlct(self, player, nmeFrens, CS, PS):
        if CS == 31:
            CS = PS 
            if self.options[CS] == "Atk": 
                self.battleBlock['curAtkSlct'] = self.attackOptionMenu(player.friends[0].attackList, self.battleBlock['prvAtkSlct']) #get the attack's number from user
                if self.battleBlock['curAtkSlct'] < 30: 
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
            elif self.options[CS] == "Tame":
                self.battleBlock['othrOpt'] = 1
            elif self.options[CS] == "Run":
                self.battleBlock['othrOpt'] = 2
        if CS == 30 or CS == 28 or CS == 29 :
            CS = PS   
        return CS

    
    def drawScreen(self, myScroller, player, nme, CS, PS): 
        thumby.display.setFPS(40)
        CS = showOptions(self.options, CS, "", 47)
        if CS  > 27:
            CS = self.makeSlct(player, nme.friends, CS, PS)
        printMon(player.friends[0].bodyBlock, 0, 1, 0)
        printMon(nme.friends[0].bodyBlock, 25, 1, 1)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
        return CS


    def npcAtkSel(self, npcAtkList):
        self.battleBlock['nmeAtkSlct'] = random.randint(0,len(npcAtkList)) - 1


    def attackAnimation(self, playerBod, nmeBod, playerAfterDmg, nmeAfterDmg, playerAtkElm, nmeAtkElm, sOr=0): 
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
        playGo = 0
        nmeGo = 0
        showPlayerHP = self.battleBlock['myB4hp']
        showNmeHP = self.battleBlock['nmeB4hp']
        if sOr == 0:
            if self.battleBlock['whoFirst'] == 1: 
                self.battleBlock['whoFirst'] = 0
            else: # whoFirst == 0:
                self.battleBlock['whoFirst'] = 1
        
        if self.battleBlock['whoFirst'] == 1:
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
                thumby.display.drawText(str(showNmeHP), 72 - len(str(self.battleBlock['nmeB4hp']) * 7), 30, 0)
                thumby.display.drawText(combatText, math.ceil(((72-(len(combatText))*6))/2)+1, 30, 0)
                if self.battleBlock['nmeB4hp'] == nmeAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and playerAtkedChk == 0 and playGo == 1: # player misses
                    combatText = self.battleBlock['myText']
                    playerAtked = 1
                    playerAttacking = 1
                elif self.battleBlock['nmeB4hp'] != nmeAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and playerAtkedChk == 0 and playGo == 1 : # player hits
                    thumby.display.blit(BoltArray[playerAttackTypeNum], (30 + animateX), math.floor(10+bobOffset), 8, 8, 0, 0, 0) #, flippy, 0)
                    showNmeHP = nmeAfterDmg
                    combatText = self.battleBlock['myText']
                    playerAtked = 1
                    playerAttacking = 1
                elif self.battleBlock['myB4hp'] == playerAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and nmeAtkedChk == 0 and nmeGo == 1: # nme misses
                    combatText = self.battleBlock['nmeText']
                    nmeAtked = 1
                    playerAttacking = 2
                elif self.battleBlock['myB4hp'] != playerAfterDmg and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and nmeAtkedChk == 0 and nmeGo == 1: # nme hits
                    thumby.display.blit(BoltArray[nmeAttackTypeNum], (36 - animateX), math.floor(10+bobOffset), 8, 8, 0, 1, 0) #, flippy, 0)
                    showPlayerHP = playerAfterDmg
                    combatText = self.battleBlock['nmeText']
                    nmeAtked = 1
                    playerAttacking = 2
                else:
                    pass
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
            if (nmeAfterDmg <= 0 and playerAtkedChk == 1) or (playerAfterDmg <= 0 and nmeAtkedChk == 1):
                break
