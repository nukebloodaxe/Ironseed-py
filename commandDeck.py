# -*- coding: utf-8 -*-
"""
Created on Sat May  9 13:10:10 2020

Main Command Deck, central operations for all systems in IronSeed.

@author: Nuke Bloodaxe
"""

import pygame, os
import global_constants as g

class CommandDeck(object):
    
    def __init__(self, ship, crew):
        
        self.ironSeed = ship
        self.crewMembers = crew
        self.commandStage = 0
        self.systemState = 10
        self.musicState = False
        
        #  Load Graphics Layers
        
        #  Command Deck Graphic
        self.commandDeckGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'main.png'))
        
        #  Prepare Command Deck Graphic for blitting
        self.commandDeckGraphicScaled = pygame.transform.scale(self.commandDeckGraphic, (g.width, g.height))
        
        
        
    #  Mouse button interaction routine.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        return self.systemState
    
    #  Draw command deck interface
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.commandDeckGraphicScaled, (0, 0))
        
    
    
    #  Check stage and run routines for initialization, ongoing ops or exit.
    def runCommandDeck(self, displaySurface):
        
        if self.commandStage == 0:
            
            #  Start deck music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'SECTOR.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.commandStage += 1
            
        elif self.commandStage == 1:
            
            self.drawInterface(displaySurface)

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()
        
        
        return self.systemState #  loop for the moment.
    
    
    def update(self, displaySurface):

        return self.runCommandDeck(displaySurface)