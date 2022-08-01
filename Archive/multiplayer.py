import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Map, Monster, Tile, RoamingMonster, TextForScroller, Item, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, obj_to_dict, save, drawArrows, showOptions, popItOff, buttonInput, noDupAtk, giveName, switchActiveMon, showMonInfo
#import micropython


def loadGame():
    gc.collect()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson')
    bigJson = ujson.load(f)
    f.close()
    return bigJson


def putGuyTogether(bigJson):
    tempPlayer = Player()
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
    return tempPlayer

    
def waitingForResponse(loadingStr, whatDoing):                
    thingAquired(whatDoing, "", "othr trainer!", loadingStr,0,0,0)
    loadingStr = loadingStr + "."
    if loadingStr == "...":
        loadingStr = ""
    return loadingStr
    
    
myGuy = Player()
yourGuy = Player()
yourGuyJson = {}
myGuyBattleJson = loadGame()
loadingStr = ""
myGuy = putGuyTogether(myGuyBattleJson)
sentAndRcvd = 0
justMyGuy = myGuyBattleJson[0]['player']


rcvCheckPlayer = {'key0' : {}}
sendCheckPlayer = {'key0' : {}}

rcvCheck = {'key0' : 0}
sendCheck = {'key0' : 0}

dataBeingSent = [{},{},{}]
dataBeingRcvd = [{},{},{}]
checkCheck = bytearray([0]) 
checkCheckOther = bytearray([0]) 

dataToSend=[{}]

keyList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil','head', 'body','legs']

