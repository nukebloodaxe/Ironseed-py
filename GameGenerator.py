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
        self.portraits = []
        
        self.shipCreator = pygame.image.load("Graphics_Assets\\char.png")
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator,(g.width,g.height))
    
    def loadPortraits(self, number=32, file="Graphics_Assets\\image", fileType=".png"):
        
        for image in range(1,number+1):
            self.portraits.append(pygame.image.load(file+str(image)+fileType))
    
    #Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        
        pass
    
    #Draw all ship related surfaces
    def drawShip(self, displaySurface):
        
        pass
    
    #On end, save the data that has been generated to a filename of users choice.
    def saveData(self, fileName="Default"):
        
        pass
    
    #update function for main game loop.
    def update(self, displaySurface):
        return self.runGenerator(displaySurface)
    
    #main generator game loop.
    def runGenerator(self, displaySurface):
        
        return self.systemState
    
    