# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:34:22 2019
IronPython - Ironseed To Python Port
Intro module
I know this is as ugly as sin, but I have to start learning somewhere...
@author: Nuke Bloodaxe
"""
import pygame, sys, time, random, numpy, pygame.sndarray, ironSeed
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
        self.versionText = ["Ironseed", g.version] #Ridiculous version string required...
        self.introText1 = ["A","Destiny: Virtual", "Designed Game"]
        self.introText2 = ["Mars", "3784 A.D."]
        self.introText3 = ["Escaping the iron fist of a fanatic",
                          "theocracy, the members of the Ironseed",
                          "Movement launch into space and are set",
                          "adrift after suffering a computer",
                          "malfunction"]
        self.introText4 = ["As captain, you awaken along with the",
                           "crew some thousand years later and are",
                           "confronted by an alien horde..."]
        self.introText5 = ["Orders: Approach and Destroy.",
                           "Jamming all Emissions.",
                           "Targeting...",
                           "Locked and Loading...",
                           "Closing for Fire..."]
        self.introText6 = ["Enemy Closing Rapidly...",
                           "Shields Imploding...",
                           "Destruction Imminent.",
                           "Attempting Crash Landing."]
        self.introText7 = ["They threaten to devour all life in",
                           "their path...your only hope of defeating",
                           "the Scavengers is to reunite the Kendar,",
                           "an ancient alliance among the free",
                           "worlds."]
        self.starField = pygame.image.load("Graphics_Assets\\cloud.png")
        self.channel7Logo = pygame.image.load("Graphics_Assets\\channel7.png")
        self.mars = pygame.image.load("Graphics_Assets\\world.png")
        self.charCom = pygame.image.load("Graphics_Assets\\charcom.png")
        self.battle = pygame.image.load("Graphics_Assets\\battle1.png")
        self.ship = pygame.image.load("Graphics_Assets\\ship1.png")
        self.intro5 = pygame.image.load("Graphics_Assets\\intro5.png")
        
        #Prime intro stage checker
        self.introStage = 0
        self.introFinished = False
        
        # prepare counters
        self.count = 1
        self.length = 0

        self.centredX = 0.0
        self.centeredY = 0.0

        #Prepare surface used for fading out.
        self.fade = pygame.Surface((g.width,g.height))
        self.fade.fill(g.BLACK)
        self.fade.set_alpha(10)
    
        #Prepare Channel 7 Logo for blitting.
        self.C7Scaled = pygame.transform.scale(self.channel7Logo,(g.width,g.height))
        self.C7LogoBlit = pygame.PixelArray(self.C7Scaled.convert())
        
        #Prepare starfield for blitting.
        self.starFieldScaled= pygame.transform.scale(self.starField,(g.width,g.height))
        #self.starFieldBlit = pygame.PixelArray(self.scaled.convert())
        
        #Prepare Mars for Blitting.
        self.marsScaled = pygame.transform.scale(self.mars,(g.width,g.height))
        #self.marsBlit = pygame.PixelArray(self.scaled.convert())        
        
    def isIntroFinished(self):
        return self.introFinished
    
    def resetIntro(self):
        self.introStage = 0
        self.introFinished = False
    
    def resetCounts(self, stage):
        self.introStage = stage
        self.count = 0
        self.fade.set_alpha(10)        
    
    # Create the channel 7 logo atop static background by gradually
    # bringing lines of pixels onto screen.
    def channel7LogoGenerate(self, logo, width, height, step, length):
        
        #Prepare Fuzz.
        comboSurface = h.makeFuzz(width,height)
        logoScreen = pygame.PixelArray(comboSurface)
        
        #Perform funky calculation to make logo appear in steps of pixels
        #of a given length.
        line = 0 # screen line we are working on
        stepNo = 0 # step effect tracking per line.
        S = h.safeWrap # reduces namespace lookups.

        while line <height:
            if length >= width:  # flood fill - guaranteed finish.
                for pixel in range(length):
                    if logo[pixel][line] != 0:
                        logoScreen[pixel][line]=logo[pixel][line]            
            else:
                for pixel in range(length):
                    loci = S(width,stepNo,pixel)
                    if logo[loci][line] != 0:
                        logoScreen[loci][line]=logo[loci][line]
            
            line += 1
            stepNo += step
        del logoScreen
        #print("return")
        return comboSurface
    
    # Create the Mars floats up into view against starfield screen.
    def marsSceneGenerate(self, planet, starfield, surface, width, height, step):
        finished = False
        if step*5 < (height/4)*3:
            surface.blit(self.starFieldScaled,(0,0))
            surface.blit(self.marsScaled,(0,height-(step*5)))
            
        else:
            finished = True
        
        return finished
    
    # Create a rotating planet on the left, and display text on the bottom
    # third of the screen.
    def planetTextGenerate(self, text, planet, starfield, surface, height,
                           width, step):
        finished = False
        surface.blit(self.starFieldScaled,(0,0))
        
        #Render planet here.
        finished = True #W00T!
        
        h.renderText(text,g.font,surface,g.WHITE,g.offset,0,0,False)
        return finished
        
        
    def update(self, displaySurface):
        return self.runIntro(displaySurface)
    
    # Do all the heavy lifting of running the intro with timers.
    def runIntro(self, displaySurface):
        
        #Start main intro music
        if self.introStage == 0:
            pygame.mixer.music.load("sound\\INTRO1.OGG")
            pygame.mixer.music.play()
            self.introStage = 1

        #start displaying screen of fuzzy static, make channel 7 logo
        #gradually appear.
        
        if self.introStage == 1:
            if self.length <= g.width and self.count < 255:
                newSurface = self.channel7LogoGenerate(self.C7LogoBlit,g.width,g.height, 10, self.length)
                displaySurface.blit(newSurface,(0,0))
                displaySurface.blit(self.fade,(0,0))
                #print(str(count)+"while loop")
                if self.length < g.width:
                    self.length += 10
                # Fade out Channel 7 logo.
                elif self.count < 255:
                    self.fade.set_alpha(self.count)
                    self.count += 15
            else:
                displaySurface.fill(g.BLACK)
                self.resetCounts(2)
        
        #Destiny Virtual Text, comes in from 4 corners towards the centre,
        #then transforms from white to red while surrounding pixels fade out.
        #self.count = 1
        
        if self.introStage == 2:
            finished, self.centredX, self.centredY = h.convergeText(self.introText1,
                                                          g.font, g.offset,
                                                          g.WHITE, g.width,
                                                          g.height,
                                                          displaySurface,
                                                          self.count)
            self.count +=1
            #print("centred: ", finished, "centredX: ", centredX, "centredY: ", centredY)        
            pygame.time.wait(10)
            if finished:
                self.resetCounts(3)
        
        if self.introStage == 3:
            finished = h.fadeInText(self.introText1, self.centredX, self.centredY,
                                    g.RED, displaySurface, self.count, True)
            self.count += 1
            pygame.time.wait(50)
            if finished:
                self.resetCounts(4)
        
        #We now bring in two surfaces, a starfield and mars.
        #print location and date one line at a time afterwards.
        if self.introStage == 4:
            finished = self.marsSceneGenerate(self.mars, self.starField,
                                              displaySurface,g.width,g.height,
                                              self.count)
            self.count +=1
            #print("centred: ", finished, "centredX: ", centredX, "centredY: ", centredY)        
            pygame.time.wait(100)
            if finished:
                self.resetCounts(5)
        
        if self.introStage == 5:
            finished = h.fadeInText(self.introText2, (g.width/2), (g.height/7),
                                    g.RED, displaySurface, self.count)
            self.count += 1
            pygame.time.wait(200)
            if finished:
                self.resetCounts(6)
        
        #Fade Out
        if self.introStage == 6:
            finished = h.fadeOut(g.width,g.height,displaySurface,self.count)
            self.count +=1
            pygame.time.wait(100)
            if finished:
                self.resetCounts(7)
        
        #The next scene is the rotating planet, Mars, on left post terraforming.
        #The text giving the escape reason is at the bottom of the screen.
        #The generic starfield is used as the background.
        #Time is given for the player to read the text.
        #This entire scene, preprepared, fades in.
        if self.introStage == 7:
            
            finished = self.planetTextGenerate(self.introText3, "mars", self.starField,
                                          displaySurface, g.height, g.width,
                                          self.count)
            
            self.count +=1
            if finished:
                self.resetCounts(8)
        
        #Fade Out
        if self.introStage == 8:
            finished = h.fadeOut(g.width,g.height,displaySurface,self.count)
            self.count +=1
            pygame.time.wait(100)
            if finished:
                self.resetCounts(9)
        
        #In this scene the Ironseed is loading in its EGO banks as the
        # members of the rebellion evacuate.
        if self.introStage == 9:

            self.resetCounts(10)
            
        #Game synopsis given at this point, the Ironseed mission overall is given.
        #Features a moon-like planet to the left as usual.
        if self.introStage == 10:
            
            finished = self.planetTextGenerate(self.introText4, "mars", self.starField,
                                          displaySurface, g.height, g.width,
                                          self.count)
            #h.fadeIn(g.width,g.height,displaySurface,self.count)
            
            self.count +=1
            if finished:
                self.resetCounts(11)
        
        #Fade Out
        if self.introStage == 11:
            finished = h.fadeOut(g.width,g.height,displaySurface,self.count)
            self.count +=1
            pygame.time.wait(100)
            if finished:
                self.resetCounts(12)
        
        #The Scavengers find the ironseed, and the Ironseed is destroyed,
        #crash landing onto a small moon.
        #This scene features plenty of moving graphics, three overlays required
        #for the monitors alone.
        
        
        #temp quick kill.
#        pygame.quit()
#        sys.exit()
        
        #check to see if we have reached final intro stage here.
        return 3 # kludge for testing.
        # Note change state to main menu on Intro finish.
    
        #Show main game menu screen
        #pygame.mixer.music.load("sound\\INTRO2.OGG")