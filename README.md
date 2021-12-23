# Tiny_Monster_Trainer 
A game for the Thumby  
(I don't know what I'm doing 🥳)  

Move around, fight monsters, collect monsters, train monsters.  


############ **Game Info** ##############

**Player Info**  
To start you can only have up to two Monsters with you.  
If you get an additional Monster, you will be asked you to select one & let it go.  
Every 10 Trainer Levels you can have an additional Monster with you, up to a maximum of 5.  
Your Trainer Level also influences how well your Active Monster can fight.  
The higher your Trainer Level, you'll seek out stronger Roaming Monsters to fight.  

**Monster Stats**  
**Health**: Amount of Health the Monster can have.  
**Agility**: Used to determine who attacks first and chance to dodge an attack.  
**Strength**: Used to determine damage for physical attacks.  
**Endurance**: Used to determine defense for physical attacks.  
**Mysticism**: Used to determine damage for magical attacks.   
**Tinfoil**: Used to determine defense for magical attacks.  
**Types**: The Type that the Monster is and what pool of moves it can learn from.  

**Battles**  
**Swap**: shows you your Active Monster and you can select another one of your Monster's to be the Active one.  
**Info**: Shows the opposing Monster's Stats/Types & the Active Monster's Stats/Types.  
**Attack**: Lets you pick a move to use against the opposing Monster.  
**Run**: Lets you escape the battle.  
**Tame**: Lets you try to tame the opposing Monster, at the cost of one Crystal.   

If a fight is won, you will gain Experience towards your Trainer Level & you might get an Item.  
If a fight is lost one of your Monsters will have its HP & Stamina restored, but it will be disheartened and lose a Training Point.  


############ **Training** #############  

Train is used to increase a stat by 1 point, up to a maximum amount.  
Learning a new attack cost 3 Training Points, a Monster can know up to 6 attacks.  
A monster can Mutate to increase a procedurally determined stat's maximum training amount.  
A monster can mutate up to 5 times, if you have duplicates of a monster they will mutate in the same ways.  
Mutating can potentially Change the look of a monster.  
Mutating can potentially add a new type to the monster, if a type is added the monster will also learn an attack from the new type.  

**Training Point (TP) Costs**  

Training:     1 TP  
Learn Attack: 3 TP  
Mutate:       5 TP  


############# **Items** ##############  
Items are not usable during combat.  

#######  
**Item List**  
#######  
Bandaids - Heals 8 HP  
PushPops - Heals 20 HP  
Stickers - Raises max trainable HP by 1 and heals for 1  
Ribbons  - Raises max trainable HP by 2 and heals for 2  
Crystals - Will restore all stamina for all moves that the active Monster knows.
         - Crystals are also needed for Taming Monsters. They are consumed by the opposing monster while attempting to Tame

############# **Types: Strengths and Weakness** ##############  

Bonus damage/defense is based on the Attack's Element Type vs Defending Monster Type  

Type | is Strong against | is Weak against
------- | ------|----------
**Earth**       |Wind      | Fire  
**Wind**        |Water     | Earth  
**Water**       |Fire      | Wind  
**Fire**        |Earth     | Water  
------- | ------|----------
**Light**       |Darkness  | Mind  
**Darkness**    |Cute      |Light  
**Cute**        |Mind      |Darkness  
**Mind**        |Light     |Cute  
------- | ------|----------
**Physical**    |Mystical  |Ethereal  
**Mystical**    |Ethereal  |Physical  
**Ethereal**    |Physical  |Mystical  


  
  
#######**Attacks**#######  

If the monster doesn't have the stamina for an attack: They will lose a % of their HP rounded up, then proceed with the attack.  


########  
**Attack List**  
########  
(Basic isn't a Monster Type, Basic attacks can't be learned, They are just default starting moves that a Monster can have)  


Monster Type | Attack Name | Element Type | Phyical/Magic
:------- | :-------: | :-------: | :-------:
**Basic** | | | 
------- |"Poke"       |No Element Type      | Physical  
------- |"Hit"        |No Element Type      | Physical  
------- |MagicHit"    |No Element Type      | Magical  
**Earth** |   |   |  
------- |"RockToss"        |Earth       |Physical  
------- |"Quake"           |Earth       | Magical  
------- |"Pressure"        |Water       |Magical     
------- |"Entomb"          |Darkness    |Physical    
**Wind**| |   |   |  
------- |"Gust"        | Wind        | Physical  
------- |"Cyclone"     | Wind        | Magical  
------- |"Lightning"   | Light       | Physical  
------- |"Divine Wind" | Ethereal    | Magical  
**Water**|   |   |  
------- |"Geyser"      | Water       | Physical  
------- |"Ice Shards"  | Water       | Magical  
------- |"Freeze"      | Mind        | Magical  
------- |"Wave"        | Physical    | Physical  
**Fire**|   |   |                                  
------- |"Torch"       | Fire        | Physical  
------- |"Blaze"       | Fire        | Magical  
------- |"Flare"       | Light       | Magical  
------- |"Inferno"     | Wind        | Physical  
**Light**|   |   |                                
------- |"Dazzle"      | Light       | Physical  
------- |"Razzle"      | Light       | Magical  
------- |"Radiance"    | Fire        | Physical  
------- |"Gleam"       | Mystical    | Magical  
**Darkness**|   |   |
------- |"Murk"        | Darkness    | Physical  
------- |"Shadow"      | Darkness    | Magical  
------- |'Unholy Poke" | Mystical    | Physical  
------- |"Dire Ruin"   | Ethereal    | Magical  
**Cute**|   |   |
------- |"Sing Song"   | Cute        | Physical  
------- |"Adorbes"     | Cute        | Magical  
------- |"Bubbles"     | Water       | Physical  
------- |"Fluff Ball"  | Physical    | Magical  
**Mind**|   |   |
------- |"Headbutt"     | Mind       | Physical  
------- |"Psychic"      | Mind       | Magical  
------- |"Project Rock" | Earth      | Physical  
------- |"Good Vibes"   | Cute       | Magical  
**Physical**|   |   |
------- |"Body Slam"    | Physical   | Physical  
------- |"Super Hit"    | Physical   | Magical  
------- |"Boulder Toss" | Earth      | Physical  
------- |"Love Tap"     | Cute       | Physical  
**Mystical**|   |   |
------- |"Magic Missile" | Mystical   | Physical  
------- |"Ritual"       | Mystical   | Magical  
------- |"Rune Toss"    | Wind       | Physical  
------- |"Immolate"     | Fire       | Magical  
**Ethereal**|   |   |
------- |"Spooky Hit"    | Ethereal   | Physical   
------- |"Superlunary"   | Ethereal   | Magical   
------- |"Obscurity"     | Darkness   | Magical  
------- |"Rue"           | Mind       | Magical  
