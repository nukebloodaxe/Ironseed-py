# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:41:15 2019
Crew, planets and Ship Generator for a new game.
This sets up all crew members according to user input.
This sets up the initial ship configuration according to user input.
This sets up all planets, rogue-like style, automatically.
The game starting state, including ship damage, crew stress and starting planet,
are saved to disk as a savegame file.
@author: Nuke Bloodaxe
"""

import io, pygame, crew, ship, items, planets, random, global_constants as g

class Generator(object):
    def __init__(self):
        self.currentShip = ship.Ship()
        self.systemState = 1 #By default, the game Generator points at itself.
        self.generationStage = 1 # The stage of generation are we at.
        self.portraits = []
        crew.loadCrewData() #To make things simpler later.
        self.shipCreator = pygame.image.load("Graphics_Assets\\char.png")
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator,(g.width,g.height))
    
        self.crewSelector = pygame.image.load("Graphics_Assets\\char2.png")
        self.crewSelectorScaled = pygame.transform.scale(self.crewSelector,(g.width,g.height))
        
    def loadPortraits(self, number=32, file="Graphics_Assets\\image", fileType=".png"):
        self.portraits.append("dummy") # dummy entry.
        for image in range(1,number+1):
            if image < 10:
                self.portraits.append(pygame.image.load(file+'0'+str(image)+fileType))
            else:
                self.portraits.append(pygame.image.load(file+str(image)+fileType))
    
    #Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        displaySurface.blit(self.crewSelectorScaled,(0,0))        
        
    
    #Draw all ship related surfaces
    def drawShip(self, displaySurface):
        displaySurface.blit(self.shipCreatorScaled,(0,0))        
        
    
    #On end, save the data that has been generated to a filename of users choice.
    def saveData(self, fileName="Default"):
        
        pass
    
    #update function for main game loop.
    def update(self, displaySurface):
        return self.runGenerator(displaySurface)
    
    #main generator game loop.
    def runGenerator(self, displaySurface):
        if self.generationStage == 1:
            drawShip(displaySurface)
            
        if self.generationStage == 2:
            drawCrew(displaySurface)
            
        return self.systemState
    
    