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
#  Note:  We assume the bounding box has already been scaled.
class Probot(object):
    
    def __init__(self, x, y, xEnd, yEnd, landBoundary):
        
        self.probotLaunched = False
        self.probotDestroyed = False
        self.probotRetrieving = False
        self.haveCargo = False
        self.planetPosition = [0, 0]  # Red dot position on scanner
        self.travelDirection = [0, 0] #  Stop movement jitter.
        self.landBoundary = landBoundary
        self.dataGathered = 0  # 100% = 1000
        self.fuel = 50  # 100% = 50, can be set on landing.

        #  Status, in order from 0:
        #  Docked, Deployed, Orbiting, Analyzing, Gathering, Returning,
        #  Refueling.
        self.status = 0
        
        #  Probot timer for current runtime.
        #  Could use stopwatch, but results might be "unrealistic."
        self.timer = 0
        
        #  Operation times, based on frames for the moment.
        self.timeLimit = 1200
        
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

    # Reset the timer.
    def resetTimer(self):
        
        self.timer = 0

    # Reset probot to default state.
    def resetProbot(self):
        
        self.probotLaunched = False
        self.probotDestroyed = False
        self.probotRetrieving = False
        self.haveCargo = False
        self.planetPosition = [0, 0]  # Red dot position on scanner
        self.travelDirection = [0, 0]
        self.status = 0
        self.timer = 0
        self.dataGathered = 0
        self.fuel = 50

    #  Check to see if the probot needs to be drawn on the planet view.
    def shouldDraw(self):
        
        yes = False
        
        if self.status == 3 or self.status == 4:
            
            yes = True
            
        return yes
        
    #  Make the red dot for the probot move around.
    #  Use retrieve check, if True then use retrieval logic.
    def move(self):
        
        if self.probotRetrieving:  # Move towards target.
            
            pass
        
        #  Change direction.  Drunken Farmer ;)
        elif (self.timeLimit/(self.timer+1)) in h.frange(0.0, 10.0, 0.5):
            
            self.travelDirection = [random.choices((-1, 0, 1))[0],
                                    random.choices((-1, 0, 1))[0]]
            
        applied = [self.planetPosition[0] + self.travelDirection[0],
                   self.planetPosition[1] + self.travelDirection[1]]
        
        #  We are wrapping from the edges, this is a planet, not a sheet
        #  with walls.
        
        if applied[0] > self.landBoundary[2]:
            
            applied = [self.landBoundary[0], applied[1]]
            
        elif applied[0] < self.landBoundary[0]:
            
            applied = [self.landBoundary[2], applied[1]]
            
        if applied[1] > self.landBoundary[3]:
            
            applied = [applied[0], self.landBoundary[1]]
            
        elif applied[1] < self.landBoundary[1]:
            
            applied = [applied[0], self.landBoundary[3]]
        
        #  Don't move when gathering.
        if self.status == 3:
        
            # Make movement potentially slower.
            if random.choice((True, False)):
                
                self.planetPosition = applied
                
        #  Use fuel
        self.fuel -= 1

    #  Perform probot tick related functions.
    def tick(self):
        
        if self.probotLaunched:
        
            self.timer += 1
        
            if self.timer == self.timeLimit:
            
                if self.status == 6:
                
                    self.status = 2
                    
                else:
                    
                    self.status += 1
                    
                self.timer = 0
            
            if self.status == 3 or self.status == 4:
                
                self.move()
            
        if self.probotRetrieving:
            
            self.timer += 1
            
            if self.timer == self.timeLimit:
                
                if self.status == 4:
                    
                    self.haveCargo = True
                    self.status = 5
                    
                    
                elif self.status == 6:
                        
                    self.status = 0
                    self.probotRetrieving = False
                    
                else:
                    
                    self.status += 1
                
                self.timer = 0
                
            if self.status == 3 or self.status == 4:
                
                self.move()        

