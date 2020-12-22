# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:02:17 2020

The Cargo Deck for Ironseed.
This area mainly shows current stored cargo, and offers the ability to
jettison cargo.  Some informational panels are available, and you can print
a list of items.

@author: Nuke Bloodaxe
"""

import buttons, pygame, os
import global_constants as g
import helper_functions as h

#  Main class for the Cargo Deck, which is yet another minigame.
class CargoDeck(object):
    
    def __init__(self, theIronseed):
        
        self.ourShip = theIronseed
        self.systemState = 4
        self.musicState = False
        self.cargoStage = 0  #  Setup/interaction stage.
        
        #  Graphics related
        self.cargoInterface = pygame.image.load(os.path.join('Graphics_Assets', 'cargo.png'))
        self.cargoInterfaceScaled = pygame.transform.scale(self.cargoInterface, (g.width, g.height))
        self.cargoInterfaceScaled.set_colorkey(g.BLACK)
        
        #  Create individual graphical elements.
        
        
        #  Define button positions scaled from a 320x200 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.exit = buttons.Button(int((g.height/200)*16),
                                   int((g.width/320)*8),
                                   (int((g.width/320)*94), int((g.height/200)*110)))
        
    
    #  Reset the Cargo Deck back to default starting values.
    def resetCargoDeck(self):
        
        self.cargoStage = -1  # Forces reset when we return.
        self.musicState = False
    
    
    #  Update loop.
    def update(self, displaySurface):

        return self.cargoInterfaceLoop(displaySurface)
        
        
        
    #  Mouse handling routines, handles all button press logic.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.exit.within(currentPosition):
            
            self.resetCargoDeck()
                        
            self.systemState = 10
            #  Reset cargo deck stage and enter command deck state.
        
        return self.systemState
    
    
    #  Interface drawing routine.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.cargoInterfaceScaled, (0, 0))
        
    #  Our main interface loop, here we run all setup and stage checks.
    def cargoInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.cargoStage == 0:
            
            #  We need to ensure our system state is set.
            self.systemState = 4
            
            #  Start main intro music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'CARGO.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.cargoStage += 1
        
        elif self.cargoStage == 1:
            
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                
                pygame.mixer.music.play()
            
            self.drawInterface(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
            
        if self.systemState != 4:
            
            self.cargoStage = 0
            self.musicState = False
        
        return self.systemState