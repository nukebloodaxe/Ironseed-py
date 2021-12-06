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

import os, pygame, crew, ship, items, planets, random, buttons
import global_constants as g
import helper_functions as h

class Generator(object):
    def __init__(self, givenShip, givenCrew, loadAndSetup, firstRun=False):
        self.currentShip = givenShip #  Should be initialised to default start values.
        self.systemState = 1 #  By default, the game Generator points at itself.
        self.generationStage = 0 #  The stage of generation are we at.
        self.crew = givenCrew
        self.crewArray = 0  #  Where we are in the crew array.
        #  Note: we only commit the crew to the crew member structure when
        #  the player has confirmed all their choices.
        #  These are crew.crewData[] array positions.
        self.psychometry = -1 #  Role 1 
        self.engineering = -1 #  Role 2
        self.science = -1 #  Role 3
        self.security = -1 #  Role 4
        self.astrogation = -1 #  Role 5
        self.medical = -1 #  Role 6
        #  Handle display area of the crew heartbeat line.
        self.pulseDisplayArea = pygame.Rect((int((g.width/320)*121),
                                             int((g.height/200)*14)),
                                            (int((g.width/320)*174),
                                             int((g.height/200)*74)))
        self.crewPositions = ["", "PSYCHOMETRY", "ENGINEERING", "SCIENCE", "SECURITY", "ASTROGATION", "MEDICAL"]
        
        self.shipSelectStage = 1  #  Indicates if we are selecting Front, Center or rear segments.
        self.crewSelectStage = 1  #  Indicates what type of crew we are selecting.
        self.shipCreator = pygame.image.load(os.path.join('Graphics_Assets', 'char.png'))
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator, (g.width, g.height))
        self.shipCreatorScaled.set_colorkey(g.BLACK)
        self.shipStatisticsNames = ["Gun Emplacements", "Maximum Fuel",
                                    "Cargo Capacity", "Ship Mass",
                                    "Max Acceleration", "Maximum Hull Points"]
        self.shipStatistics = []  #  Used later for drawing routine.
    
        #self.crewSelector = pygame.image.load("Graphics_Assets\\char2.png")
        #self.crewSelectorScaled = pygame.transform.scale(self.crewSelector, (g.width, g.height))
        #self.crewSelectorScaled.set_colorkey(g.BLACK)
        self.crewSelectorScaled = self.shipCreatorScaled
        
        #  Load ship tiles.
        
        self.frontHeavy = pygame.image.load(os.path.join('Graphics_Assets', 'IS_F_HEAVY.png'))
        self.frontHeavyScaled = pygame.transform.scale(self.frontHeavy, ( int((g.width/320)*self.frontHeavy.get_width()), int((g.height/200)*self.frontHeavy.get_height())))
        self.frontHeavyScaled.set_colorkey(g.BLACK)
        
        self.frontLight = pygame.image.load(os.path.join('Graphics_Assets', 'IS_F_LIGHT.png'))
        self.frontLightScaled = pygame.transform.scale(self.frontLight, ( int((g.width/320)*self.frontLight.get_width()), int((g.height/200)*self.frontLight.get_height())))
        self.frontLightScaled.set_colorkey(g.BLACK)
        
        self.frontStrategic = pygame.image.load(os.path.join('Graphics_Assets', 'IS_F_STRATEGIC.png'))
        self.frontStrategicScaled = pygame.transform.scale(self.frontStrategic, ( int((g.width/320)*self.frontStrategic.get_width()), int((g.height/200)*self.frontStrategic.get_height())))
        self.frontStrategicScaled.set_colorkey(g.BLACK)
        
        self.centerShuttle = pygame.image.load(os.path.join('Graphics_Assets', 'IS_C_SHUTTLE.png'))
        self.centerShuttleScaled = pygame.transform.scale(self.centerShuttle, ( int((g.width/320)*self.centerShuttle.get_width()), int((g.height/200)*self.centerShuttle.get_height())))
        self.centerShuttleScaled.set_colorkey(g.BLACK)
        
        self.centerAssault = pygame.image.load(os.path.join('Graphics_Assets', 'IS_C_ASSAULT.png'))
        self.centerAssaultScaled = pygame.transform.scale(self.centerAssault, ( int((g.width/320)*self.centerAssault.get_width()), int((g.height/200)*self.centerAssault.get_height())))
        self.centerAssaultScaled.set_colorkey(g.BLACK)
        
        self.centerStorm = pygame.image.load(os.path.join('Graphics_Assets', 'IS_C_STORM.png'))
        self.centerStormScaled = pygame.transform.scale(self.centerStorm, ( int((g.width/320)*self.centerStorm.get_width()), int((g.height/200)*self.centerStorm.get_height())))
        self.centerStormScaled.set_colorkey(g.BLACK)
        
        self.rearTransport = pygame.image.load(os.path.join('Graphics_Assets', 'IS_R_TRANSPORT.png'))
        self.rearTransportScaled = pygame.transform.scale(self.rearTransport, ( int((g.width/320)*self.rearTransport.get_width()), int((g.height/200)*self.rearTransport.get_height())))
        self.rearTransportScaled.set_colorkey(g.BLACK)
        
        self.rearFrigate = pygame.image.load(os.path.join('Graphics_Assets', 'IS_R_FRIGATE.png'))
        self.rearFrigateScaled = pygame.transform.scale(self.rearFrigate, ( int((g.width/320)*self.rearFrigate.get_width()), int((g.height/200)*self.rearFrigate.get_height())))
        self.rearFrigateScaled.set_colorkey(g.BLACK)
        
        self.rearCruiser = pygame.image.load(os.path.join('Graphics_Assets', 'IS_R_CRUISER.png'))
        self.rearCruiserScaled = pygame.transform.scale(self.rearCruiser, ( int((g.width/320)*self.rearCruiser.get_width()), int((g.height/200)*self.rearCruiser.get_height())))
        self.rearCruiserScaled.set_colorkey(g.BLACK)
        
        #  Load ball animation and resize all frames into 30 frame array.
        self.ballSurface = pygame.image.load(os.path.join('Graphics_Assets', 'charani.png'))
        self.ballFrames = []
        self.prepareBallFrames()
        
        #  Set music state, needs to be reset to false on exit.
        self.musicState = False
        
        #  Animations in effect
        #  Note:  These only take effect between stages.  Lower then raise.
        self.raiseBall = False
        self.raiseBallFrame = 0  #  Max 30
        self.lowerBall = False
        self.lowerBallFrame = 0  #  Max 30.
        
        self.changePortrait = False
        self.oldPortrait = 0
        self.newPortrait = 0
        
        #  Define button positions scaled from a 320x200 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.accept = buttons.Button(int((g.height/200)*8),
                                  int((g.width/320)*31),
                                  (int((g.width/320)*280), int((g.height/200)*133)))
        self.reject = buttons.Button(int((g.height/200)*8),
                                  int((g.width/320)*31),
                                  (int((g.width/320)*280), int((g.height/200)*141)))
        self.up = buttons.Button(int((g.height/200)*10),
                                  int((g.width/320)*12),
                                  (int((g.width/320)*283), int((g.height/200)*150)))
        self.down = buttons.Button(int((g.height/200)*10),
                                  int((g.width/320)*12),
                                  (int((g.width/320)*283), int((g.height/200)*165)))
        
        #  Generate planetary systems.
        if not firstRun:

            planets.loadPlanetarySystems(loadAndSetup)
            planets.initialisePlanets(loadAndSetup)
            planets.populatePlanetarySystems(loadAndSetup)
    
    #  take the loaded ball texture and divide it into its component frames,
    #  Assigning them to the animation array.
    #  Note:  Original uses more sensible data array file.
    def prepareBallFrames(self):
        #  6 units Wide.  5 Units high.
        for y in range(0, 5):
            
            for x in range(0, 6):
                
                #  Top and bottom border of 1 pixel.
                #  Right border of 1 pixel.
                #  Each frame 49 pixels wide.
                #  Each frame 33 pixels high.
                sourceRectangle = ((x*50),(y*35), 49, 33 )
                frame = pygame.Surface((48, 33))
                frame.blit(self.ballSurface,(0, 0), sourceRectangle)
                #  The resizing procedure does introduce innaccuracy, but
                #  unavoidable right now.
                resizeFrame = pygame.transform.scale(frame, ( int((g.width/320)*frame.get_width()), int((g.height/200)*frame.get_height())))
                self.ballFrames.append(resizeFrame)
            
    #  Draw a portrait of a crewmember, if the swap animation is in effect we
    #  draw the old portrait being changed to the new one.
    def drawPortrait(self, portrait):
        
        pass
    
    #  Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        
        crewType = "Stowaway"  #  This should not happen!
        
        if self.crewSelectStage == 1:
            
            crewType = "Psychometry"
            
        elif self.crewSelectStage == 2:
            
            crewType = "Engineering"
            
        elif self.crewSelectStage == 3:
            
            crewType = "Science"
            
        elif self.crewSelectStage == 4:
            
            crewType = "Security"
            
        elif self.crewSelectStage == 5:
            
            crewType = "Astrogation"
            
        elif self.crewSelectStage == 6:
            
            crewType = "Medical"
            
        else:
            
            pass
        
        displaySurface.fill(g.BLACK)
        
        #  Print what we are doing.
        h.renderText(["Crew Selection", crewType], g.font, displaySurface, g.WHITE, 15, (g.width/320)*179, (g.height/200)*99, True)
        
        #  Render the array containing the ship stat info.
        
        #  Name of Potential Crewmember.
        h.renderText([crew.CrewData[self.crewArray].name], g.font, displaySurface, g.WHITE, 0, (g.width/320)*3, (g.height/200)*120)
        
        #  Render Bio column of text.
        h.renderText(crew.CrewData[self.crewArray].bio, g.font, displaySurface, g.WHITE, 15, (g.width/320)*3, (g.height/200)*135)
        
        displaySurface.blit(self.crewSelectorScaled, (0, 0))        
        
        #  Render pulse line.
        #self.drawStatusLine(displaySurface, crew.CrewData[self.crewArray])
        crew.CrewData[self.crewArray].drawStatusLine(displaySurface, self.pulseDisplayArea)
        
        #  Render crewmember image.
        displaySurface.blit(crew.CrewData[self.crewArray].resizedImage, ((g.width/320)*13, (g.height/200)*7))
        
    #  Draw the ball, raising or lowering.
    def drawBall(self, displaySurface):
        
        if self.lowerBall:
            
            displaySurface.blit(self.ballFrames[self.lowerBallFrame], ((g.width/320)*22, (g.height/200)*81))
            self.lowerBallFrame += 1
            
            if self.lowerBallFrame >= 30:
                
                self.lowerBall = False
                self.raiseBall = True
                self.lowerBallFrame = 0
            
        elif self.raiseBall:
            
            displaySurface.blit(self.ballFrames[29 - self.raiseBallFrame], ((g.width/320)*22, (g.height/200)*81))
            self.raiseBallFrame += 1
            
            if self.raiseBallFrame >= 30:
                
                self.raiseBall = False
                self.raiseBallFrame = 0
                
        else:  #  Just draw the raised ball; default underlying image.
        
            pass

    #  Draw all ship related surfaces
    def drawShip(self, displaySurface):

        shipFront = self.frontHeavyScaled
        shipCenter = self.centerShuttleScaled
        shipRear = self.rearTransportScaled

        if self.currentShip.frontHull == 1:
            
            shipFront = self.frontHeavyScaled
        
        elif self.currentShip.frontHull == 2:
            
            shipFront = self.frontLightScaled
            
        elif self.currentShip.frontHull == 3:
            
            shipFront = self.frontStrategicScaled
            
        else:
            
            pass

        if self.currentShip.centerHull == 1:

            shipCenter = self.centerShuttleScaled

        elif self.currentShip.centerHull == 2:

            shipCenter = self.centerAssaultScaled

        elif self.currentShip.centerHull == 3:

            shipCenter = self.centerStormScaled
            
        else:
            
            pass

        if self.currentShip.rearHull == 1:

            shipRear = self.rearTransportScaled

        elif self.currentShip.rearHull == 2:

            shipRear = self.rearFrigateScaled

        elif self.currentShip.rearHull == 3:

            shipRear = self.rearCruiserScaled
            
        else:
            
            pass

        # 119, 99 - Text 0,0 position.

        displaySurface.fill(g.BLACK)
        displaySurface.blit(shipFront, ((g.width/320)*121, (g.height/200)*14))
        displaySurface.blit(shipCenter, ((g.width/320)*179, (g.height/200)*14))
        displaySurface.blit(shipRear, ((g.width/320)*237, (g.height/200)*14))

        #  Highlight the area of the ship being changed.
        #  This is not canon, but I accidentally made a better ship constructor.
        #  Which is what happens when you're coding something up from memory
        #  before checking the original game itself.
        if self.shipSelectStage == 1:
            
            rectangle = ((g.width/320)*121, (g.height/200)*14, (g.width/320)*58, (g.height/200)*75)
            pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)
            
        elif self.shipSelectStage == 2:
            
            rectangle = ((g.width/320)*179, (g.height/200)*14, (g.width/320)*58, (g.height/200)*75)
            pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)
        
        elif self.shipSelectStage == 3:
            
            rectangle = ((g.width/320)*237, (g.height/200)*14, (g.width/320)*58, (g.height/200)*75)
            pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)
        
        else:
            
            pass
        
        #  Print what we are doing.
        h.renderText(["Ship Selection"], g.font, displaySurface, g.WHITE, 0, (g.width/320)*179, (g.height/200)*99, True)
        
        #  Render the array containing the ship stat info.
        
        #  Ship Name/Type.
        h.renderText([self.currentShip.name], g.font, displaySurface, g.WHITE, 0, (g.width/320)*130, (g.height/200)*120, True)
        
        #  Render left column of text.
        h.renderText(self.shipStatisticsNames, g.font, displaySurface, g.WHITE, 20, (g.width/320)*3, (g.height/200)*140)
        
        #  Render right column of values.
        self.shipStatistics = [str(self.currentShip.gunMax),
                               str(round(self.currentShip.maxFuel, 2)) + " KG",
                               str(self.currentShip.cargoMax) + " Units",
                               str(round(self.currentShip.mass, 2)) + " Mt",
                               str(round(self.currentShip.acceleration, 2)) + " M/S Sqr",
                               str(self.currentShip.hullMax) + " Pts"]
        h.renderText(self.shipStatistics, g.font, displaySurface, g.WHITE, 20, (g.width/320)*180, (g.height/200)*140)
        
        displaySurface.blit(self.shipCreatorScaled, (0, 0))
        
    
    #  On end, save the data that has been generated to a filename of users choice.
    #  Note:  This is actually stored by slot, with a dump of object memory into
    #  a file per object.  Restoration should be a case of loading each object into memory,
    #  overwriting the current binary object in each case.
    def saveData(self, fileName="Default"):
        
        pass
    
    #  Update function for main game loop.
    def update(self, displaySurface):
        
        return self.runGenerator(displaySurface)
    
    #  Adjust a given crewmember assignment based on selection stage.
    def assignCrew(self):
        
        if self.crewSelectStage == 1:
            
            self.psychometry = self.crewArray
        
        elif self.crewSelectStage == 2:
            
            self.engineering = self.crewArray
        
        elif self.crewSelectStage == 3:
            
            self.science = self.crewArray
            
        elif self.crewSelectStage == 4:
            
            self.security = self.crewArray
            
        elif self.crewSelectStage == 5:
            
            self.astrogation = self.crewArray
            
        elif self.crewSelectStage == 6:
            
            self.medical = self.crewArray
    
    #  Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        #  Turn off mouse interaction during transition animation.
        if self.raiseBall == True or self.lowerBall == True:
            
            return self.systemState
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.accept.within(currentPosition):
            
            if self.shipSelectStage < 4:
            
                self.shipSelectStage += 1
                
                if self.shipSelectStage == 4:
                    
                    self.generationStage += 1
                    self.lowerBall = True
            
            elif self.crewSelectStage < 7:

                self.assignCrew()
                self.crewSelectStage += 1
                
                if self.crewSelectStage < 7:
                    
                    self.crewArray = crew.findCrew(self.crewPositions[self.crewSelectStage], self.crewArray, False)
                
                if self.crewSelectStage == 7:
                    
                    #  Final crew assignment.
                    self.crew.setCrew(crew.CrewData[self.psychometry],
                                      crew.CrewData[self.engineering],
                                      crew.CrewData[self.science],
                                      crew.CrewData[self.security],
                                      crew.CrewData[self.astrogation],
                                      crew.CrewData[self.medical])
                    
                    self.generationStage += 1
            
        elif self.reject.within(currentPosition):
            
            if self.shipSelectStage < 4 and self.shipSelectStage > 1:
            
                self.shipSelectStage -= 1
                
            if self.crewSelectStage == 1 and self.shipSelectStage == 4:
                
                self.generationStage -= 1
                self.shipSelectStage = 1
                self.lowerBall = True
                
            elif self.crewSelectStage > 1:
                
                self.crewSelectStage -= 1
                self.crewArray = crew.findCrew(self.crewPositions[self.crewSelectStage], self.crewArray, False)
            
        elif self.up.within(currentPosition):
            
            if self.shipSelectStage == 1:
                
                if self.currentShip.frontHull <= 2:
                    
                    self.currentShip.frontHull += 1
                    
                else:
                    
                    self.currentShip.frontHull = 1
                
            elif self.shipSelectStage == 2:
                
                if self.currentShip.centerHull <= 2:
                    
                    self.currentShip.centerHull += 1
                    
                else:
                    
                    self.currentShip.centerHull = 1
            
            elif  self.shipSelectStage == 3:
                
                if self.currentShip.rearHull <= 2:
                    
                    self.currentShip.rearHull += 1
                    
                else:
                    
                    self.currentShip.rearHull = 1
                
            #  Fall through and check crew selection.
            if self.generationStage == 2:
                
                self.crewArray = crew.findCrew(self.crewPositions[self.crewSelectStage], self.crewArray, False)
            
            
        elif self.down.within(currentPosition):
            
            if self.shipSelectStage == 1:
                    
                if self.currentShip.frontHull == 1:
                    
                    self.currentShip.frontHull = 3
                    
                else:
                    
                    self.currentShip.frontHull -= 1
                
            elif self.shipSelectStage == 2:
                
                if self.currentShip.centerHull == 1:
                    
                    self.currentShip.centerHull = 3
                    
                else:
                    
                    self.currentShip.centerHull -= 1
            
            elif  self.shipSelectStage == 3:
                
                if self.currentShip.rearHull == 1:
                    
                    self.currentShip.rearHull = 3
                    
                else:
                    
                    self.currentShip.rearHull -= 1
                
            #  Fall through and check crew selection.    
            if self.generationStage == 2:
                
                self.crewArray = crew.findCrew(self.crewPositions[self.crewSelectStage], self.crewArray, True)
                
        return self.systemState
    
    #  Main generator game loop.
    def runGenerator(self, displaySurface):
        
        #  Preparation routine
        if self.generationStage == 0:
            
            #  Start generator screen music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'CHARGEN.OGG'))
                pygame.mixer.music.play()
                self.systemState = 1
                self.musicState = True
                self.generationStage += 1
                
        #  Ship generator.
        elif self.generationStage == 1 and self.lowerBall == False:
            
            self.currentShip.initialiseShip()
            self.drawShip(displaySurface)
            self.drawBall(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
            
        elif self.generationStage == 1 and self.lowerBall:
            
            self.drawCrew(displaySurface)
            self.drawBall(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
        
        elif self.generationStage == 2 and self.lowerBall:
            
            self.drawShip(displaySurface)
            self.drawBall(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
            
        #  Crew Selection.
        elif self.generationStage == 2 and self.lowerBall == False:
            
            self.drawCrew(displaySurface)
            self.drawBall(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
        
        #  Roguelike game initialisation.
        elif self.generationStage == 3:
        
            #  By default this is already done on starting IronSeed fresh.
            #  The only time we need to do it again is if we are starting
            #  a new game after loading an old one, or running a fresh game.
            self.generationStage += 1 #  TODO - Variable gen.
    
        #  Save game.
        elif self.generationStage == 4:
            
            self.systemState = 10  #  We now jump to the test command deck!
            self.musicState = False
            self.crewSelectStage = 0
            self.shipSelectStage = 0
            self.generationStage = 0
            #self.systemState = 12  #  Save Game.
            
        else:
            
            self.musicState = False
            self.crewSelectStage = 0
            self.shipSelectStage = 0
            self.generationStage = 0
            return 2  #  Go to main menu.
        
        # rewind and start music playing again if track end reached.
        if not pygame.mixer.music.get_busy():
            
            pygame.mixer.music.play()
        
        return self.systemState
    
    