# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:34:22 2019
IronPython - Ironseed To Python Port
Intro module
I know this is as ugly as sin, but I have to start learning somewhere...
@author: Nuke Bloodaxe
"""
import pygame, os, pygame.sndarray, planets
import helper_functions as h
import global_constants as g

class IronseedIntro(object):
    
    def __init__(self):

        
        self.creditText = ["1994 Channel 7, Destiny: Virtual",
                           "Released Under GPL V3.0 in 2013 by Jeremy D Stanton of IronSeed.net",
                           "2013 y-salnikov - Converted IronSeed to FreePascal and GNU/Linux",
                           "2016 Nuke Bloodaxe - Code Tidying",
                           "2020 Nuke Bloodaxe - Complete Python Refactor/Rewrite",
                           "All rights reserved."]
        self.versionText = ["Ironseed", g.version] #  Ridiculous version string required...
        self.introText1 = ["A","Destiny: Virtual", "Designed Game"]
        self.introText2 = ["Mars", "3784 A.D."]
        self.introText3 = ["Escaping the iron fist of a fanatical",
                          "theocracy, the members of the Ironseed",
                          "Movement launch into space and are set",
                          "adrift after suffering a computer",
                          "malfunction"]
        self.introText4 = ["Ship IRONSEED to Relay Point:",
                           "Link Established.",
                           "Receiving Encode Variants.",
                           "Wiping Source Encodes.",
                           "Terminating Transmission.",
                           'Control Protocol Transfered to Human Encode "PRIME".']
                        #  Que Transformers theme...
        self.introText5 = ["As captain, you awaken along with the",
                           "crew some thousand years later and are",
                           "confronted by an alien horde..."]
        self.introText6 = ["Orders: Approach and Destroy.",
                           "Jamming all Emissions.",
                           "Targeting...",
                           "Locked and Loading...",
                           "Closing for Fire..."]
        self.introText7 = ["Enemy Closing Rapidly...",
                           "Shields Imploding...",
                           "Destruction Imminent.",
                           "Attempting Crash Landing."]
        self.introText8 = ["They threaten to devour all life in",
                           "their path...your only hope of defeating",
                           "the Scavengers is to reunite the Kendar,",
                           "an ancient alliance among the free",
                           "worlds."]
        self.starField = pygame.image.load(os.path.join('Graphics_Assets', 'cloud.png'))
        self.channel7Logo = pygame.image.load(os.path.join('Graphics_Assets', 'channel7.png'))
        self.mars = pygame.image.load(os.path.join('Graphics_Assets', 'world.png'))
        self.charCom = pygame.image.load(os.path.join('Graphics_Assets', 'charcom.png'))
        self.redLight = pygame.image.load(os.path.join('Graphics_Assets', 'CrewCom_RED.png'))
        self.battle = pygame.image.load(os.path.join('Graphics_Assets', 'battle1.png'))
        self.alienShip = pygame.image.load(os.path.join('Graphics_Assets', 'alien.png'))
        self.ship = pygame.image.load(os.path.join('Graphics_Assets', 'ship1.png'))
        self.intro5 = pygame.image.load(os.path.join('Graphics_Assets', 'intro5.png'))
        self.ironseed = pygame.image.load(os.path.join('Graphics_Assets', 'main3.png'))
        
        #  Prime intro stage checker
        self.introStage = 0
        self.introFinished = False
        self.musicState = False
        
        #  Prepare counters
        self.count = 1
        self.length = 0
        
        self.encodeStep = 0
        
        self.scavengerStep = 0
        
        self.crashLandingStep = 0

        self.centredX = 0.0
        self.centeredY = 0.0

        #  Prepare Ironseed Intro stopwatch.
        self.stopwatch = h.StopWatch()

        #  Prepare surface used for fading out.
        self.fade = pygame.Surface((g.width,g.height))
        self.fade.fill(g.BLACK)
        self.fade.set_alpha(10)
    
        #  Prepare Channel 7 Logo for blitting.
        self.C7Scaled = pygame.transform.scale(self.channel7Logo, (g.width, g.height))
        self.C7LogoBlit = pygame.PixelArray(self.C7Scaled.convert())
        self.C7LogoCreate = pygame.Surface((g.width, g.height), 0)
        self.C7LogoCreate.set_colorkey(g.BLACK)
        
        #  Prepare starfield for blitting.
        self.starFieldScaled = pygame.transform.scale(self.starField, (g.width, g.height))
        #self.starFieldBlit = pygame.PixelArray(self.scaled.convert())
        
        #  Prepare Mars for Blitting.
        self.marsScaled = pygame.transform.scale(self.mars, (g.width, g.height))
        #self.marsBlit = pygame.PixelArray(self.scaled.convert())
        
        #  Prepare Character communication screen for blitting.
        self.charComScaled = pygame.transform.scale(self.charCom, (g.width, g.height))
        self.charComScaled.set_colorkey(g.BLACK)
        
        # Gradient as a list of tuples.
        self.redBar = h.colourGradient(int(g.width/16)*2, g.RED)
        #  Full length Encode Bar.
        self.fullBar = h.createBar(self.redBar, int((g.width/320)*37), int((g.height/200)*2)+1)
        
        # Red tank light, including flipped version.
        self.redLightScaled = pygame.transform.scale(self.redLight, (int((g.width/320)*13), int((g.height/200)*16)))
        self.redLightScaledFlipped = pygame.transform.flip(self.redLightScaled, True, False)
        
        #  Background star with lens flare.
        self.battleScaled = pygame.transform.scale(self.battle, (g.width, g.height))
        self.battleScaled.set_colorkey(g.BLACK)
        
        #  Prepare ship for blitting, this will be transformed later.
        self.shipScaled = pygame.transform.scale(self.ship, (g.width, g.height))
        self.shipScaled.set_colorkey(g.BLACK)
        
        #  Buffer for image manipulation.
        self.bufferSurfaceImage = pygame.Surface((g.width,g.height))
        self.bufferSurfaceImage.set_colorkey(g.BLACK)
        #  TODO:  Set correct scale ratio.
        
        
        # Prepare Alien battleship deck
        self.alienShipScaled = pygame.transform.scale(self.alienShip, (g.width, g.height))
        self.alienShipScaled.set_colorkey(g.BLACK)
        
        #  Prepare Ironseed deck image;  I really should have the EGO jars
        #  bubbling in distress here.
        self.ironseedScaled = pygame.transform.scale(self.ironseed, (g.width, g.height))
        self.ironseedScaled.set_colorkey(g.BLACK)
        
        #  Create blue status bar for additive overlay.
        self.blueBar = h.colourLine(int((g.width/320)*106), g.BLUE)
        self.fullBlueBar = h.createBar(self.blueBar, int((g.width/320)*106), int((g.height/200)*10)+1)
        
        
        
    def isIntroFinished(self):
        
        return self.introFinished
    
    def resetIntro(self):
        
        self.count = 1
        self.length = 0
        self.encodeStep = 0
        self.introStage = 0
        self.scavengerStep = 0
        self.crashLandingStep = 0
        self.stopwatch.resetStopwatch()
        self.introFinished = False
        self.musicState = False
        self.fade.set_alpha(10)
    
    def resetCounts(self, stage):
        
        self.introStage = stage
        self.count = 0
        self.fade.set_alpha(10)
        self.stopwatch.resetStopwatch()
    
    #  Create the channel 7 logo atop static background by gradually
    #  bringing lines of pixels onto screen.
    def channel7LogoGenerate(self, logo, width, height, step, length):
        
        #  Prepare Fuzz.
        comboSurface = h.makeFuzz(width,height)
        logoScreen = pygame.PixelArray(comboSurface)
        C7LogoCreateBlit = pygame.PixelArray(self.C7LogoCreate)
        #  Perform funky calculation to make logo appear in steps of pixels
        #  of a given length.
        line = 0 #  screen line we are working on
        stepNo = 0 #  step effect tracking per line.
        S = h.safeWrap #  reduces namespace lookups.

        while line < height:
            
            if length >= width:  #  flood fill - guaranteed finish.
            
                for pixel in range(length):
                    
                    if self.C7LogoBlit[pixel][line] != 0:
                        
                        C7LogoCreateBlit[pixel][line] = self.C7LogoBlit[pixel][line]  
                        
            else:
                
                for pixel in range(length, length+step):
                    
                    loci = S(width, stepNo, pixel)
                    
                    if self.C7LogoBlit[loci][line] != 0:
                        
                        C7LogoCreateBlit[loci][line] = self.C7LogoBlit[loci][line]

            line += 1
            stepNo += step
            
        C7LogoCreateBlit.close()
        logoScreen.close()
        comboSurface.blit(self.C7LogoCreate, (0,0))
        #print("return")
        return comboSurface
    
    
    #  Create the Mars floats up into view against starfield screen.
    def marsSceneGenerate(self, planet, starfield, surface, width, height, step):
        
        finished = False
        
        if step*5 < (height/5)*2:
            
            surface.blit(self.starFieldScaled,(0,(0-int((height/3)))+(step*3)))
            surface.blit(self.marsScaled,(0,int(height-(height/3))-(step*5)))
            
        else:
            
            finished = True
        
        return finished
    
    #  Create a rotating planet on the left, and display text on the bottom
    #  third of the screen.
    def planetTextGenerate(self, text, planet, starfield, surface, height,
                           width, step):
        finished = False
        surface.fill(g.BLACK)  #  Blank surface, as starfield = transparent.
        surface.blit(starfield, (0,0))
        lowerThird = int(3*(height/4))
        centerWidth = int(3*(width/6))
        #  Render planet here.
        readyPlanet = pygame.Surface((g.planetWidth, g.planetHeight), 0)
        readyPlanet.set_colorkey(g.BLACK)
        terrainStart = step % (g.planetWidth+1)
        actualPlanet = planets.Planets[planet].planetBitmapToSphere2(readyPlanet, terrainStart, eclipse = True)
        surface.blit(readyPlanet,(int(g.width/16),int(g.height/8)))
        #surface.blit(actualPlanet,(200,200))
        #finished = True #  W00T!
        
        h.renderText(text,g.font,surface,g.WHITE,
                     g.offset,centerWidth,lowerThird,True)
        """
        if h.fadeIn(width, height, surface, step):
            #finished = True
            #print("We Drew: " )
            surface.blit(planets.Planets[planet].planetTexture,(0,0))
        """
        h.fadeIn(width, height, surface, step)
        
        if self.stopwatch.stopwatchSet:
            
            if self.stopwatch.getElapsedStopwatch() > 15:
                
                self.stopwatch.resetStopwatch()
                finished = True
        else:
            
            self.stopwatch.setStopwatch()
            
        # uncomment to look at planet 2D texture.
        #surface.blit(planets.Planets[planet].planetTexture,(0,0))
        return finished
    
    #  Encode helper function, draws the bars in a given position.
    def drawEncodeBar(self, surface, xPosition, yPosition):
        
            currentTimer = 4
            
            #  Set green light to red next to bar.
            if self.count <= 37:
                
                growingBar = h.createBar(self.redBar, int((g.width/320)*self.count), int((g.height/200)*2)+1)
                surface.blit(growingBar, (int((g.width/320)*xPosition), int((g.height/200)*yPosition)))
                
            else:
                
                self.encodeStep += 1
                self.count = 0
                self.stopwatch.resetStopwatch()  #  If we beat the timer.

    #  Load the encodes of the IronSeed Movement members.
    #  Terminate origin bodies on end of transmission.
    #  Note:  These guys love red, we are using count for bar length.
    #  Crafty:  We will cheat by drawing the bars first, and then drawing the
    #  Comm screen over the top...
    #  Transmission lines are supposed to draw every 2 seconds.
    #  TODO: Green lights go red on Encode load.
    def loadEncodes(self, surface):
        
        surface.fill(g.BLACK)
        finished = False
        currentTimer = 0
        lowerThird = int(7*(g.height/10))
        centerWidth = int(g.width/16)

        if self.encodeStep >= 0:
            
            currentTimer = 2
            h.renderText([self.introText4[0]], g.font, surface, g.WHITE,
                          0, centerWidth, lowerThird)

        if self.encodeStep >= 1:
            
            currentTimer = 3
            h.renderText([self.introText4[1]], g.font, surface, g.WHITE,
                         0, centerWidth*10, lowerThird)

        if self.encodeStep >= 2:
    
            currentTimer = 3
            h.renderText([self.introText4[2]], g.font, surface, g.WHITE,
            0, centerWidth, lowerThird+g.offset)
            
            if self.encodeStep == 2:
                
                self.count = 0

        #  Left Side

        if self.encodeStep == 3:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 13, 48)

        if self.encodeStep == 4:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 13, 78)

        if self.encodeStep == 5:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 13, 108)

        #  Right Side.

        if self.encodeStep == 6:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 271, 48)

        if self.encodeStep == 7:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 271, 78)

        if self.encodeStep == 8:
            
            currentTimer = 15
            #  TODO Set green light to red next to bar.
            self.drawEncodeBar(surface, 271, 108)
            
        if self.encodeStep >= 9:
            
            currentTimer = 3
            h.renderText([self.introText4[3]], g.font, surface, g.WHITE,
            0, centerWidth, lowerThird+(g.offset*2))
            
        if self.encodeStep >= 10:
            
            currentTimer = 3
            h.renderText([self.introText4[4]], g.font, surface, g.WHITE,
            0, centerWidth, lowerThird+(g.offset*3))
            
        if self.encodeStep >= 11:
            
            currentTimer = 3
            h.renderText([self.introText4[5]], g.font, surface, g.WHITE,
            0, centerWidth, lowerThird+(g.offset*4))

        # Map the red encode sections to the screen.


        #  Draw full encode bars for each cycle.
        if self.encodeStep >= 4:
            
            #  Bar 1
            surface.blit(self.fullBar, (int((g.width/320)*13), int((g.height/200)*48)))
                        
            if self.encodeStep >= 5:
                
                #  Bar 2
                surface.blit(self.fullBar, (int((g.width/320)*13), int((g.height/200)*78)))
                                
                if self.encodeStep >= 6:
                    
                    #  Bar 3
                    surface.blit(self.fullBar, (int((g.width/320)*13), int((g.height/200)*108)))
                                        
                    if self.encodeStep >= 7:
                        
                        #  Bar 4
                        surface.blit(self.fullBar, (int((g.width/320)*271), int((g.height/200)*48)))
                                            
                        if self.encodeStep >= 8:
                            
                            #  Bar 5
                            surface.blit(self.fullBar, (int((g.width/320)*271), int((g.height/200)*78)))
                                                        
                            if self.encodeStep >= 9:
                                
                                #  Bar 6
                                surface.blit(self.fullBar, (int((g.width/320)*271), int((g.height/200)*108)))
                                                            
        #  Our timer for this sequence.
        if self.stopwatch.stopwatchSet:
            
            if self.stopwatch.getElapsedStopwatch() > currentTimer:
                
                self.stopwatch.resetStopwatch()
                self.encodeStep += 1
                
        else:
            
            self.stopwatch.setStopwatch()
        """
                self.introText4 = ["Ship IRONSEED to Relay Point:",
                           "Link Established.",
                           "Receiving Encode Variants.",
                           "Wiping Source Encodes.",
                           "Terminating Transmission.",
                           'Control Protocol Transfered to Human Encode "PRIME".']
        """
        if self.encodeStep >= 1:
            
            primeStatic = h.makeFuzz(int((g.width/320)*68), int((g.height/200)*68))
            surface.blit(primeStatic, ((g.width/320)*127, (g.height/200)*41))

        surface.blit(self.charComScaled, (0, 0))
        
        # Add Tank Lights
        if self.encodeStep >= 4:
            
            # Red tank light top left
            surface.blit(self.redLightScaled, (int((g.width/320)*82), int((g.height/200)*31)))
            
            if self.encodeStep >= 5:
                
                # Red tank light middle left
                surface.blit(self.redLightScaled, (int((g.width/320)*82), int((g.height/200)*62)))
                
                if self.encodeStep >= 6:
                    
                    # Red tank light bottom left
                    surface.blit(self.redLightScaled, (int((g.width/320)*82), int((g.height/200)*92)))
                    
                    if self.encodeStep >= 7:
                        
                        # Red tank light top right
                        surface.blit(self.redLightScaledFlipped, (int((g.width/320)*226), int((g.height/200)*31)))
                    
                        if self.encodeStep >= 8:
                            
                            # Red tank light middle right
                            surface.blit(self.redLightScaledFlipped, (int((g.width/320)*226), int((g.height/200)*62)))
                            
                            if self.encodeStep >= 9:
                                
                                # Red tank light bottom right
                                surface.blit(self.redLightScaledFlipped, (int((g.width/320)*226), int((g.height/200)*92)))
        
        if self.encodeStep == 12:
            
            finished = True
        
        return finished
    
    #  Fade in a surface, step represents the opacity decrease.
    def fadeInSurface(self, surface, opacity):
        
        surface.set_alpha(255-opacity)
        
    
    #  Shrink the buffer by a ratio of 1 in all directions.
    def shrinkBufferSurface(self, ratio):
            
        self.bufferSurfaceImage = pygame.transform.smoothscale(self.bufferSurfaceImage,
                                                               (int((g.width/16)*(16-(ratio*1.6))), int((g.height/10)*(10-ratio))))
    
    #  Create the surface depicting the ironseed, add text over time
    #  as it is analysed by the alien ship.
    #  Shrink surface to bottom right console location on alien ship.
    #  Draw background graphic, Draw Alien Ship, Draw targetting consoles.
    #  Draw frames above and have targeting consoles concentrate on one point.
    def scavengersAttack(self, displaySurface, width, height, step):
        
        finished = False
        currentTimer = 0
        lowerThird = int(6*(g.height/10))
        centerWidth = int(g.width/16)*2
        displaySurface.fill(g.BLACK)  #  Reset image buffer.
                
        #  Print the Scavenger's analysis and orders.
        
        if self.scavengerStep <= 6:
            
            #  Show the ship being examined
            
            displaySurface.blit(self.shipScaled, (0, 0))
            self.bufferSurfaceImage.set_colorkey(g.RED)
            self.bufferSurfaceImage.set_colorkey(g.BLACK)
            
            if self.scavengerStep < 6:
            
                currentTimer = 3
            
            if self.scavengerStep >= 1:
                
                h.renderText([self.introText6[0]], g.font, displaySurface,
                             g.GREEN, 0, centerWidth, lowerThird)
            
            if self.scavengerStep >= 2:
                
                h.renderText([self.introText6[1]], g.font, displaySurface,
                             g.GREEN, 0, centerWidth, lowerThird+(g.offset))
                
            if self.scavengerStep >= 3:
                
                h.renderText([self.introText6[2]], g.font, displaySurface,
                             g.GREEN, 0, centerWidth, lowerThird+(g.offset*2))
            
            if self.scavengerStep >= 4:
                
                h.renderText([self.introText6[3]], g.font, displaySurface,
                             g.GREEN, 0, centerWidth, lowerThird+(g.offset*3))
            
            if self.scavengerStep >= 5:
                
                h.renderText([self.introText6[4]], g.font, displaySurface,
                             g.GREEN, 0, centerWidth, lowerThird+(g.offset*4))
            
        # Now we switch to shrinking the screen into the viewing panel.
        if self.scavengerStep == 6:
            
            #  No Timer, this needs to be FAST!
            self.bufferSurfaceImage = pygame.Surface((g.width,g.height))
            self.bufferSurfaceImage.set_colorkey(g.RED)
            self.bufferSurfaceImage.fill(g.BLACK)
            self.bufferSurfaceImage.set_colorkey(g.BLACK)
            self.bufferSurfaceImage.blit(displaySurface, (0, 0))
            #  Surface prepared!
            self.scavengerStep += 1
        
        elif (self.scavengerStep >= 7 and self.scavengerStep <= 13):
            
            self.shrinkBufferSurface(self.scavengerStep-6)
            displaySurface.set_colorkey(g.RED)
            displaySurface.fill(g.BLACK)
            displaySurface.set_colorkey(g.BLACK)
            displaySurface.blit(self.bufferSurfaceImage,
                                (int((g.width/16)*((self.scavengerStep-6)*1.6)), 
                                 int((g.height/10)*(self.scavengerStep-6))))
            self.scavengerStep += 1
        
        #  Backup display into Buffer.
        elif self.scavengerStep == 14:
            
            #  Insert sacred pixel of bug fix!
            #bugFix = pygame.PixelArray(displaySurface)
            #  Ommmmm...
            #bugfix[0][0] = (1,1,1)
            #  *Monk chant* de sacra pixel insertis bugfix *bell toll*
            #bugfix.close()
            
            #  No Timer, this needs to be FAST!
            #self.bufferSurfaceImage = displaySurface.copy()
            #  Prior Surface sampled!
            self.scavengerStep += 1
            
        
        #  Prepare display surface for later frames.
        if (self.scavengerStep >= 15 and self.scavengerStep <= 279):
            
            displaySurface.set_colorkey(g.RED)
            displaySurface.fill(g.BLACK)
            displaySurface.set_colorkey(g.BLACK)
            displaySurface.blit(self.bufferSurfaceImage,
                                (int((g.width/16)*(7*1.6)), 
                                 int((g.height/10)*7)))
        
        if (self.scavengerStep >= 15 and self.scavengerStep <= 270):
            
            #  No Timer, this needs to be FAST!
            #  TODO:  Fix mysterous bug here!
            #  Note:  Voodoo bug!  Looks to be hardware surface mapping issue!

            #  Surface prepared!
            self.alienShipScaled.set_alpha(0 + (self.scavengerStep-15))
            
            if self.scavengerStep == 270:
                
                self.scavengerStep = 272
            
            else:
                
                self.scavengerStep += 5
        
        #  Draw Command Deck
        if (self.scavengerStep >= 15 and self.scavengerStep <= 279):
            
            displaySurface.blit(self.alienShipScaled, (0, 0))
        
        
        #  Make dot move twice to Thrice.
        #  Then draw reticules (3 of em, largest to smallest, 1 at a time).
        
        #  Need to draw ship dot moving into position on X and Y screens.
        if self.scavengerStep >= 272 and self.scavengerStep <= 275:
            
            currentTimer = 1
            adjustment = self.scavengerStep-272

            displayArray = pygame.PixelArray(displaySurface)
            displayArray[int((g.width/320)*183)-adjustment, int((g.height/200)*131)+adjustment] = g.WHITE
            displayArray[int((g.width/320)*62), int((g.height/200)*148)+adjustment] = g.WHITE
            displayArray.close()
        
        #  Draw targeting reticule.
        elif self.scavengerStep >= 276 and self.scavengerStep <= 279:
            
            currentTimer = 1  #  Temp.
            circles = self.scavengerStep-275

            displayArray = pygame.PixelArray(displaySurface)
            displayArray[int((g.width/320)*180), int((g.height/200)*134)] = g.WHITE
            displayArray[int((g.width/320)*62), int((g.height/200)*151)] = g.WHITE
            displayArray.close()
            
            h.targettingReticule(displaySurface, int((g.width/320)*180), int((g.height/200)*134), g.VILE_PINK, circles, 4, 1)
            h.targettingReticule(displaySurface, int((g.width/320)*62), int((g.height/200)*151), g.VILE_PINK, circles, 4, 1)
            
        if self.scavengerStep >= 280:
            
            finished = True
            
        #  Our timer for this sequence.
        if h.GameStopwatch.stopwatchSet:
            
            if h.GameStopwatch.getElapsedStopwatch() > currentTimer:
                
                h.GameStopwatch.resetStopwatch()
                self.scavengerStep += 1
                
        else:
            
            h.GameStopwatch.setStopwatch()
        
        return finished
    
    #  Ironseed receives damage, and then crash lands.
    #  Use planet "Icarus" from Oban system for planet to left of main view.
    #  'Icarus' needs to be displayed at 1/3 size.
    #  Blue bars are used to indicate status as the ship comes under attack.
    def ironseedCrash(self, width, height, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.ironseedScaled, (0, 0))
        
        finished = False
        currentTimer = 0
        #  Bar reduction steps.  These appear to be no x 10 percentages.
        # -1,0,0,-2
        # -3,0,-1-1
        # -1,-1,0,0
        
        #  11, 159 - text box location.

        #  Bar bounding box parameters.
        #  (X to X), (Y to Y)  104 wide, 10 high.
        #  (186,290), (35,45) - Hull integrity bar. 100%
        
        #  (186,200), (55,65) - Primary Power.  10% ?
        
        #  (186,233), (75,85) - Auxiliary power. 40% ?
        
        #  (186,279), (95,105) - Shield Strength. 90% ?
        
        barLengths = {0:(290, 200, 233, 279), 1:(280, 200, 233, 259),
                      2:(250, 200, 223, 249), 3:(240, 190, 223, 249),
                      4:(240, 190, 223, 249), 5:(240, 190, 223, 249)}
        
        if self.crashLandingStep >= 1 and self.crashLandingStep <= 3 and self.count <= 10:
            
            tempLengths = [0,0,0,0]
            
            for index in range(0, 4):
                
                tempLength = barLengths[self.crashLandingStep-1][index] - barLengths[self.crashLandingStep][index]
                tempLength /= 10  #  Based on 100ms per second.
                tempLengths[index] = barLengths[self.crashLandingStep-1][index] - int(tempLength * self.count)
                
            barLengths[self.crashLandingStep] = (tempLengths[0], tempLengths[1],
                                                 tempLengths[2], tempLengths[3])
            
        defaultBar = h.colourLine(int((g.width/320)*110), g.BLUE)
        
        barLineHull = h.createBar(defaultBar, int((g.width/320)*(barLengths[self.crashLandingStep][0]-186)), int(g.height/200*10))
        barLinePri = h.createBar(defaultBar, int((g.width/320)*(barLengths[self.crashLandingStep][1]-186)), int(g.height/200*10))
        barLineAux = h.createBar(defaultBar, int((g.width/320)*(barLengths[self.crashLandingStep][2]-186)), int(g.height/200*10))
        barLineShld = h.createBar(defaultBar, int((g.width/320)*(barLengths[self.crashLandingStep][3]-186)), int(g.height/200*10))

        #  Render planet here.
        readyPlanet = pygame.Surface((g.planetWidth, g.planetHeight), 0)
        readyPlanet.set_colorkey(g.BLACK)
        terrainStart = self.crashLandingStep % (g.planetWidth+1)
        planets.Planets["Icarus"].planetBitmapToSphere2(readyPlanet, terrainStart, eclipse = True)
        displaySurface.blit(readyPlanet,(int(g.width/16),int(g.height/8)))
        
        #  Render text and bars.
        
        if self.crashLandingStep <= 4:
            
            currentTimer = 2
            h.renderText(self.introText7[0:self.crashLandingStep], g.font,
                         displaySurface, g.WHITE, g.offset,
                         int((g.width/320)*11), int((g.height/200)*159))
            
            # Draw Bars.
            displaySurface.blit(barLineHull, (int((g.width/320)*186), int((g.height/200)*35)), None, pygame.BLEND_MULT)
            displaySurface.blit(barLinePri, (int((g.width/320)*186), int((g.height/200)*55)), None, pygame.BLEND_MULT)
            displaySurface.blit(barLineAux, (int((g.width/320)*186), int((g.height/200)*75)), None, pygame.BLEND_MULT)
            displaySurface.blit(barLineShld, (int((g.width/320)*186), int((g.height/200)*95)), None, pygame.BLEND_MULT)
            
            # TODO: These bars need to reduce in length smoothly from one value to the next.
            
        else:
            
            finished = True
        
        #  Our timer for this sequence.
        if h.GameStopwatch.stopwatchSet:
            
            if h.GameStopwatch.getElapsedStopwatch() > currentTimer:
                
                h.GameStopwatch.resetStopwatch()
                self.crashLandingStep += 1
                self.count = 0
                
        else:
            
            h.GameStopwatch.setStopwatch()
        
        return finished
    
    # Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        self.resetIntro()
        return 2  # Exit intro and go to main menu.
        
    def update(self, displaySurface):
        
        return self.runIntro(displaySurface)
    
    #  Do all the heavy lifting of running the intro with timers.
    def runIntro(self, displaySurface):
        
        #  Start main intro music
        if self.introStage == 0:
            
            pygame.mixer.music.load(os.path.join('sound', 'INTRO1.OGG'))
            pygame.mixer.music.play()
            self.introStage = 1  # normally 1, use other stages for debug.

        #  Start displaying screen of fuzzy static, make channel 7 logo
        #  gradually appear.
        
        if self.introStage == 1:
            
            if self.length <= g.width and self.count < 255:
                
                newSurface = self.channel7LogoGenerate(self.C7LogoBlit,
                                                       g.width,g.height,
                                                       10,
                                                       self.length)
                displaySurface.blit(newSurface, (0,0))
                displaySurface.blit(self.fade, (0,0))
                #print(str(count)+"while loop")
                
                if self.length < g.width:
                    
                    self.length += 10
                    
                # Fade out Channel 7 logo.
                elif self.count < 300:
                    
                    self.fade.set_alpha(self.count)
                    self.count += 10
            else:
                
                displaySurface.fill(g.BLACK)
                self.resetCounts(2)
        
        #  Destiny Virtual Text, comes in from 4 corners towards the centre,
        #  then transforms from white to red while surrounding pixels fade out.
        #  self.count = 1
        
        if self.introStage == 2:
            
            finished, self.centredX, self.centredY = h.convergeText(self.introText1,
                                                          g.font, g.offset,
                                                          g.WHITE, g.width,
                                                          g.height,
                                                          displaySurface,
                                                          self.count)
            self.count += 1
            #print("centred: ", finished, "centredX: ", centredX, "centredY: ", centredY)
            

            pygame.time.wait(10)
            
            if finished:
                
                self.resetCounts(3)
        
        #  Display the destiny virtual Text at the centre of the screen.
        
        if self.introStage == 3:
            
            finished = h.fadeInText(self.introText1, self.centredX, self.centredY,
                                    g.RED, displaySurface, self.count, True)
            self.count += 1
            pygame.time.wait(50)
            
            if finished:
                
                if h.GameStopwatch.stopwatchSet:
                    
                    if h.GameStopwatch.getElapsedStopwatch() > 5:
                        
                        h.GameStopwatch.resetStopwatch()
                        self.resetCounts(4)
                        finished = True
                else:
                    
                    h.GameStopwatch.setStopwatch()
        
        #  We now bring in two surfaces, a starfield and mars.
        #  print location and date one line at a time afterwards.
        if self.introStage == 4:
            
            finished = self.marsSceneGenerate(self.mars, self.starField,
                                              displaySurface, g.width, g.height,
                                              self.count)
            self.count += 1
            #print("centred: ", finished, "centredX: ", centredX, "centredY: ", centredY)        
            pygame.time.wait(50)
            
            if finished:
                
                self.resetCounts(5)
        
        # Fade in the red text declaring the date and place.
        if self.introStage == 5:
            
            finished = h.fadeInText(self.introText2, (g.width/2), (g.height/7),
                                    g.RED, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(6)
        
        #  Fade Out
        if self.introStage == 6:
            
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(10)
            
            if finished:
                
                self.resetCounts(7)
        
        #  The next scene is the rotating planet, Mars, on left post terraforming.
        #  The text giving the escape reason is at the bottom of the screen.
        #  The generic starfield is used as the background.
        #  Time is given for the player to read the text.
        #  This entire scene, preprepared, fades in.
        if self.introStage == 7:
            
            finished = self.planetTextGenerate(self.introText3, "mars",
                                               self.starFieldScaled,
                                               displaySurface, g.height,
                                               g.width, self.count)
            
            self.count += 1

            if finished:
                
                self.resetCounts(8)
        
        #  Fade Out
        if self.introStage == 8:
            
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(9)
        
        #  In this scene the Ironseed is loading in its EGO banks as the
        #  members of the rebellion evacuate.
        if self.introStage == 9:
            
            finished = self.loadEncodes(displaySurface)
            self.count += 1
            #pygame.time.wait(500)
            
            if finished:
                
                self.resetCounts(10)
            
        #  Fade Out
        if self.introStage == 10:
            
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(11)
        
        #  Ironseed crew wake up, spot problem of an alien horde being nearby.
        #  Features a moon-like planet to the left as usual.
        if self.introStage == 11:
            
            finished = self.planetTextGenerate(self.introText5, "Icarus",
                                               self.battleScaled,
                                               displaySurface, g.height,
                                               g.width, self.count)
            #h.fadeIn(g.width,g.height,displaySurface,self.count)
            
            self.count += 1
            
            if finished:
                
                self.resetCounts(12)
        
        #  Fade Out
        if self.introStage == 12:
            
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(13)
        
        #  The Scavengers find the ironseed, and the Ironseed is destroyed,
        #  crash landing onto a small barran planet.
        #  This scene features plenty of moving graphics, three overlays
        #  required for the monitors alone.
        if self.introStage == 13:
            
            finished = self.scavengersAttack(displaySurface, g.width, g.height, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(14)
                
        #  Fade Out.
        if self.introStage == 14:
            
            #print("Stage 14")
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(15)
        
        #  Ironseed crew under attack initiate crash landing on second planet
        #  of the OBAN system.
        if self.introStage == 15:
            
            finished = self.ironseedCrash(g.width, g.height, displaySurface)
            self.count += 1
                
            pygame.time.wait(50)
            
            if finished:
                
                self.resetCounts(16)
        
        #  Fade Out, Using RED, quickly.
        if self.introStage == 16:
            
            finished = h.fadeOut(g.width, g.height, displaySurface, self.count, g.RED)
            self.count += 1
            pygame.time.wait(10)
            
            if finished:
                
                self.resetCounts(17)
                
        #  Fade red to black.
        if self.introStage == 17:

            finished = h.fadeOut(g.width, g.height, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(100)
            
            if finished:
                
                self.resetCounts(18)
        
        #  Synopsis of the goal, which is to reunite the Kendar, is given.
        if self.introStage == 18:
            
            finished = self.planetTextGenerate(self.introText8, "Icarus",
                                               self.battleScaled,
                                               displaySurface, g.height,
                                               g.width, self.count)
            #h.fadeIn(g.width,g.height,displaySurface,self.count)
            
            self.count += 1
            
            if finished:
                
                self.resetCounts(19)

        #  check to see if we have reached final intro stage here.
        if self.introStage == 19:
            
            self.resetIntro()
            return 2  #  Go to game main menu.
        
        return 3 #  Intro is ongoing