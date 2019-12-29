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
import buttons

class Generator(object):
    def __init__(self):
        self.currentShip = ship.Ship() # Should initialise to default start values.
        self.systemState = 1 # By default, the game Generator points at itself.
        self.generationStage = 1 # The stage of generation are we at.
        self.portraits = []
        crew.loadCrewData()  # To make things simpler later.
        self.shipCreator = pygame.image.load("Graphics_Assets\\char.png")
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator,(g.width,g.height))
    
        self.crewSelector = pygame.image.load("Graphics_Assets\\char2.png")
        self.crewSelectorScaled = pygame.transform.scale(self.crewSelector,(g.width,g.height))
        
        # define button positions for a 640x480 screen.
        # Note: expect this to be very buggy!  Placeholder class in effect.
        
        
        # Animations in effect
        self.raiseBall = False
        self.raiseBallFrame = 0
        self.lowerBall = False
        self.lowerBallFrame = 0
        
        self.changePortrait = False
        self.oldPortrait = 0
        self.newPortrait = 0
        
        # Generate planetary systems.
        planets.loadPlanetarySystems()
        planets.initialisePlanets()
        planets.populatePlanetarySystems()
        
    def loadPortraits(self, number=32, file="Graphics_Assets\\image", fileType=".png"):
        self.portraits.append("dummy") # dummy entry.
        for image in range(1,number+1):
            if image < 10:
                self.portraits.append(pygame.image.load(file+'0'+str(image)+fileType))
            else:
                self.portraits.append(pygame.image.load(file+str(image)+fileType))
    
    # Draw a portrait of a crewmember, if the swap animation is in effect we
    # draw the old portrait being changed to the new one.
    def drawPortrait(self, portrait):
        
        pass
    
    # Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        displaySurface.blit(self.crewSelectorScaled,(0,0))        
        
    # Draw the status line.
    def drawStatusLine(self, crewMember, displaySurface):
        
        
        
        pass
    
    
    # Draw all ship related surfaces
    def drawShip(self, displaySurface):
        displaySurface.blit(self.shipCreatorScaled,(0,0))        
        
    
    # On end, save the data that has been generated to a filename of users choice.
    def saveData(self, fileName="Default"):
        
        pass
    
    # Update function for main game loop.
    def update(self, displaySurface):
        return self.runGenerator(displaySurface)
    
    # Main generator game loop.
    def runGenerator(self, displaySurface):
        if self.generationStage == 1:
            self.drawShip(displaySurface)
            
        if self.generationStage == 2:
            self.drawCrew(displaySurface)
            
        return self.systemState
    
    