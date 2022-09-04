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


def getKeyList(whatList=0):
    if whatList == 1:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil','head', 'body','legs']
    elif whatList == 2:
        thisList = ['monster', 'name', 'numUses', 'baseDamage', 'magic', 'moveElementType']
    elif whatList == 3:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil'] #,'head', 'body','legs']        
    elif whatList == 4: 
        thisList = ['head', 'body','legs'] 
    else:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil','head', 'body','legs']
    return thisList


def waitingForResponse(loadingStr, whatDoing):                
    thingAquired(whatDoing, "", "othr trainer!", loadingStr,0,0,0)
    loadingStr = loadingStr + "."
    if loadingStr == "...":
        loadingStr = ""
    return loadingStr


def getNumberOfKeyChecks(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheck = bytearray([0]) 
    myGuyBattleJson = loadGame()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0,rangeNum):
            rcvCheck['key' + str(y+(x*rangeNum))] =  0 
            thingAquired("rcvCheck", "key" + str(y+(x*rangeNum)) + " = ", str(rcvCheck['key' + str(y+(x*rangeNum))]), "",0,0,0)
            checkCheck[0] = checkCheck[0] + 1
            thingAquired("checkCheck",str(checkCheck[0]),str(rcvCheck['key' + str(y+(x*rangeNum))]),"",0,0,0)
        y=0
        '''if x > 0:
            #print(dataToSend)
            dataToSend.append({})
            print(dataToSend)'''
    if rcvCheckOrCheck == 0:
        return checkCheck
    elif rcvCheckOrCheck == 1:
        return rcvCheck


#make sure moves are chopped up right, check how data looks in logs 15 & 16 to compare structure

def chopUpGuyToSend():
    dataToSend=[{}]
    myGuyBattleJson = loadGame()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        if x > 0:
            dataToSend.append({})  # for data to send, might be able to go to the def with the list names and cycle through those to make this smaller
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
    #f = open("/Games/Tiny_Monster_Trainer/log16.log", "w")
    #f.write( " Line 117 ish " + str(dataToSend) + "  x:" + str(x))
    #f.close()  
    return dataToSend

    