for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
    for y in range(0,14):
        rcvCheck['key' + str(y+(x*14))] =  0 
        thingAquired("rcvCheck", "key" + str(y+(x*14)) + " = ", str(rcvCheck['key' + str(y+(x*14))]), "",0,0,0)
        checkCheck[0] = checkCheck[0] + 1
        thingAquired("checkCheck",str(checkCheck[0]),str(rcvCheck['key' + str(y+(x*3))]),"",0,0,0)
    y=0
    if x > 0:
        print(dataToSend)
        dataToSend.append({})
        print(dataToSend)
    dataToSend[x]['name'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['name']
    dataToSend[x]['given_name'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['given_name']
    dataToSend[x]['Health'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Health']
    dataToSend[x]['Type1'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type1']
    dataToSend[x]['Type2'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type2']
    dataToSend[x]['Type3'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type3']
    dataToSend[x]['Agility'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Agility']
    dataToSend[x]['Strength'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Strength']
    dataToSend[x]['Endurance'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Endurance']
    dataToSend[x]['Mysticism'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Mysticism']
    dataToSend[x]['Tinfoil'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Tinfoil']
    dataToSend[x]['head'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['head']
    dataToSend[x]['body'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['body']
    dataToSend[x]['legs'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['legs']
x=0
print(dataToSend)


currentSelect = 0
thumby.display.setFPS(40)

#add a while that will send and receive a random number then after a received 
# a number start a timer that will continue to send until timer is done
#then after both thumbys have received a random number, compair that number to see
#which one will send first and which one will receive first
t0 = 0
handshakeTimer = 0
random.seed(time.ticks_ms())
whoSendsFirst = bytearray([0]) 
whoSendsFirst[0] = random.randint(1, 255)
whoSendsFirstRcvd = bytearray([0]) 

thingAquired("Send / Rcv", str(whoSendsFirst[0]), "", "",1,0,0)

timerTrigger = 0

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
            if whoSendsFirst[0] == whoSendsFirstRcvd[0]:
                whoSendsFirst[0] = random.randint(1, 255)
                

if whoSendsFirst[0] >= whoSendsFirstRcvd[0]:
    currentSelect = 31
else:
    currentSelect = 30
    
rcvCheckPlayer['key0'] = 0
sendCheckPlayer['key0'] = 0
print(rcvCheckPlayer, " again")

time.sleep(.5)
try:
    while (sentAndRcvd == 0):
        if currentSelect == 31:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "1 Sending to") # was getting passed this, dunno what i did
                thumby.link.send(ujson.dumps(justMyGuy).encode())
                received = thumby.link.receive()
                if received != None:
                    rcvCheckPlayer = ujson.loads(received.decode())
                    sentAndRcvd = sentAndRcvd + 1
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 0
                        print("Rcv check did not = 1, in while == 0")
        if currentSelect == 30:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "1 Receiving")
                sendCheckPlayer['key0'] = 1
                received = thumby.link.receive()
                if received != None:
                    yourGuyJson = ujson.loads(received.decode())
                    thumby.link.send(ujson.dumps(sendCheckPlayer).encode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 1
                        sentAndRcvd = sentAndRcvd + 1
                        print("Rcv check did not = 1, in while == 0 for rcv loop")
except Exception as e:
    f = open("/Games/Tiny_Monster_Trainer/crash6.log", "w")
    f.write(str(e) + " Line 120 ish ")
    f.close()    


if currentSelect == 30:
    currentSelect = 31
else:
    currentSelect = 30 
    
sentAndRcvd = 0
rcvCheckPlayer['key0'] = 0
sendCheckPlayer['key0'] = 0

while(sentAndRcvd == 0): 
    if currentSelect == 31:
        while(rcvCheckPlayer['key0'] == 0):
            loadingStr = waitingForResponse(loadingStr, "2 Sending to")
            thumby.link.send(ujson.dumps(justMyGuy).encode())
            received = thumby.link.receive()
            if received != None:
                rcvCheckPlayer = ujson.loads(received.decode())
                sentAndRcvd = sentAndRcvd + 1
                if rcvCheckPlayer['key0'] != 1:
                    rcvCheckPlayer['key0'] = 0
                    print("Rcv check did not = 1, in while == 0")
    if currentSelect == 30:
        while(rcvCheckPlayer['key0'] == 0):
            loadingStr = waitingForResponse(loadingStr, "2 Receiving")
            sendCheckPlayer['key0'] = 1
            received = thumby.link.receive()
            if received != None:
                yourGuyJson = ujson.loads(received.decode())
                thumby.link.send(ujson.dumps(sendCheckPlayer).encode())
                if rcvCheckPlayer['key0'] != 1:
                    rcvCheckPlayer['key0'] = 1
                    sentAndRcvd = sentAndRcvd + 1
                    print("Rcv check did not = 1, in while == 0 for rcv loop")                    
                    
                    

thingAquired(justMyGuy['name'], "vs.", yourGuyJson['name'], "yay!",1,0,0)

t0 = 0
handshakeTimer = 0
timerTrigger = 0
while(t0 - handshakeTimer < 300):
    if timerTrigger == 1:
        t0 = time.ticks_ms()
    loadingStr = waitingForResponse(loadingStr, "Monsters to")

    thumby.link.send(checkCheck)
    received5 = thumby.link.receive()
    
    if received5 != None:
        if handshakeTimer == 0:
            checkCheckOther = received5
            handshakeTimer = time.ticks_ms()
            timerTrigger = 1
            
thingAquired(str(checkCheck[0]), "check vs othr", str(checkCheckOther[0]), "yay!!",1,0,0)
for x in range(0, checkCheckOther[0]):
    sendCheck['key' + str(x)] =  0
    thingAquired("sendCheck", "key" + str(x) + " = ", str(sendCheck['key' + str(x)]), "",0,0,0)
x = 0

if whoSendsFirst[0] >= whoSendsFirstRcvd[0]:
    currentSelect = 31
else:
    currentSelect = 30
'''    
dataToRcv = [{'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              },
              {'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              },
              {'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              },
              {'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              },
              {'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              },
              {'name': "",
              'given_name': "",
              'Health' : 0,
              'Type1' : "",
              'Type2' : "",
              'Type3' : "",
              'Agility' : 0,
              'Strength' : 0,
              'Endurance' : 0,
              'Mysticism' : 0,
              'Tinfoil' : 0,
              'head' : [],
              'body' : [],
              'legs' : []
              }]'''


#put thing in dictionary, send to otherside # break up send into ints and other stuff, send ints first, then send other stuff?
for z in range(0,2): # need to reset key checks, i think
    if currentSelect == 31:
        for x in range (0, (checkCheck[0]/14)): 
            for y in range (0, 14):
                dictToSend = {}
                dictToRcv = {}
                while rcvCheck['key' + str(y+(x*14))] == 0: # need to check that key is right
                    
                    #loadingStr = waitingForResponse(loadingStr, "Sending M to")
                    dictToSend['key'] = y
                    dictToSend['key2'] = y+(x*14)
                    dictToSend[keyList[y]] = dataToSend[x][keyList[y]]
                    thumby.link.send(ujson.dumps(dictToSend).encode()) 
                    received1 = thumby.link.receive()
                    f = open("/Games/Tiny_Monster_Trainer/log1.log", "w")
                    f.write( " Line 350 ish " + str(dictToSend) +  ",,  urguy " + str(yourGuyJson) + " ,,, myguy " + str(justMyGuy))
                    f.close()
                    dictToSend.pop(keyList[y])
                    f = open("/Games/Tiny_Monster_Trainer/log2.log", "w")
                    f.write( " Line 350 ish " + str(dictToSend) +  ",,  urguy " + str(yourGuyJson) + " ,,, myguy " + str(justMyGuy))
                    f.close()
                    thingAquired(str(x), str(y), "x, y", "send ", 0, 0, 0)
                    
                    if received1 != None:
                        try:
                            dictToRcv = ujson.loads(received1.decode())
                            if dictToRcv['key2'] != dictToSend['key2']:
                                rcvCheck['key'+str(y+(x*14))] = 1 
                        except Exception as e:
                            f = open("/Games/Tiny_Monster_Trainer/crash1.log", "w")
                            f.write(str(e) + " Line 247 ish " + str(dictToRcv) +  ",,   " + str(received1) + ",,  " + str(dictToSend))
                            f.close()
            y=0
        x=0
    if currentSelect == 30:
        for x in range (0, (checkCheckOther[0]/14)): #+1? -1?
            for y in range (0, 14):
                dictToSend = {}
                dictToRcv = {}
                while sendCheck['key' + str(y+(x*14))] == 0: # need to check that key is right
                    #loadingStr = waitingForResponse(loadingStr, "Receiving M")
                    dictToSend['key'] = y
                    dictToSend['key2'] = y+(x*14)
                    thumby.link.send(ujson.dumps(dictToSend).encode())
                    #['key'] = y+(x*14)
                    received2 = thumby.link.receive()
                    thingAquired(str(x), str(y), "x, y", "rcv ", 0, 0, 0)
                    if received2 != None: # need to check that key is right
                        try:
                            dictToRcv = ujson.loads(received2.decode())
                            if dictToRcv['key2'] == dictToSend['key2']:
                                dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[y]]
                                sendCheck['key' + str(y+(x*3))] = 1
                        except Exception as e:
                            f = open("/Games/Tiny_Monster_Trainer/crash45.log", "w")
                            f.write(str(e) + " Line 380 ish x=" + str(x) +  ",,   y= " + str(y))
                            f.close()
                if y == 13:
                    dictToSend['key'] = y + 1
                    dictToSend['key2'] = y+(x*14)+1
                    thumby.link.send(ujson.dumps(dictToSend).encode())
                            
            y=0            
        x=0                
    if currentSelect == 30:
        currentSelect = 31
    else:
        currentSelect = 30 
    thingAquired("", "switch", "over", "", 0, 0, 0)
    time.sleep(3)
    
thingAquired("out", "of", "send/rcv", "loops", 0, 0, 0)   
   
while (1):
    thingAquired(justMyGuy['name'], "vs.", yourGuyJson['name'], "yay!!",1,0,0)
    thingAquired(dataToSend[0]['given_name'], "vs.", dataBeingRcvd[0]['given_name'], "yay!!",1,0,0)
    thumby.display.fill(0)
    thumby.display.blit(bytearray(dataToSend[0]['head']), 10, 10, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(dataToSend[0]['body']), 10, 10+9, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(dataToSend[0]['legs']), 10, 10+18, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(dataBeingRcvd[0]['head']), 40, 10, 20, 9, 0, 1, 0)
    thumby.display.blit(bytearray(dataBeingRcvd[0]['body']), 40, 10+9, 20, 9, 0, 1, 0)
    thumby.display.blit(bytearray(dataBeingRcvd[0]['legs']), 40, 10+18, 20, 9, 0, 1, 0)
    thumby.display.update() 
    time.sleep(2)
       
    
'''        


ujson.loads(received.decode())

except Exception as e:
    f = open("/Games/Tiny_Monster_Trainer/crash.log", "w")
    f.write(str(e))
    f.close() '''



    
    
    