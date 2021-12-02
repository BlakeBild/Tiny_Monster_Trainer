import gc
gc.enable() 
import time
import thumby
import math
import random
import micropython

player3_sprite = [0,46,251,127,123,255,46,0]
blob_sprite = (56,124,124,54,62,116,124,56)
wall_sprite = (24,126,255,102,102,255,126,24)
floor_sprite = (0,0,0,0,0,0,0,0)
floor_crack = (0,0,0,0,40,20,0,0)
door_sprite = (255,255,3,1,17,19,255,255)
tree1_sprite = (14,31,151,255,255,155,31,14)
tree3_sprite = (255,157,14,8,2,14,159,247)
mountain1_sprite = (192,120,12,30,63,14,60,224)

head0_sprite = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
birbHead_sprite = (0,0,0,0,192,192,240,240,248,248,255,190,60,60,240,240,224,192,0,0,
            0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0)
birbBody_sprite = (0,0,0,255,255,255,255,253,120,24,253,255,255,31,255,255,249,243,0,0,
            0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0)
birbLegs_sprite = (0,24,62,55,51,49,180,246,179,59,185,252,190,63,31,15,7,1,0,0,
            0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0)


class Tile:
    def __init__(self):
        self.tileType = 0
        self.tileSpawn = 0
        self.isObjectHere = 0
                            
    def generateTile(self, preTileType):
        if preTileType == 0: 
            pass
        elif preTileType == 1: 
            self.isObjectHere = 0
        elif preTileType == 2: 
            self.tileType = 2 
            self.isObjectHere = 1
        elif preTileType == 3: 
            self.tileType = 3 
            self.isObjectHere = 2
        elif preTileType == 8: 
            self.tileType = 8 
            self.isObjectHere = 1
        elif preTileType == 9:
            self.tileType = 9 
            self.isObjectHere = 0
        else:
            self.tileType = 1 
            self.isObjectHere = 0


class Map:
    def __init__(self):
        self.elementType = 0
        self.floor = []
        self.roomNumber = 0 
        self.mapX = 9
        self.mapY = 5
 
        for i in range(self.mapX * self.mapY):
            floorTile = Tile()
            self.floor.append(floorTile)
            self.floor[i].tileType = 2 
            self.floor[i].isObjectHere = 1 
        for x in range(0, self.mapX): 
            self.floor[x].tileType = 1 
            self.floor[x].isObjectHere = 0
            self.floor[4*self.mapX+x].tileType = 1
            self.floor[4*self.mapX+x].isObjectHere = 0
        for y in range(0, self.mapY):
            self.floor[y*self.mapX].tileType = 1 
            self.floor[y*self.mapX].isObjectHere = 0
            self.floor[y*self.mapX+8].tileType = 1
            self.floor[y*self.mapX+8].isObjectHere = 0
        for x in range(0, self.mapX):
            if x == math.floor(self.mapX / 2):
                self.floor[x].tileType = 3 
                self.floor[x].isObjectHere = 2
                self.floor[4*self.mapX+x].tileType = 3
                self.floor[4*self.mapX+x].isObjectHere = 2
        for y in range(0, self.mapY):
            if y == math.floor(self.mapY / 2):
                self.floor[y*self.mapX].tileType = 3
                self.floor[y*self.mapX].isObjectHere = 2
                self.floor[y*self.mapX+8].tileType = 3
                self.floor[y*self.mapX+8].isObjectHere = 2

    def procGenMap(self):
        terrainChance = 20
        self.elementType = random.randint(1,12)
        for x in range (0,self.mapX):
            for y in range(0,self.mapY):
                floor = self.floor[y*self.mapX+x]
                if floor.tileType == 1:
                    pass
                if floor.tileType == 2:
                    somethingHere = random.randint(0,terrainChance)
                    if somethingHere == 1:
                        terrainTile = random.randrange(7,9)
                        self.floor[y*self.mapX+x].generateTile(terrainTile)

 
    def displayMap(self):
        for x in range(0, self.mapX):
            for y in range(0, self.mapY):
                floor = self.floor[y*self.mapX+x]
                if(floor.tileType == 1 and self.elementType < 3):
                    thumby.display.blit(tree3_sprite, x*8 ,y*8 , 8, 8)
                    if y*self.mapX+8 == 18 or y*self.mapX+8 == 35:
                        thumby.display.blit(tree1_sprite, x*8 ,y*8 , 8, 8)
                    if y*self.mapX == 9 or y*self.mapX == 27:
                        thumby.display.blit(tree1_sprite, x*8 ,y*8 , 8, 8)
                elif(floor.tileType == 1 and self.elementType < 9):
                    thumby.display.blit(mountain1_sprite, x*8 ,y*8 , 8, 8)
                elif(floor.tileType == 1):
                    thumby.display.blit(wall_sprite, x*8 ,y*8 , 8, 8)
                elif(floor.tileType == 2):
                    thumby.display.blit(floor_sprite, x*8 ,y*8 , 8, 8)
                elif(floor.tileType == 3):
                    thumby.display.blit(door_sprite, x*8 ,y*8 , 8, 8)
                elif(floor.tileType == 8):
                    thumby.display.blit(floor_crack, x*8 ,y*8 , 8, 8)
                else:
                    thumby.display.blit(floor_one, x*8 ,y*8 , 8, 8)


class AttackMove():
    def __init__(self, name="", numUses=0, baseDamage=0, magic = 0, moveElementType="", statusEffect=0):
        self.name = name 
        self.numUses = numUses 
        self.currentUses = numUses 
        self.baseDamage = baseDamage 
        self.magic = magic # 0 or 1
        self.moveElementType = moveElementType
        self.statusEffect = statusEffect 
        
        
    def getAnAttackMove(self, selectionNum, elmType=""):

        basicList = []
        if elmType == "Default":
            poke = AttackMove("Poke", 15, 0)
            basicList.append(poke)
            hit = AttackMove("Hit", 10, 1)
            basicList.append(hit)
            tackle =  AttackMove("Tackle", 7, 5)
            basicList.append(tackle)
            magicHit = AttackMove("MagicHit", 10, 1, 1)
            basicList.append(magicHit)
        elif elmType == "Wind":
            gust = AttackMove("Gust", 15, 5, 0, "Wind")
            basicList.append(gust)
            cyclone = AttackMove("Cyclone", 15, 5, 1, "Wind")
            basicList.append(cyclone)
            gust1 = AttackMove("Gust1", 15, 5, 0, "Wind")
            basicList.append(gust1)
            gust2 = AttackMove("Gust2", 15, 5, 0, "Wind")
            basicList.append(gust2)
        elif elmType == "Earth":
            rockToss = AttackMove("RockToss", 15, 5, 0, "Earth")
            basicList.append(rockToss)
            quake = AttackMove("Quake", 15, 5, 1, "Earth")
            basicList.append(quake)
            quake1 = AttackMove("Quake1", 15, 5, 1, "Earth")
            basicList.append(quake1)
            quake2 = AttackMove("Quake2", 15, 5, 1, "Earth")
            basicList.append(quake2)
        elif elmType == "Water":
            iceHit = AttackMove("IceHit", 15, 5, 0, "Water")
            basicList.append(iceHit)
            freeze = AttackMove("Freeze", 15, 5, 1, "Water", 2)
            basicList.append(freeze)
            bubble = AttackMove("Bubble", 15, 5, 1, "Water")
            basicList.append(bubble)
            wave = AttackMove("Wave", 15, 5, 0, "Water")
            basicList.append(wave)
        elif elmType == "Fire":
            fireHit = AttackMove("FireHit", 15, 5, 0, "Fire")
            basicList.append(fireHit)
            burn = AttackMove("Burn", 15, 5, 1, "Fire", 1) 
            basicList.append(burn)
            flame = AttackMove("Flame", 15, 5, 1, "Fire")
            basicList.append(flame)
            lava = AttackMove("Lava", 15, 5, 0, "Fire")
            basicList.append(lava)
        elif elmType == "Mind":
            headbutt = AttackMove("Headbutt", 15, 5, 0, "Mind")
            basicList.append(headbutt)
            psychic = AttackMove("Psychic", 15, 5, 1, "Mind")
            basicList.append(psychic)
            psychic1 = AttackMove("Psychic1", 15, 5, 1, "Mind")
            basicList.append(psychic1)
            psychic2 = AttackMove("Psychic2", 15, 5, 1, "Mind")
            basicList.append(psychic2)
        elif elmType == "Darkness":
            darkHit = AttackMove("DarkHit", 15, 5, 1, "Darkness")
            basicList.append(darkHit)
            shadow = AttackMove("Shadow", 15, 5, 1, "Darkness")
            basicList.append(shadow)
            shadow1 = AttackMove("Shadow1", 15, 5, 1, "Darkness")
            basicList.append(shadow1)
            shadow2 = AttackMove("Shadow2", 15, 5, 1, "Darkness")
            basicList.append(shadow2)
        elif elmType == "Cute":
            cuteHit = AttackMove("CuteHit", 15, 5, 0, "Cute")
            basicList.append(cuteHit)
            adorbes = AttackMove("Adorbes", 15, 5, 1, "Cute")
            basicList.append(adorbes)
            flufBall = AttackMove("FlufBall", 10, 10, 0, "Cute")
            basicList.append(flufBall)
            singSong = AttackMove("singSong", 5, 15, 1, "Cute")
            basicList.append(singSong)
        elif elmType == "Light":
            lightHit = AttackMove("LightHit", 15, 5, 0, "Light")
            basicList.append(lightHit)
            flash = AttackMove("Flash", 15, 5, 1, "Light")
            basicList.append(flash)
            razzle = AttackMove("Razzle", 10, 10, 0, "Light")
            basicList.append(razzle)
            dazzle = AttackMove("Dazzle", 10, 10, 1, "Light")
            basicList.append(dazzle)
        elif elmType == "Physical":
            bodySlam = AttackMove("BodySlam", 15, 5, 0, "Physical")
            basicList.append(bodySlam)
            lowKick = AttackMove("Low Kick", 10, 10, 0, "Physical")
            basicList.append(lowKick)
            judoThrow = AttackMove("JudoThrow", 5, 15, 0, "Physical")
            basicList.append(judoThrow)
            SuperHit = AttackMove("SuperHit", 15, 5, 1, "Physical")
            basicList.append(SuperHit)
        elif elmType == "Mystical":
            mystHit = AttackMove("MystHit", 15, 5, 0, "Mystical")
            basicList.append(mystHit)
            magicMys = AttackMove("MagicMys", 15, 5, 1, "Mystical")
            basicList.append(magicMys)
            brainMelt = AttackMove("Ritual", 5, 10, 1, "Mystical")
            basicList.append(brainMelt)
            runeToss = AttackMove("RuneToss", 5, 15, 1, "Mystical")
            basicList.append(magicMys)
        elif elmType == "Ethereal":
            ghostHit = AttackMove("SpookyHit", 15, 5, 0, "Ethereal")
            basicList.append(ghostHit)
            ethMagic = AttackMove("EthMagic", 15, 5, 1, "Ethereal")
            basicList.append(ethMagic)
            ghostHand = AttackMove("GhostHand", 5, 10, 1, "Ethereal")
            basicList.append(ghostHand)
            rueDay = AttackMove("Rue Day", 5, 15, 1, "Ethereal")
            basicList.append(rueDay)
        else:
            selectionNum = 0
            elsePoke = AttackMove("ElsePoke", 15, -1)
            basicList.append(elsePoke)
            
        self.name = basicList[selectionNum].name
        self.numUses = basicList[selectionNum].numUses
        self.currentUses = basicList[selectionNum].currentUses
        self.baseDamage = basicList[selectionNum].baseDamage
        self.magic = basicList[selectionNum].magic
        self.moveElementType = basicList[selectionNum].moveElementType
        self.statusEffect = basicList[selectionNum].statusEffect


