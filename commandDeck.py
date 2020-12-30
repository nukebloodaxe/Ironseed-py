# -*- coding: utf-8 -*-
"""
Created on Sat May  9 13:10:10 2020

Main Command Deck, central operations for all systems in IronSeed.

Note:  State button logic will crash game for unimplmented states.
TODO:  Ship damage check to see if function available.

@author: Nuke Bloodaxe
"""

import buttons, pygame, sys, os, io, random
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
    def addButton(self, height, width, x, y, returnValue):
        
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
        self.cubeSpinQueue = []  # Queue of targets we spin through.
        self.cubeSpinning = False  # Are we spinning the cube?  (can't interact.)
        self.cubeSpinEnd = int((g.width/320)*50)
        #  Determine the x,y position of the facet when drawn.
        self.relativePosition = (int((g.width/320)*214),
                                 int((g.height/200)*145))


    #  Check to see if the cube has had a button pressed.
    def checkSideButton(self, position):
        
        cubePositionX = position[0] - self.relativePosition[0]
        cubePositionY = position[1] - self.relativePosition[1]
        
        return self.sides[self.currentSide].checkButtonPress((cubePositionX,
                                                              cubePositionY))
    
    #  Initiate a facet change.
    #  ToDo:  Add spin logic.
    def changeFacet(self, newFacet):
        
        self.oldFacet = self.currentSide
        self.currentSide = newFacet
    
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
        self.commandStage = 0  #  What stage of setup/interaction are we at.
        self.systemState = 10
        self.musicState = False
        self.cube = Cube()
        self.theCube = [0, 1, 2, 3, 4, 5, 6]  #  Cube function shortcut.
        self.cubeGraphic = [0, 1, 2, 3, 4, 5, 6]  #  Cube graphic shortcuts.
        self.subFunctions = []  # sub-functions in operation.
        self.buttons = [] #  Command deck buttons, not on cube.
        
        #  Load Graphics Layers
        
        self.mainCubeGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'main-cube.png'))

        #  Sub-Divide cube graphics into correct groups.
        
        self.psychoGraphic = pygame.Surface((50, 44), 0)
        self.psychoGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 0, 50, 44))
        self.psychoGraphicScaled = pygame.transform.scale(self.psychoGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[0] = self.psychoGraphicScaled
        
        self.engineeringGraphic = pygame.Surface((50, 44), 0)
        self.engineeringGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 45, 50, 44))
        self.engineeringGraphicScaled = pygame.transform.scale(self.engineeringGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[1] = self.engineeringGraphicScaled
        
        self.scienceGraphic = pygame.Surface((50, 44), 0)
        self.scienceGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 90, 50, 44))
        self.scienceGraphicScaled = pygame.transform.scale(self.scienceGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[2] = self.scienceGraphicScaled
        
        self.securityGraphic = pygame.Surface((50, 44), 0)
        self.securityGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 135, 50, 44))
        self.securityGraphicScaled = pygame.transform.scale(self.securityGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[3] = self.securityGraphicScaled
        
        self.astrogationGraphic = pygame.Surface((50, 44), 0)
        self.astrogationGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 180, 50, 44))
        self.astrogationGraphicScaled = pygame.transform.scale(self.astrogationGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[4] = self.astrogationGraphicScaled
        
        self.medicalGraphic = pygame.Surface((50, 44), 0)
        self.medicalGraphic.blit(self.mainCubeGraphic, (0, 0), (0, 225, 50, 44))
        self.medicalGraphicScaled = pygame.transform.scale(self.medicalGraphic, (int((g.width/320)*50), int((g.height/200)*44)))
        self.cubeGraphic[5] = self.medicalGraphicScaled
        
        #  Command Deck Graphic
        self.commandDeckGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'main.png'))
        
        #  Prepare Command Deck Graphic for blitting
        self.commandDeckGraphicScaled = pygame.transform.scale(self.commandDeckGraphic, (g.width, g.height))
        
        #  prepare major command deck buttons.
        
        #  Choose Psychometry
        self.buttons.append((0, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*183),
                                                int((g.height/200)*149)))))

        #  Choose Engineering
        self.buttons.append((1, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*183),
                                                int((g.height/200)*161)))))
        
        #  Choose Science
        self.buttons.append((2, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*183),
                                                int((g.height/200)*173)))))
        
        #  Choose Security
        self.buttons.append((3, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*274),
                                                int((g.height/200)*149)))))
        
        #  Choose Astrogation
        self.buttons.append((4, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*274),
                                                int((g.height/200)*161)))))
        
        #  Choose medical
        self.buttons.append((5, buttons.Button(int((g.height/200)*9),
                                               int((g.width/320)*23),
                                               (int((g.width/320)*274),
                                                int((g.height/200)*173)))))
        
        # Choose 
    #  The cube for interaction is fairly involved, it has major functions
    #  which take the player to a seperate screen and therefore class.
    #  However, the sub-functions can act as overlay windows on the command
    #  deck window.
    
    #TODO: Sub-Function list and calls.
    
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
                
    #  Activate a sub-function.
    #  Note: Original game has only 1 window at a time.
    #  Feature Enhancement: Multiple windows with widgets,
    #  hey, it worked for Windows 3.11!
    def subFunctionActivate(self, subFunction):
        
        if subFunction not in self.subFunctions:
            
            randX = int((g.width/200)*random.randint(30, 100))
            randY = int((g.height/200)*random.randint(30, 100))
            self.subFunctions.append(SubFunction(subFunction, randX, randY))
    
    
    #  Interactive panel 0: Psychometry.
    def cubePsycho(self, currentButton):
        
        state = self.systemState
        
        # Psy Eval
        if currentButton == 1:
            
            state = 9
        
        # Crew Status
        elif currentButton == 2:
            
            state = 13
        
        # Planet Comm
        #TODO: Evaluate if comms possible first.
        elif currentButton == 3:
            
            state = 14
            
        
        # Ship Hail
        #TODO: Evaluate if ship comms possible.
        elif currentButton == 4:
        
            #if ship comms possible
            #state = 6
            
            #else:
            # do nothing.
            pass
            
        # Research
        #TODO: Activate research routine for team.
        elif currentButton == 5:
            
            pass
        
        # Crew Comm
        elif currentButton == 6:
            
            state = 8
        
        return state
    
    #  Interactive Panel 1: Engineering.
    def cubeEngineering(self, currentButton):
        
        state = self.systemState
        
        # Damage control - Sub-Function.
        if currentButton == 1:
            
            pass
        
        # Shields - Sub-Function
        elif currentButton == 2:
            
            pass
        
        # Weapons - Sub-Function
        elif currentButton == 3:
            
            pass
        
        # Configure - Sub-Function
        elif currentButton == 4:
            
            pass
        
        # Ship Logs
        elif currentButton == 5:
            
            #state = 15
            pass
        
        # Research
        #TODO: Activate research routine for team.
        elif currentButton == 6:
            
            pass
        
        # Bot Control - Sub-Function
        elif currentButton == 7:
            
            pass
        
        # Creation
        elif currentButton == 8:
            
            #state = 16
            pass
        
        # Cargo
        elif currentButton == 9:
        
            state = 4
            
        return state
    
    #  Interactive Panel 2: Science.
    def cubeScience(self, currentButton):
        
        state = self.systemState
        
        # Short Range - Sub-Function
        if currentButton == 1:
        
            pass
        
        # Long Range - Sub-Function
        elif currentButton == 2:
            
            pass
        
        # System Info - Sub-Function
        elif currentButton == 3:
            
            pass
        
        # Planet Scan
        elif currentButton == 4:
            
            state = 5
        
        # Research
        #TODO: Activate research routine for team.
        elif currentButton == 5:
            
            pass
        
        # Star Logs - Sub-Function
        elif currentButton == 6:
            
            pass
            
        return state
    
    #  Interactive Panel 3: Security.
    #  Note: Not really sub-functions, are ship state changers.
    def cubeSecurity(self, currentButton):
        
        state = self.systemState
            
        # Retreat - Attempt to run away
        if currentButton == 1:
            
            pass
        
        # Shields - Raise Shields (yellow alert?)
        elif currentButton == 2:
            
            pass
        
        # Weapons - Activate Weapons (red alert?)
        elif currentButton == 3:
            
            pass
        
        # Masking - Electronic masking, evasion, silent running (grey alert?)
        elif currentButton == 4:
            
            pass
        
        # Research
        #TODO: Activate research routine for team.
        elif currentButton == 5:
            
            pass
        
        # Drones - combat practice.
        # Attack - Real combat.
        # Note: populate combat queue before entry.
        # Note: Avoid gameover bug with drones.
        elif currentButton in [6, 7]:
            
            #state = 7
            pass
        
        return state
    
    #  Interactive Panel 4: Astrogation.
    def cubeAstrogation(self, currentButton):
        
        state = self.systemState
            
        # Star Map - Sub-Function
        if currentButton == 1:
            
            pass
        
        # Sector Map
        elif currentButton == 2:
            
            #state = 17
            pass
        
        # History Map - Sub-Function
        elif currentButton == 3:
            
            pass
        
        # Quick Stats - Sub-Function
        elif currentButton == 4:
            
            pass
        
        # Target - Sub-Function
        elif currentButton == 5:
            
            pass

        # Research
        #TODO: Activate research routine for team.
        elif currentButton == 6:
            
            pass
        
        # Ship Status - Sub-Function
        elif currentButton == 7:
            
            pass
        
        # Local Info - Sub-Function
        elif currentButton == 8:
            
            pass
        
        return state
    
    #  Interactive Panel 5: Medical.
    def cubeMedical(self, currentButton):
        
        state = self.systemState
        
        # Game Options - Sub-Function
        # Note: This really should be an option on the game main menu.
        if currentButton == 1:
            
            pass
        
        # Time burst - accelerate game clock ticks.
        elif currentButton == 2:
            
            pass
        
        # clear screen - Clear all Sub-Functions, gently.
        elif currentButton == 3:
            
            for check in self.subFunctions:
            
                self.subFunctionDeactivate(check.subFunction)
        
        # Save - Sub-Function
        elif currentButton == 4:
            
            pass
        
        # Load - Sub-Function
        elif currentButton == 5:
            
            pass
        
        #TODO: Activate research routine for team.
        elif currentButton == 6:
            
            pass
        
        # Encode - Sub-Function
        elif currentButton == 7:
            
            pass
        
        # Decode - Sub-Function
        elif currentButton == 8:
            
            pass
        
        # Exit - Quit from the game violently.
        elif currentButton == 9:
            
            sys.exit()
        
        return state

    #  Populate cube function shortcuts.
    def cubeFunctionLoading(self):
        
        self.theCube[0] = self.cubePsycho
        self.theCube[1] = self.cubeEngineering
        self.theCube[2] = self.cubeScience
        self.theCube[3] = self.cubeSecurity
        self.theCube[4] = self.cubeAstrogation
        self.theCube[5] = self.cubeMedical

    #  Mouse button interaction routine.
    #TODO:  Lots of button support.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        cubeCheck = self.cube.checkSideButton(currentPosition)
        
        if cubeCheck[0]:
            
            self.systemState = self.theCube[self.cube.currentSide](cubeCheck[1])
            
        # Debug.
        print("Cube Check: ", cubeCheck[0], " State: ", cubeCheck[1])
        
        #self.systemState = self.theCube[self.cubeFacet](currentPosition)
        
        #  Check buttons for cube facets.
        for button in self.buttons:
            
            changeFacet = button[1].within(currentPosition)
            
            if changeFacet:
                
                self.cube.changeFacet(button[0])
                break
        
        
        return self.systemState
    
    #  Spinning the cube between facets is a trapezoidal transformation.
    #  Note:  only see two surfaces at any one time, no isomeric view.
    def drawCubeSpin(self):
        
        pass
    
    #  Draw command deck interface.
    #  Note: The cube draws itself in at the start using multiple lasers.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        # TODO: Draw planet here.
        displaySurface.blit(self.commandDeckGraphicScaled, (0, 0))
        # TODO: check frames and drawing of spinning cube.
        # Simply draw current cube side for now.
        displaySurface.blit(self.cubeGraphic[self.cube.currentSide],
                            (self.cube.relativePosition[0],
                             self.cube.relativePosition[1]))
        
    
    
    #  Check stage and run routines for initialization, ongoing ops or exit.
    def runCommandDeck(self, displaySurface):
        
        if self.commandStage == 0:
            
            #  We need to ensure our system state is set.
            self.systemState = 10
            
            #  Start deck music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'SECTOR.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.commandStage += 1
            
            #  Construct the cube.
            self.cube.constructCube(os.path.join('Data_Generators', 'Other', 'IronPy_CubeFacets.tab'))
            self.cubeFunctionLoading()
            
        elif self.commandStage == 1:
            
            self.drawInterface(displaySurface)

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()
        
        if self.systemState != 10:
            
            self.commandStage = 0
            self.musicState = False
        
        return self.systemState #  loop for the moment.
    
    
    def update(self, displaySurface):

        return self.runCommandDeck(displaySurface)