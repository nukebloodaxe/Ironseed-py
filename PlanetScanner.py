# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:35:51 2019
Planet Scanner
@author: Nuke Bloodaxe
"""

# This requires rather a lot of things to be working beforehand.
# However, it also is the best way to test the planet related code.

import random, math, io, time, os, buttons, planets, pygame, items, ship, crew
import global_constants as g
import helper_functions as h

# To encapsulate most probot logic
# Having launch and retrieve here allows for asynchronous operations.
class Probot(object):
    
    def __init__(self, x, y, xEnd, yEnd):
        
        self.probotLaunched = False
        self.probotDestroyed = False
        self.probotRetrieving = False
        self.haveCargo = False
        self.planetPosition = [0, 0]  # Red dot position on scanner

        #  Status, in order from 0:
        #  Docked, Deployed, Orbiting, Analyzing, Gathering, Returning,
        #  Refueling.
        self.status = 0
        
        #  Probot timer for current runtime.
        #  Could use stopwatch, but results might be "unrealistic."
        self.timer = 0
        
        #  Operation times, based on frames for the moment.
        self.timeLimit = 30
        
        #  Probots have 4 acivity monitors on main screen, these are the
        #  bounding-box positions.
        self.BoundingBox = (x, y, xEnd, yEnd)

        self.BoundingBoxScaled = (int((g.width/320)*x),
                                        int((g.height/200)*y),
                                        int((g.width/320)*xEnd),
                                        int((g.height/200)*yEnd))

        # Descriptors
        self.probotFeedback = ["Docked", "Deployed", "Orbiting", "Analyzing",
                               "Gathering", "Returning", "Refueling",
                               "Destroyed"]

    # reset the timer.
    def resetTimer(self):
        
        self.timer = 0

    #  Perform probot tick related functions.
    def tick(self):
        
        if self.probotLaunched:
        
            self.timer += 1
        
            if self.timer == 30:
            
                if self.status == 6:
                
                    self.status = 2
                    
                else:
                    
                    self.status += 1
                    
                self.timer = 0
            
        if self.probotRetrieving:
            
            self.timer += 1
            
            if self.timer == 30:
                
                if self.status == 4:
                    
                    self.haveCargo = True
                    self.status = 5
                    
                    
                elif self.status == 6:
                        
                    self.status = 0
                    self.probotRetrieving = False
                    
                else:
                    
                    self.status += 1
                
                self.timer = 0
        

# This class is essentially a mini-game called "The planet scanner" ;)
class PlanetScanner(object):
    
    def __init__(self, playerShip):
        
        self.scannerStage = 0  # what we are doing.
        self.ironSeed = playerShip
        self.probotCount = self.ironSeed.getItemQuantity("Probot")
        self.scanning = [False, False, False, False, False]
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        self.scanned = [0, 0, 0, 0, 0]  # Historically 0 to 2.
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        
        # Up to 4 probots can be partaking in a scan
        self.probot = [Probot(281, 18, 312, 43),
                       Probot(281, 58, 312, 83),
                       Probot(281, 98, 312, 83),
                       Probot(281, 138, 312, 163)]

        
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
        self.probotScanning.blit(self.scanInterface, (0, 0), self.probot[0].BoundingBox )
        self.probotScanningScaled = pygame.transform.scale(self.probotScanning, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotDocked = pygame.Surface((31, 24), 0)
        self.probotDocked.blit(self.scanInterface, (0, 0), self.probot[1].BoundingBox )
        self.probotDockedScaled = pygame.transform.scale(self.probotDocked, (int((g.width/320)*30), int((g.height/200)*24)))
        
        self.probotRefuel = pygame.Surface((31, 24), 0)
        self.probotRefuel.blit(self.scanInterface, (0, 0), self.probot[2].BoundingBox )
        self.probotRefuelScaled = pygame.transform.scale(self.probotRefuel, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotTransit = pygame.Surface((31, 24), 0)
        self.probotTransit.blit(self.scanInterface, (0, 0), self.probot[3].BoundingBox )
        self.probotTransitScaled = pygame.transform.scale(self.probotTransit, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotEmpty = pygame.Surface((31, 24), 0)
        self.probotEmptyScaled = pygame.transform.scale(self.probotEmpty, (int((g.width/320)*31), int((g.height/200)*24)))
        
        #  Landform bounding area for planet texture
        self.mainViewBoundary = (int((g.width/320)*28),
                                 int((g.height/200)*13),
                                 int((g.width/320)*267),
                                 int((g.height/200)*132))
        
        #  Zoomed view bounding area for zoomed planet texture.
        self.zoomedViewBoundary = (int((g.width/320)*206),
                                   int((g.height/200)*140),
                                   int((g.width/320)*265),
                                   int((g.height/200)*198))
        
        #  Selected zone for zoomedViewBoundary; default = top left corner.
        self.zoomedViewSelected = (int((g.width/320)*28),
                                   int((g.height/200)*13),
                                   int((g.width/320)*59),
                                   int((g.height/200)*59))
        
        self.zoomLevel = 1  #  The zoom applied to the zoom view.  Max 3.
        
        #  Zoom texture for showing zoomed area of landmass.
        self.zoomTexture = pygame.Surface((int((g.width/320)*59),
                                           int((g.height/200)*59)),
                                          0)
        
        self.zoomTextureScaled = pygame.transform.scale(self.zoomTexture,
                                                        (int((g.width/320)*59),
                                                         int((g.height/200)*59)))
        
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
        self.planetMap = buttons.Button(int((g.height/200)*119),
                                        int((g.width/320)*239),
                                        (int((g.width/320)*28), int((g.height/200)*13)))
        
        #  The planet object.
        self.thePlanet = "placeholder"
        
        #  Music/Sound handlers.
        self.musicState = False
        
        self.systemState = 5
        
    # Launch probots for a scan
    def launchProbots(self):
        
        for bot in self.probot:
            
            bot.status = 1  #  Deployed
        
    # Run an update tick of the probot timer logic.
    def probotTick(self):
        
        for bot in self.probot:
            
            if bot.status != 0:
                
                bot.timer += 1
            
    # Destroy a quantity of Probots.
    #  TODO:  Make more elaborate with big popup box and report on how it was
    #  destroyed.
    def destroyProbot(self, quantity):
        
        self.ironSeed.removeCargo("Probot", quantity)
        self.probotCount = self.ironSeed.getItemQuantity("Probot")
        
        if quantity > 1:
            
            self.ironseed.addMessage( str(quantity) + " Probots Destroyed!", 3)
                
        else:
            
            self.ironseed.addMessage( "Probot Destroyed!", 3)
    
    # The planet we will scan for anomalies etc.
    def scanPlanet(self):
        
        pass
    
    # Retrieve anomalies and put into ship cargo.
    def retrieveAnomalies(self):
        
        pass
    
    def update(self, displaySurface):
        
        return self.runScanner(displaySurface)
    
    #  Regenerate the texture for the zoomed in area of land.
    def setZoomTexture(self):
        
        self.zoomTexture.blit(self.thePlanet.planetTexture,
                              (0, 0),
                              self.zoomedViewSelected)
        
        #  Generate the zoom texture according to zoom level.
     
        tempTexture = pygame.transform.scale(self.zoomTexture,
                                             ((int((g.width/320)*59)*self.zoomLevel),
                                             (int((g.height/200)*59)*self.zoomLevel)))
        
        self.zoomTextureScaled = pygame.transform.scale(tempTexture,
                                                        (int((g.width/320)*59),
                                                         int((g.height/200)*59)))
        
        self.zoomTextureScaled.blit(tempTexture, 
                                    (0, 0), 
                                    (0, 0, int((g.width/320)*59), int((g.height/200)*59)))
        
    
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
                self.setZoomTexture()
        
        elif self.zoomOut.within(currentPosition):
            
            if self.zoomLevel > 1:
                self.zoomLevel -= 1
                self.setZoomTexture()
        
        
        elif self.Retrieve.within(currentPosition):
            
            pass
        
        elif self.planetMap.within(currentPosition):
            
            # The position on the screen needs to be adjusted for the relative
            # texture position.
            
            AdjustedPositionX = currentPosition[0] - self.mainViewBoundary[0]
            AdjustedPositionY = currentPosition[1] - self.mainViewBoundary[1]
            
            #  Check the selected area is still within the bounds of the map.
            #  If not, restrict position into bounding area.
            if (currentPosition[0] + int((g.width/320)*59)) > self.mainViewBoundary[2]:
                
                AdjustedPositionX = self.mainViewBoundary[2] - int((g.width/320)*59)
                AdjustedPositionX -= self.mainViewBoundary[0]

            if (currentPosition[1] + int((g.height/200)*59)) > self.mainViewBoundary[3]:
                
                AdjustedPositionY = self.mainViewBoundary[3] - int((g.height/200)*59)
                AdjustedPositionY -= self.mainViewBoundary[1]
                
            #  Change view point for zoomed view.
            self.zoomedViewSelected = (AdjustedPositionX,
                                       AdjustedPositionY,
                                       int((g.width/320)*59),
                                       int((g.height/200)*59))
            
            self.setZoomTexture()
        
        return self.systemState
    
    #  Draw a probot status monitor.
    #  stage is the probot frame to draw.
    #  destination is a pygame rect
    #  Status, in order from 0:
    #  Docked, Deployed, Orbiting, Analyzing, Gathering, Returning,
    #  Refueling.
    #  TODO:  transit, complex planet resize required.
    def drawProbotMonitor(self, displaySurface, stage, destination):

        if stage == 0:
            
            displaySurface.blit(self.probotDockedScaled, destination)

        elif stage == 1:
            
            displaySurface.blit(self.probotTransitScaled, destination)

        elif stage == 2:
            
            displaySurface.blit(self.probotTransitScaled, destination)

        elif stage == 3:
            
            displaySurface.blit(self.probotScanningScaled, destination)

        elif stage == 4:

            displaySurface.blit(self.probotScanningScaled, destination)
            
        elif stage == 5:
            
            displaySurface.blit(self.probotTransitScaled, destination)
            
        elif stage == 6:
            
            displaySurface.blit(self.probotRefuelScaled, destination)
            
        else:

             displaySurface.blit(self.probotEmptyScaled, destination)

    def drawInterface(self, displaySurface):

        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.scanInterfaceScaled, (0, 0))
        displaySurface.blit(self.thePlanet.planetTexture, self.mainViewBoundary)
        displaySurface.blit(self.zoomTextureScaled, self.zoomedViewBoundary)
        
        #  Draw bounding rectangle on map view.
        rectangle = (self.zoomedViewSelected[0] + self.mainViewBoundary[0],
                     self.zoomedViewSelected[1] + self.mainViewBoundary[1],
                     self.zoomedViewSelected[2],
                     self.zoomedViewSelected[3])
        pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)

        count = 1
        
        for bot in self.probot:
            
            if count <= self.probotCount:
                
                self.drawProbotMonitor(displaySurface,
                                       bot.status,
                                       bot.BoundingBoxScaled)
            else:
                
                self.drawProbotMonitor(displaySurface,
                                       99,
                                       bot.BoundingBoxScaled)

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
            self.setZoomTexture()
        
        if self.scannerStage == 1:
            
            self.probotTick() # Run a tick update for the probots.
            self.drawInterface(displaySurface)
            
        
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                    
                pygame.mixer.music.play()

        return self.systemState