class TextForScroller():
    def __init__(self, scrollingText):
        self.scrollingText = scrollingText
        self.scrollerLength = 0


    def getScrollerLength(self):
        textLength = len(self.scrollingText)
        self.scrollerLength = textLength * 8 + 82 
 

class Item():
    def __init__(self, name, key, bonus = 0):
        self.name = name
        self.key = key
        self. bonus = bonus
        
    def doAction(self, monsterInfo):
        '''keys =   1: healing items
                    2: maxHP increase items '''
        if self.key == 1:
            monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['currentHealth'] + 10 + self.bonus
            if monsterInfo.statBlock['currentHealth'] > monsterInfo.statBlock['Health']:
               monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['Health']            
        elif self.key == 2:
            monsterInfo.statBlock['maxHealth'] = monsterInfo.statBlock['maxHealth'] + 1 + self.bonus
            if  monsterInfo.statBlock['currentHealth'] < monsterInfo.statBlock['Health']:
                monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['currentHealth'] + 1 + self.bonus
                if monsterInfo.statBlock['currentHealth'] > monsterInfo.statBlock['Health']:
                     monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['Health']
        else:
            pass
           
            
    def getItem(self):
        randoNum = random.randint(1,4)
        if randoNum == 1:
            self.name = "Bandaid"
            self.key = 1
            self.bonus = -2
        elif randoNum == 2:
            self.name = "PushPop"
            self.key = 1
            self.bonus = 10
        elif randoNum == 3:
            self.name = "Stickers"
            self.key = 2
        elif randoNum == 4:
            self.name = "Ribbons"
            self.key = 2
            self.bonus = 1
        else:
            pass


class Player:
    def __init__(self):                                           
        self.name = "CoolDude"
        self.trainerLevel = 1
        self.experience = 0
        self.friends = []
        self.friendMax = 2
        self.inventory = []
        self.maxHelditems = 10
        self.mapX = 9
        self.mapY = 5
        self.currentPos = math.ceil((self.mapX * self.mapY) / 2)
        self.position = []
        for i in range(self.mapX * self.mapY):
            self.position.append(0)
        self.position[self.currentPos] = 1
 
 
    def drawPlayer(self):
        for x in range(0, self.mapX):
            for y in range(0, self.mapY):
                if self.position[y*self.mapX+x] == 1 :
                    thumby.display.blit(player3_sprite, x*8 ,y*8 , 8, 8)
 
 
    def movePlayer(self, currentRoom, monster):
        while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
            pass 
        if(thumby.buttonU.pressed() == True):
            while(thumby.buttonU.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 9
                self.position[self.currentPos] = 1
                monster.moveMonster(self, world[room])
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room])
        if(thumby.buttonD.pressed() == True):
            while(thumby.buttonD.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos+9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 9
                self.position[self.currentPos] = 1
                self.drawPlayer()
                monster.moveMonster(self, world[room])
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room])
        if(thumby.buttonL.pressed() == True):
            while(thumby.buttonL.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 1
                self.position[self.currentPos] = 1
                self.drawPlayer()
                monster.moveMonster(self, world[room])
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room])
        if(thumby.buttonR.pressed() == True):
            while(thumby.buttonR.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos+1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 1
                self.position[self.currentPos] = 1
                self.drawPlayer()
                monster.moveMonster(self, world[room])
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room])


    def levelUpCheck(self):
        self.experience = self.experience + 1
        if self.experience ==  math.floor(self.trainerLevel * 1.5):
            self.trainerLevel = self.trainerLevel + 1
            thumby.display.fill(0)
            thumby.display.drawText("Your", 0, 0, 1) 
            thumby.display.drawText("Trainer", 0, 9, 1) 
            thumby.display.drawText("Level is", 0, 20, 1)
            thumby.display.drawText("now", 0, 29, 1)
            thumby.display.drawText(str(self.trainerLevel), 40, 29, 1)
            thumby.display.update()
            time.sleep(5)
    
 
