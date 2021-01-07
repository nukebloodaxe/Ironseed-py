# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 17:09:37 2020

Planet communications module, the is the ship to planet communications
screen.  Oddly, planets don't initiate communications, but I personally
feel this is an oversight; probably not possible in original constraints of
engine.

Note: Ironseed does not feature Space Stations...  which is plain weird,
probably a design and time restraint, plus new mechanics required all over.

@author: Nuke Bloodaxe
"""

import planets, buttons, pygame, os
import global_constants as g
import helper_functions as h

#  Alien class for alien graphics, and thei timers for display.
#  Note:  May be moved into alien.py in a later consolidation effort.
#  textureDetails is a list of tuples of (x, y, time, rows, columns)
class AlienCommGraphics(object):
    
    def __init(self, comboTexture, textureDetails):
        
        self.originalTexture = comboTexture
        self.textureDetails = textureDetails
        self.animations = []
        # An entry in animations consists of an entry containing the following
        # tuple entry:
        # ([frames], time, x, y)
        #  This way we can cycle each frame every "time" and render at x,y.
        
        #  resize all animation frames by regenerating them.
        def resize(self):
    
            pass
        
        #  Convert the texture into animation frames.
        def makeAnimations(self):
            
            #  Using each entry in "textureDetails", we create a series of
            #  animation frames, add them to a list, then combine the
            #  information from "textureDetails" and these frames into
            #  "animations" tuple entries.
            
            pass
    

#  Main class for the Planet Comms Deck, which is yet another minigame.
class PlanetComm(object):
    
    def __init__(self, playerShip):
        
        self.ironSeed = playerShip
        self.thePlanet = "Placeholder"
        self.systemState = 14
        self.planetCommsStage = 0  #  Setup/interaction stage.
        self.musicState = False
        
        #  Graphics related
        self.planetCommsInterface = pygame.image.load(os.path.join('Graphics_Assets', 'com.png'))
        self.planetCommsInterfaceScaled = pygame.transform.scale(self.planetCommsInterface, (g.width, g.height))
        self.planetCommsInterfaceScaled.set_colorkey(g.WHITE)  # !
        
        #  There are rather a lot of alien backgrounds, so we will
        #  Use an array to store them.
        self.alienBackground = []
        
        self.loadBackgrounds()
        
        #  The alien textures are much the same.
        self.alienTextures = []
        
        self.loadAlienTextures()
        
        #  Alien graphics as an array of arrays.
        
        self.aliens = []
        
        #  With the alien textures, they appear to almost be unique per alien
        #  in terms of available elements, sizes etc.
        #  It will necessary to create an alien texture format tab delimited
        #  file with some semblance of formatting along the lines of:
        #  Alien Type
        #  Graphic, frame amount
        #  co-ordinate 1 etc.
        #  Keep repeating until EOA, then next alien entry.
        
        #  Create individual graphical elements.
        
        
        
        #  Define button positions scaled from a 320x200 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.exit = buttons.Button(int((g.height/200)*9),
                                   int((g.width/320)*16),
                                   (int((g.width/320)*310),
                                    int((g.height/200)*152)))
        
    
    #  Reset the planet communications Deck back to default starting values.
    def resetPlanetComms(self):
        
        self.planetCommsStage = -1  # Forces reset when we return.
        self.musicState = False
    
    
    #  Load all alien related graphics files, these are in array order.
    def loadAlienTextures(self):

        self.alienTextures.append("placeholder")        

        for image in range(1,10):
        
            self.alienTextures.append( pygame.image.load(os.path.join('Graphics_Assets', 'alien'+str(image)+'.png')))
            self.alienTexturesScaled = pygame.transform.scale(self.alienTextures[image], (g.width, g.height))
        
    
    #  Load all background related graphics files.
    #  Note:  Not as easy as it seems, they are out-of-order, based on race.
    def loadBackgrounds(self):
        
        #  List represents the background iamge order for the predefined races.
        #  Other backgrounds begin after image 11.
        imageList = ["01", "07", "18", "09", "15", "22", "17", "04", "14", "02",
                     "21", "19", "01", "03", "05", "06", "08", "10", "11", "12",
                     "13", "16", "20"]
        count = 0
        
        for image in imageList:
        
            self.alienBackground.append( pygame.image.load(os.path.join('Graphics_Assets', 'back'+image+'.png')))
            self.alienBackgroundScaled = pygame.transform.scale(self.alienBackground[count], (g.width, g.height))
            count = 1
    
    #  Update loop.
    def update(self, displaySurface):

        return self.planetCommsInterfaceLoop(displaySurface)
        
        
        
    #  Mouse handling routines, handles all button press logic.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.exit.within(currentPosition):
            
            self.resetPlanetComms()
                        
            self.systemState = 10
            #  Reset planet communications stage and enter command deck state.
        
        return self.systemState
    
    
    #  Interface drawing routine.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.planetCommsInterfaceScaled, (0, 0))
        
    #  Our main interface loop, here we run all setup and stage checks.
    def planetCommsInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.planetCommsStage == 0:
            
            #  We need to ensure our system state is set.
            self.systemState = 14
            
            #  Establish ship position and planet for pointer.
            X, Y, Z = self.ironSeed.getPosition()
            self.thePlanet = planets.findPlanetarySystem(X, Y, Z).getPlanetAtOrbit(self.ironSeed.getOrbit())
            
            #TODO: Reorder to fit game logic.
            alienMusic = ['SECTOR.OGG', #  Lifeless, comms auto fail.
                          'SENGZHAC.OGG', #  The Sengzhac live here.
                          'DPAK.OGG', #  The Dpak live here.
                          'AARD.OGG', #  The Aard live here.
                          'EMERGEN.OGG', #  The Emergen live here.
                          'Titarian.OGG', #  The Titarian live here.
                          'QUAI.OGG', #  The Quai live here.
                          'SCAVENG.OGG', #  The Scavengers live here.
                          'ICON.OGG', #  The Icon live here.
                          'GUILD.OGG', #  The Guild live here.
                          'PHADOR.OGG', #  The Phador live here.
                          'VOID.OGG', #  The Void Dwellers live here.
                          ]
            
            #  Start comms music
            if self.musicState == False:
                
                #  Comms music changes according to alien type,
                #  or lack thereof.
                if self.thePlanet.owned >= 0 and self.thePlanet.owned <= 11:
                    
                    pygame.mixer.music.load(os.path.join('sound', alienMusic[self.thePlanet.owned]))
         
                elif self.thePlanet.owned > 29:
                    
                    #  Life present.
                    pygame.mixer.music.load(os.path.join('sound', 'PROBE.OGG'))
                    
                else:
                    
                    #  Lifeless, comms autofail.
                    pygame.mixer.music.load(os.path.join('sound', 'SECTOR.OGG'))
                    
                pygame.mixer.music.play()
                self.musicState = True
                self.planetCommsStage += 1
        
        elif self.planetCommsStage == 1:
            
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                
                pygame.mixer.music.play()
            
            self.drawInterface(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
            
        if self.systemState != 14:
            
            self.planetCommsStage = 0
            self.musicState = False
        
        return self.systemState