# Tiny_Monster_Trainer 
A game for the Thumby  
(I don't know what I'm doing 🥳)    
  
(If you're here for the most recent version of tiny monster trainer, that is not on the thumby arcade yet. You just need to put Tiny_Monster_Trainer.py, the /Curtain folder, and the /Ghost folder on the thumby.)  

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
**Swap**: shows you your Active Monster and you can select another one of your Monsters to be the Active one.  
**Info**: Shows the opposing Monster's Stats/Types & the Active Monster's Stats/Types.  
**Attack**: Lets you pick a move to use against the opposing Monster.  
**Run**: Lets you escape the battle.  
**Tame**: Lets you try to tame the opposing Monster, at the cost of one Crystal.   

**If a fight is won**, Your active monster will gain 1 Training Point, you will gain an Experience Point towards your Trainer Level, & you might get an Item.  
**If a fight is lost**, one of your Monsters will have its HP & Stamina restored, but it will also be disheartened and lose a Training Point.  


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


Monster Type | Attack Name | Element Type | Damage based on Strength/Mysticism
:------- | :-------: | :-------: | :-------:
**Basic** | | | 
------- |"Poke"       |No Element Type      | Strength  
------- |"Hit"        |No Element Type      | Strength  
------- |MagicHit"    |No Element Type      | Mysticism   
**Earth** |   |   |  
------- |"RockToss"        |Earth       | Strength  
------- |"Quake"           |Earth       | Mysticism  
------- |"Pressure"        |Water       | Mysticism     
------- |"Entomb"          |Darkness    | Strength    
**Wind**| |   |   |  
------- |"Gust"        | Wind        | Strength  
------- |"Cyclone"     | Wind        | Mysticism  
------- |"Lightning"   | Light       | Strength  
------- |"Divine Wind" | Ethereal    | Mysticism  
**Water**|   |   |  
------- |"Geyser"      | Water       | Physical  
------- |"Ice Shards"  | Water       | Mysticism  
------- |"Freeze"      | Mind        | Mysticism  
------- |"Wave"        | Physical    | Strength  
**Fire**|   |   |                                  
------- |"Torch"       | Fire        | Strength  
------- |"Blaze"       | Fire        | Mysticism  
------- |"Flare"       | Light       | Mysticism  
------- |"Inferno"     | Wind        | Strength  
**Light**|   |   |                                
------- |"Dazzle"      | Light       | Strength  
------- |"Razzle"      | Light       | Mysticism  
------- |"Radiance"    | Fire        | Strength  
------- |"Gleam"       | Mystical    | Mysticism  
**Darkness**|   |   |
------- |"Murk"        | Darkness    | Strength  
------- |"Shadow"      | Darkness    | Mysticism  
------- |'Unholy Poke" | Mystical    | Strength  
------- |"Dire Ruin"   | Ethereal    | Mysticism  
**Cute**|   |   |
------- |"Sing Song"   | Cute        | Strength  
------- |"Adorbes"     | Cute        | Mysticism  
------- |"Bubbles"     | Water       | Strength  
------- |"Fluff Ball"  | Physical    | Mysticism  
**Mind**|   |   |
------- |"Headbutt"     | Mind       | Strength  
------- |"Psychic"      | Mind       | Mysticism  
------- |"Telekinesis" | Earth      | Strength  
------- |"Good Vibes"   | Cute       | Mysticism  
**Physical**|   |   |
------- |"Body Slam"    | Physical   | Strength  
------- |"Super Hit"    | Physical   | Mysticism  
------- |"Boulder Toss" | Earth      | Strength  
------- |"Love Tap"     | Cute       | Strength  
**Mystical**|   |   |
------- |"Magic Missile" | Mystical   | Strength  
------- |"Ritual"       | Mystical   | Mysticism  
------- |"Rune Toss"    | Wind       | Strength  
------- |"Immolate"     | Fire       | Mysticism  
**Ethereal**|   |   |
------- |"Spooky Hit"    | Ethereal   | Strength   
------- |"Superlunary"   | Ethereal   | Mysticism   
------- |"Obscurity"     | Darkness   | Mysticism  
------- |"Rue"           | Mind       | Mysticism  
  
    
Updates as of 11/06/22:  
Versus modes have been added. You can fight other players via the link cable though the Link Battle mode. After you've fought someone over a link cable their data is saved so you can fight them offline via the Ghost Battle mode.  
  
 
  
Updates as of 11/1/22:   
I've added live vs battes, but it's super janky right now. To get it to work you need to make sure you have a ghost folder per the update as of 9/4/22, then you need to make sure you have all the .py files that are in the /Curtain folder. update the Tiny_Monster_Trainer.py to the one above. then to get it to work you need to open tiny monster trainer on the thumby. have both thumbys select "multiplay" in the game mode menu, let it do its thing. Then go into game mode menu and select Live. After that select the name of the trainer you are fighting. Then it will load into a multi player battle. It's going to pop up with a bunch of debugging stuff and it won't animate the battle. but you can at least hit eachother. only one of the thumbys is keeping tack of the battle HP so it will show the wrong HP on one of the thumby's between attacks, but it should show the correct HP on the scroller at the bottom of the screen, after the attack happens. Let me know if you have any questions. I'll be cleaning this mess up over the next few weeks.   

  
Updates as of 9/4/22:   
  
Offline ghost battles are a thing now! I'm not going to add it to the arcade yet because I want to make sure that I didn't miss any bugs & I want to try to add legit multiplay first.  

  
To get offline ghost battles to work you need to create a '/Ghost/' folder in the tiny monster trainer directory.   
Update the Tiny_Monster_Tainer.py to the one above on GitHub.  
Then add the multiplayer.py & ghostbattles.py to the '/Curtain/' folder.  
After that you can connect two thumbys together via the link cable, and have them start tiny monster trainer, then have both select multiplayer under game modes.  
It will do it's thing and both thumbys will have a .ujson file in their ghost folder with the opposing trainer's name.  
Select the ghost battle mode to pick the ghost you want to fight.   
You can download Blake.ujson in the ghost folder above to fight my trainer from my longest saved game.   
  

Updates as of 9/1/22:  
Geeze it's been a minute, work got busy. Also I couldn't figure out a bug with the code for the longest time. But I rounded that corner and I've mostly added ghost battles, I still need to do some testing to make sure it's working right. Right now multiplayer.py just sends ghost files over to the other thumby, I need to add a way to cycle through ghost files, ghost file ujsons need to be manually changed in ghostBattle.py code

   
Updates as of 04/18/22:  
Restructured things, now using methods and stuff. The game will now make a list of monsters to load from for when you encounter a roaming monster. Player now roams the wilderness.   
Things are setup so that new modes can be added, multiplayer is coming "soon(TM)" (Planning on adding live multiplayer via Link Cable & Ghost Multiplayer, to load someone else's trainer you have saved to fight them that way too), A storage mode to save monsters & be able to trade them via Link Cable. We'll see how far I can get with those things.  
  
Updates as of 4/16/22:  
Started restructuring things so that I can work on multiplayer.  Things that will be added are: generate a list of monsters then save that list to a .ujson, this will be the pool of monsters for the players world. The ability to save monsters in storage.  I will probably change the way that monsters are created so that I can have monsters the player encounters train themselves, learn new attacks, and mutate before a fight (I think this would help the monsters scale with players at higher trainer levels). I will add vs fights against other players. (i want to save player ghosts so you can battle against them when they aren't around, this will be added a lot later, if added at all). If you win a vs. fight against another player I'd like to add a random monster from their pool of monsters to yours. I want to add monster trading, but that will probably be later. I would like to add a way to temporarily change the player's world seed, and maybe visit the world seed of other players.
    
Updates as of 4/14/22:   
Fixed issue with mutate animation wouldn't load if you had 5 monsters.  
Added more body parts for monsters.  
  
Updates as of 4/11/22:   
Fixed issue where items were not being loaded correctly, it only loaded the first item that was saved.  
Added numbers to item screen, to help show how many items the player has.   
Added text to tell the player they used an item.   
   
Updates as of 4/10/22:  
Rewrote the battle animation screen.    
Attacks will pick a bolt that goes across the screen based on the element type for the attack that was selected.  
Fixed maxFriends, so that you can't go above the max amount anymore.    
Had to lower monster count to 22 due to memory issues that comes up when loading a game with 5 monsters on your team, from the title screen.  
  
Updates as of 4/9/22:  
Changed up the combat math, trying to make it less swingy.  
  
Updates as of 4/8/22:  
Fixed - now the game will let you know that active monster doesn't have enough HP to fight, if in a fight it will tell you that it switched to another monster that has HP  
Added mutate animation ( That takes up too many lines :D )  

Updates as of 4/6/22:  
Added the ability to cycle up through select first monster/monster info/swap active screens.   
Changed the way the options menu checks for the correct selection.  

Updates as of 3/26/22:  
Fixed issue where the worldseed wasn't assigned to the player block and the game would always load the default 0 world  
If the world seed equals the default of '0' then the game will give you a new world seed.
Fixed scroller speed on opening screen  

Updates as of 1/19/22:  
Fixed issue where you could go above the max amount for some skills

Updates as of 1/14/22:  
Issue where there was not enough memory to load TMT from the thumby launcher on physical thumby. Moved images and attacks to their own ujson files in an attempt to fix this.
Fixed issue where there where two images named legs7. Changed name of Mind move to telekinesis from project rock. Added tmt.ujson save for ease of testing.

Updates as of 1/5/22:  
Changed some combat math s'more. I like it better now, but I still haven't been able to play it long enough to see what it might be like at higher trainer levels. I also added some visuals and more monster parts. I fixed some more things that I found that weren’t working as intended.

Updates as of 1/3/22:  
Changed combat math so that the potential for high agility monsters avoiding all damage, all the time, was hopefully removed. Added a couple of monster parts. Added some visuals to help with navigating the game. Rewrote some functions to be the same, they just take up less lines. Removed some errors that caused the game to break. Fixed some things that weren't working as intended.    

Random thoughts as of 12/24/21:  
Future things I'd like to do/add:  
(Probably will need to wait until i get a physical Thumby to see what I can do for these things)  
A way to store additional monsters that aren't with you. (I want to add a campfire you can visit & swap out monsters at)  
Add a way to change the world seed (Thinking about adding an item you might be able to find after a specific trainer level, that when used will change the player's world seed)   
Change Info, in battle, so that you can only see the other monster’s info after a specific trainer level.  
Multiplayer (for trading and battling)    
Redo some combat maths.  
Rewrite a few functions to be smaller.    
Balance some stuff.    
Clean up Player Creation.  
