import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Monster, AttackMove
from funcLib import thingAquired, obj_to_dict


def loadGameString():
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
    thingAquired(whatDoing, "to other", "trainer!", loadingStr,0,0,0)
    loadingStr = loadingStr + "."
    if loadingStr == "...":
        loadingStr = ""
    return loadingStr


def getNumberOfKeyChecks(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheck = bytearray([0]) 
    myGuyBattleJson = loadGameString()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0,rangeNum):
            rcvCheck['key' + str(y+(x*rangeNum))] =  0 
            #thingAquired("rcvCheck", "key" + str(y+(x*rangeNum)) + " = ", str(rcvCheck['key' + str(y+(x*rangeNum))]), "",0,0,0)
            checkCheck[0] = checkCheck[0] + 1
    if rcvCheckOrCheck == 0:
        return checkCheck
    elif rcvCheckOrCheck == 1:
        return rcvCheck


def chopUpGuyToSend():
    dataToSend=[{}]
    myGuyBattleJson = loadGameString()
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
    return dataToSend

    
def chopUpMovesToSend():   
    dataToSend=[{}]
    myGuyBattleJson = loadGameString()
    numberOfAtks = 0
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
    return dataToSend
    

def getNumberOfKeyChecksMoves(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheckM = bytearray([0]) 
    myGuyBattleJson = loadGameString()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0, len(myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])):
            for z in range(0,rangeNum):
                checkCheckM[0] = checkCheckM[0] + 1
                rcvCheck['key' + str(checkCheckM[0])] =  0
    if rcvCheckOrCheck == 0:
        return checkCheckM
    elif rcvCheckOrCheck == 1:
        return rcvCheck    


def findWhoSendsFirst():
    t0 = 0
    handshakeTimer = 0
    random.seed(time.ticks_ms())
    whoSendsFirst = bytearray([0]) 
    whoSendsFirst[0] = random.randint(1, 255)
    whoSendsFirstRcvd = bytearray([0]) 
    loadingStr = ""
    timerTrigger = 0
    while(t0 - handshakeTimer < 30):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Calling")
        thumby.link.send(whoSendsFirst)
        received = thumby.link.receive()
        if received != None:
            if handshakeTimer == 0:
                whoSendsFirstRcvd = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
                #i should do something if whoSendsFirst[0] == whoSendsFirstRcvd[0] but the odds of that are so low that i probably won't
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
    myGuyBattleJson = loadGameString()
    justMyGuy = myGuyBattleJson[0]['player']
    del myGuyBattleJson
    for z in range(0,2):
        if sOr == 1:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "Calling") 
                thumby.link.send(ujson.dumps(justMyGuy).encode())
                received = thumby.link.receive()
                if received != None:
                    rcvCheckPlayer = ujson.loads(received.decode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 0
        if sOr == 0:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "Calling")
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
        loadingStr = waitingForResponse(loadingStr, "Sending Vibe")
        thumby.link.send(checkCheckNum)
        received = thumby.link.receive()
        if received != None:
            if handshakeTimer == 0:
                checkCheckOther = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
    return checkCheckOther
                        

