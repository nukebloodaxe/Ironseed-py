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

import io, pygame, crew, ship, items, planets, random, buttons
import global_constants as g
import helper_functions as h

class Generator(object):
    def __init__(self, givenShip, givenCrew):
        self.currentShip = givenShip #  Should be initialised to default start values.
        self.systemState = 1 #  By default, the game Generator points at itself.
        self.generationStage = 0 #  The stage of generation are we at.
        self.portraits = []
        self.crew = givenCrew
        self.shipSelectStage = 1  #  Indicates if we are selecting Front, Center or rear segments.
        self.crewSelectStage = 1  #  Indicates what type of crew we are selecting.
        self.shipCreator = pygame.image.load("Graphics_Assets\\char.png")
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator, (g.width, g.height))
        self.shipCreatorScaled.set_colorkey(g.BLACK)
        self.shipStatisticsNames = ["Gun Emplacements", "Maximum Fuel",
                                    "Cargo Capacity", "Ship Mass",
                                    "Max Acceleration", "Maximum Hull Points"]
        self.shipStatistics = []  #  Used later for drawing routine.
    
        self.crewSelector = pygame.image.load("Graphics_Assets\\char2.png")
        self.crewSelectorScaled = pygame.transform.scale(self.crewSelector, (g.width, g.height))
        self.crewSelectorScaled.set_colorkey(g.BLACK)
        
        #  Load ship tiles.
        
        self.frontHeavy = pygame.image.load("Graphics_Assets\\IS_F_HEAVY.png")
        self.frontHeavyScaled = pygame.transform.scale(self.frontHeavy, ( int((g.width/320)*self.frontHeavy.get_width()), int((g.height/200)*self.frontHeavy.get_height())))
        self.frontHeavyScaled.set_colorkey(g.BLACK)
        
        self.frontLight = pygame.image.load("Graphics_Assets\\IS_F_LIGHT.png")
        self.frontLightScaled = pygame.transform.scale(self.frontLight, ( int((g.width/320)*self.frontLight.get_width()), int((g.height/200)*self.frontLight.get_height())))
        self.frontLightScaled.set_colorkey(g.BLACK)
        
        self.frontStrategic = pygame.image.load("Graphics_Assets\\IS_F_STRATEGIC.png")
        self.frontStrategicScaled = pygame.transform.scale(self.frontStrategic, ( int((g.width/320)*self.frontStrategic.get_width()), int((g.height/200)*self.frontStrategic.get_height())))
        self.frontStrategicScaled.set_colorkey(g.BLACK)
        
        self.centerShuttle = pygame.image.load("Graphics_Assets\\IS_C_SHUTTLE.png")
        self.centerShuttleScaled = pygame.transform.scale(self.centerShuttle, ( int((g.width/320)*self.centerShuttle.get_width()), int((g.height/200)*self.centerShuttle.get_height())))
        self.centerShuttleScaled.set_colorkey(g.BLACK)
        
        self.centerAssault = pygame.image.load("Graphics_Assets\\IS_C_ASSAULT.png")
        self.centerAssaultScaled = pygame.transform.scale(self.centerAssault, ( int((g.width/320)*self.centerAssault.get_width()), int((g.height/200)*self.centerAssault.get_height())))
        self.centerAssaultScaled.set_colorkey(g.BLACK)
        
        self.centerStorm = pygame.image.load("Graphics_Assets\\IS_C_STORM.png")
        self.centerStormScaled = pygame.transform.scale(self.centerStorm, ( int((g.width/320)*self.centerStorm.get_width()), int((g.height/200)*self.centerStorm.get_height())))
        self.centerStormScaled.set_colorkey(g.BLACK)
        
        self.rearTransport = pygame.image.load("Graphics_Assets\\IS_R_TRANSPORT.png")
        self.rearTransportScaled = pygame.transform.scale(self.rearTransport, ( int((g.width/320)*self.rearTransport.get_width()), int((g.height/200)*self.rearTransport.get_height())))
        self.rearTransportScaled.set_colorkey(g.BLACK)
        
        self.rearFrigate = pygame.image.load("Graphics_Assets\\IS_R_FRIGATE.png")
        self.rearFrigateScaled = pygame.transform.scale(self.rearFrigate, ( int((g.width/320)*self.rearFrigate.get_width()), int((g.height/200)*self.rearFrigate.get_height())))
        self.rearFrigateScaled.set_colorkey(g.BLACK)
        
        self.rearCruiser = pygame.image.load("Graphics_Assets\\IS_R_CRUISER.png")
        self.rearCruiserScaled = pygame.transform.scale(self.rearCruiser, ( int((g.width/320)*self.rearCruiser.get_width()), int((g.height/200)*self.rearCruiser.get_height())))
        self.rearCruiserScaled.set_colorkey(g.BLACK)
        
        #  define button positions for a 640x480 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        
        #  Set music state, needs to be reset to false on exit.
        self.musicState = False
        
        #  Animations in effect
        self.raiseBall = False
        self.raiseBallFrame = 0
        self.lowerBall = False
        self.lowerBallFrame = 0
        
        self.changePortrait = False
        self.oldPortrait = 0
        self.newPortrait = 0
        
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.accept = buttons.Button(15, 60, (559, 317)) # Based on 640x480
        self.reject = buttons.Button(15, 60, (559, 337))
        self.up = buttons.Button(20, 24, (566, 359))
        self.down = buttons.Button(20, 24, (566, 394))
        
        #  Generate planetary systems.
        planets.loadPlanetarySystems()
        planets.initialisePlanets()
        planets.populatePlanetarySystems()
        
    def loadPortraits(self, number=32, file="Graphics_Assets\\image", fileType=".png"):
        self.portraits.append("dummy") #  dummy entry.
        for image in range(1,number+1):
            if image < 10:
                self.portraits.append(pygame.image.load(file+'0'+str(image)+fileType))
            else:
                self.portraits.append(pygame.image.load(file+str(image)+fileType))
    
    #  Draw a portrait of a crewmember, if the swap animation is in effect we
    #  draw the old portrait being changed to the new one.
    def drawPortrait(self, portrait):
        
        pass
    
    #  Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        displaySurface.blit(self.crewSelectorScaled,(0,0))        
        
    #  Draw the sine-wave status line.
    def drawStatusLine(self, crewMember, displaySurface):
        
        
        
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
                               str(self.currentShip.maxFuel) + " KG",
                               str(self.currentShip.cargoMax) + " Units",
                               str(self.currentShip.mass) + " Mt",
                               str(self.currentShip.acceleration) + " M/S Sqr",
                               str(self.currentShip.hullMax) + " Pts"]
        h.renderText(self.shipStatistics, g.font, displaySurface, g.WHITE, 20, (g.width/320)*180, (g.height/200)*140)
        
        displaySurface.blit(self.shipCreatorScaled, (0, 0))
        
    
    #  On end, save the data that has been generated to a filename of users choice.
    def saveData(self, fileName="Default"):
        
        pass
    
    #  Update function for main game loop.
    def update(self, displaySurface):
        return self.runGenerator(displaySurface)
    
    #  Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.accept.within(currentPosition):
            
            if self.shipSelectStage < 4:
            
                self.shipSelectStage += 1
                
                if self.shipSelectStage == 4:
                    
                    self.generationStage += 1
            
            if self.crewSelectStage < 7:
                
                self.crewSelectStage += 1
                
                if self.crewSelectStage == 7:
                    
                    self.generationStage += 1
            
        elif self.reject.within(currentPosition):
            
            if self.shipSelectStage < 4 and self.shipSelectStage > 1:
            
                self.shipSelectStage -= 1
                
            if self.crewSelectStage == 1 and self.shipSelectStage == 4:
                
                self.generationStage -= 1
                self.shipSelectStage = 1
                
            elif self.crewSelectStage > 1:
                
                self.crewSelectStage -= 1
            
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
        
        return self.systemState
    
    #  Main generator game loop.
    def runGenerator(self, displaySurface):
        #  Preparation routine
        if self.generationStage == 0:
            #  Start main intro music
            if self.musicState == False:
                pygame.mixer.music.load("sound\\CHARGEN.OGG")
                pygame.mixer.music.play()
                self.musicState = True
                self.generationStage += 1
                
        #  Ship generator.
        elif self.generationStage == 1:
            self.currentShip.initialiseShip()
            self.drawShip(displaySurface)
        
        #  Crew Selection.
        elif self.generationStage == 2:
            self.drawCrew(displaySurface)
        
        #  Roguelike game initialisation.
        elif self.generationStage == 3:
        
            pass
    
        #  Save game.
        elif self.generationStage == 4:
            
            
            self.systemState = 12
            
        else:
            self.musicState = False
            return 2  #  Go to main menu.
        
        return self.systemState
    
    