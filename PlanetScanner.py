# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:35:51 2019
Planet Scanner
@author: Nuke Bloodaxe
"""

# This requires rather a lot of things to be working beforehand.
# However, it also is the best way to test the planet related code.

import random, math, io, time, os, buttons, planets, pygame, items, ship
import global_constants as g
import helper_functions as h

# This class is essentially a self-contained game called "The planet scanner" ;)
class PlanetScanner(object):
    
    def __init__(self, playerShip):
        
        self.scannerStage = 0 # what we are doing.
        self.ironSeed = playerShip
        self.probotCount = self.ironSeed.getItemQuantity("Probot")
        self.scanning = [False, False, False, False, False]
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        
        # Up to 4 probots can be partaking in a scan
        self.probot1 = [0,0] # red dot position
        self.probot2 = [0,0]
        self.probot3 = [0,0]
        self.probot4 = [0,0]
        
        self.probotStatus = [1, 1, 1, 1]
        #  Status, in order from 0:
        #  Scanning, Docked, Refueling, Transit To, Transit Back.
        
        #  Probots have 4 acivity monitors on main screen, these are the
        #  bounding-box positions.
        self.probot1BoundingBox = (281,
                                  18,
                                  312,
                                  43)

        self.probot2BoundingBox = (281,
                                  58,
                                  312,
                                  83)

        self.probot3BoundingBox = (281,
                                  98,
                                  312,
                                  123)
        
        self.probot4BoundingBox = (281,
                                  138,
                                  312,
                                  163)
        
        self.probot1BoundingBoxScaled = (int((g.width/320)*281),
                                        int((g.height/200)*18),
                                        int((g.width/320)*312),
                                        int((g.height/200)*43))
        
        self.probot2BoundingBoxScaled = (int((g.width/320)*281),
                                        int((g.height/200)*58),
                                        int((g.width/320)*312),
                                        int((g.height/200)*83))
        
        self.probot3BoundingBoxScaled = (int((g.width/320)*281),
                                        int((g.height/200)*98),
                                        int((g.width/320)*312),
                                        int((g.height/200)*123))
        
        self.probot4BoundingBoxScaled = (int((g.width/320)*281),
                                        int((g.height/200)*138),
                                        int((g.width/320)*312),
                                        int((g.height/200)*163))
        
        # Descriptors
        self.probotFeedback = ["Docked", "Deployed", "Orbiting", "Gathering",
                               "Analyzing", "Returning", "Refueling",
                               "Destroyed", "Docked"]
        self.scanTypes = ["Lithosphere", "Hydrosphere", "Atmosphere", "Biosphere",
                          "Anomaly"]
        self.planetActivity = ["Calm", "Mild", "Moderate", "Heavy", "Massive"]
        self.lifeforms = ["Avian", "Monoped", "Biped", "Triped", "Quadraped",
                          "Octaped", "Aquatics", "Fungi", "Carniferns",
                          "Crystalline", "Symbiots", "Floaters"]
        
        #  Planet Scanner related graphics layers.
        self.scanInterface = pygame.image.load(os.path.join('Graphics_Assets', 'landform.png'))
        self.scanInterfaceScaled = pygame.transform.scale(self.scanInterface, (g.width, g.height))
        self.scanInterfaceScaled.set_colorkey(g.BLACK)
        
        #  Probot frames, Frames have following dimensions: 
        #  20 wide x 22 high.
        #  Scan text 281, 18:301, 40.
        #  Docked 281, 58:301, 80.
        #  Refueling 281, 98:301, 120.
        #  Launched and in transit.  281, 138:301, 160.
        #  When no probot present, blank area of unit with black square.
        
        self.probotScanning = pygame.Surface((31, 24), 0)
        self.probotScanning.blit(self.scanInterface, (0, 0), self.probot1BoundingBox )
        self.probotScanningScaled = pygame.transform.scale(self.probotScanning, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotDocked = pygame.Surface((31, 24), 0)
        self.probotDocked.blit(self.scanInterface, (0, 0), self.probot2BoundingBox )
        self.probotDockedScaled = pygame.transform.scale(self.probotDocked, (int((g.width/320)*30), int((g.height/200)*24)))
        
        self.probotRefuel = pygame.Surface((31, 24), 0)
        self.probotRefuel.blit(self.scanInterface, (0, 0), self.probot3BoundingBox )
        self.probotRefuelScaled = pygame.transform.scale(self.probotRefuel, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotTransit = pygame.Surface((31, 24), 0)
        self.probotTransit.blit(self.scanInterface, (0, 0), self.probot4BoundingBox )
        self.probotTransitScaled = pygame.transform.scale(self.probotTransit, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotEmpty = pygame.Surface((31, 24), 0)
        self.probotEmptyScaled = pygame.transform.scale(self.probotEmpty, (int((g.width/320)*31), int((g.height/200)*24)))
        
        #  Landform bounding area for planet texture
        self.mainViewBoundary = (int((g.width/320)*28),
                                 int((g.height/200)*13),
                                 int((g.width/320)*239),
                                 int((g.height/200)*119))
        
        #  Zoomed view bounding area for planet texture.
        self.zoomedViewBoundary = (int((g.width/320)*206),
                                   int((g.height/200)*139),
                                   int((g.width/320)*59),
                                   int((g.height/200)*59))
        
        #  Selected zone for zoomedViewBoundary; default = top left corner.
        self.zoomedViewBoundary = (int((g.width/320)*28),
                                   int((g.height/200)*13),
                                   int((g.width/320)*59),
                                   int((g.height/200)*59))
        
        self.zoomLevel = 0  #  The zoom applied to the zoom view.  Max 3.
        
        #  bounding for writing graphic = (28, 13, 18, 15)
        
        #  define button positions:  Scaling experiment.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.land = buttons.Button(0, 0, (0, 0))
        self.sea = buttons.Button(0, 0, (0, 0))
        self.air = buttons.Button(0, 0, (0, 0))
        self.life = buttons.Button(0, 0, (0, 0))
        self.anomaly = buttons.Button(0, 0, (0, 0))
        self.exit = buttons.Button(0, 0, (0, 0))
        self.next = buttons.Button(0, 0, (0, 0))
        self.previous = buttons.Button(0, 0, (0, 0))
        self.zoomIn = buttons.Button(0, 0, (0, 0))
        self.zoomOut = buttons.Button(0, 0, (0, 0))
        self.Retrieve = buttons.Button(0, 0, (0, 0))
        
        # Special
        self.planetMap = buttons.Button(int((g.width/320)*239), int((g.height/200)*119), (int((g.width/320)*28), int((g.height/200)*13)))
        
        #  The planet object.
        self.thePlanet = "placeholder"
        
        #  Music/Sound handlers.
        self.musicState = False
        
        self.systemState = 5
        
    # Launch probots for a scan
    def launchProbots(self):
        
        pass
    
    # The planet we will scan for anomalies etc.
    def scanPlanet(self):
        
        pass
    
    # Retrieve anomalies and put into ship cargo.
    def retrieveAnomalies(self):
        
        pass
    
    def update(self, displaySurface):
        
        return self.runScanner(displaySurface)
    
    # Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.land.within(currentPosition):
            
            pass
        
        elif self.sea.within(currentPosition):
            
            pass
        
        elif self.air.within(currentPosition):
            
            pass
        
        elif self.life.within(currentPosition):
            
            pass
        
        elif self.anomaly.within(currentPosition):
            
            pass
        
        elif self.exit.within(currentPosition):
            
            pass
        
        elif self.next.within(currentPosition):
            
            pass
        
        elif self.previous.within(currentPosition):
            
            pass
        
        elif self.zoomIn.within(currentPosition):
            
            if self.zoomLevel < 3:
                self.zoomLevel += 1
        
        elif self.zoomOut.within(currentPosition):
            
            if self.zoomLevel > 0:
                self.zoomLevel -= 1
        
        elif self.Retrieve.within(currentPosition):
            
            pass
        
        elif self.planetMap.within(currentPosition):
            
            #  Change view point for zoomed view.
            self.zoomedViewBoundary = (currentPosition[0],
                                       currentPosition[1],
                                       self.zoomedViewBoundary[2],
                                       self.zoomedViewBoundary[3])
        
        return self.systemState
    
    #  Draw a probot status monitor.
    #  stage is the probot frame to draw.
    #  destination is a pygame rect
    #  TODO:  transit, complex planet resize required.
    def drawProbotMonitor(self, displaySurface, stage, destination):
        
        if stage == 0:
            
            displaySurface.blit(self.probotScanningScaled, destination)
            
        elif stage == 1:
            
            displaySurface.blit(self.probotDockedScaled, destination)
        
        elif stage == 2:
            
            displaySurface.blit(self.probotRefuelScaled, destination)
            
        elif stage == 3:
            
            displaySurface.blit(self.probotTransitScaled, destination)
            
        elif stage == 4:
            
            displaySurface.blit(self.probotTransitScaled, destination)
            
        else:
            
             displaySurface.blit(self.probotEmptyScaled, destination)
    
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.scanInterfaceScaled, (0, 0))
        displaySurface.blit(self.thePlanet.planetTexture, self.mainViewBoundary)
        
        #  I know this looks strange, but it is efficient.
        
        if self.probotCount >= 1:
            
            self.drawProbotMonitor(displaySurface,
                                   self.probotStatus[0],
                                   self.probot1BoundingBoxScaled)
        else:
            
            self.drawProbotMonitor(displaySurface,
                                   99,
                                   self.probot1BoundingBoxScaled)
        
        if self.probotCount >= 2:
            
            self.drawProbotMonitor(displaySurface,
                                   self.probotStatus[1],
                                   self.probot2BoundingBoxScaled)
        else:
            
            self.drawProbotMonitor(displaySurface,
                                   99,
                                   self.probot2BoundingBoxScaled)
            
        if self.probotCount >= 3:
            
            self.drawProbotMonitor(displaySurface,
                                   self.probotStatus[2],
                                   self.probot3BoundingBoxScaled)
        else:
            
            self.drawProbotMonitor(displaySurface,
                                   99,
                                   self.probot3BoundingBoxScaled)
            
        if self.probotCount >= 4:
            
            self.drawProbotMonitor(displaySurface,
                                   self.probotStatus[3],
                                   self.probot4BoundingBoxScaled)
        else:
            
            self.drawProbotMonitor(displaySurface,
                                   99,
                                   self.probot4BoundingBoxScaled)
    
    def runScanner(self, displaySurface):
        
        #  System setup.
        if self.scannerStage == 0:
            
            #  Start scanner music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'SCANNER.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.scannerStage += 1
                
            #  Establish ship position and planet.
            X, Y, Z = self.ironSeed.getPosition()
            self.thePlanet = planets.findPlanetarySystem(X, Y, Z).getPlanetAtOrbit(self.ironSeed.getOrbit())
            
            if self.thePlanet.planetTextureExists == False:
                
                self.thePlanet.generatePlanetTexture()
                
            #  Sort out Probot count.
            self.probotCount = self.ironSeed.getItemQuantity("Probot")
        
        if self.scannerStage == 1:
            
            self.drawInterface(displaySurface)
            
        
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                    
                pygame.mixer.music.play()

        return self.systemState