class Monster:
    def __init__(self):
        self.statBlock = {'name' : "", 
                        'given_name' : "",
                        'level' : 1,
                        'trainingPoints' : 5,
                        'Type1' : "",
                        'Type2' : "",
                        'Type3' : "",
                        'Health' : 1,
                        'currentHealth' : 1,
                        'maxHealth' : 1,
                        'Strength' : 1,
                        'maxStrength' : 1,
                        'Agility' : 1,
                        'maxAgility' : 1,
                        'Endurance' : 1,
                        'maxEndurance' : 1,
                        'Mysticism' : 1,
                        'maxMysticism' : 1,
                        'Tinfoil' : 1,
                        'maxTinfoil' : 1}
                        
        self.keyList = ['Health',       # 0
                        'Type1',        # 1
                        'Type2',        # 2
                        'Type3',        # 3
                        'Strength',     # 4
                        'Agility',      # 5
                        'Endurance',    # 6
                        'Mysticism',    # 7
                        'Tinfoil']      # 8
            
        
        self.bodyBlock = {'head' : head0_sprite,
                            'body' : head0_sprite,
                            'legs' : head0_sprite}
        
        self.attackList = []
        self.statusEffectList = []
        self.mutateSeed = []
                
    
    def makeName(self):
        gc.collect()
        name = ""
        prevLetter1 = 0
        prevLetter2 = 0
        name_length = random.randrange(3, 8)
        firstLetter = 1
        capAlphabet = [' ', 'A', 'E', 'I', 'O','U','Y','B','C','D','F','G','H',
                        'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
                        'W', 'X', 'Z']
        alphabet = [' ', 'a', 'e', 'i', 'o', 'u', 'y', 'b', 'c', 'd', 'f', 'g',
                    'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q','r', 's', 't', 'v',
                    'w', 'x', 'z']
                    
        for i in range(1, name_length): 
            
            if firstLetter < 1: 
                if prevLetter1 >= 6 and prevLetter2 >= 6: 
                    getLetter = random.randint(1, 5)
                    if getLetter == prevLetter1 and getLetter == prevLetter2:
                        getLetter = random.randint(1, 26) 
                        if getLetter == prevLetter1:
                            while getLetter != prevLetter1:
                                getLetter = random.randint(1, 26)
                    prevLetter2 = prevLetter1
                    prevLetter1 = getLetter
                    letter = alphabet[getLetter]
                else: # just gets a random leter
                    getLetter = random.randint(1, 26)
                    prevLetter2 = prevLetter1
                    prevLetter1 = getLetter
                    letter = alphabet[getLetter]
            else:  
                getLetter = random.randint(1, 26)
                prevLetter2 = prevLetter1
                prevLetter1 = getLetter
                letter = capAlphabet[getLetter]
                firstLetter = 0
            
            name = name + letter
            if letter == "q" or letter == "Q":
                name = name + "u"
            
        shortNameCheck = len(name)
        if shortNameCheck == 2: 
            if prevLetter1 >= 6 and prevLetter2 >=6:
                getLetter = random.randint(1, 5)
                name = capAlphabet[prevLetter2] + alphabet[getLetter] + alphabet[prevLetter1]
        return name

    
    @staticmethod
    def makeStat(baseStat, maxStat=0):
        if baseStat < 3:  
            baseStat = random.randint(3, 10)
            return baseStat
        elif maxStat == 1: 
            maxStat = random.randint(7, 21)
            if maxStat < baseStat:  
                maxStat = baseStat
            return maxStat
        return baseStat
    
    
    def makeMonBody(self):
        gc.collect()
        
        head1_sprite = (0,0,0,0,48,48,200,236,76,112,112,76,236,200,48,48,0,0,0,0,
           0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0)
        head2_sprite = (16,124,68,76,84,124,48,22,190,224,224,190,22,48,124,68,76,84,124,16,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0)
        head3_sprite = (0,0,0,0,62,66,129,1,193,33,65,33,197,5,137,66,62,0,0,0,
            0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,0,0)
        head4_sprite = (16,56,68,206,84,56,124,134,35,3,11,51,134,124,56,68,206,84,56,16,
            0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0)
        head5_sprite = (0,7,30,62,62,124,254,131,17,69,69,17,131,254,124,62,62,30,7,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0)            
        head6_sprite = (0,0,0,0,0,248,12,6,35,3,131,7,47,30,252,120,0,0,0,0,
            0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0)            
        head7_sprite = (0,0,0,120,224,124,196,28,120,32,170,32,120,28,196,124,224,120,0,0,
            0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0)            
        head8_sprite = (0,0,0,0,0,0,206,159,57,153,63,147,51,159,206,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0)
        head9_sprite = (0,0,0,2,196,200,192,36,232,32,252,32,232,36,192,200,196,2,0,0,
            0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0)
        head10_sprite = (0,0,0,0,32,112,32,4,98,68,64,68,98,4,32,112,32,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        body1_sprite = (0,62,255,219,118,60,31,255,255,193,193,207,135,183,255,252,0,0,0,0,
           0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0)
        body2_sprite = (0,56,252,204,30,62,115,231,253,248,16,248,253,231,115,62,30,204,252,56,
           0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0)
        body3_sprite = (0,56,16,60,100,198,19,17,74,130,130,74,9,19,198,100,60,16,56,0,
            0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0)
        body4_sprite =  (6,4,28,52,38,80,254,131,41,125,117,41,131,254,80,32,32,248,136,80,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0)
        body5_sprite = (0,2,8,4,16,0,57,65,1,170,170,170,1,65,57,0,16,4,8,2,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        body6_sprite = (146,124,16,56,124,198,1,56,68,17,17,68,56,1,198,124,56,16,124,146,
            0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0)
        body7_sprite = (0,192,192,224,32,46,167,131,249,172,238,172,249,131,167,46,32,60,12,12,
            0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0)
        body8_sprite = (0,31,19,19,24,28,24,16,145,255,255,255,145,16,24,28,24,19,19,31,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0)
        body9_sprite = (0,0,0,0,0,0,135,135,1,131,215,131,1,135,135,0,0,0,0,0,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0)
        body10_sprite = (0,0,32,124,126,38,14,27,183,227,9,227,183,27,14,38,126,124,32,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0)
        body11_sprite = (0,16,127,48,32,32,230,226,255,127,0,0,255,226,206,128,192,112,0,0,
            0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0)
        body12_sprite = (0,28,62,127,248,240,224,71,76,254,232,254,76,71,224,240,248,127,62,28,
            0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0)
        legs1_sprite = (0,0,0,24,30,7,1,159,255,227,1,227,255,159,0,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0)
        legs2_sprite = (0,0,0,48,124,30,7,243,125,7,241,3,31,121,3,199,126,60,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        legs3_sprite = (0,0,112,24,60,78,247,123,137,14,14,14,137,123,231,78,60,16,112,0,
            0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0)
        legs4_sprite = (0,8,24,56,40,44,39,161,225,172,36,38,163,225,179,30,12,0,0,0,
            0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0)
        legs5_sprite = (14,31,31,191,231,49,249,154,15,15,15,15,154,249,49,231,191,31,31,14,
            0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0)
        legs6_sprite = (0,0,0,0,0,0,1,2,5,7,7,7,5,2,1,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)          
        legs7_sprite = (0,0,68,156,176,184,159,207,255,115,1,3,231,255,158,52,180,146,72,0,
            0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0)
        legs7_sprite = (0,0,0,0,16,86,148,165,169,171,255,171,169,165,148,86,16,0,0,0,
            0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0)
        legs8_sprite = (240,156,198,96,120,140,6,1,121,253,253,253,121,1,6,140,120,96,192,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0)
        legs9_sprite = (0,0,0,0,120,140,6,1,57,125,125,125,57,1,6,140,120,0,0,0,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0)
        legs10_sprite = (124,194,128,56,76,224,193,131,14,172,248,94,6,131,193,228,184,0,198,124,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0)
        
        if random.randint(0,50) != 1:
            randoNum = random.randint(0,11)
            heads = {
            0: head0_sprite,
            1: head1_sprite,
            2: head2_sprite,
            3: head3_sprite,
            4: head4_sprite,
            5: head5_sprite,
            6: head6_sprite,
            7: head7_sprite,
            8: head8_sprite,
            9: head9_sprite,
            10: head10_sprite,
            11: body12_sprite}
            self.bodyBlock['head'] = heads[randoNum]
        
            randoNum = random.randint(1,12)
            bodyyodyody = {
            1: body1_sprite,
            2: body2_sprite,
            3: body3_sprite,
            4: body4_sprite,
            5: body5_sprite,
            6: body6_sprite,
            7: body7_sprite,
            8: body8_sprite,
            9: body9_sprite,
            10: body10_sprite,
            11: body11_sprite,
            12: body12_sprite}
            self.bodyBlock['body'] = bodyyodyody[randoNum]
        
            randoNum = random.randint(1,10)
            legDay = {
            1: legs1_sprite,
            2: legs2_sprite,
            3: legs3_sprite,
            4: legs4_sprite,
            5: legs5_sprite,
            6: legs6_sprite,
            7: legs7_sprite,
            8: legs8_sprite,
            9: legs9_sprite,
            10: legs10_sprite}
            self.bodyBlock['legs'] = legDay[randoNum]

        else:
            randoNum = random.randint(1,1)
            specialHeads = {
                1: birbHead_sprite}
            specialBodies = {
                1: birbBody_sprite}
            specialLegs = {
                1: birbLegs_sprite}
            self.bodyBlock['head'] = specialHeads[randoNum]
            self.bodyBlock['body'] = specialBodies[randoNum]
            self.bodyBlock['legs'] = specialLegs[randoNum]
    
    
    def makeType(self):
        monsterTypes = ['', "Wind", "Earth", "Water", "Fire", "Mind", "Darkness", 
                        "Cute", "Light", "Physical", "Mystical", "Ethereal"]
        if self.statBlock['Type1'] == "":
            monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            return monType
        elif self.statBlock['Type2'] == "":
            monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1']:
                monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            return monType
        elif self.statBlock['Type3'] == "":
            monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1'] or monType == self.statBlock['Type2']:
                monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            return monType
        return monType


    def mutateMon(self):
        if self.statBlock['trainingPoints'] > 4:
            if self.mutateSeed[1] < 4:
                random.seed(self.mutateSeed[0] + (self.mutateSeed[1] * 100))
                mutation = random.randint(1, 5)
                if mutation > 2 :
                    mutation = random.randint(4, 8) 
                    if mutation == 0 or mutation > 3 :
                        self.statBlock['max' + self.keyList[mutation]] = self.statBlock['max' + self.keyList[mutation]] + 10
                else:
                    if self.bodyBlock['head'] != birbHead_sprite:
                        self.makeMonBody()
                    if self.statBlock['Type2'] == "":
                        self.statBlock['Type2'] = self.makeType()
                        myAttack = AttackMove()
                        randoNum = random.randint(0,3)
                        myAttack.getAnAttackMove(randoNum, self.statBlock['Type2'])
                        self.attackList.append(myAttack)
                        makeSureNoDuplicateAttacks(self, self.attackList)
                    elif self.statBlock['Type3'] == "":
                        self.statBlock['Type3'] = self.makeType()
                        myAttack = AttackMove()
                        randoNum = random.randint(0,3)
                        myAttack.getAnAttackMove(randoNum, self.statBlock['Type3'])
                        makeSureNoDuplicateAttacks(self, self.attackList)
                    self.statBlock['maxHealth'] = self.statBlock['maxHealth'] + 20
                self.mutateSeed[1] = self.mutateSeed[1] + 1
                self.statBlock['trainingPoints'] = self.statBlock['trainingPoints'] - 5 
            else:
                pass
        else:
            pass
                    

    def makeMonster(self):
        gc.collect()
        genStat = self.makeStat
        self.statBlock['name'] = self.makeName()
        self.statBlock['given_name'] = self.statBlock['name']
        self.statBlock['level'] = 1
        self.statBlock['trainingPoints'] = 5
        self.statBlock['Type1'] = self.makeType()
        randoNum = random.randint(1,3)
        if randoNum == 1:
            self.statBlock['Type2'] = self.makeType()
            randoNum = random.randint(1,100)
            if randoNum == 1:
                self.statBlock['Type3'] = self.makeType()
        self.statBlock['Health'] = genStat(0)
        self.statBlock['currentHealth'] = self.statBlock['Health']
        self.statBlock['maxHealth'] = genStat(self.statBlock['Health'], 1)
        self.statBlock['Strength'] = genStat(0)
        self.statBlock['maxStrength'] = genStat(self.statBlock['Strength'], 1)
        self.statBlock['Agility'] = genStat(0)
        self.statBlock['maxAgility'] = genStat(self.statBlock['Agility'], 1)
        self.statBlock['Endurance'] = genStat(0)
        self.statBlock['maxEndurance'] = genStat(self.statBlock['Endurance'], 1)
        self.statBlock['Mysticism'] = genStat(0)
        self.statBlock['maxMysticism'] = genStat(self.statBlock['Mysticism'], 1)
        self.statBlock['Tinfoil'] = genStat(0)
        self.statBlock['maxTinfoil'] = genStat(self.statBlock['Tinfoil'], 1)
        self.mutateSeed.append(random.randint(0,50))
        self.mutateSeed.append(0)
        #print(self)
    
    
class StatusEffect():
    def __init__(self):
        self.effectInfo = { 'name' : "",
                            'turnsLeft' : 0,
                            'thingToDo' : 0,
                            'needToHit' : 0,
                            'onMon' :  0,
                            'statusDamage' : 0,
                            'statusBonus' : 0,
                            'elementType' : ""}


def makeStatusEffect(effectBeingMade):
    newStatus = StatusEffect()
    newStatus.effectInfo = newStatus.effectInfo.copy()
    if effectBeingMade == 1:
        newStatus.effectInfo['name'] = "Burn"
        newStatus.effectInfo['turnsLeft'] = 5
        newStatus.effectInfo['thingToDo'] = 1
        newStatus.effectInfo['needToHit'] = 0
        newStatus.effectInfo['onMon'] = 0
        newStatus.effectInfo['statusDamage'] = 2
        newStatus.effectInfo['statusBonus'] = 0
        newStatus.effectInfo['elementType'] = "Fire"
    elif effectBeingMade == 2:
        newStatus.effectInfo['name'] = "Freeze"
        newStatus.effectInfo['turnsLeft'] = 2
        newStatus.effectInfo['thingToDo'] = 2
        newStatus.effectInfo['needToHit'] = 0
        newStatus.effectInfo['onMon'] = 0
        newStatus.effectInfo['statusDamage'] = 0
        newStatus.effectInfo['statusBonus'] = 3
        newStatus.effectInfo['elementType'] = "Water"
    return newStatus


class RoamingMonster:
    def __init__ (self, currentPos=0, mapX=9, mapY=5, position=[]):
    
        self.mapX = mapX
        self.mapY = mapY
        self.currentPos = currentPos
        self.position = position
        for i in range(self.mapX * self.mapY):
            self.position.append(0)
    
    
    def drawMonster(self):
        for x in range(0, self.mapX):
            for y in range(0, self.mapY):
                if self.position[y*self.mapX+x] == 1 :
                    thumby.display.blit(blob_sprite, x*8 ,y*8 , 8, 8)
    
    
    def placeMonster(self, map): # appox code
        findEmptySpot = 0
        while(findEmptySpot != 1):
            findEmptySpot = random.randint(9, 34)
            if map.floor[findEmptySpot].isObjectHere == 1:
                self.currentPos = findEmptySpot
                self.position[self.currentPos] = 1
                findEmptySpot = 1
    
    
    def removeMonster(self): # appox code
        self.position[self.currentPos] = 0
        self.currentPos = 0
    
    
    def moveMonster(self, player, currentRoom):
        if math.ceil(self.currentPos/9) > math.ceil(player.currentPos/9): 
            if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:  
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 9
                self.position[self.currentPos] = 1
                self.drawMonster()
            else:
                self.drawMonster()
        elif math.ceil(self.currentPos/9) < math.ceil(player.currentPos/9): 
            if currentRoom.floor[self.currentPos+9].isObjectHere >= 1: 
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 9
                self.position[self.currentPos] = 1
                self.drawMonster()
            else:
                self.drawMonster() 
        elif self.currentPos == player.currentPos:
            self.drawMonster()
        elif self.currentPos >= player.currentPos:
            if currentRoom.floor[self.currentPos-1].isObjectHere >= 1: 
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 1
                self.position[self.currentPos] = 1
                self.drawMonster()
            else:
                self.drawMonster()
        elif self.currentPos <= player.currentPos:
            if currentRoom.floor[self.currentPos+1].isObjectHere >= 1: # check for blocked
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 1
                self.position[self.currentPos] = 1
                self.drawMonster()
            else:
                self.drawMonster()
        else:
            self.drawMonster()
 
 
def worldRangeCheck(test):
    if test >= 19:
        test = test - 25
    if test <= -19:
        test = test + 25
    return test


def mapChangeCheck(player, worldMap, worldRoom):
    gc.collect()
    if worldMap.floor[player.currentPos].isObjectHere == 2:
        if player.currentPos == 4:
            player.position[player.currentPos] = 0
            player.currentPos = 31
            player.position[player.currentPos] = 1
            player.drawPlayer()
            worldRoom = worldRoom - 5
            worldMap.displayMap()
            worldRoom = worldRangeCheck(worldRoom)
            return worldRoom
        elif player.currentPos == 40:
            player.position[player.currentPos] = 0
            player.currentPos = 13
            player.position[player.currentPos] = 1
            player.drawPlayer()
            worldRoom = worldRoom + 5
            worldRoom = worldRangeCheck(worldRoom)
            worldMap.displayMap()
            return worldRoom
        elif player.currentPos == 26:
            player.position[player.currentPos] = 0
            player.currentPos = 19
            player.position[player.currentPos] = 1
            player.drawPlayer()
            worldRoom = worldRoom + 1
            worldRoom = worldRangeCheck(worldRoom)
            worldMap.displayMap()
            return worldRoom
        elif player.currentPos == 18:
            player.position[player.currentPos] = 0
            player.currentPos = 25
            player.position[player.currentPos] = 1
            player.drawPlayer()
            worldRoom = worldRangeCheck(worldRoom)
            worldRoom = worldRoom - 1
            worldMap.displayMap()
            return worldRoom
    worldMap.displayMap()
    return worldRoom


def battleStartAnimation(color):
    for x in range(0,71):
        for y in range (0, 41):
            thumby.display.drawLine(x, 0, 0, y, color)
            thumby.display.drawLine(72, 40-y, 70-x, 40, color)
        thumby.display.update()
    thumby.display.fill(0)
    thumby.display.update()


def buttonInput(selectPos):                
    selectionBoxPos = selectPos
    
    while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
        pass # Wait for the user to give us something
    if(thumby.buttonU.pressed() == True):
        while(thumby.buttonU.pressed() == True): 
            pass
        selectionBoxPos = selectionBoxPos - 1
        return selectionBoxPos
    if(thumby.buttonD.pressed() == True):
        while(thumby.buttonD.pressed() == True): 
            pass
        if (selectionBoxPos <= 11):
            selectionBoxPos = selectionBoxPos + 1
            return selectionBoxPos
        else:
            return selectionBoxPos
    if(thumby.buttonL.pressed() == True):
        while(thumby.buttonL.pressed() == True): 
            pass
        selectionBoxPos = 13
        return selectionBoxPos
    if(thumby.buttonR.pressed() == True):
        while(thumby.buttonR.pressed() == True): 
            pass
        selectionBoxPos = 12
        return selectionBoxPos
    if(thumby.buttonA.pressed() == True):
        while(thumby.buttonA.pressed() == True):
            pass
        selectionBoxPos = 15
        return selectionBoxPos
    if(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
        selectionBoxPos = 14
        return selectionBoxPos
    return selectionBoxPos    
    

def dropSEturnsLeft(currentEffect):
    currentEffect.effectInfo['turnsLeft'] = currentEffect.effectInfo['turnsLeft'] - 1


def doStatusEffect(currentMon, currentEffect):
    if currentEffect.effectInfo['thingToDo'] == 1:
        damageDone = currentMon.statBlock['currentHealth']
        currentMon.statBlock['currentHealth'] = currentMon.statBlock['currentHealth'] - currentEffect.effectInfo['statusDamage']
        damageDone = damageDone - currentMon.statBlock['currentHealth']
        if currentMon.statBlock['currentHealth'] < 0:
            currentMon.statBlock['currentHealth'] = 0
        dropSEturnsLeft(currentEffect)
        return 0
    elif currentEffect.effectInfo['thingToDo'] == 2:
        dropSEturnsLeft(currentEffect)
        return 3 
    else:
        return 0
    

def processStatusEffects(monsterInfo):
    statusCheck = 0
    listRangeCheck = 0
    for effects in range(0, len(monsterInfo.statusEffectList)):
        if len(monsterInfo.statusEffectList) > 0:
            if effects <= (effects - listRangeCheck):
                statusCheck = doStatusEffect(monsterInfo, monsterInfo.statusEffectList[effects]) + statusCheck
                if monsterInfo.statusEffectList[effects].effectInfo['turnsLeft'] <= 0:
                    monsterInfo.statusEffectList.pop(effects)
                    listRangeCheck = listRangeCheck + 1
                
    return statusCheck


def attackAnimation(playerBod, nmeBod, nmeAttk, missFlag, hpBefore, amountOfDmg, attackerHP):
    for x in range(0, 4):
        playerX = 8
        nmeX = 42
        y = 0
        nmeY = 0
        if x == 2:
            y = 10
            if nmeAttk == 1:
                y = 0
                nmeY = 10
        thumby.display.fill(0)
        thumby.display.blit(playerBod['head'], playerX + y, 0, 20, 9)
        thumby.display.blit(playerBod['body'], playerX + y, 9, 20, 9)
        thumby.display.blit(playerBod['legs'], playerX + y, 18, 20, 9)
        thumby.display.drawSprite(nmeBod['head'], nmeX - nmeY, 0, 20, 9, 1, 0, 0)
        thumby.display.drawSprite(nmeBod['body'], nmeX - nmeY, 9, 20, 9, 1, 0, 0)
        thumby.display.drawSprite(nmeBod['legs'], nmeX - nmeY, 18, 20, 9, 1, 0, 0)
        thumby.display.fillRect(0, 29, 72, 9, 1)
        if nmeAttk == 0:
            thumby.display.drawText(str(attackerHP), 0, 30, 0)
            thumby.display.drawText(str(hpBefore), 72 - len(str(attackerHP) * 8), 30, 0)
        else:
            thumby.display.drawText(str(attackerHP), 72 - len(str(attackerHP) * 8), 30, 0)
            thumby.display.drawText(str(hpBefore), 0, 30, 0)
        thumby.display.update()
        if missFlag == 1 and x > 1 and nmeAttk == 0:
            thumby.display.drawText("Miss", 20, 30, 0)
        if missFlag == 0 and x > 1 and nmeAttk == 0:
            thumby.display.fillRect(0, 29, 72, 9, 1)
            thumby.display.drawText("Hit!", 20, 30, 0)
            thumby.display.drawText(str(attackerHP), 0, 30, 0)
            thumby.display.drawText(str(hpBefore - amountOfDmg), 72 - len(str(hpBefore - amountOfDmg) * 8), 30, 0)
        if missFlag == 1 and x > 1 and nmeAttk == 1:
            thumby.display.drawText("Miss", 20, 30, 0)
        if missFlag == 0 and x > 1 and nmeAttk == 1:
            thumby.display.fillRect(0, 29, 72, 9, 1)
            thumby.display.drawText("Hit!", 20, 30, 0)
            thumby.display.drawText(str(attackerHP), 0, 72 - len(str(hpBefore - amountOfDmg) * 8), 0)
            thumby.display.drawText(str(hpBefore - amountOfDmg), 0, 30, 0)
            
        thumby.display.update()
        time.sleep(1)
        y = 0
        nmeY = 0



def attack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    dodge = defenceMon.statBlock['Agility'] + defTrainLevel
    if activeAttack.magic == 1:
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel
        defence = defenceMon.statBlock['Tinfoil'] + defTrainLevel
    else:
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel
        defence = defenceMon.statBlock['Endurance'] + defTrainLevel
    hp2 = defenceMon.statBlock['currentHealth']
    damage = 0
    attackMod = activeAttack.baseDamage + random.randint(0,5)
    defenceMod = random.randint(0,7)
    if attackAmnt + attackMod > dodge + defenceMod:
        damage = attackAmnt - defence
        if damage <= 0:
            damage = 1
    hp2 = hp2 - damage
    if hp2 < 0:
        hp2 = 0
    defenceMon.statBlock['currentHealth'] = hp2
    

def attackOptionMenu(playerMon, npcMon, scrollerTxt, playerTrainLevel, npcTrainLevel, isPlayer=0):  
    currentSelect = 1
    tempSelect = currentSelect
    npcStatusEffCheck = 0
    playerStatusEffCheck = 0
    playerOptionList = []
    
    for attacksKnown in range(0, len(playerMon.attackList) - 1):
        playerOptionList.append(playerMon.attackList[attacksKnown].name)
        
    while(currentSelect != 15):
        thumby.display.fill(0)
        tempSelect = currentSelect
        currentSelect = showOptions(playerOptionList, currentSelect, "Vigor: " + str(playerMon.attackList[currentSelect].currentUses))
        thumby.display.update()
        if currentSelect == 15:
            playerStatusEffCheck = processStatusEffects(playerMon)
            npcStatusEffCheck = processStatusEffects(npcMon)
            if playerMon.statBlock['currentHealth'] < 1:
                return 0 
            if npcMon.statBlock ['currentHealth'] < 1:
                return 3
            agileTie = 0
            if (playerMon.statBlock['Agility'] + playerTrainLevel) == (npcMon.statBlock['Agility'] + npcTrainLevel):
                agileTie = random.randint(-2,1)
            if (playerMon.statBlock['Agility'] + playerTrainLevel + agileTie) >= (npcMon.statBlock['Agility'] + npcTrainLevel): # check for player to attack first
                if playerStatusEffCheck < 3: #check if too many effects to attack
                    if playerMon.attackList[tempSelect].statusEffect > 0:
                        npcMon.statusEffectList.append(makeStatusEffect(playerMon.attackList[tempSelect].statusEffect))
                    hpBeforeDmg = npcMon.statBlock['currentHealth']
                    attack(playerMon, npcMon, playerMon.attackList[tempSelect], playerTrainLevel, npcTrainLevel)
                    amntOfDmg = hpBeforeDmg - npcMon.statBlock['currentHealth'] 
                    if amntOfDmg >= 1:
                        attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 0, 0, hpBeforeDmg, amntOfDmg, playerMon.statBlock['currentHealth'])
                        scrollerTxt.scrollingText = (playerMon.statBlock['given_name'] + " did " + str(amntOfDmg) + " points of damage!")
                    else:
                        attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 0, 1, hpBeforeDmg, amntOfDmg, playerMon.statBlock['currentHealth'])
                        scrollerTxt.scrollingText = (playerMon.statBlock['given_name'] + "'s " + playerMon.attackList[tempSelect].name + " attack missed!" )
                    scrollerTxt.getScrollerLength()                        
                if npcMon.statBlock['currentHealth'] >= 1:
                    if npcStatusEffCheck < 3: #check if too many effects to attack
                        hpBeforeDmg = playerMon.statBlock['currentHealth']
                        attack(npcMon, playerMon, npcMon.attackList[random.randint(0, len(npcMon.attackList) -1)], npcTrainLevel, playerTrainLevel)
                        amntOfDmg = hpBeforeDmg - playerMon.statBlock['currentHealth']
                        if amntOfDmg >= 1:
                            attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 1, 0, hpBeforeDmg, amntOfDmg, npcMon.statBlock['currentHealth'])
                        else:
                            attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 1, 1, hpBeforeDmg, amntOfDmg, npcMon.statBlock['currentHealth'])
                if npcMon.statBlock['currentHealth'] <= 0:
                    return 3
            else: 
                if npcStatusEffCheck < 3: #check if too many effects to attack
                    hpBeforeDmg = playerMon.statBlock['currentHealth']
                    attack(npcMon, playerMon, npcMon.attackList[random.randint(0, len(npcMon.attackList) -1)], npcTrainLevel, playerTrainLevel)
                    amntOfDmg = hpBeforeDmg - playerMon.statBlock['currentHealth']
                    if amntOfDmg >= 1:
                        attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 1, 0, hpBeforeDmg, amntOfDmg, npcMon.statBlock['currentHealth'])
                    else:
                        attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 1, 1, hpBeforeDmg, amntOfDmg, npcMon.statBlock['currentHealth'])
                if playerMon.statBlock['currentHealth'] >= 1:
                    if playerStatusEffCheck < 3: #check if too many effects to attack
                        if playerMon.attackList[tempSelect].statusEffect > 0:
                            npcMon.statusEffectList.append(makeStatusEffect(playerMon.attackList[tempSelect].statusEffect))
                        hpBeforeDmg = npcMon.statBlock['currentHealth']
                        attack(playerMon, npcMon, playerMon.attackList[tempSelect], playerTrainLevel, npcTrainLevel)
                        amntOfDmg = hpBeforeDmg - npcMon.statBlock['currentHealth']
                        if amntOfDmg >= 1:
                            attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 0, 0, hpBeforeDmg, amntOfDmg, playerMon.statBlock['currentHealth'])
                            scrollerTxt.scrollingText = ("You did " + str(amntOfDmg) + " points of damage!")
                        else:
                            attackAnimation(playerMon.bodyBlock, npcMon.bodyBlock, 0, 1, hpBeforeDmg, amntOfDmg, playerMon.statBlock['currentHealth'])
                            scrollerTxt.scrollingText = (playerMon.statBlock['given_name'] + "'s " + playerMon.attackList[tempSelect].name + " attack missed!" )
                        scrollerTxt.getScrollerLength()
                if npcMon.statBlock['currentHealth'] <= 0:
                    return 3
            waitingForSelect = 0
        if currentSelect == 14:
            return 1
        elif currentSelect == 12 or currentSelect == 13:
            currentSelect = tempSelect
    return 0
    
    
