# -*- coding: utf-8 -*-
"""
Created on Sat May  9 13:10:10 2020

Main Command Deck, central operations for all systems in IronSeed.

@author: Nuke Bloodaxe
"""

import buttons, pygame, os, io
import global_constants as g

#  The side of a cube, including buttons.
class CubeSide(object):
    
    def __init__(self):
    
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.buttons = []
                        
    #  Add a button to this facet, and also convert for current resolution.
    def addButton(self, x, y, height, width, returnValue):
        
        self.buttons.append((returnValue, buttons.Button(int((g.height/200)*height),
                                                         int((g.width/320)*width),
                                                         (int((g.width/320)*x),
                                                          int((g.height/200)*y)))))
    
    #  Return tuple of False and 0 when nothing matched.
    def checkButtonPress(self, position):
        
        match = False
        buttonType = 0
        
        for button in self.buttons:
        
            if button[1].within(position):
                
                match = True
                buttonType = button[0]
                break
        
        return (match, buttonType)
    
#  A cube in memory, stores and interacts with the cube used on the command deck.
class Cube(object):

    def __init__(self):
        
        self.sides = [CubeSide(), CubeSide(), CubeSide(),
                      CubeSide(), CubeSide(), CubeSide()]
        self.currentSide = 0  # In crew role order.
        self.oldFacet = 0  # previous facet
        self.spinPosition = 0  # Where are we for a spin?
        self.cubeSpinning = False  # Are we spinning the cube?  (can't interact.)
        self.cubeSpinEnd = int((g.width/320)*50)


    #  Check to see if the cube has had a button pressed.
    def checkSideButton(self, position):
        
        return self.sides[self.currentSide].checkButtonPress(position)
    
    
    #  Load and parse cube definition data.  This populates the 5 sides with
    #  their button positions and return numbers.
    def loadCubeData(self, file):

        cubeFacetFile = io.open(file, "r")
        temp = [""]

        # Clear file comment lines.        
        while temp[0] != "BEGINCUBE":

            temp[0] = cubeFacetFile.readline().split('\n')[0]
        
        temp = (cubeFacetFile.readline().split('\n')[0]).split('\t') # Data Line
    
        #  Add buttons to facets.
        while temp[0] != "ENDF":
        
            #print(temp)
        
            try:
                
                self.sides[int(temp[0])].addButton(int(temp[1]), int(temp[2]),
                                                   int(temp[3]), int(temp[4]),
                                                   int(temp[5]))
            except:
                    
                print("Absolutely fatal Error loading cube data!")
            
            temp = (cubeFacetFile.readline().split('\n')[0]).split('\t') # Data Line
        
    
    #  Run construction routine, this makes an actual memory cube.
    def constructCube(self, file):
        
        self.loadCubeData(file)
        
        layout = [[0, 1, 2, 3, 4],
                  [1, 5, 2, 0, 4],
                  [2, 5, 3, 0, 1],
                  [3, 5, 4, 0, 2],
                  [4, 5, 1, 0, 3],
                  [5, 1, 4, 3, 2]]
        
        #  link all six sides.
        for side in layout:
            
            self.sides[side[0]].top = side[1]
            self.sides[side[0]].right = side[2]
            self.sides[side[0]].bottom = side[3]
            self.sides[side[0]].left = side[4]
            
            
            

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
        self.cube = Cube()
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
    
    
    #  Interactive panel 0: Psychometry.
    def cubePsycho(self, currentPosition):
        
        pass
    
    #  Interactive Panel 1: Engineering.
    def cubeEngineering(self, currentPosition):
        
        pass
    
    #  Interactive Panel 2: Science.
    def cubeScience(self, currentPosition):
        
        pass
    
    #  Interactive Panel 3: Security.
    def cubeSecurity(self, currentPosition):
        
        pass
    
    #  Interactive Panel 4: Astrogation.
    def cubeAstrogation(self, currentPosition):
        
        pass
    
    #  Interactive Panel 5: Medical.
    def cubeMedical(self, currentPosition):
        
        pass

    #  Mouse button interaction routine.
    #TODO:  Lots of button support.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        cubeCheck = self.cube.checkSideButton(currentPosition)
        
        #self.systemState = self.theCube[self.cubeFacet](currentPosition)
        
        
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
            
            #  Construct the cube.
            self.cube.constructCube(os.path.join('Data_Generators', 'Other', 'IronPy_CubeFacets.tab'))
            
        elif self.commandStage == 1:
            
            self.drawInterface(displaySurface)

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()
        
        
        return self.systemState #  loop for the moment.
    
    
    def update(self, displaySurface):

        return self.runCommandDeck(displaySurface)