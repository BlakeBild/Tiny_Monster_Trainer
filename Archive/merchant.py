## WIP merchant class
import time
import thumby
import math

class Merchant(NPC):
    def __init__(self):
        self.items2Sell = ["Stickers", "Vitamins", "Helium", "Pillows", "Stardust", "Tinfoil", "Bandaids", "PushPops", "Crystals"]
    
    def PlayerBuy(playerMoney):
        
    def PlayerSell(playerItems, playerMoney): 
    
    def getLooks:
        # BITMAP: width: 36, height: 29
        bean = bytearray([0,0,0,0,0,0,128,224,48,136,12,36,2,138,194,194,226,242,242,226,226,230,196,132,36,12,8,120,192,0,0,0,0,0,0,0,
            0,0,0,0,0,254,3,128,0,48,252,255,255,253,241,241,255,127,31,255,241,241,253,255,255,60,128,252,7,0,0,0,0,0,0,0,
            0,0,0,0,0,199,124,0,0,136,96,7,15,31,31,191,243,247,247,179,31,31,207,103,57,4,3,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,1,7,28,12,6,2,2,2,3,3,7,12,31,12,7,3,3,3,3,2,6,28,16,0,0,0,0,0,0,0,0])
        beanM = bytearray([0,0,0,0,0,0,128,224,240,248,252,252,254,254,254,254,254,254,254,254,254,254,252,252,252,252,248,248,192,0,0,0,0,0,0,0,
            0,0,0,0,0,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,7,0,0,0,0,0,0,0,
            0,0,0,0,0,199,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,7,3,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,1,7,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,30,28,16,0,0,0,0,0,0,0,0])
        # BITMAP: width: 40, height: 32
        firstB = bytearray([255,255,3,3,3,3,3,3,3,131,195,35,51,147,11,43,11,11,139,203,203,139,139,155,19,19,147,51,35,227,3,3,3,3,3,3,3,3,255,255,
            255,255,0,0,0,0,0,248,14,3,0,194,240,252,252,246,199,199,255,255,127,255,199,199,247,254,252,240,0,241,31,0,0,0,0,0,0,0,255,255,
            255,255,0,0,0,0,0,31,240,2,0,32,131,31,63,127,127,255,207,221,220,207,127,127,63,159,231,16,14,3,0,0,0,0,0,0,0,0,255,255,
            255,255,128,128,128,128,128,135,157,240,176,154,137,136,136,140,140,158,179,255,179,158,140,140,143,141,136,152,240,192,128,128,128,128,128,128,128,128,255,255])
    def drawScreen:
        #maybe just do some retangles for the box
        # BITMAP: width: 40, height: 32
        box = bytearray([255,255,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,255,255,
            255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,
            255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,
            255,255,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,255,255])
        # BITMAP: width: 36, height: 29
        blahTest = bytearray([0,100,10,196,10,100,10,196,10,100,10,196,10,100,10,196,10,100,10,196,10,100,10,196,10,100,10,196,10,100,10,196,10,100,10,0,
            0,27,0,54,0,27,0,54,0,155,0,54,0,27,0,182,0,27,0,54,0,27,64,54,0,27,0,54,0,155,0,54,0,27,0,0,
            0,73,0,0,68,0,0,145,0,0,32,2,0,0,128,8,0,0,132,0,0,32,2,0,0,2,132,0,0,16,0,0,0,2,128,0,
            0,0,0,0,2,0,0,0,4,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,4,0,0,1,0,0,0,0,0])    
        
        
        
        
        
bean = bytearray([0,0,0,0,0,0,128,224,48,136,12,36,2,138,194,194,226,242,242,226,226,230,196,132,36,12,8,120,192,0,0,0,0,0,0,0,
    0,0,0,0,0,254,3,128,0,48,252,255,255,253,241,241,255,127,31,255,241,241,253,255,255,60,128,252,7,0,0,0,0,0,0,0,
    0,0,0,0,0,199,124,0,0,136,96,7,15,31,31,191,243,247,247,179,31,31,207,103,57,4,3,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,1,7,28,12,6,2,2,2,3,3,7,12,31,12,7,3,3,3,3,2,6,28,16,0,0,0,0,0,0,0,0])
beanM = bytearray([0,0,0,0,0,0,128,224,240,248,252,252,254,254,254,254,254,254,254,254,254,254,252,252,252,252,248,248,192,0,0,0,0,0,0,0,
    0,0,0,0,0,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,7,0,0,0,0,0,0,0,
    0,0,0,0,0,199,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,7,3,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,1,7,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,30,28,16,0,0,0,0,0,0,0,0])
blahTest = bytearray([0,0,48,40,36,44,40,40,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96,80,80,80,72,72,88,80,112,32,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            
# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)
thumbySprite = thumby.Sprite(36, 29, bean)
thumbySpriteM = thumby.Sprite(36, 29, beanM)
thumbySpriteBG = thumby.Sprite(36, 29, blahTest)

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black

    bobRate = 250 # Set arbitrary bob rate (higher is slower)
    bobRange = 5  # How many pixels to move the sprite up/down (-5px ~ 5px)

    # Calculate number of pixels to offset sprite for bob animation
    bobOffset = math.sin(t0 / bobRate) * bobRange

    # Center the sprite using screen and bitmap dimensions and apply bob offset
    thumbySprite.x = 34
    thumbySprite.y = 2
    thumbySpriteBG.x = 34
    thumbySpriteBG.y = 2

    # Display the bitmap using bitmap data, position, and bitmap dimensions
    thumby.display.drawSprite(thumbySpriteBG)
    thumby.display.drawSpriteWithMask(thumbySprite, thumbySpriteM)
    thumby.display.update()