def battleScreen(playerMon, nmeMon, playerTrainLevel, npcTrainLevel):
    print(" Hi, you are in a fight! ")
    scroller = 0
    myScroller = TextForScroller(playerMon.statBlock['given_name'] + " has entered into battle with a roaming " + nmeMon.statBlock['name'] + "!")
    myScroller.getScrollerLength()
    currentSelect = 1
    tempSelect = currentSelect
    options = ["Itm", "Atk", "Run", "Cap", "Chg"] 
    
    while((playerMon.statBlock['currentHealth'] >= 1) and (nmeMon.statBlock['currentHealth'] >= 1)):
        thumby.display.fill(0)
        tempSelect = currentSelect
        currentSelect = showOptions(options, currentSelect, "", 48)
        if scroller >= myScroller.scrollerLength:
            scroller = 0
        scroller = scroller + 1
        thumby.display.fillRect(0, 30, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(scroller)+80, 30, 1)
        if currentSelect == 15: 
            currentSelect = tempSelect
            if options[currentSelect] == "Atk": 
                cancelCheck = attackOptionMenu(playerMon, nmeMon, myScroller, playerTrainLevel, npcTrainLevel, 1)
                if cancelCheck == 0:
                    thumby.display.update()
                    #time.sleep(1)
                if cancelCheck == 3:
                    return 1
            elif options[currentSelect] == "Run": 
                nmeMon.statBlock['currentHealth'] = 0
                return 0
            elif options[currentSelect] == "Cap": 
                doesCap = random.randint(0,1)
                if doesCap == 1:
                    return 2 
            elif options[currentSelect] == "Itm": 
                pass
            elif options[currentSelect] == "Chg": 
                return 4 
            else: 
                pass
        if currentSelect == 14 or currentSelect == 12 or currentSelect == 13 :
            currentSelect = tempSelect    
        thumby.display.blit(playerMon.bodyBlock['head'], 0, 0, 20, 9)
        thumby.display.blit(playerMon.bodyBlock['body'], 0, 9, 20, 9)
        thumby.display.blit(playerMon.bodyBlock['legs'], 0, 18, 20, 9)
        thumby.display.drawSprite(nmeMon.bodyBlock['head'], 25, 0, 20, 9, 1, 0, 0)
        thumby.display.drawSprite(nmeMon.bodyBlock['body'], 25, 9, 20, 9, 1, 0, 0)
        thumby.display.drawSprite(nmeMon.bodyBlock['legs'], 25, 18, 20, 9, 1, 0, 0)
        thumby.display.update()

    
