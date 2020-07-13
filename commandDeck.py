# -*- coding: utf-8 -*-
"""
Created on Sat May  9 13:10:10 2020

Main Command Deck, central operations for all systems in IronSeed.

@author: Nuke Bloodaxe
"""

import pygame, os
import global_constants as g

#  Store the current position of a subFunction, and which it is.
class SubFunction(object):
    
    def __init__(self, functionType, positionX, positionY):
        
        self.functionType = functionType
        self.active = True
        self.positionX = positionX
        self.positionY = positionY

#  The main command deck of the IronSeed.  All areas ultimately come here.
class CommandDeck(object):
    
    def __init__(self, ship, crew):
        
        self.ironSeed = ship
        self.crewMembers = crew
        self.commandStage = 0
        self.systemState = 10
        self.musicState = False
        self.cubeFacet = 0  # cube for multi-button system access and control.
        self.oldFacet = 0  # previous facet
        self.spinPosition = 1  # Where are we for a spin?
        self.cubeSpinning = False  # Are we spinning the cube?  (can't interact.)
        self.cubeSpinEnd = int((g.width/320)*50)
        self.theCube = [0, 1, 2, 3, 4, 5, 6]  #  Cube function shortcut.
        self.subFunctions = []  # sub-functions in operation.
        
        #  Load Graphics Layers
        
        self.mainCubeGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'main-cube.png'))

        #  Sub-Divide cube graphics into correct groups.
        
        self.psychoGraphic = pygame.Surface((50, 44), 0)
        self.psychoGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 0, 50, 44))
        self.psychoGraphicScaled = pygame.transform.scale(self.psychoGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        self.engineeringGraphic = pygame.Surface((50, 44), 0)
        self.engineeringGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 45, 50, 44))
        self.engineeringGraphicScaled = pygame.transform.scale(self.engineeringGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        self.scienceGraphic = pygame.Surface((50, 44), 0)
        self.scienceGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 90, 50, 44))
        self.scienceGraphicScaled = pygame.transform.scale(self.scienceGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        self.securityGraphic = pygame.Surface((50, 44), 0)
        self.securityGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 135, 50, 44))
        self.securityGraphicScaled = pygame.transform.scale(self.securityGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        self.astrogationGraphic = pygame.Surface((50, 44), 0)
        self.astrogationGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 180, 50, 44))
        self.astrogationGraphicScaled = pygame.transform.scale(self.astrogationGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        self.medicalGraphic = pygame.Surface((50, 44), 0)
        self.medicalGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 225, 50, 44))
        self.medicalGraphicScaled = pygame.transform.scale(self.medicalGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        
        #  Command Deck Graphic
        self.commandDeckGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'main.png'))
        
        #  Prepare Command Deck Graphic for blitting
        self.commandDeckGraphicScaled = pygame.transform.scale(self.commandDeckGraphic, (g.width, g.height))

    #  The cube for interaction is fairly involved, it has major functions
    #  which take the player to a seperate screen and therefore class.
    #  However, the sub-functions can act as overlay windows on the command
    #  deck window.
    
    #  check to see if a sub-function is active.
    def subFunctionCheck(self, subFunction):
        
        result = False
        
        for check in self.subFunctions:
            
            if check.functionType == subFunction:
                
                if check.active:
                
                    result = True
                break
                
        return result
    
    #  Deactivate a sub-function.
    def subFunctionDeactivate(self, subFunction):
        
        for check in self.subFunctions:
            
            if check.subFunction == subFunction:
                
                check.active = False
        

    #  Interactive panel 1: Psychometry.
    def cubePsycho(self, currentPosition):
        
        pass
    
    #  Interactive Panel 2: Engineering.
    def cubeEngineering(self, currentPosition):
        
        pass
    
    #  Interactive Panel 3: Science.
    def cubeScience(self, currentPosition):
        
        pass
    
    #  Interactive Panel 4: Security.
    def cubeSecurity(self, currentPosition):
        
        pass
    
    #  Interactive Panel 5: Astrogation.
    def cubeAstrogation(self, currentPosition):
        
        pass
    
    #  Interactive Panel 6: Medical.
    def cubeMedical(self, currentPosition):
        
        pass
    
        
    #  Mouse button interaction routine.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        self.systemState = self.theCube[self.cubeFacet](currentPosition)
        
        return self.systemState
    
    #  Spinning the cube between facets is a trapezoidal transformation.
    def drawCubeSpin(self):
        
        pass
    
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
                
            #  Populate the cube shortcut function list.
            self.theCube[1] = self.cubePsycho
            self.theCube[2] = self.cubeEngineering
            self.theCube[3] = self.cubeScience
            self.theCube[4] = self.cubeSecurity
            self.theCube[5] = self.cubeAstrogation
            self.theCube[6] = self.cubeMedical
            
        elif self.commandStage == 1:
            
            self.drawInterface(displaySurface)

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()
        
        
        return self.systemState #  loop for the moment.
    
    
    def update(self, displaySurface):

        return self.runCommandDeck(displaySurface)