# This is just a backup of a rewrite in progress, for the battle screen & combat code

import time
import thumby
import math
import random

class Battle:
    def __init__(self):                                           
        self.battleBlock = {'myMon' : "", #maybe just have an empty dict here
                            'nmeMon' : "",
                            'myTL' : 0,
                            'nmeTL' : 0,
                            'myDmg' : 0,
                            'nmeDmg' : 0,
                            'myOutSta' : 0,
                            'nmeOutSta' : 0,
                            'textScroll' : ""
                            'curSelect' : 0,
                            'prevSelect' : 0,
                            'prvAtkSlct': 0
                            }
        self.options = ["Info", "Atk", "Swap"] #add tame
    
    
    def setBattle(player, nmePlayer)
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
                            'prevSelect' : 0,
                            'prvAtkSlct': 0
                            }
    

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
    
    
    def staChk(mon2Chk):
        if mon2Chk.attackList[self.battleBlock[curAtkSlct]].currentUses <= 0:
            player.friends[0].statBlock['currentHealth'] = math.floor(player.friends[0].statBlock['currentHealth'] * 0.7)
            # display that mon is out of sta for move and that they took damage 
        mon2Chk.attackList[mySelectedAttackNum].currentUses = mon2Chk.attackList[mySelectedAttackNum].currentUses -1                            
        if player.friends[0].attackList[mySelectedAttackNum].currentUses < 0:
            player.friends[0].attackList[mySelectedAttackNum].currentUses = 0
            

    
    def battleCrunch(firstMon, secMon, firstAtk, SecAtk): #(should be able to use self.battleBlock['curAtkSlct']) and not send firstAtk
        firstDodge = btl.dodge(secMon, firstMon, secMon.attackList[SecAtk]) #, player.playerBlock['trainerLevel'], nmePlayer.playerBlock['trainerLevel'])  ########### remember to look at this to see if i'm doing the right mon's attack
        secDodge = btl.dodge(firstMon, secMon, firstMon.attackList[firstAtk]) #, nmePlayer.playerBlock['trainerLevel'], player.playerBlock['trainerLevel'])
        firstDmg = btl.attack(firstMon, nmeGuy.friends[0], firstMon.attackList[firstAtk]) #, btl.battleBlock['myTL'], btl.battleBlock['nmeTL'])
        secDmg = btl.attack(secMon, firstMon, secMon.attackList[SecAtk]) #, nmePlayer.playerBlock['trainerLevel'], firstMon.playerBlock['trainerLevel'])

        if firstDodge > 0:
            secDmg = math.floor(secDmg / firstDodge)      
        if secDodge > 0: 
            firstDmg = math.floor(firstDmg / secDodge)
        staChk(firstMon)
        if player.friends[0].statBlock['currentHealth'] > 0:
            nmePlayer.friends[0].statBlock['currentHealth'] = nmePlayer.friends[0].statBlock['currentHealth'] - firstDmg 
            staChk(secMon)
            if nmePlayer.friends[0].statBlock['currentHealth'] > 0:
                firstMon.statBlock['currentHealth'] = firstMon.statBlock['currentHealth'] - secDmg
    
    def makeSlct(player, nmeFrens):
        if self.battleBlock['curSelect'] == 31: # 31 = selection made so go on to see what happens
            self.battleBlock['curSelect'] = self.battleBlock['prevSelect'] #reset curSelect to prevSelect so it's not 31 anymore
            if self.options[self.battleBlock['curSelect']] == "Atk": # and myAttackRdy == 0: <-ignore comment
                self.battleBlock['curAtkSlct'] = attackOptionMenu(player.friends[0].attackList, self.battleBlock['prvAtkSlct']) #get the attack's number from user
                if self.battleBlock['curAtkSlct'] < 30: # < 30 = an attack is selected, make prvAtkSlct = curAtkSlct
                    self.battleBlock['prvAtkSlct'] = self.battleBlock['curAtkSlct']
                 else:
                     self.battleBlock['curAtkSlct'] = 15 # 15 = no attack selected
                     
            elif self.options[self.battleBlock['curSelect']] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmeFrens[0])
                tempPlayer.friends.append(player.friends[0])
                showMonInfo(tempPlayer, 0, 1)
                del tempPlayer
            elif self.options[self.battleBlock['curSelect']] == "Swap":
                showMonInfo(player, 0, 2)
        if self.battleBlock['curSelect'] == 30 or self.battleBlock['curSelect'] == 28 or self.battleBlock['curSelect'] == 29 :
            self.battleBlock['curSelect'] = self.battleBlock['prevSelect']    
            
    def drawScreen(myAttackList):
        self.battleBlock['curSelect'] = showOptions(self.options, self.battleBlock['curSelect'], "", 47)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
    
    def npcAtkSel(npcAtkList):
        self.battleBlock['nmeAtkSlct'] = random.randint(0,len(npcAtkList)) - 1
            
main:
    btl = Battle()
    setBattle(myGuy, nmeGuy)
    loop
        btl.drawScreen()
        ~getInput   #set btl.battleBlock['curSelect'] & btl.battleBlock['prevSelect'] here
        btl.makeSlct(myGuy, nmeGuy.friends)
        if btl.battleBlock['curAtkSlct'] != 15:
            agileTie = random.randint(-2,1)
            if (myGuy.friends[0].statBlock['Agility'] + myGuy.playerBlock['trainerLevel'] + agileTie) >= (nmeGuy.friends[0].statBlock['Agility'] + nmeGuy.playerBlock['trainerLevel']):
                btl.npcAtkSel(nmeGuy.friends[0].attackList)
                battleCrunch(myGuy, nmeGuy, self.battleBlock[curAtkSlct], self.battleBlock['nmeAtkSlct'])
            else:
                battleCrunch(nmeGuy, myGuy, self.battleBlock['nmeAtkSlct'], self.battleBlock[curAtkSlct])
            self.battleBlock['prvAtkSlct'] = btl.battleBlock['curAtkSlct']
            self.battleBlock['curAtkSlct'] = 15
        
        tempSelect = self.battleBlock['curSelect']