def makeSureNoDuplicateAttacks(currentMon, currentAttackList):
    checkingTotal = 0
    listRangeCheck = 0
    for attacksKnown in currentAttackList:
        checkingTotal = checkingTotal + 1
    for i in range(0, checkingTotal):
        for n in range(0, checkingTotal):
            if i <= (i - listRangeCheck):
                if (currentMon.attackList[i].name == currentAttackList[n].name) and (i != n):
                    currentMon.attackList.pop(n)
                    listRangeCheck = listRangeCheck + 1


def switchActiveMon(playerInfo, oldActiveMon, newActiveMon, newActiveMonOldPos):
    gc.collect()
    tempMon = oldActiveMon
    tempMon.statBlock = oldActiveMon.statBlock.copy()
    tempMon.bodyBlock = oldActiveMon.bodyBlock.copy() 
    tempMon.attackList = oldActiveMon.attackList.copy()
    tempMon.mutateSeed = oldActiveMon.mutateSeed.copy() 
    
    playerInfo.friends[0] = newActiveMon
    playerInfo.friends[0].statBlock = newActiveMon.statBlock.copy()
    playerInfo.friends[0].bodyBlock = newActiveMon.bodyBlock.copy()
    playerInfo.friends[0].attackList = newActiveMon.attackList.copy()
    playerInfo.friends[0].mutateSeed = newActiveMon.mutateSeed.copy() 
    
    playerInfo.friends[newActiveMonOldPos] = tempMon
    playerInfo.friends[newActiveMonOldPos].statBlock = tempMon.statBlock.copy()
    playerInfo.friends[newActiveMonOldPos].bodyBlock = tempMon.bodyBlock.copy()
    playerInfo.friends[newActiveMonOldPos].attackList = tempMon.attackList.copy() 
    playerInfo.friends[newActiveMonOldPos].mutateSeed = tempMon.mutateSeed.copy() 