# This class is essentially a mini-game called "The planet scanner" ;)
# The original game logic is relatively sophisticated, analysing individual
# pixels the probot is examining, looking to see if they match the "right"
# type of data the probot is seeking + how rich the data is.
# To support the above, the Planet class in planets.py needs to be expanded,
# so that individual pixels can be tested via targetted procedural generation.
# Note:  The original code is not too creative with "interference" from the
# "natives", I believe here is a lot of potential there; Roswell? ;)
class PlanetScanner(object):
    
    def __init__(self, playerShip):
        
        self.scannerStage = 0  # what we are doing.
        self.ironSeed = playerShip
        self.probotCount = self.ironSeed.getItemQuantity("Probot")
        
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        self.scanning = [False, False, False, False, False]
        self.scanned = [0, 0, 0, 0, 0]  # Historically 0 to 2
        self.dataCollected = [0, 0, 0, 0, 0]  # Historically 1000 per point.
        
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

        #  Landform bounding area for planet texture
        self.mainViewBoundary = (int((g.width/320)*28),
                                 int((g.height/200)*13),
                                 int((g.width/320)*267),
                                 int((g.height/200)*132))
        
        #  Planet texture scaled to the Landform Bounding area.
        self.planetTextureScaled = "Placeholder"
        
        #  Planet sphere scaled to size of probot monitor
        self.miniPlanet = "Placeholder"
        
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
        
        # Up to 4 probots can be partaking in a scan
        self.probot = [Probot(281, 18, 312, 43, self.mainViewBoundary),
                       Probot(281, 58, 312, 83, self.mainViewBoundary),
                       Probot(281, 98, 312, 83, self.mainViewBoundary),
                       Probot(281, 138, 312, 163, self.mainViewBoundary)]
        
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

        #  define button positions:  Scaling experiment.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        # height, width, (x,y) position
        self.land = buttons.Button(int((g.height/200)*8),
                                   int((g.width/320)*21),
                                   (int((g.width/320)*1), int((g.height/200)*21)))
        self.sea = buttons.Button(int((g.height/200)*8),
                                  int((g.width/320)*21),
                                  (int((g.width/320)*1), int((g.height/200)*30)))
        self.air = buttons.Button(int((g.height/200)*8),
                                  int((g.width/320)*21),
                                  (int((g.width/320)*1), int((g.height/200)*39)))
        self.life = buttons.Button(int((g.height/200)*8),
                                   int((g.width/320)*21),
                                   (int((g.width/320)*1), int((g.height/200)*48)))
        self.anomaly = buttons.Button(int((g.height/200)*8),
                                      int((g.width/320)*21),
                                      (int((g.width/320)*1), int((g.height/200)*57)))
        self.exit = buttons.Button(int((g.height/200)*20),
                                        int((g.width/320)*11),
                                        (int((g.width/320)*11), int((g.height/200)*66)))
        self.next = buttons.Button(int((g.height/200)*18),
                                   int((g.width/320)*7),
                                   (int((g.width/320)*135), int((g.height/200)*180)))
        self.previous = buttons.Button(int((g.height/200)*18),
                                       int((g.width/320)*7),
                                       (int((g.width/320)*135), int((g.height/200)*146)))
        self.zoomIn = buttons.Button(int((g.height/200)*9),
                                     int((g.width/320)*9),
                                     (int((g.width/320)*195), int((g.height/200)*177)))
        self.zoomOut = buttons.Button(int((g.height/200)*9),
                                      int((g.width/320)*9),
                                      (int((g.width/320)*195), int((g.height/200)*187)))
        self.Retrieve = buttons.Button(int((g.height/200)*26),
                                       int((g.width/320)*48),
                                       (int((g.width/320)*270), int((g.height/200)*173)))
        
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
            bot.probotLaunched = True
        
    # Run an update tick of the probot timer logic.
    def probotTick(self):
        
        for bot in self.probot:
            
            bot.tick()
            
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
    
    #  Synchronise data with planet.
    def planetSynchronise(self):

        self.thePlanet.lithosphere = self.scanned[0]
        self.thePlanet.hydrosphere = self.scanned[1]
        self.thePlanet.atmosphere = self.scanned[2]
        self.thePlanet.biosphere = self.scanned[3]
        self.thePlanet.anomaly = self.scanned[4]
    
    # Increment the scandata arrays according to the amount of data found
    # by a probot.
    # Datatype refers to the array position for that data type (0 to 5)
    # Amount refers to the data collected, in points.
    # 1000 points = 50% of total data collected for dataType, +1 to scanned.
    def incrementScanData(self, dataType, amount):
        
        self.dataCollected[dataType] += amount
        
        if self.dataCollected[dataType] >= 1000:
            
            if self.dataCollected[dataType] >= 2000:
                
                self.scanned[dataType] = 2
                self.scanning[dataType] = False
                
            else:
                self.scanned[dataType] = 1
        
        self.planetSynchronise()
        
    
    def update(self, displaySurface):
        
        return self.runScanner(displaySurface)
    
    #  Regenerate the texture for the zoomed in area of land.
    #  Note:  Multiply the zoom by 2, divide target by value.
    #  Result should provide x and y of top left corner if centered.
    def setZoomTexture(self):
        
        self.zoomTexture.blit(self.planetTextureScaled,
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
        
    
    #  Set the bounding of the zoomed graphic texture and it's entries in memory.
    def setZoomBoundaries(self, currentPosition):
                 
        AdjustedPositionX = currentPosition[0]
        AdjustedPositionY = currentPosition[1]
            
        #  Determine bounding rectangle size based on zoom level.
        rectangle = (self.zoomedViewSelected[0] + self.mainViewBoundary[0],
                     self.zoomedViewSelected[1] + self.mainViewBoundary[1],
                     int(self.zoomedViewSelected[2] / self.zoomLevel),
                     int(self.zoomedViewSelected[3] / self.zoomLevel))
                    
        #  Check the selected area is still within the bounds of the map.
        #  If not, restrict position into bounding area.
        if (currentPosition[0] + self.mainViewBoundary[0] + rectangle[2]) > self.mainViewBoundary[2]:
            
            AdjustedPositionX = self.mainViewBoundary[2] - rectangle[2]
            AdjustedPositionX -= self.mainViewBoundary[0]

        if (currentPosition[1] + self.mainViewBoundary[1] + rectangle[3]) > self.mainViewBoundary[3]:
                
            AdjustedPositionY = self.mainViewBoundary[3] - rectangle[3]
            AdjustedPositionY -= self.mainViewBoundary[1]
                
        #  Change view point for zoomed view.
        self.zoomedViewSelected = (AdjustedPositionX,
                                   AdjustedPositionY,
                                   int((g.width/320)*59),
                                   int((g.height/200)*59))
    
    #  Check if Scanning and launch probots if not.
    #  Also check to make sure we are not launching Probots if we already
    #  have data.
    def scanAndLaunch(self, scanType):
        
        isScanning = False
        
        #  A probot scan can be interrupted, so we need to check the scanned
        #  value carefully.
        
        #  Check to see if we are scanning something.
        for check in self.scanning:
                    
            if check:
                        
                isScanning = True
        
        
        if isScanning:
                
            if self.scanned[scanType] <= 1 and self.scanning[scanType]:
            
                self.launchProbots()
            
        else:
            
            if self.scanned[scanType] <= 1:
            
                self.scanning[scanType] = True
                self.launchProbots()        
    
    # Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        
        if self.land.within(currentPosition):
            
            self.scanAndLaunch(0)
        
        elif self.sea.within(currentPosition):
            
            self.scanAndLaunch(1)
        
        elif self.air.within(currentPosition):
            
            self.scanAndLaunch(2)
        
        elif self.life.within(currentPosition):
            
            self.scanAndLaunch(3)
        
        elif self.anomaly.within(currentPosition):
            
            self.scanAndLaunch(4)
        
        elif self.exit.within(currentPosition):
            
            self.scannerStage = 0
            self.musicState = False
            
            # Reset all probots to default state; assume they all get back.
            for bot in self.probot:
            
                bot.resetProbot()
            
            self.systemState = 10
            #  Reset scanner stage and enter main screen system state.
            
        
        elif self.next.within(currentPosition):
            
            pass
        
        elif self.previous.within(currentPosition):
            
            pass
        
        elif self.zoomIn.within(currentPosition):
            
            if self.zoomLevel < 3:
                self.zoomLevel += 1
                self.setZoomBoundaries(self.zoomedViewSelected)
                self.setZoomTexture()
        
        elif self.zoomOut.within(currentPosition):
            
            if self.zoomLevel > 1:
                self.zoomLevel -= 1
                self.setZoomBoundaries(self.zoomedViewSelected)
                self.setZoomTexture()
        
        
        elif self.Retrieve.within(currentPosition):
            
            pass
        
        elif self.planetMap.within(currentPosition):
            
            # The position on the screen needs to be adjusted for the relative
            # texture position.
            
            AdjustedPositionX = currentPosition[0] - self.mainViewBoundary[0]
            AdjustedPositionY = currentPosition[1] - self.mainViewBoundary[1]
            
            self.setZoomBoundaries([AdjustedPositionX, AdjustedPositionY])
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

    #  Draw planet summary information;  this is drawn after all data
    #  from the planet is collected.
    def drawPlanetDataSummary(self, displaySurface):
        
        pass
             
    #  Draw the red dots for deployed Probots on Planets Surface.


    def drawInterface(self, displaySurface):

        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.scanInterfaceScaled, (0, 0))
        displaySurface.blit(self.planetTextureScaled, self.mainViewBoundary)
        displaySurface.blit(self.zoomTextureScaled, self.zoomedViewBoundary)
        
        #  Draw bounding rectangle on map view.
        rectangle = (self.zoomedViewSelected[0] + self.mainViewBoundary[0],
                     self.zoomedViewSelected[1] + self.mainViewBoundary[1],
                     int(self.zoomedViewSelected[2] / self.zoomLevel),
                     int(self.zoomedViewSelected[3] / self.zoomLevel))
        pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)

        count = 1
        
        for bot in self.probot:
            
            if count <= self.probotCount:
                
                self.drawProbotMonitor(displaySurface,
                                       bot.status,
                                       bot.BoundingBoxScaled)
                
                # Check and draw movement pixel.  (scale?)
                if bot.shouldDraw():
                    
                    displaySurface.fill(g.RED, (bot.planetPosition[0],
                                                bot.planetPosition[1],
                                                int((g.width/320)*1),
                                                int((g.height/200)*1)))
                
            else:
                
                self.drawProbotMonitor(displaySurface,
                                       99,
                                       bot.BoundingBoxScaled)

    def runScanner(self, displaySurface):
        
        #  System setup.
        if self.scannerStage == 0:
            
            #  Make sure our system state is 5, in case we are returning after
            #  exiting.
            self.systemState = 5
            
            #  Start scanner music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'SCANNER.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.scannerStage += 1
                
            #  Establish ship position and planet.
            X, Y, Z = self.ironSeed.getPosition()
            self.thePlanet = planets.findPlanetarySystem(X, Y, Z).getPlanetAtOrbit(self.ironSeed.getOrbit())
            
            #  Make sure the planet surface is generated for the view window.
            
            if self.thePlanet.planetTextureExists == False:
                
                self.thePlanet.generatePlanetTexture()
                
            self.planetTextureScaled = pygame.transform.scale(self.thePlanet.planetTexture,
                                                              (int((g.width/320)*239), int((g.height/200)*119)))
            
            #  Generate the mini planet for probot travel
            preMiniPlanet = pygame.Surface((g.planetWidth, g.planetHeight), 0)
            preMiniPlanet.set_colorkey(g.BLACK)
            self.thePlanet.planetBitmapToSphere(preMiniPlanet, 0, eclipse = True)
            self.miniPlanet = pygame.transform.scale(preMiniPlanet,
                                                     (int((g.width/320)*31), int((g.height/200)*24)))
            
            #  Sort out Probot count.
            self.probotCount = self.ironSeed.getItemQuantity("Probot")
            self.setZoomTexture()
            
            #  Syncronise our scan data with the planet.
            self.scanned[0] = self.thePlanet.lithosphere
            self.scanned[1] = self.thePlanet.hydrosphere
            self.scanned[2] = self.thePlanet.atmosphere
            self.scanned[3] = self.thePlanet.biosphere
            self.scanned[4] = self.thePlanet.anomaly
            
            for dataValue in range(0,5):
                
                self.scanned[dataValue] = 1000 * self.scanned[dataValue]
            
        
        if self.scannerStage == 1:
            
            self.probotTick() # Run a tick update for the probots.
            self.drawInterface(displaySurface)
            
        
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                    
                pygame.mixer.music.play()

        return self.systemState