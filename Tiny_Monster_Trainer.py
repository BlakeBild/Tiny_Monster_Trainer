import gc
gc.enable()
import time
import thumby
import math
import random
import micropython
import ujson


player3_sprite = [0,46,251,127,123,255,46,0]
blob_sprite = [56,124,124,54,62,116,124,56]
head0_sprite = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class Tile:
    def __init__(self):
        self.tileType = 0
        self.isObjectHere = 0

    def generateTile(self, preTileType):
        if preTileType == 0: # nothing
            pass
        elif preTileType == 1: # wall
            self.isObjectHere = 0
        elif preTileType == 2: # floor
            self.tileType = 2 
            self.isObjectHere = 1
        elif preTileType == 3: # door
            self.tileType = 3 
            self.isObjectHere = 2
        elif preTileType == 8: # crack
            self.tileType = 8 
            self.isObjectHere = 1
        else:
            self.tileType = 1 # wall
            self.isObjectHere = 0


class Map:
    def __init__(self):
        self.elementType = 0
        self.floor = []
        self.roomNumber = 0 
        for i in range(9 * 5):
            floorTile = Tile()
            self.floor.append(floorTile)
            self.floor[i].tileType = 2
            self.floor[i].isObjectHere = 1 
        for x in range(0, 9): 
            self.floor[x].tileType = 1 
            self.floor[x].isObjectHere = 0
            self.floor[4*9+x].tileType = 1
            self.floor[4*9+x].isObjectHere = 0
        for y in range(0, 5):
            self.floor[y*9].tileType = 1 
            self.floor[y*9].isObjectHere = 0
            self.floor[y*9+8].tileType = 1
            self.floor[y*9+8].isObjectHere = 0
        for x in range(0, 9):
            if x == math.floor(9 / 2):
                self.floor[x].tileType = 3 
                self.floor[x].isObjectHere = 2
                self.floor[4*9+x].tileType = 3
                self.floor[4*9+x].isObjectHere = 2
        for y in range(0, 5):
            if y == math.floor(5 / 2):
                self.floor[y*9].tileType = 3
                self.floor[y*9].isObjectHere = 2
                self.floor[y*9+8].tileType = 3
                self.floor[y*9+8].isObjectHere = 2

 
    def procGenMap(self):
        terrainChance = 20
        self.elementType = random.randint(0,10)
        for x in range (0,9):
            for y in range(0,5):
                floor = self.floor[y*9+x]
                if floor.tileType == 1:
                    pass
                if floor.tileType == 2:
                    somethingHere = random.randint(0,terrainChance)
                    if somethingHere == 1:
                        terrainTile = random.randrange(7,9)
                        self.floor[y*9+x].generateTile(terrainTile)

 
    def displayMap(self):
        
        wall_sprite = [24,126,255,102,102,255,126,24]
        floor_sprite = [0,0,0,0,0,0,0,0]
        floor_crack = [0,0,0,0,40,20,0,0]
        door_sprite = [255,255,3,1,17,19,255,255]
        tree2_sprite = [0,14,95,119,127,91,14,0]
        tree3_sprite = [255,157,14,8,2,14,159,247]
        mountain1_sprite = [192,120,12,30,63,14,60,224]
        
        for x in range(0, 9):
            for y in range(0, 5):
                floor = self.floor[y*9+x]
                if(floor.tileType == 1 and self.elementType < 3):
                    thumby.display.blit(bytearray(tree2_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1 and self.elementType < 9):
                    thumby.display.blit(bytearray(mountain1_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1):
                    thumby.display.blit(bytearray(wall_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 2):
                    thumby.display.blit(bytearray(floor_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 3):
                    thumby.display.blit(bytearray(door_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 8):
                    thumby.display.blit(bytearray(floor_crack), x*8 ,y*8 , 8, 8, 0, 0, 0)
                else:
                    thumby.display.blit(bytearray(tree2_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)


class AttackMove():
    def __init__(self, name="", numUses=0, baseDamage=0, magic=0, moveElementType=""):
        self.name = name 
        self.numUses = numUses 
        self.currentUses = numUses 
        self.baseDamage = baseDamage  
        self.magic = magic 
        self.moveElementType = moveElementType


    def getAnAttackMove(self, selectionNum, elmType=""):
        basicList = []
        attack1 = AttackMove("ElsePoke1", 15, -2)
        attack2 = attack1
        attack3 = attack1
        attack4 = attack1
        if elmType == "Default":
            attack1 = AttackMove("Poke", 15, 0)
            attack2 = AttackMove("Hit", 10, 1)
            attack3 = AttackMove("MagicHit", 10, 1, 1)
        elif elmType == "Earth":
            attack1 = AttackMove("RockToss", 15, 5, 0, "Earth")
            attack2 = AttackMove("Quake", 15, 5, 1, "Earth")
            attack3 = AttackMove("Pressure", 10, 2, 1, "Water")
            attack4 = AttackMove("Entomb", 10, 2, 0, "Darkness")
        elif elmType == "Wind":
            attack1 = AttackMove("Gust", 15, 5, 0, "Wind")
            attack2 = AttackMove("Cyclone", 15, 5, 1, "Wind")
            attack3 = AttackMove("Lightning", 10, 2, 0, "Light")
            attack4 = AttackMove("Divine Wind", 10, 2, 1, "Ethereal")
        elif elmType == "Water":
            attack1 = AttackMove("Geyser", 15, 5, 0, "Water")
            attack2 = AttackMove("Ice Shards", 15, 5, 1, "Water")
            attack3 = AttackMove("Freeze", 10, 2, 1, "Mind")
            attack4 = AttackMove("Wave", 10, 2, 0, "Physical")
        elif elmType == "Fire":
            attack1 = AttackMove("Torch", 15, 5, 0, "Fire")
            attack2 = AttackMove("Blaze", 15, 5, 1, "Fire") 
            attack3 = AttackMove("Flare", 10, 2, 1, "Light")
            attack4 = AttackMove("Inferno", 10, 2, 0, "Wind")
        elif elmType == "Light":
            attack1 = AttackMove("Dazzle", 15, 5, 0, "Light")
            attack2 = AttackMove("Razzle", 15, 5, 1, "Light")
            attack3 = AttackMove("Radiance", 10, 2, 0, "Fire")
            attack4 = AttackMove("Gleam", 10, 2, 1, "Mystical")
        elif elmType == "Darkness":
            attack1 = AttackMove("Murk", 15, 5, 0, "Darkness")
            attack2 = AttackMove("Shadow", 15, 5, 1, "Darkness")
            attack3 = AttackMove("Unholy Poke", 10, 2, 0, "Mystical")
            attack4 = AttackMove("Dire Ruin", 10, 2, 1, "Ethereal")
        elif elmType == "Cute":
            attack1 = AttackMove("Sing Song", 15, 5, 0, "Cute")
            attack2 = AttackMove("Adorbes", 15, 5, 1, "Cute")
            attack3 = AttackMove("Bubbles", 10, 2, 0, "Water")
            attack4 = AttackMove("Fluff Ball", 10, 2, 1, "Physical")
        elif elmType == "Mind":
            attack1 = AttackMove("Headbutt", 15, 5, 0, "Mind")
            attack2 = AttackMove("Psychic", 15, 5, 1, "Mind")
            attack3 = AttackMove("Project Rock", 10, 2, 0, "Earth")
            attack4 = AttackMove("Good Vibes", 10, 2, 1, "Cute")
        elif elmType == "Physical":
            attack1 = AttackMove("Body Slam", 15, 5, 0, "Physical")
            attack2 = AttackMove("Super Hit", 10, 10, 1, "Physical")
            attack3 = AttackMove("Boulder Toss", 10, 2, 0, "Earth")
            attack4 = AttackMove("Love Tap", 10, 2, 0, "Cute")
        elif elmType == "Mystical":
            attack1 = AttackMove("Magic Missile", 15, 5, 0, "Mystical")
            attack2 = AttackMove("Ritual", 15, 5, 1, "Mystical")
            attack3 = AttackMove("Rune Toss", 10, 2, 0, "Wind")
            attack4 = AttackMove("Immolate", 10, 2, 1, "Fire")
        elif elmType == "Ethereal":
            attack1 = AttackMove("Spooky Hit", 15, 5, 0, "Ethereal")
            attack2 = AttackMove("Superlunary", 15, 5, 1, "Ethereal")
            attack3 = AttackMove("Obscurity", 10, 2, 1, "Darkness")
            attack4 = AttackMove("Rue", 10, 2, 1, "Mind")
        basicList.append(attack1)
        basicList.append(attack2)
        basicList.append(attack3)
        basicList.append(attack4)
        self.name = basicList[selectionNum].name
        self.numUses = basicList[selectionNum].numUses
        self.currentUses = basicList[selectionNum].currentUses
        self.baseDamage = basicList[selectionNum].baseDamage
        self.magic = basicList[selectionNum].magic
        self.moveElementType = basicList[selectionNum].moveElementType


class TextForScroller():
    def __init__(self, scrollingText):
        self.scrollingText = scrollingText
        self.scrollerLength = len(self.scrollingText) * 6 +82
        self.scroller = 0
    
    def moveScroll(self):
        if self.scroller >= self.scrollerLength:
                self.scroller = 0
        else:
            self.scroller = self.scroller + 1
        return self.scroller
 

class Item():
    def __init__(self, name, key, bonus=0):
        self.name = name
        self.key = key
        self.bonus = bonus
        
    def doAction(self, monsterInfo):
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
        elif self.key == 3:
            for moves in range(0, len(monsterInfo.attackList)):
                monsterInfo.attackList[moves].currentUses = monsterInfo.attackList[moves].numUses
        else:
            pass

    def getItem(self):
        randoNum = random.randint(1,5)
        if randoNum == 1:
            self.name = "Bandaids"
            self.key = 1
            self.bonus = -2
        elif randoNum == 2:
            self.name = "PushPops"
            self.key = 1
            self.bonus = 10
        elif randoNum == 3:
            self.name = "Stickers"
            self.key = 2
        elif randoNum == 4:
            self.name = "Ribbons"
            self.key = 2
            self.bonus = 1
        elif randoNum == 5:
            self.name = "Crystals"
            self.key = 3
            self.bonus = random.randint(0,7)
        else:
            pass


class Player:
    def __init__(self):                                           
        self.playerBlock = {'name' : "CoolDude",
                            'trainerLevel' : 1,
                            'experience' : 0,
                            'friendMax' : 2,
                            'worldSeed' : 0}
            
        self.friends = []
        self.inventory = []
        self.maxHelditems = 10
        self.lOrR = 0
        self.currentPos = math.ceil((9 * 5) / 2)
        self.position = []
        for i in range(9 * 5):
            self.position.append(0)
        self.position[self.currentPos] = 1
 
 
    def drawPlayer(self):
        for x in range(0, 9):
            for y in range(0, 5):
                if self.position[y*9+x] == 1 :
                    thumby.display.blit(bytearray(player3_sprite), x*8 , y*8, 8, 8, -1, self.lOrR, 0)
 
 
    def movePlayer(self, currentRoom, monster, monsterMovement):
        while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
            pass
        if(thumby.buttonU.pressed() == True):
            while(thumby.buttonU.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 9
                self.position[self.currentPos] = 1
                monster.moveMonster(self, world[room], monsterMovement)
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
                monster.moveMonster(self, world[room], monsterMovement)
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room], 0)
        if(thumby.buttonL.pressed() == True):
            while(thumby.buttonL.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 1
                self.position[self.currentPos] = 1
                self.lOrR = 0
                self.drawPlayer()
                monster.moveMonster(self, world[room], monsterMovement)
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
                self.lOrR = 1
                self.drawPlayer()
                monster.moveMonster(self, world[room], monsterMovement)
            else:
                self.drawPlayer()
                monster.moveMonster(self, world[room], monsterMovement)


    def levelUpCheck(self):
        self.playerBlock['experience'] = self.playerBlock['experience'] + 1
        if self.playerBlock['experience'] ==  math.floor(self.playerBlock['trainerLevel'] * 1.5):
            self.playerBlock['trainerLevel'] = self.playerBlock['trainerLevel'] + 1
            thingAquired("Your", "Trainer", "Level is", "Now " + str(self.playerBlock['trainerLevel']), 2)
            if self.playerBlock['trainerLevel'] % 10 == 0 & self.playerBlock['friendMax'] < 4: #I haven't tested this yet. Hope it works :P
                self.playerBlock['friendMax'] = self.playerBlock['friendMax'] + 1
                #print("friendMax = ", str(self.playerBlock['friendMax'])) 

        
class Monster:
    def __init__(self):
        self.statBlock = {'name' : "", 
                        'given_name' : "",
                        'trainingPoints' : 7,
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
                        'Type1',        # 1     Move types to end of keyList so that showMonInfo can be more intuitive
                        'Type2',        # 2
                        'Type3',        # 3
                        'Agility',      # 4
                        'Strength',     # 5
                        'Endurance',    # 6
                        'Mysticism',    # 7
                        'Tinfoil']      # 8
                        
                     
        self.bodyBlock = {'head' : head0_sprite,
                            'body' : head0_sprite,
                            'legs' : head0_sprite}
                            
        self.attackList = []
        self.mutateSeed = []
                

    @staticmethod
    def makeName():
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
                else: 
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
        head1_sprite =  [0,0,0,0,48,48,200,236,76,112,112,76,236,200,48,48,0,0,0,0,
           0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        head2_sprite =  [16,124,68,76,84,124,48,22,190,224,224,190,22,48,124,68,76,84,124,16,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0]
        head3_sprite =  [0,0,0,0,62,66,129,1,193,33,65,33,197,5,137,66,62,0,0,0,
            0,0,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,0,0]
        head4_sprite =  [16,56,68,206,84,56,124,134,35,3,11,51,134,124,56,68,206,84,56,16,
            0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0]
        head5_sprite =  [0,7,30,62,62,124,254,131,17,69,69,17,131,254,124,62,62,30,7,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0]         
        head6_sprite =  [0,0,0,0,0,248,12,6,35,3,131,7,47,30,252,120,0,0,0,0,
            0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0]          
        head7_sprite =  [0,0,0,120,224,124,196,28,120,32,170,32,120,28,196,124,224,120,0,0,
            0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0]          
        head8_sprite =  [0,0,0,0,0,0,206,159,57,153,63,147,51,159,206,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0]
        head9_sprite =  [0,0,0,2,196,200,192,36,232,32,252,32,232,36,192,200,196,2,0,0,
            0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0]
        head10_sprite =  [0,0,0,0,32,112,32,4,98,68,64,68,98,4,32,112,32,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        head11_sprite =  [124,198,131,1,5,5,9,131,198,124,124,198,131,1,5,5,9,131,198,124,
           0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0]
        body1_sprite =  [0,62,255,219,118,60,31,255,255,193,193,207,135,183,255,252,0,0,0,0,
           0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0]
        body2_sprite =  [0,56,252,204,30,62,115,231,253,248,16,248,253,231,115,62,30,204,252,56,
           0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        body3_sprite =  [0,56,16,60,100,198,19,17,74,130,130,74,9,19,198,100,60,16,56,0,
            0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0]
        body4_sprite =  [6,4,28,52,38,80,254,131,41,125,117,41,131,254,80,32,32,248,136,80,
            0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0]
        body5_sprite =  [0,2,8,4,16,0,57,65,1,170,170,170,1,65,57,0,16,4,8,2,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        body6_sprite =  [146,124,16,56,124,198,1,56,68,17,17,68,56,1,198,124,56,16,124,146,
            0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0]
        body7_sprite =  [0,192,192,224,32,46,167,131,249,172,238,172,249,131,167,46,32,60,12,12,
            0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0]
        body8_sprite =  [0,31,19,19,24,28,24,16,145,255,255,255,145,16,24,28,24,19,19,31,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        body9_sprite =  [0,254,96,56,126,211,215,133,17,147,198,147,17,133,215,211,126,56,12,254,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        body10_sprite =  [0,0,32,124,126,38,14,27,183,227,9,227,183,27,14,38,126,124,32,0,
            0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0]
        body11_sprite =  [0,16,127,48,32,32,230,226,255,127,0,0,255,226,206,128,192,112,0,0,
            0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0]
        body12_sprite =  [0,28,62,127,248,240,224,71,76,254,232,254,76,71,224,240,248,127,62,28,
            0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0]
        body13_sprite = [0,0,124,198,131,49,69,65,41,3,28,16,32,38,41,41,29,129,194,60,
           0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0]
        legs1_sprite =  [0,0,0,24,30,7,1,159,255,227,1,227,255,159,0,0,0,0,0,0,
            0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0]
        legs2_sprite =  [0,0,0,48,124,30,7,243,125,7,241,3,31,121,3,199,126,60,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        legs3_sprite =  [0,0,112,24,60,78,247,123,137,14,14,14,137,123,231,78,60,16,112,0,
            0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0]
        legs4_sprite =  [0,8,24,56,40,44,39,161,225,172,36,38,163,225,179,30,12,0,0,0,
            0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0]
        legs5_sprite =  [14,31,31,191,231,49,249,154,15,15,15,15,154,249,49,231,191,31,31,14,
            0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0]
        legs6_sprite =  [0,0,0,0,0,0,1,2,5,7,7,7,5,2,1,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]        
        legs7_sprite =  [0,0,68,156,176,184,159,207,255,115,1,3,231,255,158,52,180,146,72,0,
            0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0]
        legs7_sprite =  [0,0,0,0,16,86,148,165,169,171,255,171,169,165,148,86,16,0,0,0,
            0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0]
        legs8_sprite =  [240,156,198,96,120,140,6,1,121,253,253,253,121,1,6,140,120,96,192,0,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
        legs9_sprite =  [0,0,0,0,120,140,6,1,57,125,125,125,57,1,6,140,120,0,0,0,
            0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
        legs10_sprite =  [124,194,128,56,76,224,193,131,14,172,248,94,6,131,193,228,184,0,198,124,
            0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
        legs11_sprite = [24,48,224,240,184,128,129,207,253,219,237,59,13,7,1,0,0,0,0,0,
           0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
        birbHead_sprite = [0,0,0,0,192,192,240,240,248,248,255,190,60,60,240,240,224,192,0,0,
            0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
        birbBody_sprite = [0,0,0,255,255,255,255,253,120,24,253,255,255,31,255,255,249,243,0,0,
            0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0]
        birbLegs_sprite = [0,24,62,55,51,49,180,246,179,59,185,252,190,63,31,15,7,1,0,0,
            0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0]
        
        if random.randint(0,50) != 1:
            randoNum = random.randint(0,12)
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
            11: body12_sprite,
            12: head11_sprite}
            self.bodyBlock['head'] = heads[randoNum]
            randoNum = random.randint(1,13)
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
            12: body12_sprite,
            13: body13_sprite}
            self.bodyBlock['body'] = bodyyodyody[randoNum]
            randoNum = random.randint(1,11)
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
            10: legs10_sprite,
            11: legs11_sprite}
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
        monsterTypes = ["Wind", "Earth", "Water", "Fire", "Mind", "Darkness", 
                        "Cute", "Light", "Physical", "Mystical", "Ethereal"]
        if self.statBlock['Type1'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            return monType
        elif self.statBlock['Type2'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1']:
                monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            return monType
        elif self.statBlock['Type3'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1'] or monType == self.statBlock['Type2']:
                monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
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
                        noDupAtk(self.attackList)
                    elif self.statBlock['Type3'] == "":
                        self.statBlock['Type3'] = self.makeType()
                        myAttack = AttackMove()
                        randoNum = random.randint(0,3)
                        myAttack.getAnAttackMove(randoNum, self.statBlock['Type3'])
                        noDupAtk(self.attackList)
                    self.statBlock['maxHealth'] = self.statBlock['maxHealth'] + 20
                self.mutateSeed[1] = self.mutateSeed[1] + 1
                self.statBlock['trainingPoints'] = self.statBlock['trainingPoints'] - 5 
                thingAquired(self.statBlock['given_name'], "has", "mutated!", "", 2)
            else:
                thingAquired(self.statBlock['given_name'], "is unable to", "mutate", "again", 2)
        else:
            howManyPoints = self.statBlock['trainingPoints']
            thingAquired(self.statBlock['given_name'], ("needs " + str(5 - howManyPoints) + " more"), "Training", "Points", 2)


    def makeMonster(self):
        gc.collect()
        genStat = self.makeStat
        self.statBlock['name'] = self.makeName()
        self.statBlock['given_name'] = self.statBlock['name']
        self.statBlock['trainingPoints'] = 7
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
        for x in range (4,9):
            self.statBlock[self.keyList[x]] = genStat(0)
            self.statBlock['max' + self.keyList[x]] = genStat(self.statBlock[self.keyList[x]], 1)
        self.mutateSeed.append(random.randint(0,50))
        self.mutateSeed.append(0)

    
class RoamingMonster:
    def __init__ (self, currentPos=0, position=[]):
        self.currentPos = currentPos
        self.position = position
        for i in range(9 * 5):
            self.position.append(0)
    
    
    def drawMonster(self):
        for x in range(0, 9):
            for y in range(0, 5):
                if self.position[y*9+x] == 1 :
                    thumby.display.blit(bytearray(blob_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
    
    
    def placeMonster(self, map):
        random.seed(time.ticks_ms())
        findEmptySpot = 0
        while(findEmptySpot != 1):
            findEmptySpot = random.randint(9, 34)
            if map.floor[findEmptySpot].isObjectHere == 1:
                self.currentPos = findEmptySpot
                self.position[self.currentPos] = 1
                findEmptySpot = 1
    
    
    def removeMonster(self):
        self.position[self.currentPos] = 0
        self.currentPos = 0
    
    
    def moveMonster(self, player, currentRoom, monsterMovement=0):
        if monsterMovement == 0:
            if math.ceil(self.currentPos/9) > math.ceil(player.currentPos/9): 
                if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:  # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos - 9
                    self.position[self.currentPos] = 1
                    self.drawMonster()
                else:
                    self.drawMonster()
            elif math.ceil(self.currentPos/9) < math.ceil(player.currentPos/9): # move monster down
                if currentRoom.floor[self.currentPos+9].isObjectHere >= 1: # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos + 9
                    self.position[self.currentPos] = 1
                    self.drawMonster()
                else:
                    self.drawMonster() 
            elif self.currentPos == player.currentPos: # if monster is on same tile as player, don't move
                self.drawMonster()
            elif self.currentPos >= player.currentPos: # move monster left
                if currentRoom.floor[self.currentPos-1].isObjectHere >= 1: # check for blocked 
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos - 1
                    self.position[self.currentPos] = 1
                    self.drawMonster()
                else:
                    self.drawMonster()
            elif self.currentPos <= player.currentPos: # move monster right
                if currentRoom.floor[self.currentPos+1].isObjectHere >= 1: # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos + 1
                    self.position[self.currentPos] = 1
                    self.drawMonster()
                else:
                    self.drawMonster()
            else:
                self.drawMonster()
        else:
            randomDirList = [-9, -1, 1, 9]
            x = random.randint(0,3)
            if currentRoom.floor[self.currentPos + randomDirList[x]].isObjectHere == 1: # check for blocked
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + randomDirList[x]
                self.position[self.currentPos] = 1
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
    thumby.display.setFPS(0)
    for x in range(0,72):
        for y in range (0, 40):
            thumby.display.drawLine(x, 0, 0, y, color)
            thumby.display.drawLine(72, 40-y, 72-x, 40, color)
        thumby.display.update()
    thumby.display.fill(0)
    thumby.display.update()
    thumby.display.setFPS(30)


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


def attackAnimation(playerBod, nmeBod, attackIsPlayer, missFlag, amountOfDmg, playerHP, nmeHP, atkTxt):
    for x in range(0, 4):
        playerX = 8
        nmeX = 42
        y = 0
        nmeY = 0
        if x == 2 and attackIsPlayer == 1:
            y = 10
        elif x == 2 and attackIsPlayer == 0:
            nmeY = 10
        thumby.display.fill(0)
        printMon(playerBod, playerX + y, 0, 0)
        printMon(nmeBod, nmeX - nmeY, 0, 1)
        thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
        thumby.display.drawText(str(playerHP), 2, 30, 0)
        thumby.display.drawText(str(nmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
        thumby.display.update()
        if missFlag == 1 and x > 1 and attackIsPlayer == 1: # player misses
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2), 30, 0)
        if missFlag == 0 and x > 1 and attackIsPlayer == 1: # player hits
            thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2), 30, 0)
            thumby.display.drawText(str(playerHP), 2, 30, 0)
            thumby.display.drawText(str(nmeHP - amountOfDmg), 72 - len(str(nmeHP - amountOfDmg) * 7), 30, 0)
        if missFlag == 1 and x > 1 and attackIsPlayer == 0: # nme misses
            thumby.display.drawText("Miss", 24, 30, 0)
        if missFlag == 0 and x > 1 and attackIsPlayer == 0: # nme hits
            thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2), 30, 0)
            thumby.display.drawText(str(nmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
            thumby.display.drawText(str(playerHP - amountOfDmg), 2, 30, 0)
        thumby.display.update()
        time.sleep(1)
        y = 0
        nmeY = 0


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


def attack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    if activeAttack.magic == 1:
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + activeAttack.baseDamage
        defence = defenceMon.statBlock['Tinfoil'] + defTrainLevel + random.randint(0, 12)
    else:
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + activeAttack.baseDamage
        defence = defenceMon.statBlock['Endurance'] + defTrainLevel + random.randint(0, 12)
    hp2 = defenceMon.statBlock['currentHealth']
    dodge = defenceMon.statBlock['Agility'] + defence
    damage = 0
    hit = 1
    atkTypeBonus = 1
    defTypeBonus = 1
    if (dodge + random.randint(-abs(attackTrainLevel),100)) > (90 - defTrainLevel): # check for dodge
        if ((attackAmnt + attackMon.statBlock['Agility']) + random.randint(-10,10)) >= dodge: # check for glance
            hit = 2
        else:
            hit = 0
    if hit > 0:
        for x in range(1,3):
            atkTypeBonus = isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
        #attackMod = activeAttack.baseDamage + random.randint(0,attackTrainLevel)
        for x in range(1,3):
            defTypeBonus = isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
        #defenceMod = random.randint(0, defTrainLevel)
        damage = (attackAmnt * atkTypeBonus) - (defence * defTypeBonus)
        if damage <= 0:
            damage = 1
        else:
            damage = math.ceil(damage/hit)
    hp2 = hp2 - damage
    if hp2 < 0:
        hp2 = 0
    defenceMon.statBlock['currentHealth'] = hp2
    if hit == 1:
        return "Hit!"
    elif hit == 2:
        return "Glance"
    elif hit == 0:
        return "Miss"
    


def afterAttackSelect(attackingMon, atkChoice, defMon, playerTrainLevel, attackIsPlayer):
    scrollText = ""
    hpBeforeDmg = defMon.statBlock['currentHealth']
    attackText = attack(attackingMon, defMon, attackingMon.attackList[atkChoice], playerTrainLevel, (playerTrainLevel + random.randint(-2, 2)))
    amntOfDmg = hpBeforeDmg - defMon.statBlock['currentHealth'] 
    if amntOfDmg >= 1:
        if attackIsPlayer == 1:
            attackAnimation(attackingMon.bodyBlock, defMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, attackingMon.statBlock['currentHealth'], hpBeforeDmg, attackText)
            scrollText = (attackingMon.statBlock['given_name'] + " did " + str(amntOfDmg) + " points of damage!")
        else:
            attackAnimation(defMon.bodyBlock, attackingMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, hpBeforeDmg, attackingMon.statBlock['currentHealth'], attackText)
    else:
        if attackIsPlayer == 1:
            attackAnimation(attackingMon.bodyBlock, defMon.bodyBlock, attackIsPlayer, 1, amntOfDmg, attackingMon.statBlock['currentHealth'], hpBeforeDmg, attackText)
            scrollText = (attackingMon.statBlock['given_name'] + "'s " + attackingMon.attackList[atkChoice].name + " attack missed!" )
        else: 
            attackAnimation(defMon.bodyBlock, attackingMon.bodyBlock, attackIsPlayer, 1, amntOfDmg, hpBeforeDmg, attackingMon.statBlock['currentHealth'], attackText)
    return scrollText


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
    
    
def battleScreen(playerMon, nmeMon, playerTrainLevel, npcTrainLevel):
    #print("Hi, you are in a fight!")
    myScroller = TextForScroller(playerMon.statBlock['given_name'] + " has entered into battle with a roaming " + nmeMon.statBlock['name'] + "!")
    currentSelect = 1
    tempSelect = currentSelect
    options = ["Info", "Atk", "Run", "Tame", "Swap"] 
    while((playerMon.statBlock['currentHealth'] >= 1) and (nmeMon.statBlock['currentHealth'] >= 1)):
        thumby.display.fill(0)
        tempSelect = currentSelect
        currentSelect = showOptions(options, currentSelect, "", 47)
        thumby.display.drawFilledRectangle(0, 30, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        if currentSelect == 31: 
            currentSelect = tempSelect
            if options[currentSelect] == "Atk": 
                selectCheck = attackOptionMenu(playerMon.attackList)
                if selectCheck < 30:
                    if playerMon.attackList[selectCheck].currentUses <= 0:
                        playerMon.statBlock['currentHealth'] = math.floor(playerMon.statBlock['currentHealth'] * 0.7)
                        thingAquired(playerMon.statBlock['given_name'], "is out of", "stamina", "HP lost", 2)
                        if playerMon.statBlock['currentHealth'] <= 0:
                            return 
                    agileTie = 0
                    if (playerMon.statBlock['Agility'] + playerTrainLevel) == (nmeMon.statBlock['Agility'] + npcTrainLevel):
                        agileTie = random.randint(-2,1)
                    if (playerMon.statBlock['Agility'] + playerTrainLevel + agileTie) >= (nmeMon.statBlock['Agility'] + npcTrainLevel):
                        myScroller = TextForScroller(afterAttackSelect(playerMon, selectCheck, nmeMon, playerTrainLevel, 1))
                        if npcMon.statBlock['currentHealth'] <= 0:
                            playerMon.attackList[selectCheck].currentUses = playerMon.attackList[selectCheck].currentUses -1
                            if playerMon.attackList[selectCheck].currentUses < 0:
                                playerMon.attackList[selectCheck].currentUses = 0
                            return 1 
                        junk = afterAttackSelect(nmeMon, (len(nmeMon.attackList) -1), playerMon, playerTrainLevel, 0) 
                        del junk
                    else:
                        junk = afterAttackSelect(nmeMon, (len(nmeMon.attackList) -1), playerMon, playerTrainLevel, 0)
                        del junk
                        if playerMon.statBlock['currentHealth'] <= 0:
                            return 0 
                        myScroller = TextForScroller(afterAttackSelect(playerMon, selectCheck, nmeMon, playerTrainLevel, 1))
                    playerMon.attackList[selectCheck].currentUses = playerMon.attackList[selectCheck].currentUses -1
                    if playerMon.attackList[selectCheck].currentUses < 0:
                        playerMon.attackList[selectCheck].currentUses = 0
                    if npcMon.statBlock['currentHealth'] <= 0:
                        return 1 
            elif options[currentSelect] == "Run": 
                nmeMon.statBlock['currentHealth'] = 0
                return 0
            elif options[currentSelect] == "Tame": 
                return 2 
            elif options[currentSelect] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmeMon)
                tempPlayer.friends.append(playerMon)
                showMonInfo(tempPlayer, 0 , 1)
                del tempPlayer
            elif options[currentSelect] == "Swap":
                return 4 
            else: 
                pass
        if currentSelect == 30 or currentSelect == 28 or currentSelect == 29 :
            currentSelect = tempSelect    
        printMon(playerMon.bodyBlock, 0, 0, 0)
        printMon(nmeMon.bodyBlock, 25, 0, 1)
        thumby.display.update()
    return 0  

    
def noDupAtk(currentAttackList):
    checkingTotal = 0
    listRangeCheck = 0
    for attacksKnown in currentAttackList:
        checkingTotal = checkingTotal + 1
    for i in range(0, checkingTotal):
        for n in range(0, checkingTotal):
            if i <= (i - listRangeCheck):
                if (currentAttackList[i].name == currentAttackList[n].name) and (i != n):
                    currentAttackList.pop(n)
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


def autoSwitchMon(playerInfo):
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
    thumby.display.drawFilledRectangle(0+x, 9, 72, 9, 1)
    if optionAmount > 1: 
        thumby.display.drawText(options[currentSelect - 1], 1+x, 1, 1) # prints top opt
        if optionAmount > 2:
            thumby.display.drawText(options[currentSelect+1], 1+x, 19, 1) #prints bottom opt
    thumby.display.drawText(options[currentSelect], 1+x, 10, 0) # prints center opt
    thumby.display.drawLine(0, 28, 72, 28, 1)
    if bottomText != "":
        thumby.display.drawText(bottomText, 1, 30, 1) # prints other info on bottom of screen
    currentSelect = buttonInput(currentSelect)
    if optionAmount <= 1:
        if currentSelect == 31:
            return currentSelect
        elif currentSelect == 30:
            return currentSelect
        elif currentSelect > 0 or currentSelect < 0:
            return 0
    return currentSelect


def playerInformation(playerInfo):
    thumby.display.fill(0)
    thumby.display.drawText(playerInfo.playerBlock['name'], 0, 0 ,1)
    thumby.display.blit(bytearray(player3_sprite),0 ,9 ,8 ,8 ,0 ,0 ,0)
    thumby.display.drawText("Lvl: " + str(playerInfo.playerBlock['trainerLevel']), 0, 19, 1)
    thumby.display.drawText("Exp: " + str(playerInfo.playerBlock['experience']), 0, 28, 1)
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
        while curSelect < 11:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect ==  31:
                playerInfo.inventory[tempSelect].doAction(playerInfo.friends[0]) 
                playerInfo.inventory.pop(tempSelect)
            elif curSelect == 30:
                pass
            elif curSelect > 11:
                curSelect = tempSelect
            thumby.display.update()
    else:
        pass


def drawArrows(l, r, d, u=1): # x, y):
    arrowLR = [4,4,4,31,14,4] # 6 x 5
    arrowUD = [8,24,63,24,8] # 5 x 6    # last three are: key, mirrorX, mirrorY
    thumby.display.blit(bytearray(arrowLR), 1, 17, 6, 5, l, abs(l), 0)
    thumby.display.blit(bytearray(arrowLR), 65, 17, 6, 5, r, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 30, 5, 6, d, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 4, 5, 6, u, 0, abs(u))


def showMonInfo(playerInfo, startOfgameCheck=0, combatCheck=0):
    left = 1
    right = -1
    down = -1
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
            printMon(monsterListInfo[x].bodyBlock, 25 ,0, 0)
            drawArrows(left, right, down)
            thumby.display.drawText(monsterListInfo[x].statBlock['given_name'], math.floor(((72-(len(monsterListInfo[x].statBlock['given_name']))*6))/2), 28, 1)
        elif currentSelect == -1:
            thingAquired(monsterListInfo[x].statBlock['given_name'], "is a", monsterListInfo[x].statBlock['name'], "", 0, 1)
            drawArrows(left, right, down, -1)
        elif currentSelect <= 8:
            while(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]] == ""):
                currentSelect = currentSelect + 1
            thingAquired(monsterListInfo[x].statBlock['given_name'] + "'s",
                        monsterListInfo[x].keyList[currentSelect], 
                        "is",str(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]]), 0, 1)
            drawArrows(left, right, down)
        thumby.display.update()
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 31 and combatCheck == 0:
            if playerInfo.friends[0] != playerInfo.friends[x] or startOfgameCheck == 1:
                switchActiveMon(playerInfo, monsterListInfo[0], monsterListInfo[x], x)
                thingAquired(monsterListInfo[0].statBlock['given_name'], "is now", "your active", "monster!", 2)
                x = 0
                currentSelect = -2
                if startOfgameCheck == 1:
                    goBack = 1
            else:
                currentSelect = tempSelect
        elif currentSelect == 30 and startOfgameCheck == 0:
            goBack = 1
        elif currentSelect == 28:
            x = x + 1
            currentSelect = tempSelect
            if x >= xMonRange:
                x = x - 1
        elif currentSelect == 29:
            x = x - 1
            currentSelect = tempSelect
            if x < 0:
                x = x + 1
        elif currentSelect >= 30:
            currentSelect = -2
        else:
            pass
        if x > 0 and x < (xMonRange-1):
            left = -1
            right = -1
        elif xMonRange == 1:
            left = 1
            right = 1
        elif x == (xMonRange - 1):
            left = -1
            right = 1
        elif x == 0:
            left = 1
            right = -1



def trainActiveMon(myMonStats, monsterBody):
    gc.collect()
    micropython.mem_info()
    thumby.display.fill(0)
    healthAmtTxt = (str(myMonStats['Health']) + '/' + str(myMonStats['maxHealth']))
    agileAmtTxt = (str(myMonStats['Agility']) + '/' + str(myMonStats['maxAgility']))
    strengthAmtTxt = (str(myMonStats['Strength']) + '/' + str(myMonStats['maxStrength']))
    enduranceAmtTxt = (str(myMonStats['Endurance']) + '/' + str(myMonStats['maxEndurance']))
    mystAmtTxt = (str(myMonStats['Mysticism']) + '/' + str(myMonStats['maxMysticism'])) 
    tinfoilAmtTxt = (str(myMonStats['Tinfoil']) + '/' + str(myMonStats['maxTinfoil']))
    trainingPointsTxt = ("TP: " + str(myMonStats['trainingPoints']))
    statNameList = ["Health", "Agility", "Strength", "Endurance", "Mysticism", "Tinfoil"]
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
        thingAquired(statNameList[currentSelect], statNumsList[currentSelect], trainingPointsTxt, myMonStats['given_name'], 0, 1)
        drawArrows(1, 1, -1, -1)
        tempSelect = currentSelect
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 28 or currentSelect == 29:
            currentSelect = tempSelect
        elif currentSelect == 30: 
            goBack = 1
        elif currentSelect == 31:
            currentSelect = tempSelect
            if myMonStats['trainingPoints'] > 0:
                if currentSelect == 0 and myMonStats['Health'] < myMonStats['maxHealth']: 
                    myMonStats['Health'] = myMonStats['Health'] + 1
                    myMonStats['currentHealth'] = myMonStats['Health']
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "health!", 2) 
                elif currentSelect == 1 and myMonStats['Agility'] < myMonStats['maxAgility']: 
                    myMonStats['Agility'] = myMonStats['Agility'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "agility!", 2)
                elif currentSelect == 2 or currentSelect == -4 and myMonStats['Strength'] < myMonStats['maxStrength']: 
                    myMonStats['Strength'] = myMonStats['Strength'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "strength!", 2)
                elif currentSelect == 3 or currentSelect == -3  and myMonStats['Endurance'] < myMonStats['maxEndurance']: 
                    myMonStats['Endurance'] = myMonStats['Endurance'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "endurance", 2)
                elif currentSelect == 4 or currentSelect == -2  and myMonStats['Mysticism'] < myMonStats['maxMysticism']: 
                    myMonStats['Mysticism'] = myMonStats['Mysticism'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "practiced", "their", "mysticism", 2)
                elif currentSelect == -1 and myMonStats['Tinfoil'] < myMonStats['maxTinfoil']: 
                    myMonStats['Tinfoil'] = myMonStats['Tinfoil'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "polished", "their", "tinfoil", 2)
                else:
                    thingAquired("Stat is", "already", "maxed out", "", 2)
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] + 1
                myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
            else:
                thingAquired("Not", "Enough", "Trainer", "Points", 2)
            thumby.display.update()
            goBack = 1
        thumby.display.update()


def giveName(beingNamed):
    capAlphabet = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z']
    character_list = [' ','a','b','c','d','e','f','g', 'h', 'i', 'j','k','l',
                        'm','n', 'o', 'p','q','r','s','t','u','v','w','x','y','z'] 
    selected_chars = beingNamed
    c = 1
    tempC = c
    goBack = 0
    addDelLtr2 = [0,124,18,18,124,0,0,40,40,40,40,0,124,84,84,0,120,16,8,120,0,124,68,68,56,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           8,28,42,8,8,8,0,20,20,20,20,0,62,34,34,28,0,62,42,42,0,62,32,32,0,62,42,42,0,2,62,2,0,62,42,42,0,0,0,0,
           4,4,4,21,14,4,0,10,10,10,10,0,31,5,5,31,0,31,17,17,14,0,31,17,17,14,0,0,31,16,16,1,31,1,0,31,9,9,22,0]
    while(goBack != 1):
        tempC = c
        c = showOptions(character_list, c, selected_chars, 0)
        thumby.display.drawFilledRectangle(8, 9, 72, 9, 0)
        thumby.display.blit(bytearray(addDelLtr2), 25, 3, 40, 21, -1, 0, 0)
        thumby.display.update()
        if c == 28:
            if len(selected_chars) == 0 or selected_chars[-1] == ' ':
                selected_chars = selected_chars + capAlphabet[tempC]
            else:
                selected_chars = selected_chars + character_list[tempC]
        elif c == 29:
            if len(selected_chars) > 0:
                selected_chars = selected_chars.rstrip(selected_chars[-1])
        elif c == 31:
            if len(selected_chars) > 0 :
                beingNamed = selected_chars
                goBack = 1
        if c >= 28:
            c = tempC
    return beingNamed


def optionScreen(playerInfo):
    if(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
        thumby.display.fill(0)
        gc.collect()
        curSelect = 1
        tempSelect = curSelect
        cancelCheck = 0
        optionList = ["My Info", "My Monsters", "Items", "Save", "Back"]
        subOptionsFriends = ["Swap Active", "Train", "Learn Attack", "Give Name", "Mutate", "Back"]
        while cancelCheck != 1:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            if curSelect == 28 or curSelect == 29:
                curSelect = tempSelect
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect == 31:
                curSelect = tempSelect
                if optionList[curSelect] == "My Info":
                    playerInformation(playerInfo)
                if optionList[curSelect] == "My Monsters":
                    goBack = 0
                    curSelect = 1
                    while(goBack != 1):
                        thumby.display.fill(0)
                        if curSelect == 28 or curSelect == 29:
                            curSelect = tempSelect
                        tempSelect = curSelect
                        curSelect = showOptions(subOptionsFriends, curSelect, "My Friends")
                        if curSelect == 31:
                            curSelect = tempSelect
                            if subOptionsFriends[curSelect] == "Swap Active":
                                showMonInfo(playerInfo)
                            if subOptionsFriends[curSelect] == "Train":
                                trainActiveMon(playerInfo.friends[0].statBlock, playerInfo.friends[0].bodyBlock)
                            if subOptionsFriends[curSelect] == "Learn Attack":
                                trainAnAttackMove(playerInfo.friends[0].attackList, playerInfo.friends[0].statBlock, playerInfo.friends[0].keyList)
                                while len(playerInfo.friends[0].attackList) > 6:
                                    popItOff(playerInfo.friends[0].attackList, "moves! Please forget one!")
                            if subOptionsFriends[curSelect] == "Give Name":
                                playerInfo.friends[0].statBlock['given_name'] = giveName(playerInfo.friends[0].statBlock['given_name'])
                            if subOptionsFriends[curSelect] == "Mutate":
                                playerInfo.friends[0].mutateMon()
                            if subOptionsFriends[curSelect] == "Back":
                                curSelect = 1
                                goBack = 1
                        if curSelect == 30:
                            curSelect = 1
                            goBack = 1
                        thumby.display.update()
                if optionList[curSelect] == "Items":
                    displayItems(playerInfo)
                if optionList[curSelect] == "Save":
                    save(playerInfo)
                    thingAquired("","Game","Saved","", 1, 0)
                if optionList[curSelect] == "Back": 
                    cancelCheck = 1
            if curSelect == 30:
                cancelCheck = 1
                thumby.display.fill(0)
            thumby.display.update()


def trainAnAttackMove(attackList, statBlock, keyList):
        gc.collect()
        howManyTypes = 0
        newAttack = AttackMove()
        attacksKnown = len(attackList)
        attackLearned = 0
        noAttacksToLearn = 0
        if statBlock['trainingPoints'] >= 3:
            for x in range(1,4):
                if statBlock[keyList[x]] != "":
                    howManyTypes = howManyTypes + 1
            while(attackLearned != 1):
                learnFromType = random.randint(1,howManyTypes)
                selectionNumber = random.randint(0, 3)
                newAttack.getAnAttackMove(selectionNumber, statBlock[keyList[learnFromType]])
                attackList.append(newAttack)
                noDupAtk(attackList)
                checkKnownAttacks = len(attackList)
                if attacksKnown != checkKnownAttacks:
                    attackLearned = 1
                    thingAquired(statBlock['given_name'], "learned", attackList[-1].name, "", 2)
                    statBlock['trainingPoints'] = statBlock['trainingPoints'] - 3
                    break
                noAttacksToLearn = noAttacksToLearn  + 1
                if noAttacksToLearn == 30:
                    thingAquired(statBlock['given_name'], "did not", "learn a", "new attack", 2)
                    break
        else:
            howManyPoints = statBlock['trainingPoints'] 
            thingAquired(statBlock['given_name'], ("needs " + str(3 - howManyPoints) + " more"), "Training", "Points", 2)
            
 
def tameMon(playerInfo, npcMon):
    gc.collect()
    newMon = Monster()
    newMon.statBlock = npcMon.statBlock.copy()
    newMon.bodyBlock = npcMon.bodyBlock.copy()
    newMon.attackList = npcMon.attackList.copy()
    newMon.mutateSeed = npcMon.mutateSeed.copy()
    if len(playerInfo.friends) >= playerInfo.playerBlock['friendMax']:
            popItOff(playerInfo.friends, "monsters, please let one go!")
    else: 
        playerInfo.friends.append(newMon)

 
def makeWorld(wSeed):
    gc.collect()
    random.seed(wSeed) 
    #worldSize = 25 
    worldList = []
    for i in range(0 , 25):
        newMap = Map()
        newMap.procGenMap()
        newMap.roomNumber = i + 1
        worldList.append(newMap)
    return worldList
    

def makeMonsterList(mSeed):
    gc.collect()
    random.seed(mSeed) 
    #numberOfMons = 25
    monsterList = []
    for i in range (0 , 25):
        newMon = Monster()
        newMon.makeMonster()
        monsterList.append(newMon)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,2), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,2), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(0,3), monsterList[i].statBlock['Type1'])
        monsterList[i].attackList.append(newMonAtk)
        noDupAtk(newMon.attackList)
        monsterList[i].makeMonBody()
    return monsterList
    

def makePlayer(monster1, monster2, monster3, seed):
    gc.collect()
    currentSelect = 0
    newPlayer = Player()
    thumby.display.fill(0)
    thingAquired("Press A", "to give", "your", "name!", 0)
    while(currentSelect != 31):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.playerBlock['name'] = giveName(newPlayer.playerBlock['name'])
    thumby.display.fill(0)
    thingAquired("Press A", "to pick", "your", "Monster!", 0)
    while(currentSelect != 31):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.friends.append(monster1)
    newPlayer.friends.append(monster2)
    newPlayer.friends.append(monster3)
    showMonInfo(newPlayer, 1)
    thumby.display.update()
    newPlayer.friends.pop()
    newPlayer.friends.pop()
    tameMon(newPlayer, newPlayer.friends[0])
    newPlayer.friends.pop(0)
    newItem = Item("Crystals", 3, random.randint(0,7))
    newPlayer.inventory.append(newItem)
    newPlayer.inventory.append(newItem)
    thingAquired("", "Good", "Luck", "", 2)
    newPlayer.worldSeed = seed 
    return newPlayer 
    

def thingAquired(word1, word2, itemName, word4 ="", setSleep=1, skipUpdate=0):
    thumby.display.fill(0)
    thumby.display.drawText(word1, math.floor(((72-(len(word1))*6))/2), 1, 1)
    thumby.display.drawText(word2, math.floor(((72-(len(word2))*6))/2), 10, 1)
    thumby.display.drawText(itemName, math.floor(((72-(len(itemName))*6))/2), 19, 1)
    thumby.display.drawText(word4, math.floor(((72-(len(word4))*6))/2), 28, 1)
    if skipUpdate == 0:
        thumby.display.update()
    time.sleep(setSleep)


def findAnItem(playerInv, maxItems):
    gc.collect()
    newItem = Item("GenHeal", 1)
    newItem.getItem()
    playerInv.append(newItem)
    thingAquired("You", "found", newItem.name, "", 2)
    if maxItems <= len(playerInv):
        popItOff(playerInv, "items! Please lose one.")


def makeTheList(theObj):
    gc.collect()
    makingAList = []
    if hasattr(theObj[0],  'statBlock') == True:
        for names in range(0, len(theObj)):
            makingAList.append(theObj[names].statBlock['given_name'])
    else:
        for names in range(0, len(theObj)):
            makingAList.append(theObj[names].name)
    return makingAList


def popItOff(theListofObjs, word):
    thumby.display.fill(0)
    gc.collect()
    myScroller = TextForScroller("Too many " + word)
    currentSelect = 0
    tempSelect = currentSelect
    origListLen = len(theListofObjs)
    listOfNames = makeTheList(theListofObjs)
    while(origListLen == len(theListofObjs)):
        tempSelect = currentSelect
        currentSelect = showOptions(listOfNames, currentSelect, "", 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        if currentSelect == 31:
            theListofObjs.pop(tempSelect)
        if currentSelect > 10:
            currentSelect = tempSelect
        thumby.display.update()


def printMon(monsterBody, x, y, playerOrNPC):
        thumby.display.blit(bytearray(monsterBody['head']), x, y, 20, 9, 0, playerOrNPC, 0)
        thumby.display.blit(bytearray(monsterBody['body']), x, y+9, 20, 9, 0, playerOrNPC, 0)
        thumby.display.blit(bytearray(monsterBody['legs']), x, y+18, 20, 9, 0, playerOrNPC, 0)

    
def trainAnimation(monsterBody):
    barbell2 = [124,254,255,255,253,253,251,230,124,24,56,48,56,24,56,56,48,56,24,56,48,124,254,255,255,253,253,251,230,124,
           0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0]
    t0 = 0
    ct0 = time.ticks_ms()
    while(t0 - ct0 < 3000):
        t0 = time.ticks_ms()
        bobRate = 250
        bobRange = 5
        bobOffset = math.sin(t0 / bobRate) * bobRange
        thumby.display.fill(0)
        printMon(monsterBody, 26, 12, 0)
        thumby.display.blit(bytearray(barbell2), 21, math.floor(5+bobOffset), 30, 9, 0, 0, 0)
        thumby.display.update()


def openScreen():
    myScroller = TextForScroller("Press A to Start or B to Load!")
    while(1):
        whatDo = 0
        thingAquired("Tiny", "Monster", "Trainer!", "", 0, 1)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        thumby.display.update()
        whatDo = buttonInput(whatDo)
        if whatDo == 31:
            battleStartAnimation(0)
            return 0
        elif whatDo == 30:
            try:
                f = open("tmt.json", "r")
                f.close()
            except OSError:
                battleStartAnimation(0)
                return 0
            battleStartAnimation(0)
            return 1

   
def obj_to_dict(obj):
    return obj.__dict__

def save(playerInfo):
    gc.collect()
    statDict = {}
    bodyDict = {}
    attackDict = {}
    mutateDict = {}
    itemDict = {}
    for x in range(0, len(playerInfo.friends)):
        tempAttackDict = {}
        for y in range (0, len(playerInfo.friends[x].attackList)):
            tempAttackDict['attack' + str(y)] = obj_to_dict(playerInfo.friends[x].attackList[y])
            attackDict['mon' + str(x) + 'atk'] = tempAttackDict
        statDict['mon' + str(x) + 'stat'] = playerInfo.friends[x].statBlock
        bodyDict['mon' + str(x) + 'body'] = playerInfo.friends[x].bodyBlock
        mutateDict['mon' + str(x) + 'mutate'] = playerInfo.friends[x].mutateSeed
    for x in range(0, len(playerInfo.inventory)):
        itemDict['item' + str(x)] = obj_to_dict(playerInfo.inventory[x])
    bigDict = [{'player' : playerInfo.playerBlock, 'items' : [itemDict], 'monsterInfo': [statDict, bodyDict, attackDict, mutateDict]}]
    with open('tmt.ujson', 'w') as f:
        ujson.dump(bigDict, f)
        f.close()

def loadGame():
    gc.collect()
    tempPlayer = Player()
    f = open('tmt.ujson')
    bigJson = ujson.load(f)
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
    if bigJson[0]['items'] != [{}]:
        for x in range(0, len(bigJson[0]['items'])):
            tempPlayer.inventory.append(Item(bigJson[0]['items'][0]['item' + str(x)]['name'], bigJson[0]['items'][0]['item' + str(x)]['key'], bigJson[0]['items'][0]['item' + str(x)]['bonus'])) ############# key, bonus=0
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


def makeRandomStats(monToStat, trainerLevel):
    random.seed(time.ticks_ms())
    tempMon = monToStat
    tempMon.statBlock = tempMon.statBlock.copy()
    genStat = tempMon.makeStat
    tempMon.statBlock['Health'] = genStat(0) + random.randint(0, trainerLevel)
    if tempMon.statBlock['Health'] > tempMon.statBlock['maxHealth']:
        tempMon.statBlock['Health'] = tempMon.statBlock['maxHealth']
    tempMon.statBlock['currentHealth'] = tempMon.statBlock['Health']
    for x in range (4,9):
        tempMon.statBlock[tempMon.keyList[x]] = genStat(0) + random.randint(0, trainerLevel)
        if tempMon.statBlock[tempMon.keyList[x]] > tempMon.statBlock['max' + tempMon.keyList[x]]:
            tempMon.statBlock[tempMon.keyList[x]] = tempMon.statBlock['max' + tempMon.keyList[x]]
    return tempMon

    
def makeRandomMon(monsterList, roomElm):
    random.seed(time.ticks_ms())
    spawnType = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    for x in range(0,10):
        thisGuyRightHere = monsterList[random.randint(0,24)]
        if (thisGuyRightHere.statBlock['Type1'] == spawnType[roomElm]
                or thisGuyRightHere.statBlock['Type2'] == spawnType[roomElm] 
                or thisGuyRightHere.statBlock['Type3'] == spawnType[roomElm]):
            thisGuyRightHere = makeRandomStats(thisGuyRightHere, 0)
            return thisGuyRightHere
    thisGuyRightHere = monsterList[random.randint(0,24)]
    thisGuyRightHere = makeRandomStats(thisGuyRightHere, 0)
    return thisGuyRightHere


def loss(curMon):
    curMon.statBlock['currentHealth'] = curMon.statBlock['Health']
    for attacks in range(0, len(curMon.attackList)):
        curMon.attackList[attacks-1].currentUses = curMon.attackList[attacks-1].numUses
    curMon.statBlock['trainingPoints'] = curMon.statBlock['trainingPoints'] - 1
    thingAquired(curMon.statBlock['given_name'], "is", "Disheartened", "TP lost", 2)

    
## Setting up the game ##

world=[]
monsterList=[]
myGuy = Player()
load = openScreen()
if load == 1: 
    myGuy = loadGame()
    world = makeWorld(myGuy.playerBlock['worldSeed'])
    monsterList = makeMonsterList(myGuy.playerBlock['worldSeed'])
else:
    theWorldSeed = time.ticks_us()
    random.seed(theWorldSeed)
    #print("World Seed = ", theWorldSeed)
    world = makeWorld(theWorldSeed)
    monsterList = makeMonsterList(theWorldSeed) 
    myGuy = makePlayer(monsterList[0],monsterList[1], monsterList[2], theWorldSeed)

npcMon = Monster()
activeMon = 0
room = math.ceil(25 / 2) # I guess i could just change this to 13
tempRoom = room
npcMonRoaming = RoamingMonster()
monsterMovement = 0
battle = 0
victory = 0

## Pretty much the game after this point :D ##

while(1):
    gc.collect() 
    #print(gc.mem_free())
    micropython.mem_info()
    micropython.qstr_info()
    while(battle != 1):
        thumby.display.fill(0)
        room = mapChangeCheck(myGuy, world[room], room)
        if tempRoom != room:
            npcMonRoaming.removeMonster()
            npcMonRoaming.placeMonster(world[room])
            tempRoom = room
            monsterMovement = random.randint(0,2)
        myGuy.movePlayer(world[room], npcMonRoaming, monsterMovement)
        npcMonRoaming.drawMonster()
        myGuy.drawPlayer()
        optionScreen(myGuy)
        thumby.display.update()
        if myGuy.currentPos == npcMonRoaming.currentPos:
            npcMonRoaming.removeMonster()
            battle = 1
            battleStartAnimation(1)
    npcMon = makeRandomMon(monsterList, world[room].elementType)
    battleMon = makeRandomStats(npcMon, myGuy.playerBlock['trainerLevel'])
    while(battle == 1):
        victory = 0
        thumby.display.fill(0)
        victory = battleScreen(myGuy.friends[activeMon], battleMon, myGuy.playerBlock['trainerLevel'], (myGuy.playerBlock['trainerLevel'] + random.randrange(-2,2)))
        autoSwitchMon(myGuy)
        if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
            battle = 0
            loss(myGuy.friends[random.randint(0, len(myGuy.friends) - 1)])
        if npcMon.statBlock['currentHealth'] == 0:
            battle = 0
        if victory == 2:
            if len(myGuy.inventory) > 0:
                for things in range(0, len(myGuy.inventory)):
                    if myGuy.inventory[things-1].name == "Crystals":
                        if (random.randint(0,20) + myGuy.inventory[things-1].bonus + myGuy.playerBlock['trainerLevel']) > 15: 
                            gc.collect()
                            tameMon(myGuy, npcMon)
                            myGuy.friends[-1].statBlock['currentHealth'] = myGuy.friends[-1].statBlock['Health']
                            thingAquired(npcMon.statBlock['name'], "was", "Tamed!", "<3", 3)
                            myGuy.inventory.pop(things-1)
                            battle = 0
                            break
                        else:
                            thingAquired("Crystal", "Used,", "Not", "Tamed", 2)
                            myGuy.inventory.pop(things-1)
                            break
                    else:
                        thingAquired("You don't", "have any", "Taming", "Crystals", 2) 
            else:
                thingAquired("You don't", "have any", "Taming", "Crystals", 2)
        if victory == 4:
            showMonInfo(myGuy)
            victory = 0
        thumby.display.update()
    battleStartAnimation(0) 
    if victory == 1:
        myGuy.levelUpCheck()
        myGuy.friends[0].statBlock['trainingPoints'] = myGuy.friends[0].statBlock['trainingPoints'] + 1
        if len(myGuy.inventory) < myGuy.maxHelditems:
            randoNum = random.randint(1,10)
            if randoNum > 3:
                findAnItem(myGuy.inventory, myGuy.maxHelditems)