def autoMonsterSwitchInBattle(playerInfo):
    if playerInfo.friends[0].statBlock['currentHealth'] < 1:
        x = 0
        for monsters in playerInfo.friends:
            if playerInfo.friends[x].statBlock['currentHealth'] > 0:
                switchActiveMon(playerInfo, playerInfo.friends[0], playerInfo.friends[x], x)
            x = x + 1


def currentSelectCheckRange(optionAmount, currentSelect):
    if optionAmount > 1 and optionAmount !=2:
        if currentSelect > optionAmount - 2 :
            currentSelect = currentSelect - optionAmount
        if currentSelect < -abs(optionAmount) + 2:
            currentSelect = currentSelect + optionAmount
    else:
        if currentSelect > optionAmount - 1 :
            currentSelect = currentSelect - optionAmount
        if currentSelect < -abs(optionAmount) + 1:
            currentSelect = currentSelect + optionAmount
    return currentSelect


def showOptions(options, currentSelect, bottomText, x=0):
    optionAmount = len(options)
    currentSelect = currentSelectCheckRange(optionAmount, currentSelect)
    
    thumby.display.fill(0)
    thumby.display.fillRect(0+x, 9, 72, 9, 1)
    if optionAmount > 1: 
        thumby.display.drawText(options[currentSelect - 1], 0+x, 1, 1) # prints top opt
        if optionAmount > 2:
            thumby.display.drawText(options[currentSelect+1], 0+x, 19, 1) #prints bottom opt
    thumby.display.drawText(options[currentSelect], 0+x, 10, 0) # prints center opt
    
    thumby.display.drawText(bottomText, 0, 28, 1) # prints other info on bottom of screen
    currentSelect = buttonInput(currentSelect)
    if optionAmount <= 1:
        if currentSelect == 15:
            return currentSelect
        elif currentSelect == 14:
            return currentSelect
        elif currentSelect > 0 or currentSelect < 0:
            return 0
    return currentSelect


def playerInformation(playerInfo):
    thumby.display.fill(0)
    thumby.display.drawText(playerInfo.name, 0, 0 ,1)
    thumby.display.blit(player3_sprite,0,9,8,8)
    thumby.display.drawText("Lvl: " + str(playerInfo.trainerLevel), 0, 19, 1)
    thumby.display.drawText("Exp: " + str(playerInfo.experience), 0, 28, 1)
    thumby.display.update()
    time.sleep(2)

def displayItems(playerInfo):
    thumby.display.fill(0)
    gc.collect()
    curSelect = 0
    tempSelect = curSelect
    cancelCheck = 0
    optionList = []
    for items in playerInfo.inventory:
        optionList.append(items.name)
    x = len(optionList)
    if x > 0:
        while cancelCheck != 1:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect ==  15:
                curSelect = tempSelect
                playerInfo.inventory[curSelect].doAction(playerInfo.friends[0]) 
                playerInfo.inventory.pop(curSelect)
                cancelCheck = 1
            if curSelect == 14:
                cancelCheck = 1
            thumby.display.update()
    else:
        pass


