# This is just a backup of a rewrite in progress, for the battle screen & combat code

import time
import thumby
import math
import random

class BattleScreen:
    def __init__(self):                                           
        self.battleBlock = {'myMon' : "",
                            'nmeMon' : "",
                            'myTL' : 0,
                            'nmeTL' : 0,
                            'myDmg' : 0,
                            'nmeDmg' : 0,
                            'textScroll' : "",
                            'curSelect' : 0,
                            'curAtkSlct' : 15,
                            'prvAtkSlct': 0,
                            'nmeAtkSlct':0
                            }
        self.options = ["Info", "Atk", "Swap"] 
    
    def setBattleScreen(player, nmePlayer)
        self.battleBlock = {'myMon' : player.friends[0].statBlock['given_name'],
                            'nmeMon' : nmePlayer.friends[0].statBlock['given_name'],
                            'myTL' : player.playerBlock['trainerLevel'],
                            'nmeTL' : nmePlayer.playerBlock['trainerLevel'],
                            'myDmg' : 0,
                            'nmeDmg' : 0,
                            'myOutSta' : 0,
                            'nmeOutSta' : 0,
                            'textScroll' : self.battleBlock['textScroll'] = TextForScroller(self.battleBlock['myMon'] + " has entered into battle with " + self.battleBlock['nmeMon'] + "!"),
                            'curSelect' : 0,
                            'prvAtkSlct': 0}
    

    def attackOptionMenu(monAtkList, prvSlct):  
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
    
    def attack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
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
        
    def dodge(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    
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
    
    
    def outOfStaChk(mon2Chk):
        if firstMon[0].attackList[self.battleBlock[curAtkSlct]].currentUses <= 0:
            player.friends[0].statBlock['currentHealth'] = math.floor(player.friends[0].statBlock['currentHealth'] * 0.7)
            self.battleBlock['myOutSta'] = 1
            firstMon[0].attackList[mySelectedAttackNum].currentUses = firstMon[0].attackList[mySelectedAttackNum].currentUses -1                            
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

    
    def battleCrunch(firstMon, secMon, firstAtk, SecAtk): #(should be able to use self.battleBlock['curAtkSlct']) and not send firstAtk
            firstDodge = btlScn.dodge(firstMon, secMon, firstMon.attackList[firstAtk]) #, player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel'])  ########### remember to look at this to see if i'm doing the right mon's attack
            secDodge = btlScn.dodge(secMon, firstMon, secMon.attackList[nmeAtkToUse]) #, nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
            firstDmg = btlScn.attack(firstMon, nmeGuy.friends[0], firstMon.attackList[firstAtk]) #, btlScn.battleBlock['myTL'], btlScn.battleBlock['nmeTL'])
            secDmg = btlScn.attack(secMon, firstMon.friends[0], nmePlayer.friends[0].attackList[nmeAtkToUse]) #, nmePlayer.playerBlock['trainerLevel'], firstMon.playerBlock['trainerLevel'])

            if secDodge > 0: #"what's oppDodge? Not much, what's up with you?" 
                firstDmg = math.floor(firstDmg / secDodge) 
            secDmg = multiPlayerAttack(secMon, firstMon, secMon[0].attackList[nmeAtkToUse]) #, nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
            if firstDodge > 0:
                secDmg = math.floor(secDmg / firstDodge)      
            outOfStaChk(firstMon)
            if player.friends[0].statBlock['currentHealth'] > 0:
                nmePlayer.friends[0].statBlock['currentHealth'] = nmePlayer.friends[0].statBlock['currentHealth'] - firstDmg 
                outOfStaChk(secMon)
                if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                    firstMon.statBlock['currentHealth'] = firstMon.statBlock['currentHealth'] - secDmg
    
    def makeSlct(player, nmeFrens):
         if self.battleBlock['curSelect'] == 31: 
            self.battleBlock['curSelect'] = tempSelect
            if self.options[self.battleBlock['curSelect']] == "Atk":# and myAttackRdy == 0: 
                self.battleBlock['curAtkSlct'] = attackOptionMenu(player.friends[0].attackList, self.battleBlock['prvAtkSlct'])
                if self.battleBlock['curAtkSlct'] < 30:
                    #mySelectedAttackName = player.friends[0].attackList[selectCheck].name
                    self.battleBlock['prvAtkSlct'] = self.battleBlock['curAtkSlct']
                    
                    
            elif self.options[self.battleBlock['curSelect']] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmeFrens[0])
                tempPlayer.friends.append(player.friends[0])
                showMonInfo(tempPlayer, 0 , 1)
                del tempPlayer
            elif self.options[self.battleBlock['curSelect']] == "Swap":
                showMonInfo(player, 0, 2)
        if self.battleBlock['curSelect'] == 30 or self.battleBlock['curSelect'] == 28 or self.battleBlock['curSelect'] == 29 :
            self.battleBlock['curSelect'] = tempSelect    
            
    def drawScreen(myAttackList):
        self.battleBlock['curSelect'] = showOptions(self.options, self.battleBlock['curSelect'], "", 47)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
       
            
main:
    btlScn = BattleScreen()
    setBattleScreen(myGuy, nmeGuy)
    loop
        btlScn.drawScreen()
        ~getInput     
        btlScn.makeSlct(myGuy, nmeGuy.friends)
        if btlScn.battleBlock['curAtkSlct'] != 15:
            agileTie = 0
            if (player.friends[0].statBlock['Agility'] + player.playerBlock['trainerLevel']) == (nmePlayer.friends[0].statBlock['Agility'] + nmePlayer.playerBlock['trainerLevel']):
                agileTie = random.randint(-2,1)
            if (player.friends[0].statBlock['Agility'] + player.playerBlock['trainerLevel'] + agileTie) >= (nmePlayer.friends[0].statBlock['Agility'] + nmePlayer.playerBlock['trainerLevel']):
                battleCrunch(myGuy, nmeGuy)
            else:
                battleCrunch(nmeGuy, myGuy)
            self.battleBlock['prvAtkSlct'] = btlScn.battleBlock['curAtkSlct']
            self.battleBlock['curAtkSlct'] = 15
        
        tempSelect = self.battleBlock['curSelect']
        
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
        
        
        
        self.lOrR = 0    
        self.friends = []
        self.inventory = []
        self.maxHelditems = 10
        self.currentPos = math.ceil((9 * 5) / 2)
        self.position = []
        self.sprite = [0,46,251,127,123,255,46,0]
        for i in range(9 * 5):
            self.position.append(0)
        self.position[self.currentPos] = 1
    