def sendAndReceive(dataToSend, checkCheck, checkCheckOther, sendOrReceive, rcvCheckNum, numOfData=0, listNumber=0):
    keyList = getKeyList(listNumber)
    sendCheck = {'key0' : 0}
    dataBeingRcvd = [{}]
    xSame = 0
    loadingStr = ""
    time.sleep(.1) #11*3*22
    for c in range(0, (checkCheckOther[0])):
        sendCheck['key' + str(c)] =  0
    for z in range(0,2):
        if sendOrReceive == 1:
            for x in range (0, ((checkCheck[0])/numOfData)): 
                for y in range (0, numOfData):
                    dictToSend = {}
                    dictToRcv = {}
                    while rcvCheckNum['key' + str(y+(x*numOfData))] == 0: 
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        dictToSend[keyList[y]] = dataToSend[x][keyList[y]] #this is where the data I care about is being sent
                        thumby.link.send(ujson.dumps(dictToSend).encode()) 
                        received1 = thumby.link.receive()
                        dictToSend.pop(keyList[y])
                        if received1 != None:
                            try:
                                dictToRcv = ujson.loads(received1.decode())
                                loadingStr = waitingForResponse(loadingStr, "Speaking")
                                if dictToRcv['key2'] != dictToSend['key2']: #if key2 isn't different, don't advance rcvCheckNum so that it'll keep trying to send the same information to the other thumby
                                    rcvCheckNum['key'+str(y+(x*numOfData))] = 1 #if key2 is different advance change it to once so that the while ends and the x/y loops can adv
                                    loadingStr = waitingForResponse(loadingStr, "Speaking")
                            except:
                                pass
        sendLoopExit = math.ceil((checkCheckOther[0])/numOfData)
        if sendOrReceive == 0:
            for x in range (0, ((checkCheckOther[0])/numOfData)): 
                for y in range (0, numOfData):
                    dictToSend = {} 
                    dictToRcv = {}
                    while sendCheck['key' + str(y+(x*numOfData))] == 0:
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        thumby.link.send(ujson.dumps(dictToSend).encode())
                        received2 = thumby.link.receive()
                        if received2 != None: 
                            try:   
                                dictToRcv = ujson.loads(received2.decode())
                                loadingStr = waitingForResponse(loadingStr, "Listening")
                                if dictToRcv['key2'] == dictToSend['key2']:
                                    if x > 0 and xSame != x+y:                                    
                                        dataBeingRcvd.append({})
                                        xSame = x+y
                                    dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[dictToRcv['key']]] #original line: dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[y]]
                                    sendCheck['key' + str(y+(x*numOfData))] = 1
                                    loadingStr = waitingForResponse(loadingStr, "Listening")
                                    for m in range(0, len(dataBeingRcvd)):
                                        try:
                                            if dataBeingRcvd[m] == {}:
                                                dataBeingRcvd.pop(m)
                                        except:
                                            pass
                            except Exception as e:
                                f = open("/Games/Tiny_Monster_Trainer/crashWat.log", "w")
                                f.write(str(e) + " " + str(dictToRcv)+ " on Line 401 ish")
                                f.close()
                if y == (numOfData - 1) and x == (sendLoopExit - 1):
                    dictToSend['key2'] = (y+(x*numOfData)+1)
                    thumby.link.send(ujson.dumps(dictToSend).encode())
        if sendOrReceive == 0:
            sendOrReceive = 1
        else:
            sendOrReceive = 0 
        time.sleep(.5)
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
        for z in range(0, len(otrMonMoves)):
            if otrMonMoves[z]['monster'] == x:
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

    
def doTheThing(dataNum, sOr):
    dataToSend1=[{}]
    listNum = 0
    checkCheck1 = bytearray([0]) 
    checkCheck1 = getNumberOfKeyChecks(0, dataNum)
    rcvCheck1 = {'key0' : 0} 
    if dataNum == 14:
        checkCheck1 = getNumberOfKeyChecks(0, dataNum)
        rcvCheck1 = getNumberOfKeyChecks(1, dataNum)
        dataToSend1 =  chopUpGuyToSend() 
        listNum = 1
    else:
        checkCheck1 = getNumberOfKeyChecksMoves(0, 6)
        rcvCheck1 = getNumberOfKeyChecksMoves(1, 6)
        dataToSend1 = chopUpMovesToSend()
        listNum = 2
    time.sleep(1)
    checkCheckOther1 = sendCheckAndGetCheck(checkCheck1)
    time.sleep(1)
    dataFromOtherThumby = sendAndReceive(dataToSend1, checkCheck1, checkCheckOther1, sOr, rcvCheck1,  dataNum, listNum)   
    return dataFromOtherThumby   


#find out who sends first
sendOrReceive2 = findWhoSendsFirst()

### v- sending guy -v
time.sleep(.5)
yourGuyJson = {}
yourGuyJson = sendOrReceiveGuy(sendOrReceive2)    


### v- sending monsters -v
#try: #Add this try and except back in, if game crashes in the middle of speaking and listening
time.sleep(1)
gc.collect()
rcvOtrMonData = doTheThing(14, sendOrReceive2)
'''except Exception as e:
        f = open("/Games/Tiny_Monster_Trainer/crash48.log", "w")
        f.write(str(e) + " on Line 401 ish")
        f.close()'''

### v- sending moves -v
#try: #Add this try and except back in, if game crashes in the middle of speaking and listening
time.sleep(1)  
gc.collect()
rcvOtrMonMoves = doTheThing(6, sendOrReceive2)
'''except Exception as e:
    f = open("/Games/Tiny_Monster_Trainer/crashA.log", "w")
    f.write(str(e) + " on Line 410 ish")
    f.close() '''

thingAquired("Hi!!", yourGuyJson['name'] , "", "", 0, 0, 0)
putGhostTogether(rcvOtrMonData, rcvOtrMonMoves, yourGuyJson)
thingAquired("","Yay!","<3","", 1,0,0)