def showMonInfo(playerInfo, startOfgameCheck=0):
    x = 0
    xMonRange = len(playerInfo.friends)
    currentSelect = -2
    tempSelect = currentSelect
    goBack = 0
    
    monsterListInfo = playerInfo.friends
    while(goBack != 1): 
        if currentSelect == 9:
            currentSelect = -2
        currentSelect = currentSelectCheckRange(10, currentSelect)
        if (currentSelect < tempSelect) and currentSelect != -2:
            currentSelect = tempSelect
        tempSelect = currentSelect
        thumby.display.fill(0)
        if currentSelect == -2: 
            thumby.display.blit(monsterListInfo[x].bodyBlock['head'], 25, 0, 20, 9)
            thumby.display.blit(monsterListInfo[x].bodyBlock['body'], 25, 9, 20, 9)
            thumby.display.blit(monsterListInfo[x].bodyBlock['legs'], 25, 18, 20, 9)
            thumby.display.drawText(monsterListInfo[x].statBlock['given_name'], 0, 28, 1)
        elif currentSelect == -1:
            thumby.display.drawText(monsterListInfo[x].statBlock['given_name'], 0, 1, 1)
            thumby.display.drawText("is a", 0, 9, 1)
            thumby.display.drawText(str(monsterListInfo[x].statBlock['name']), 0, 19, 1)
        elif currentSelect <=8:
            while(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]] == ""):
                currentSelect = currentSelect + 1
            thumby.display.drawText(monsterListInfo[x].keyList[currentSelect], 0, 1, 1)
            thumby.display.drawText(str(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]]), 0, 9, 1)
        thumby.display.update()
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 15:
            if playerInfo.friends[0] != playerInfo.friends[x] or startOfgameCheck == 1:
                switchActiveMon(playerInfo, monsterListInfo[0], monsterListInfo[x], x)
                #print(playerInfo.friends[0].statBlock['name'], " is now active.")
                x = 0
                currentSelect = -2
                if startOfgameCheck == 1:
                    goBack = 1
            else:
                pass #print("already active")
        elif currentSelect == 14 and startOfgameCheck == 0:
            goBack = 1
        elif currentSelect == 12:
            x = x + 1
            currentSelect = -2
            if x >= xMonRange:
                x = x - 1
        elif currentSelect == 13:
            x = x - 1
            currentSelect = -2
            if x < 0:
                x = x + 1
        else:
            pass


def trainActiveMon(myMonStats):  
    gc.collect()
    micropython.mem_info()
    thumby.display.fill(0)
    healthAmtTxt = (str(myMonStats['Health']) + '/' + str(myMonStats['maxHealth']))
    agileAmtTxt = (str(myMonStats['Agility']) + '/' + str(myMonStats['maxAgility']))
    strengthAmtTxt = (str(myMonStats['Strength']) + '/' + str(myMonStats['maxStrength']))
    enduranceAmtTxt = (str(myMonStats['Endurance']) + '/' + str(myMonStats['maxEndurance']))
    mystAmtTxt = (str(myMonStats['Mysticism']) + '/' + str(myMonStats['maxMysticism']))  # mysticism
    tinfoilAmtTxt = (str(myMonStats['Tinfoil']) + '/' + str(myMonStats['maxTinfoil']))
    trainingPointsTxt = ("TP: " + str(myMonStats['trainingPoints']))
    
    statNameList = ["Health", "Agile", "Strength", "Endurance", "Mysticism", "Tinfoil"]
    statNumsList = [healthAmtTxt, agileAmtTxt, strengthAmtTxt, enduranceAmtTxt, mystAmtTxt, tinfoilAmtTxt]
    
    goBack = 0
    currentSelect = 1
    tempSelect = currentSelect
    while goBack != 1:
        
        if currentSelect > 6 - 2 :
            currentSelect = currentSelect - 6
        if currentSelect < -6 + 2: 
            currentSelect = currentSelect + 6
        thumby.display.fill(0)
        thumby.display.drawText(statNameList[currentSelect], 0, 1, 1)
        thumby.display.drawText(statNumsList[currentSelect], 0, 10, 1)
        thumby.display.drawText(trainingPointsTxt, 0, 19, 1)
        thumby.display.drawText(myMonStats['given_name'], 0, 28, 1)
        tempSelect = currentSelect
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 14: 
            goBack = 1
        if currentSelect == 15:
            currentSelect = tempSelect
            if myMonStats['trainingPoints'] > 0:
                if currentSelect == 0 and myMonStats['Health'] < myMonStats['maxHealth']: 
                    myMonStats['Health'] = myMonStats['Health'] + 1
                    myMonStats['currentHealth'] = myMonStats['Health']
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                elif currentSelect == 1 and myMonStats['Agility'] < myMonStats['maxAgility']: 
                    myMonStats['Agility'] = myMonStats['Agility'] + 1
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                elif currentSelect == 2 or currentSelect == -4 and myMonStats['Strength'] < myMonStats['maxStrength']: 
                    myMonStats['Strength'] = myMonStats['Strength'] + 1
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                elif currentSelect == 3 or currentSelect == -3  and myMonStats['Endurance'] < myMonStats['maxEndurance']: 
                    myMonStats['Endurance'] = myMonStats['Endurance'] + 1
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                elif currentSelect == 4 or currentSelect == -2  and myMonStats['Mysticism'] < myMonStats['maxMysticism']: 
                    myMonStats['Mysticism'] = myMonStats['Mysticism'] + 1
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                elif currentSelect == -1 and myMonStats['Tinfoil'] < myMonStats['maxTinfoil']: 
                    myMonStats['Tinfoil'] = myMonStats['Tinfoil'] + 1
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
                else:
                    thumby.display.fill(0)
                    thumby.display.drawText("Stat is", 0, 1, 1)
                    thumby.display.drawText("already", 0, 10, 1)
                    thumby.display.drawText("maxed out", 0, 19, 1)
                    thumby.display.update()
                    time.sleep(1)
            else:
                thumby.display.fill(0)
                thumby.display.drawText("Not", 0, 1, 1)
                thumby.display.drawText("Enough", 0, 10, 1)
                thumby.display.drawText("Trainer", 0, 19, 1)
                thumby.display.drawText("Points", 0, 28, 1)
                thumby.display.update()
                time.sleep(1)
            goBack = 1
        thumby.display.update()


def giveName(beingNamed):
    capAlphabet = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z']
    character_list = [' ','a','b','c','d','e','f','g', 'h', 'i', 'j','k','l',
                        'm','n', 'o', 'p','q','r','s','t','u','v','w','x','y','z'] 
    selected_chars = beingNamed
    c = 1
    goBack = 0
    addDelLtr_sprite = [8,28,42,8,8,8,0,20,20,20,20,0,62,34,34,28,0,62,42,42,0,62,32,32,0,62,42,42,0,2,62,2,0,62,42,42,0,0,0,0,
           4,4,4,21,14,4,0,10,10,10,10,0,31,5,5,31,0,31,17,17,14,0,31,17,17,14,0,0,0,31,16,16,1,31,1,0,31,9,9,22]

    while(goBack != 1):

        thumby.display.fill(0)
        thumby.display.fillRect(0, 9, 10, 10, 1)
        thumby.display.drawText(character_list[c - 1], 1, 0, 1)
        thumby.display.drawText(character_list[c], 1, 10, 0)
        thumby.display.drawText(character_list[c + 1], 1, 19, 1)
        thumby.display.drawText(selected_chars, 1, 27, 1)
        thumby.display.blit(addDelLtr_sprite, 25, 10, 40, 16)
        thumby.display.update()
    
        while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
            pass # Wait for the user to give us something
        if(thumby.buttonU.pressed() == True):
            while(thumby.buttonU.pressed() == True):  
                pass
            if c == -24:
                c = 3
            c = c - 1
        if(thumby.buttonD.pressed() == True):
            while(thumby.buttonD.pressed() == True):  
                pass
            if c == 24:
                c = -3
            c = c + 1
        if(thumby.buttonR.pressed() == True):
            while(thumby.buttonR.pressed() == True):  
                pass
            if len(selected_chars) == 0:
                selected_chars = selected_chars + capAlphabet[c]
            else:
                selected_chars = selected_chars + character_list[c]
        if(thumby.buttonL.pressed() == True):
            while(thumby.buttonL.pressed() == True):  
                pass
            if len(selected_chars) > 0:
                selected_chars = selected_chars.rstrip(selected_chars[-1])
        if(thumby.buttonA.pressed() == True ):
            while(thumby.buttonA.pressed() == True):
                pass
            if len(selected_chars) > 0 :
                beingNamed = selected_chars
            goBack = 1
        if(thumby.buttonB.pressed() == True ):
            while(thumby.buttonB.pressed() == True):
                pass
            goBack = 1
    return beingNamed


