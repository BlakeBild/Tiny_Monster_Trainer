def attack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    if activeAttack.magic == 1:
        dodgeBonus = defenceMon.statBlock['Tinfoil'] + random.randint(-1, 6)
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2) 
        defence =  defTrainLevel + dodgeBonus
    else:
        dodgeBonus = defenceMon.statBlock['Endurance'] + random.randint(-1, 6)
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
        defence = defTrainLevel + dodgeBonus
    hp2 = defenceMon.statBlock['currentHealth']
    dodge = defenceMon.statBlock['Agility'] + dodgeBonus #+ math.ceil(defence/2) 
    damage = 0
    hit = 1
    atkTypeBonus = 1
    defTypeBonus = 1
    print("dodgeBonus = ", dodgeBonus)
    test2 = -abs(attackTrainLevel)
    test = random.randint(test2,(100 - defTrainLevel))
    print("100 - def trainer level = ", 100 - defTrainLevel)
    print("attack amount = ", attackAmnt)
    print("dodge = ", dodge)
    print("Abs trainer lvl neg, test 2 = ", test2)
    print("random test, test2 thru 100 = ", test)
    print ("dodge + test = ", dodge + test)
    print(" 90 - defTrainLevel = ", 90 - defTrainLevel)
    print("dodge: ", dodge + test, " vs ", 90 - defTrainLevel )
    if (dodge + test)+100 > (90 - defTrainLevel)+100: # check for dodge
        glanceCheck = random.randint(-20, 20)
        print("glanceCheck = ", glanceCheck)
        print("glance check: ", ((math.ceil(attackAmnt/2) + attackMon.statBlock['Agility']) + glanceCheck), " vs ", dodge)
        if ((math.ceil(attackAmnt/2) + attackMon.statBlock['Agility']) + glanceCheck) >= dodge+defTrainLevel: # check for glance
            hit = 2
            print("glance")
        else:
            print("miss")
            hit = 0
    if hit > 0:
        for x in range(1,3):
            atkTypeBonus = isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
        for x in range(1,3):
            defTypeBonus = isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
        print("attackAmnt = ", attackAmnt)
        print("defence = ", defence)
        print((math.ceil((attackAmnt * atkTypeBonus)/3)), " - ", math.ceil((defence * defTypeBonus)/3))
        damage = math.ceil((attackAmnt * atkTypeBonus)/3) - math.ceil((defence * defTypeBonus)/3)
        if damage <= 0:
            damage = 1
        else:
            damage = math.ceil(damage/hit)
    print("Hit for: ", damage)
    if hit == 1: 
        piz = [0,0,0,1,1,1,2,2,3]
        paz = random.randint(0,8)
        damage = damage + piz[paz]
        print("damage = ", damage, ", Pizpaz = ", piz[paz])
    hp2 = hp2 - damage
    if hp2 < 0:
        hp2 = 0
    defenceMon.statBlock['currentHealth'] = hp2
    if hit == 1:
        return "Hit!"
    elif hit == 2:
        return "Glance"
    else: # hit == 0:
        return "Miss"
        