def chopUpMovesToSend():   
    dataToSend=[{}]
    myGuyBattleJson = loadGame()
    numberOfAtks = 0
    try:
        for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
            for y in range(0, len(myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
                if y == 0 and x == 0:
                    pass
                else:
                    dataToSend.append({})
                dataToSend[numberOfAtks]['monster'] =  x  
                dataToSend[numberOfAtks]['name'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'] 
                dataToSend[numberOfAtks]['numUses'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses']
                dataToSend[numberOfAtks]['baseDamage'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage']
                dataToSend[numberOfAtks]['magic'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic']
                dataToSend[numberOfAtks]['moveElementType'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType']
                numberOfAtks = numberOfAtks + 1
        #f = open("/Games/Tiny_Monster_Trainer/log15.log", "w")
        #f.write( " Line 117 ish " + str(dataToSend) + "  x:" + str(x) + "  y:" + str(y))
        #f.close()
    except Exception as e:
            f = open("/Games/Tiny_Monster_Trainer/crashChop.log", "w")
            f.write(str(e) + " on Line 131 ish")
            f.close()  
    return dataToSend
    

def getNumberOfKeyChecksMoves(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheckM = bytearray([0]) 
    myGuyBattleJson = loadGame()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0, len(myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])):
            for z in range(0,rangeNum):
                checkCheckM[0] = checkCheckM[0] + 1
                rcvCheck['key' + str(checkCheckM[0])] =  0
                #old way: rcvCheck['key' + str(z+(x*rangeNum)+(y*rangeNum))] =  0 
                # old way: thingAquired("rcvCheck", "key" + str(z+(x*rangeNum)+(y*rangeNum)) + " = ", str(rcvCheck['key' + str(z+(x*rangeNum)+(y*rangeNum))]), "",0,0,0)
                # old way: checkCheckM[0] = checkCheckM[0] + 1
                #thingAquired("checkCheck",str(checkCheck[0]),str(rcvCheck['key' + str(y+(x*3))]),"",0,0,0)
            z=0
        y=0
        '''if x > 0:
            print(dataToSend)
            dataToSend.append({})
            print(dataToSend)'''
    #f = open("/Games/Tiny_Monster_Trainer/checksM.log", "w")
    #f.write(str(checkCheckM[0]) + " on Line 142 ish " + str(rcvCheck))
    #f.close() 
    if rcvCheckOrCheck == 0:
        return checkCheckM
    elif rcvCheckOrCheck == 1:
        return rcvCheck    

#def chopUpMovesToSend --- add function to grab moves from monster

def findWhoSendsFirst():
    t0 = 0
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


def sendOrReceiveGuy(sOr):   
    yourGuyJson = {}
    loadingStr = ""
    rcvCheckPlayer = {'key0' : {}}
    sendCheckPlayer = {'key0' : {}}
    rcvCheckPlayer['key0'] = 0 
    sendCheckPlayer['key0'] = 0
    myGuyBattleJson = loadGame()
    justMyGuy = myGuyBattleJson[0]['player']
    del myGuyBattleJson
 
    for z in range(0,2):
        if sOr == 1:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, str(z) + " Sending to") 
                thumby.link.send(ujson.dumps(justMyGuy).encode())
                received = thumby.link.receive()
                if received != None:
                    rcvCheckPlayer = ujson.loads(received.decode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 0
                        print("Rcv check did not = 1, in while == 0")
        if sOr == 0:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, str(z) + " Receiving")
                sendCheckPlayer['key0'] = 1
                received1 = thumby.link.receive()
                if received1 != None:
                    yourGuyJson = ujson.loads(received1.decode())
                    thumby.link.send(ujson.dumps(sendCheckPlayer).encode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 1
        rcvCheckPlayer['key0'] = 0
        if sOr == 0:
            sOr = 1
        else:
            sOr = 0 
    return yourGuyJson
                      

def sendCheckAndGetCheck(checkCheckNum):
    t0 = 0
    handshakeTimer = 0
    timerTrigger = 0
    loadingStr = ""
    checkCheckOther = bytearray([0])
    while(t0 - handshakeTimer < 300):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Checks")
    
        thumby.link.send(checkCheckNum)
        received = thumby.link.receive()
        
        if received != None:
            if handshakeTimer == 0:
                checkCheckOther = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
    return checkCheckOther
                        

# once it goes to x = 1 data is not being sent, make it print what it's trying to send    
def sendAndReceive(dataToSend, checkCheck, checkCheckOther, sendOrReceive, rcvCheckNum, numOfData=0, listNumber=0):

    keyList = getKeyList(listNumber)
    sendCheck = {'key0' : 0}
    dataBeingRcvd = [{}]
    xSame = 0
    
    for c in range(0, (checkCheckOther[0])):
        sendCheck['key' + str(c)] =  0
        thingAquired("sendCheck", "key" + str(c) + " = ", str(sendCheck['key' + str(c)]), "",0,0,0)
    for z in range(0,2):
        #x = 0 #?
        #y = 0 #?
        if sendOrReceive == 1:
            for x in range (0, ((checkCheck[0])/numOfData)): 
                for y in range (0, numOfData):
                    dictToSend = {}
                    dictToRcv = {}
                    while rcvCheckNum['key' + str(y+(x*numOfData))] == 0: # need to check that key is right
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        dictToSend[keyList[y]] = dataToSend[x][keyList[y]] #this is where the data I care about is being sent
                        thumby.link.send(ujson.dumps(dictToSend).encode()) 
                        received1 = thumby.link.receive()
                        dictToSend.pop(keyList[y])
                        
                        if received1 != None:
                            try:
                                dictToRcv = ujson.loads(received1.decode())
                                thingAquired(str(x) + " " + str(y) + " " + str(y+(x*numOfData)) + " send.",  str(dictToSend['key']) + " " + str(dictToSend['key2']) + " " + str(dictToRcv['key2']) , "x*y,k,k2,sk2", "rcvChk" + str(y+(x*numOfData)) + " " + str(rcvCheckNum['key' + str(y+(x*numOfData))]), 0, 0, 0)                                            
                                if dictToRcv['key2'] != dictToSend['key2']: #if key2 isn't different, don't advance rcvCheckNum so that it'll keep trying to send the same information to the other thumby
                                    rcvCheckNum['key'+str(y+(x*numOfData))] = 1 #if key2 is different advance change it to once so that the while ends and the x/y loops can adv
                                    thingAquired(str(x) + " " + str(y) + " " + str(y+(x*numOfData)) + " send",  str(dictToSend['key']) + " " + str(dictToSend['key2']) + "v" + str(dictToRcv['key2']) , "x*y,k,k2,sk2", "rcvChk" + str(y+(x*numOfData)) + " " + str(rcvCheckNum['key' + str(y+(x*numOfData))]), 0, 0, 0)                                            
                                    #time.sleep(.5)
                                #thingAquired(str(x) + " " + str(y) + " " + str(y+(x*numOfData)) + " send",  str(dictToSend['key']) + " " + str(dictToSend['key2']) + "v" + str(dictToRcv['key2']) , "x*y,k,k2,sk2", "rcvChk" + str(y+(x*numOfData)) + " " + str(rcvCheckNum['key' + str(y+(x*numOfData))]), 0, 0, 0)                                            
                            except:
                                pass
                y=0
            x=0
        # rcvCheckNum['key' + str(y+(x*numOfData))] is staying at 0 after x goes to 1, not 
        sendLoopExit = math.ceil((checkCheckOther[0])/numOfData)
        if sendOrReceive == 0:
            for x in range (0, ((checkCheckOther[0])/numOfData)): #+1? -1?
                for y in range (0, numOfData):
                    dictToSend = {} 
                    dictToRcv = {}
                    while sendCheck['key' + str(y+(x*numOfData))] == 0: # need to check that key is right
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        thumby.link.send(ujson.dumps(dictToSend).encode())
                        received2 = thumby.link.receive()
                        if received2 != None: 
                            try:   #dictToRcv['key2'] == dictToSend['key2'] == the same, y no change?
                                dictToRcv = ujson.loads(received2.decode())
                                thingAquired("rcv. " + str(x) + " " + str(y) + " " + str(y+(x*numOfData)), str(dictToRcv['key']) + " " + str(dictToRcv['key2']) + " " + str(dictToSend['key2']), "x*y,k,k2,sk2", "sendChk" + str(y+(x*numOfData)) + " " + str(sendCheck['key' + str(y+(x*numOfData))]), 0, 0, 0)
                                if dictToRcv['key2'] == dictToSend['key2']:
                                    if x > 0 and xSame != x+y:                                    
                                        dataBeingRcvd.append({})
                                        xSame = x+y
                                    dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[dictToRcv['key']]] #original line: dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[y]]
                                    sendCheck['key' + str(y+(x*numOfData))] = 1
                                    thingAquired("rcv " + str(x) + " " + str(y) + " " + str(y+(x*numOfData)), str(dictToRcv['key']) + " " + str(dictToRcv['key2']) + "v" + str(dictToSend['key2']), "x*y,k,k2,sk2", "sendChk" + str(y+(x*numOfData)) + " " + str(sendCheck['key' + str(y+(x*numOfData))]), 0, 0, 0)
                                    adjustment = len(dataBeingRcvd)
                                    for m in range(0, len(dataBeingRcvd)):
                                        try:
                                            if dataBeingRcvd[m] == {}:
                                                dataBeingRcvd.pop(m)
                                        except:
                                            pass
                                    #time.sleep(.5)
                                #thingAquired("rcv " + str(x) + " " + str(y) + " " + str(y+(x*numOfData)), str(dictToRcv['key']) + " " + str(dictToRcv['key2']) + "v" + str(dictToSend['key2']), "x*y,k,k2,sk2", "sendChk" + str(y+(x*numOfData)) + " " + str(sendCheck['key' + str(y+(x*numOfData))]), 0, 0, 0)
                            except Exception as e:
                                f = open("/Games/Tiny_Monster_Trainer/Rcv2.log", "w")
                                f.write(str(e) + " on Line 323 ish " + str(dictToRcv) + " " + str(dictToRcv['key']) + " " + str(dictToRcv['key2']))
                                f.close() 
                #maybe try this one more time? 8-30-22
                if y == (numOfData - 1) and x == (sendLoopExit - 1):
                    dictToSend['key2'] = (y+(x*numOfData)+1)
                    thumby.link.send(ujson.dumps(dictToSend).encode())
                    #thingAquired("in end of","y if","","",0,0,0)
                    #time.sleep(1)
                #thingAquired("out of y","","","",0,0,0)
                #time.sleep(.1)
                y=0
            x=0
        if sendOrReceive == 0:
            sendOrReceive = 1
        else:
            sendOrReceive = 0 
        thingAquired("", "switch", "over", "", 1, 0, 0)
        #time.sleep(1)
    thingAquired("out", "of", "send/rcv", "loops", 1, 0, 0)
    return dataBeingRcvd
    

def putGhostTogether(otrMonData, otrMonMoves, yourGuyJson):
    monKeys = getKeyList(3)
    bodKeys = getKeyList(4)
    opponent = Player()
    opponent.playerBlock['name'] = yourGuyJson['name']
    opponent.playerBlock['trainerLevel'] = yourGuyJson['trainerLevel']
    opponent.playerBlock['experience'] = yourGuyJson['experience']
    opponent.playerBlock['friendMax'] = yourGuyJson['friendMax']
    opponent.playerBlock['worldSeed'] = yourGuyJson['worldSeed']
    for x in range(0, len(otrMonData)):
        rezMon = Monster()
        for y in range(0, len(monKeys)):
            monKeys = getKeyList(1)
            rezMon.statBlock[monKeys[y]] = otrMonData[x][monKeys[y]]
        for b in range(0, len(bodKeys)):
            rezMon.bodyBlock[bodKeys[b]] = otrMonData[x][bodKeys[b]]
        for z in range(0, len(rcvOtrMonMoves)):
            if rcvOtrMonMoves[z]['monster'] == x:
                tempAttackMove = AttackMove(otrMonMoves[z]['name'],
                                    otrMonMoves[z]['numUses'],
                                    otrMonMoves[z]['baseDamage'],
                                    otrMonMoves[z]['magic'],
                                    otrMonMoves[z]['moveElementType'])
                tempAttackMove.currentUses = otrMonMoves[z]['numUses']
                rezMon.attackList.append(tempAttackMove) 
        rezMon.attackList = rezMon.attackList.copy()
        opponent.friends.append(rezMon)
        opponent.friends = opponent.friends.copy()
        
    saveGhost(opponent)    
        

def saveGhost(ghostInfo):
    gc.collect()
    statDict = {}
    bodyDict = {}
    attackDict = {}

    for x in range(0, len(ghostInfo.friends)):
        tempAttackDict = {}
        for y in range (0, len(ghostInfo.friends[x].attackList)):
            tempAttackDict["attack" + str(y)] = obj_to_dict(ghostInfo.friends[x].attackList[y])
            attackDict["mon" + str(x) + "atk"] = tempAttackDict
        statDict["mon" + str(x) + "stat"] = ghostInfo.friends[x].statBlock
        bodyDict["mon" + str(x) + "body"] = ghostInfo.friends[x].bodyBlock
    playerDict = [{"player" : ghostInfo.playerBlock, "monsterInfo": [statDict, bodyDict, attackDict]}]
    with open('/Games/Tiny_Monster_Trainer/Ghosts/'+ghostInfo.playerBlock['name']+'.ujson', 'w') as f:
        ujson.dump(playerDict, f)
        f.close()
    del playerDict
    gc.collect()            
    
    




thingAquired("about to send", " ", "Monsters", "", 2,0,0)    
checkCheck1 = bytearray([0]) 
checkCheck1 = getNumberOfKeyChecks(0, 14)
rcvCheck1 = {'key0' : 0} 
rcvCheck1 = getNumberOfKeyChecks(1, 14)
#f = open("/Games/Tiny_Monster_Trainer/rcvCheck1.log", "w")
#f.write(str(rcvCheck1) + " on Line 349 ish")
#f.close() 

    
dataToSend =  chopUpGuyToSend()   
#thumby.display.setFPS(40) dunno if i need to do this, may delete later

sendOrReceive2 = findWhoSendsFirst() #original place for sendOrReceive
#thingAquired("sendOrReceive", " = ", str(sendOrReceive), "", 0,0,0) just used for debugging, can be deleted later
#time.sleep(1) crashed once, worked 4 other times, watch and see if a delay is needed here.
yourGuyJson = {}
yourGuyJson = sendOrReceiveGuy(sendOrReceive2)    
thingAquired("Hi!!", yourGuyJson['name'] , "", "", 0, 0, 0)




checkCheckOther1 = sendCheckAndGetCheck(checkCheck1)
 
try:
    time.sleep(1)
    #rcvOtrMonData = [{},{},{}]
    rcvOtrMonData = sendAndReceive(dataToSend, checkCheck1, checkCheckOther1, sendOrReceive2, rcvCheck1,  14, 1)    
except Exception as e:
        f = open("/Games/Tiny_Monster_Trainer/crash48.log", "w")
        f.write(str(e) + " on Line 307 ish")
        f.close()  
    

### v- sending moves -v

time.sleep(1)
checkCheck2 = bytearray([0]) 
checkCheck2 = getNumberOfKeyChecksMoves(0, 6)
thingAquired("checkCheck2", " = ", str(checkCheck2[0]), "", 2,0,0) 
rcvCheck2 = {'key0' : 0} 
rcvCheck2 = getNumberOfKeyChecksMoves(1, 6)
thingAquired("rcvCheck2", " = ", str(rcvCheck2['key0']), "", 2,0,0)
#f = open("/Games/Tiny_Monster_Trainer/rcvCheck2.log", "w")
#f.write(str(rcvCheck2) + " on Line 382 ish")
#f.close() 
dataToSend2 =  chopUpMovesToSend()  
thingAquired("dataToSend[0]['name']", " = ", dataToSend[0]['name'], "", 2,0,0)
#sendOrReceive1 = findWhoSendsFirst()
#try:
checkCheckOther2 = sendCheckAndGetCheck(checkCheck2)
thingAquired("checkCheckOther2", " = ", str(checkCheckOther2[0]), "", 2,0,0) 
#except Exception as e:
'''f = open("/Games/Tiny_Monster_Trainer/crashB.log", "w")
f.write(str(e) + " on Line 333 ish" + str(rcvCheck2))
f.close()'''  
        
time.sleep(1)        

#thingAquired("sendOrReceive1", " = ", str(sendOrReceive1), "", 2,0,0)
try:
    thingAquired("about to send", " ", "Moves", "", 2,0,0)    
    rcvOtrMonMoves = sendAndReceive(dataToSend2, checkCheck2, checkCheckOther2, sendOrReceive2, rcvCheck2, 6, 2)
except Exception as e:
    f = open("/Games/Tiny_Monster_Trainer/crashA.log", "w")
    f.write(str(e) + " on Line 336 ish")
    f.close() 



#while(1):
#print(checkCheck[0], " ", rcvCheck['key12'])
#print(sendOrReceive)
thingAquired("Hi!", yourGuyJson['name'] , "", "", 0, 0, 0)
try:
    thingAquired("Hi!", yourGuyJson['name'] , rcvOtrMonData[0]['name'], rcvOtrMonMoves[0]['name'], 1, 0, 0)
    thumby.display.fill(0)
    thumby.display.blit(bytearray(dataToSend[0]['head']), 10, 10, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(dataToSend[0]['body']), 10, 10+9, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(dataToSend[0]['legs']), 10, 10+18, 20, 9, 0, 0, 0)
    thumby.display.blit(bytearray(rcvOtrMonData[0]['head']), 40, 10, 20, 9, 0, 1, 0)
    thumby.display.blit(bytearray(rcvOtrMonData[0]['body']), 40, 10+9, 20, 9, 0, 1, 0)
    thumby.display.blit(bytearray(rcvOtrMonData[0]['legs']), 40, 10+18, 20, 9, 0, 1, 0)
    thumby.display.update()
    time.sleep(1)
    f = open("/Games/Tiny_Monster_Trainer/DataRcvd.log", "w")
    f.write(" on Line 443 ish " + str(rcvOtrMonData) + " " + str(rcvOtrMonMoves))
    f.close()
except Exception as e:
        f = open("/Games/Tiny_Monster_Trainer/crash46.log", "w")
        f.write(str(e))
        f.close()  
    #print(dataToSend)
try:
    del dataToSend
    del dataToSend2
    gc.collect()
    putGhostTogether(rcvOtrMonData, rcvOtrMonMoves, yourGuyJson)
except Exception as e:
        f = open("/Games/Tiny_Monster_Trainer/crash76.log", "w")
        f.write(str(e) + " on Line 466 ish ")
        f.close()  
    
thingAquired("","Yay!","<3","", 1,0,0)
    