def optionScreen(playerInfo): #monsterInfo)
    if(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
    
        thumby.display.fill(0)
        gc.collect()
        curSelect = 1
        tempSelect = curSelect
        cancelCheck = 0
        optionList = ["YourInfo", "Friends", "Items", "Monsters", "Save", "Back"]
        subOptionsFriends = ["Info", "Train", "LearnAtk", "GiveName", "Mutate", "Back"]
    
        while cancelCheck != 1:
            gc.collect()
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            if curSelect == 12 or curSelect == 13:
                curSelect = tempSelect
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect == 15:
                curSelect = tempSelect
                if optionList[curSelect] == "YourInfo":
                    playerInformation(playerInfo)
                if optionList[curSelect] == "Friends":
                    goBack = 0
                    curSelect = 1
                    while(goBack != 1):
                        thumby.display.fill(0)
                        if curSelect == 12 or curSelect == 13:
                            curSelect = tempSelect
                        tempSelect = curSelect
                        curSelect = showOptions(subOptionsFriends, curSelect, "Friends")
                        if curSelect == 15:
                            curSelect = tempSelect
                            if subOptionsFriends[curSelect] == "Info":
                                showMonInfo(playerInfo)
                            if subOptionsFriends[curSelect] == "Train":
                                trainActiveMon(playerInfo.friends[0].statBlock)
                            if subOptionsFriends[curSelect] == "LearnAtk":
                                trainAnAttackMove(playerInfo.friends[0])
                            if subOptionsFriends[curSelect] == "GiveName":
                                playerInfo.friends[0].statBlock['given_name'] = giveName(playerInfo.friends[0].statBlock['given_name'])
                            if subOptionsFriends[curSelect] == "Mutate":
                                playerInfo.friends[0].mutateMon()
                                print("mutate stuff happened, check Info or Train to see what changed") 
                            if subOptionsFriends[curSelect] == "Back":
                                curSelect = 1
                                goBack = 1
                        if curSelect == 14:
                            curSelect = 1
                            goBack = 1
                        thumby.display.update()
                if optionList[curSelect] == "Items":
                    displayItems(playerInfo)
            if curSelect == 14:
                cancelCheck = 1
                thumby.display.fill()
            thumby.display.update()


def trainAnAttackMove(monsterInfo):
        tpRequired = 5 
        howManyTypes = 0
        newAttack = AttackMove()
        attacksKnown = len(monsterInfo.attackList)
        #print("attacksKnown = ", attacksKnown)
        attackLearned = 0
        noAttacksToLearn = 0
        numberOfAttacks = 1
        
        if monsterInfo.statBlock['trainingPoints'] >= tpRequired:
            for x in range(1,4):
                if monsterInfo.statBlock[monsterInfo.keyList[x]] != "":
                    howManyTypes = howManyTypes + 1
        learnFromType = random.randint(1,howManyTypes)
        while(attackLearned != 1):
            selectionNumber = random.randint(0, numberOfAttacks)
            newAttack.getAnAttackMove(selectionNumber, monsterInfo.statBlock[monsterInfo.keyList[learnFromType]])
            monsterInfo.attackList.append(newAttack)
            monsterInfo.attackList = monsterInfo.attackList.copy()
            makeSureNoDuplicateAttacks(monsterInfo, monsterInfo.attackList)
            checkKnownAttacks = len(monsterInfo.attackList)
            if attacksKnown != checkKnownAttacks:
                attackLearned = 1
            noAttacksToLearn = noAttacksToLearn  + 1
            if noAttacksToLearn == 4:
                attackLearned = 1


def tameMon(playerInfo, npcMon):
    gc.collect()
    newMon = Monster()
    newMon.statBlock = npcMon.statBlock.copy()
    newMon.bodyBlock = npcMon.bodyBlock.copy()
    newMon.attackList = npcMon.attackList.copy()
    newMon.mutateSeed = npcMon.mutateSeed.copy()
    gc.collect()
    playerInfo.friends.append(newMon)
    

def makeWorld():
    gc.collect()
    worldSize = 25 
    worldList = []
    for i in range(0 , worldSize):
        newMap = Map()
        newMap.procGenMap()
        newMap.roomNumber = i + 1
        worldList.append(newMap)
    return worldList
    

def makeMonsterList():
    gc.collect()
    numberOfMons = 25
    monsterList = []
    #random.seed()                                                      # you can set the here if you want to see the same set of monsters each run
    for i in range (0 , numberOfMons):
        newMon = Monster()
        newMon.makeMonster()
        monsterList.append(newMon)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,3), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,3), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,1), monsterList[i].statBlock['Type1'])
        monsterList[i].attackList.append(newMonAtk)
        makeSureNoDuplicateAttacks(newMon, newMon.attackList)
        monsterList[i].makeMonBody()
    return monsterList


def openScreen():
    thumby.display.fill(0)
    thumby.display.drawText("Tiny Mon!", 0, 10, 1)
    thumby.display.drawText("Press A/B", 0, 24, 1)
    thumby.display.update()
    while(thumby.actionPressed == True):
        pass    
    while(thumby.actionPressed() == False):
        pass
    battleStartAnimation(0)    
    

def makePlayer(monster1, monster2, monster3):
    currentSelect = 0
    newPlayer = Player()
    thumby.display.fill(0)
    thumby.display.drawText("Press A", 0, 0, 1)
    thumby.display.drawText("to give", 0, 9, 1)
    thumby.display.drawText("yourself", 0, 18, 1)
    thumby.display.drawText("a name!", 0, 27, 1)
    thumby.display.update()
    while(currentSelect != 15):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.name = giveName(newPlayer.name)
    thumby.display.fill(0)
    thumby.display.drawText("Press A", 0, 0, 1)
    thumby.display.drawText("to pick", 0, 9, 1)
    thumby.display.drawText("yourFirst", 0, 18, 1)
    thumby.display.drawText("Monster!", 0, 27, 1)
    thumby.display.update()
    while(currentSelect != 15):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.friends.append(monster1)
    newPlayer.friends.append(monster2)
    newPlayer.friends.append(monster3)
    showMonInfo(newPlayer, 1)
    thumby.display.update()
    newPlayer.friends.pop()
    newPlayer.friends.pop()
    thumby.display.fill(0)
    thumby.display.drawText("Good", 0, 0, 1)
    thumby.display.drawText("Luck!", 0, 9, 1)
    thumby.display.update()
    while(currentSelect != 15):
        currentSelect = buttonInput(currentSelect)
    return newPlayer 


####  ---- main ---  ####

print(time.gmtime(0))

npcMon = Monster()
world=[]
monsterList=[]
room = 0
activeMon = 0
world = makeWorld()
monsterList = makeMonsterList()
openScreen()
random.seed(time.ticks_ms())
monsterList = makeMonsterList()
myGuy = makePlayer(monsterList[0],monsterList[1], monsterList[2])

#pretty much the game after this point

room = math.ceil(25 / 2)
tempRoom = room
npcMonRoaming = RoamingMonster() 
npcMonRoaming.placeMonster(world[room])
battle = 0
while(1):
    gc.collect() 
    micropython.mem_info()
    micropython.qstr_info()
    
    while(battle != 1):
        thumby.display.fill(0)
        myGuy.drawPlayer()
        room = mapChangeCheck(myGuy, world[room], room) 
        if tempRoom != room:
            npcMonRoaming.removeMonster()
            npcMonRoaming.placeMonster(world[room])
            tempRoom = room
        npcMonRoaming.drawMonster()
        myGuy.movePlayer(world[room], npcMonRoaming)
        myGuy.drawPlayer()
        optionScreen(myGuy)
        thumby.display.update()
        
        if myGuy.currentPos == npcMonRoaming.currentPos:
            npcMonRoaming.removeMonster()
            battle = 1
            battleStartAnimation(1)
    
    gc.collect()
    npcMon = monsterList[random.randint(0,25 - 1)]
    while(battle == 1):
        victory = 0
        thumby.display.fill(0)
        victory = battleScreen(myGuy.friends[activeMon], npcMon, myGuy.trainerLevel, (myGuy.trainerLevel + random.randrange(-2,2)))
        autoMonsterSwitchInBattle(myGuy)
        if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
            battle = 0
            myGuy.friends[activeMon].statBlock['currentHealth'] = myGuy.friends[activeMon].statBlock['Health'] # added to reset my monster's HP after a loss, while testing
        if npcMon.statBlock['currentHealth'] == 0:
            battle = 0
            if victory == 1: 
                myGuy.levelUpCheck()
                myGuy.friends[0].statBlock['trainingPoints'] = myGuy.friends[0].statBlock['trainingPoints'] + 1
                if len(myGuy.inventory) < myGuy.maxHelditems:
                    randoNum = random.randint(1,4)
                    if randoNum == 1:
                        newItem = Item("GenHeal", 1)
                        newItem.getItem()
                        myGuy.inventory.append(newItem)
            npcMon.statBlock['currentHealth'] = npcMon.statBlock['Health']
        if victory == 2: 
            gc.collect()
            tameMon(myGuy,npcMon)
            print("You tamed the monster! yay! <3")
            battle = 0
        if victory == 4: 
            showMonInfo(myGuy)
            victory = 0
            
        thumby.display.update()
    battleStartAnimation(0) 
