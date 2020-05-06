# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:35:51 2019
Planet Scanner
@author: Nuke Bloodaxe
"""

# This requires rather a lot of things to be working beforehand.
# However, it also is the best way to test the planet related code.

import random, os, buttons, planets, pygame, items
import global_constants as g
import helper_functions as h

# Encapsulate the Anomaly logic, it is really a wrapped item class with a
# location parameter.
class Anomaly(object):

    def __init__(self, anomalyItem, boundary):

        self.item = anomalyItem
        self.alternateName = items.getAlternateName(self.item)

        #  Set a random location
        self.locationX = random.randint(boundary[0], boundary[2])
        self.locationY = random.randint(boundary[1], boundary[3])


# To encapsulate most probot logic
# Having launch and retrieve here allows for asynchronous operations.
# Note:  We assume the bounding box has already been scaled.
class Probot(object):

    def __init__(self, x, y, xEnd, yEnd, landBoundary):

        self.probotLaunched = False
        self.probotDestroyed = False
        self.probotRetrieving = False
        self.haveCargo = False
        self.anomaly = "placeholder" # For tracking anomaly retrieval.
        self.planetPosition = [0, 0]  # Red dot position on scanner
        self.travelDirection = [0, 0]  #  Stop movement jitter.
        self.dataTarget = [0, 0]  # Target point for investigation.
        self.landBoundary = landBoundary
        self.dataGathered = 0  # 100% = 1000
        self.scanType = -1
        self.fuel = 50  # 100% = approx 50 seconds, can be set on landing.

        #  Status, in order from 0:
        #  Docked, Deployed, Orbiting, Gathering, Analyzing, Returning,
        #  Refueling.
        self.status = 0

        #  Probot timer for current runtime.
        #  Use stopwatch, careful, results might be "unrealistic."
        self.timer = h.StopWatch()
        self.timerLastCheck = 0.0  #  Used for minor time checks.

        #  Time limit for current stage, semi-random.
        self.statusTimeLimit = 0.0

        #  Operation times, basing on real-world seconds elapsed.
        #  Something seems a bit off, adjusting from original logic.
        self.timeLimit = 50.0
        self.deployedTimeLimit = 2.0 # 15.0
        self.orbitingTimeLimit = 3.0 # 10.0
        self.gatheringTimeLimit = 10.0
        #self.analyzingTimeLimit = 10.0
        self.returningTimeLimit = 5.0 # 25.0
        self.refuelingTimeLimit = 5.0

        #  Probots have 4 acivity monitors on main screen, these are the
        #  bounding-box positions.
        self.BoundingBox = (x, y, xEnd, yEnd)

        self.BoundingBoxScaled = (int((g.width/320)*x),
                                        int((g.height/200)*y),
                                        int((g.width/320)*xEnd),
                                        int((g.height/200)*yEnd))

        self.textPosition = [int((g.width/320)*x),
                             int((g.height/200)*(yEnd))]

        # Descriptors
        self.probotFeedback = ["Docked", "Deployed", "Orbiting", "Gathering",
                               "Analyzing", "Returning", "Refueling",
                               "Destroyed"]


    # Reset the timer.
    def resetTimer(self):

        self.timer.resetStopwatch()


    # Reset probot to default state.
    def resetProbot(self):

        self.probotLaunched = False
        self.probotDestroyed = False
        self.probotRetrieving = False
        self.haveCargo = False
        self.anomaly = "placeholder"
        self.planetPosition = [0, 0]  # Red dot position on scanner
        self.travelDirection = [0, 0]
        self.dataGathered = 0
        self.scanType = -1
        self.fuel = 50.0
        self.status = 0
        self.timer.resetStopwatch()
        self.statusTimeLimit = 0.0
        self.timerLastCheck = 0.0


    #  Refuel the probot.
    def refuelProbot(self):

        self.fuel = 50.0  # Approx real-World flight seconds.


    #  Check to see if the probot needs to be drawn on the planet view.
    def shouldDraw(self):

        yes = False

        if self.status == 3 or self.status == 4:

            yes = True

        return yes


    #  Set a data target
    def setDataTarget(self):

        if self.probotRetrieving:

            try:

                self.dataTarget = [self.anomaly.locationX,
                                   self.anomaly.locationY]

            except:

                print("Exception:Anomaly:setDataTarget: ", str(self.anomaly))
                self.probotRetrieving = False

        else:

            self.dataTarget = [random.randint(self.landBoundary[0],
                                              self.landBoundary[2]),
                               random.randint(self.landBoundary[1],
                                              self.landBoundary[3])]


    #  Set Stage Time Limit according to current stage and set timer.
    def setCurrentStageTimeLimit(self):

        if self.status == 1:

            self.statusTimeLimit = self.deployedTimeLimit

        elif self.status == 2:

            self.statusTimeLimit = self.orbitingTimeLimit

        elif self.status == 3:

            self.statusTimeLimit = self.gatheringTimeLimit

        elif self.status == 4:  #  Shouldn't hit unless on target.

            self.statusTimeLimit = random.randrange(0, 7)
            #80.0 + random.randrange(0, 50)  # ridiculous.

        elif self.status == 5:

            self.statusTimeLimit = self.returningTimeLimit

        else:

            self.statusTimeLimit = self.refuelingTimeLimit

        self.timer.setStopwatch()


    #  Check if stage time limit has been exceeded or matched.
    #  Returns True if time exceeded, False otherwise.
    def checkTimeLimitReached(self):

        exceeded = False
        
        if self.timer.getElapsedStopwatch() >= self.statusTimeLimit:
            
            exceeded = True
            
        return exceeded
    
    #  Return the current amount of time elapsed for the Probot, for this
    #  operation stage.  Int return value.
    def stageTimeElapsed(self):
        
        return int(self.timer.getElapsedStopwatch())

    #  Make the red dot for the probot move around.
    #  Use retrieve check, if True then use retrieval logic.
    def move(self):
        
        if self.planetPosition[0] > self.dataTarget[0]:
                
            self.travelDirection[0] = -1
            
        elif self.planetPosition[0] < self.dataTarget[0]:
            
            self.travelDirection[0] = 1
            
        else:
            
            self.travelDirection[0] = 0


        if self.planetPosition[1] > self.dataTarget[1]:
            
            self.travelDirection[1] = -1
        
        elif self.planetPosition[1] < self.dataTarget[1]:
            
            self.travelDirection[1] = 1
            
        else:
            
            self.travelDirection[1] = 0
        
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

        if self.status == 3:
        
            self.planetPosition = applied
        
        #  Don't move when Analysing.
        if (applied == self.dataTarget) and (self.status != 4):
            
            self.status = 4
            #  Analysis time is semi-random
            self.setCurrentStageTimeLimit()

        if self.timer.getTime() - self.timerLastCheck >= 1.0:
                
            #  Use fuel
            self.fuel -= 1.0
            self.timerLastCheck = self.timer.getTime()


    #  Launch the probot.
    def launch(self):
        
        if self.status == 0:

            self.status = 1  #  Deployed
                
        self.probotLaunched = True
        self.setCurrentStageTimeLimit()


    #  Perform probot tick related functions.
    def tick(self, crewMembers):
        
        if self.fuel <= 0.0 or self.dataGathered >= 500:
            
            if self.status != 5 and self.status != 6:
                
                #print("Set Status 5")
                self.status = 5
                self.setCurrentStageTimeLimit()
        
        if self.probotLaunched:
                
            if self.checkTimeLimitReached():
            
                if self.status == 6:
                    
                    #print("Status 6: Refueled")
                    self.refuelProbot()
                    self.status = 1
                    
                elif self.status == 4:
                    
                    #  Increment data gathered here.
                    #  Note, first time crew member skills + stress actually used in this engine.
                    self.dataGathered += int((crewMembers.skillRange(crewMembers.science, 5, 10) + 20) * (10 / 100))
                    
                    self.status = 3
                    self.setDataTarget()

                else:
                    
                    self.status += 1
                    
                self.setCurrentStageTimeLimit()
            
            if self.status == 3 or self.status == 4:
                
                self.move()
            
            else:
            
                self.setDataTarget()

        if self.probotRetrieving:
            
            if self.checkTimeLimitReached():
                
                if self.status == 4:  #  Temp, adjust logic later.
                    
                    self.haveCargo = True
                    self.status = 5
                    
                elif self.status == 6:
                        
                    self.status = 0
                    self.probotRetrieving = False
                    self.refuelProbot()
                    
                else:
                    
                    self.status += 1
                
                self.setCurrentStageTimeLimit()
                
            if self.status == 3 or self.status == 4:
                
                self.move()
            
            else:
            
                self.setDataTarget()
        
        #  We reset our timer every second.
        #if self.timer.getTime() - self.timerLastCheck >= 1.0:
            
        #    self.timerLastCheck = self.timer.getTime()


# This class is essentially a mini-game called "The planet scanner" ;)
# The original game logic is relatively sophisticated, analysing individual
# pixels the probot is examining, looking to see if they match the "right"
# type of data the probot is seeking + how rich the data is.
# To support the above, the Planet class in planets.py needs to be expanded,
# so that individual pixels can be tested via targetted procedural generation.
# Note:  The original code is not too creative with "interference" from the
# "natives", I believe here is a lot of potential there; Roswell? ;)
class PlanetScanner(object):
    
    def __init__(self, playerShip, crewMembers):
        
        self.scannerStage = 0  # what we are doing.
        self.ironSeed = playerShip
        self.crewMembers = crewMembers
        self.probotCount = self.ironSeed.getItemQuantity("Probot")
        
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        self.scanning = [False, False, False, False, False]
        self.scanned = [0, 0, 0, 0, 0]  # Historically 0 to 2
        self.dataCollected = [0, 0, 0, 0, 0]  # Historically 1000 per point.
        self.scanningComplete = False
        
        # Which scan window data is displaying right now?
        # Also, state 4 turns off full-panel summary and displays land map
        # again, with strobing anomalies.
        self.scanDisplay = 5  # 5 is the scan progress screen.
        
        # Anomaly items with locations.
        self.anomalies = []
        
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
        
        #  Scan Data Text
        self.scanDataText = ["Information Gathered", " Lithosphere..",
                             " Hydrosphere..", " Atmosphere...",
                             " Biosphere....", " Anomaly......", "0/2", "1/2",
                             "Completed."]
        
        #  Planet Scanner related graphics layers.
        self.scanInterface = pygame.image.load(os.path.join('Graphics_Assets', 'landform.png'))
        self.scanInterfaceScaled = pygame.transform.scale(self.scanInterface, (g.width, g.height))
        self.scanInterfaceScaled.set_colorkey(g.BLACK)
        
        #  Scanner green text frames.
        self.greenTextFrames = []
        self.prepareGreenTextFrames()

        #  Landform bounding area for planet texture
        self.mainViewBoundary = (int((g.width/320)*28),
                                 int((g.height/200)*13),
                                 int((g.width/320)*267),
                                 int((g.height/200)*132))
        
        #  Planet texture scaled to the Landform Bounding area.
        self.planetTextureScaled = "Placeholder"
        
        #  Planet sphere scaled to size of probot monitor
        self.miniPlanet = "Placeholder"
        
        #  Planet sphere animation frames
        self.miniPlanetAnimation = []
        
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
        
        self.zoomLevel = 1  # The zoom applied to the zoom view.  Max 3.
        
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
                       Probot(281, 98, 312, 123, self.mainViewBoundary),
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
        self.probotScanningScaled.set_colorkey(g.BLACK)
        
        self.probotDocked = pygame.Surface((31, 24), 0)
        self.probotDocked.blit(self.scanInterface, (0, 0), self.probot[1].BoundingBox )
        self.probotDockedScaled = pygame.transform.scale(self.probotDocked, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotRefuel = pygame.Surface((31, 24), 0)
        self.probotRefuel.blit(self.scanInterface, (0, 0), self.probot[2].BoundingBox )
        self.probotRefuelScaled = pygame.transform.scale(self.probotRefuel, (int((g.width/320)*31), int((g.height/200)*24)))
        
        self.probotTransit = pygame.Surface((31, 24), 0)
        self.probotTransit.blit(self.scanInterface, (0, 0), self.probot[3].BoundingBox )
        self.probotTransitScaled = pygame.transform.scale(self.probotTransit, (int((g.width/320)*31), int((g.height/200)*24)))
        self.probotTransitScaled.set_colorkey(g.BLACK)
        
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


    #  Reset the planet scanner back to default starting values.
    def resetScanner(self):
        
        self.scannerStage = 0  # Forces reset when we return to scanner.
        self.scanning = [False, False, False, False, False]
        self.scanned = [0, 0, 0, 0, 0]  # Historically 0 to 2
        self.dataCollected = [0, 0, 0, 0, 0]  # Historically 1000 per point.
        self.scanningComplete = False
        self.anomalies = []
        self.zoomLevel = 1
        self.musicState = False
        
        # Reset all probots to default state; assume they all get back.
        for bot in self.probot:
            
            bot.resetProbot()
        
    
    # Load green text animation frames
    def prepareGreenTextFrames(self):
        
        #  7 units Wide.
        for icon in range(1, 6):
                
            #  Top and bottom border of 1 pixel.
            #  Right border of 1 pixel.
            #  Each frame 20 pixels wide.
            #  Each frame 13 pixels high.
            sourceRectangle = ((icon*28),13, 20, 13 )
            frame = pygame.Surface((20, 13))
            frame.blit(self.scanInterface,(0, 0), sourceRectangle)
            #  The resizing procedure does introduce innaccuracy, but
            #  unavoidable right now.
            resizeFrame = pygame.transform.scale(frame, (int((g.width/320)*frame.get_width()), int((g.height/200)*frame.get_height())))
            resizeFrame.set_colorkey(g.BLACK)
            self.greenTextFrames.append(resizeFrame)
            
    #  Create the mini planet animation frames from current mini sphere.
    #  5 frames.
    def prepareMiniPlanetFrames(self):

        #  Generate the mini planet for probot travel
        preMiniPlanet = pygame.Surface((g.planetHeight, g.planetHeight), 0)
        preMiniPlanet.set_colorkey(g.BLACK)
        self.thePlanet.planetBitmapToSphere(preMiniPlanet, 0, eclipse = True)
        specialX = int((g.width/320)*31) # Scaled correct X
        specialY = int(((g.height/200)*24)) # Scaled correct Y.
        self.miniPlanet = pygame.transform.scale(preMiniPlanet,
                                                 (specialX, specialY))
        
        for count in range(3, 0, -1):
            
            tempFrame = pygame.transform.scale(self.miniPlanet, (int(specialX/count), int(specialY/count)))
            realFrame = pygame.Surface((specialX, specialY), 0)
            realFrame.set_colorkey(g.BLACK)
            realFrame.blit(tempFrame, ((specialX-tempFrame.get_width()), 0))
            self.miniPlanetAnimation.append(realFrame)
        
        tempFrame = pygame.transform.scale(self.miniPlanet, (specialX, specialY))
        self.miniPlanetAnimation.append(tempFrame)

    # Launch probots for a scan or retrieval.
    def launchProbots(self):
        
        for bot in self.probot:
            
            bot.launch()
            
        
    # Run an update tick of the probot timer logic.
    def probotTick(self):
                
        for bot in self.probot:
            
            bot.tick(self.crewMembers)
            
            if bot.status == 6:  #  Refueling
                
                if bot.probotRetrieving:
                    
                    if bot.haveCargo:
                        
                        result = self.ironSeed.addCargo(bot.anomaly.item, 1)
                        
                        if result[1] == 0:
                            
                            self.thePlanet.removeItemFromCache(bot.anomaly.item)
                            bot.anomaly = "placeholder"
                            bot.haveCargo = False
                            bot.probotRetrieving = False
                            
                            #  Cycle through looking for an anomaly that
                            #  will fit ship, and clear list of those which
                            #  won't.  They stay in the planet cache.
                            while len(self.anomalies) >= 1:
                                
                                bot.anomaly = self.anomalies.pop()
                                
                                if self.ironSeed.willThisFit(bot.anomaly.item):
                                    
                                    bot.probotRetrieving = True
                                    bot.setDataTarget()
                                    break
                                
                                else:
                                    
                                    bot.resetProbot()
                                    
                        #  Shouldn't happen!
                        else:  #  Cargo full!  Put item back in cache.
                            
                            #  Assume bot returns it.
                            bot.anomaly = "placeholder"
                            #  As this was popped, it won't try again.
                            #bot.resetProbot()  #  ?
                
                else:
                    
                    self.incrementScanData(bot.scanType, bot.dataGathered)
                    bot.dataGathered = 0

                    if self.scanned[bot.scanType] == 2:
                        
                        self.scanning[bot.scanType] = False
                        bot.resetProbot()


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


    # When a planet is scanned for the first time, we add enough items for a
    # full cache.  This is assuming we have scanned the planet fully.
    # Call this only once per planet.  Also populates planet cache, in case
    # we leave and then come back later.
    def createAnomalies(self):
        
        if self.thePlanet.anomalyGeneration == True:
            
            return  #  Exit without doing anyhing.
        
        if self.thePlanet.systemName == "EXOPID" and self.thePlanet.orbit == 0:

            if 28 in g.eventFlags:
                
                self.anomalies.append(Anomaly("Temporal Anchor",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Heavy Corse Grenade",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Heavy Corse Grenade",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Sling of David",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Sling of David",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Thynne Vortex",
                                              self.mainViewBoundary))
                self.anomalies.append(Anomaly("Thynne Vortex",
                                              self.mainViewBoundary))
                
        else:
            
            # Set random value to planet seed.
            random.seed(self.thePlanet.seed)
            
            for count in range(7):
                
                d100 = random.randint(0, 100)
                randomItem = "placeholder"
                # The item is determined by the planet state.
                if self.thePlanet.state == 0:
                    
                    if d100 < 25:
                        
                        randomItem = items.getRandomItem("MATERIAL",
                                                         g.totalMaterials)
                
                elif self.thePlanet.state == 1 or self.thePlanet.state == 2:
                    
                    if d100 < 76:
                        
                        randomItem = items.getRandomItem("ELEMENT",
                                                         g.totalElements)
                    
                elif self.thePlanet.state == 3:
                    
                    if d100 < 51:
                        
                        randomItem = items.getRandomItem("ELEMENT",
                                                         g.totalElements)
                    
                    elif random.choice([True, False]):
                        
                        randomItem = items.getRandomItem("MATERIAL",
                                                         g.totalMaterials)
                        
                    else:
                        
                        randomItem = items.getRandomItem("COMPONENT",
                                                         g.totalComponents)
                    
                elif self.thePlanet.state == 4:
                    
                    if d100 < 41:
                        
                        randomItem = items.getRandomItem("ELEMENT",
                                                         g.totalElements)
                    
                    elif d100 < 71:
                        
                        randomItem = items.getRandomItem("COMPONENT",
                                                         g.totalComponents)
                        
                    elif d100 == 74 or d100 == 75:
                        
                        # TODO Artifact code.
                        pass
                    
                elif self.thePlanet.state == 5:
                    
                    if d100 < 66:
                        
                        if random.choice([True, False]):
                        
                            randomItem = items.getRandomItem("MATERIAL",
                                                             g.totalMaterials)
                        
                        else:
                        
                            randomItem = items.getRandomItem("COMPONENT",
                                                             g.totalComponents)
                            
                    elif d100 == 73 or d100 == 74 or d100 == 75:
                        
                        # TODO Artifact code.
                        pass
                    
                else:  # Must be 6.
                    
                    if d100 < 6:
                        
                        # TODO Artifact code.
                        pass
                
                if randomItem != "placeholder":
                    
                    #print("RandomItem: ", randomItem)
                    
                    self.anomalies.append(Anomaly(randomItem,
                                                  self.mainViewBoundary))
        
        for anomaly in self.anomalies:
        
            #  Fill planet cache with generated items.
            self.thePlanet.addItemToCache(anomaly.item)
            
        # Reset random number seed.
        random.seed()
        self.thePlanet.anomalyGeneration = True


    # Retrieve anomalies to put into ship cargo.
    # Note: probot actually carries object!  Make sure you put it into cargo!
    def retrieveAnomalies(self):
        
        #  Don't do anything if we haven't scanned everything.
        if self.scanningComplete == False:
            
            return
        
        count = 0
        
        for bot in self.probot:
            
            if bot.probotDestroyed == False and bot.probotRetrieving == False:
                
                count += 1
                
                if count <= self.probotCount:
                    
                    bot.anomaly = self.anomalies.pop()  # Much excitement!
                    bot.probotRetrieving = True
                    bot.setDataTarget()


    #  Test scan data to see if we have scanned everything
    def testScanData(self):
        
        allTestedComplete = True
        
        for test in self.scanned:
            
            if test != 2:
                
                allTestedComplete = False
                break
        
        return allTestedComplete


    #  Synchronise scan data with planet.
    def planetSynchronise(self):

        self.thePlanet.lithosphere = self.scanned[0]
        self.thePlanet.hydrosphere = self.scanned[1]
        self.thePlanet.atmosphere = self.scanned[2]
        self.thePlanet.biosphere = self.scanned[3]
        self.thePlanet.anomaly = self.scanned[4]
        self.thePlanet.fullyScanned = self.scanningComplete


    # Increment the scandata arrays according to the amount of data found
    # by a probot.
    # Datatype refers to the array position for that data type (0 to 5)
    # Amount refers to the data collected, in points.
    # 1000 points = 50% of total data collected for dataType, +1 to scanned.
    def incrementScanData(self, dataType, amount):
        
        self.dataCollected[dataType] += amount
        
        if self.dataCollected[dataType] >= 500:
            
            if self.dataCollected[dataType] >= 1000:
                
                self.scanned[dataType] = 2
                
                #  Generate Anomalies only when all anomaly data collected.
                if dataType == 4:
                    
                    self.createAnomalies()
                
            else:
                
                self.scanned[dataType] = 1
                
        if self.testScanData():
            
            self.scanningComplete = True
        
        self.planetSynchronise()

    
    #  Update call for this section of the state engine.
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
    #  Note:  We centre the view on the clicked position.
    def setZoomBoundaries(self, currentPosition):
                 
        #  Determine bounding rectangle size based on zoom level.
        rectangle = (self.zoomedViewSelected[0] + self.mainViewBoundary[0],
                     self.zoomedViewSelected[1] + self.mainViewBoundary[1],
                     int(self.zoomedViewSelected[2] / self.zoomLevel),
                     int(self.zoomedViewSelected[3] / self.zoomLevel))

        AdjustedPositionX = currentPosition[0] - int(rectangle[2]/2)
        AdjustedPositionY = currentPosition[1] - int(rectangle[3]/2)
            
                    
        #  Check the selected area is still within the bounds of the map.
        #  If not, restrict position into bounding area.
        if (AdjustedPositionX + self.mainViewBoundary[0] + rectangle[2]) > self.mainViewBoundary[2]:
            
            AdjustedPositionX = self.mainViewBoundary[2] - rectangle[2]
            AdjustedPositionX -= self.mainViewBoundary[0]
            
        elif (AdjustedPositionX + self.mainViewBoundary[0]) < self.mainViewBoundary[0]:
            
            AdjustedPositionX += (self.mainViewBoundary[0] - AdjustedPositionX)
            AdjustedPositionX -= self.mainViewBoundary[0]

        if (AdjustedPositionY + self.mainViewBoundary[1] + rectangle[3]) > self.mainViewBoundary[3]:
                
            AdjustedPositionY = self.mainViewBoundary[3] - rectangle[3]
            AdjustedPositionY -= self.mainViewBoundary[1]
            
        elif (AdjustedPositionY + self.mainViewBoundary[1]) < self.mainViewBoundary[1]:
            
            AdjustedPositionY += (self.mainViewBoundary[1] - AdjustedPositionY)
            AdjustedPositionY -= self.mainViewBoundary[1]
            
        #  Change view point for zoomed view.
        self.zoomedViewSelected = (AdjustedPositionX,
                                   AdjustedPositionY,
                                   int((g.width/320)*59),
                                   int((g.height/200)*59))


    #  Draw the HUD display green "text" and targetting reticules.
    #  These should be drawn during the main drawing routine, so the zoom
    #  texture is left intact.
    def drawZoomHUD(self, displaySurface):
        
        xCentre = (self.zoomedViewBoundary[2] - self.zoomedViewBoundary[0]) / 2
        xCentre = int(xCentre + self.zoomedViewBoundary[0])
        
        yCentre = (self.zoomedViewBoundary[3] - self.zoomedViewBoundary[1]) / 2
        yCentre = int(yCentre + self.zoomedViewBoundary[1])
        
        h.targettingReticule(displaySurface,
                             xCentre,
                             yCentre,
                             g.BLUE,
                             2,
                             int(((self.zoomedViewBoundary[2]-self.zoomedViewBoundary[0])/15)*self.zoomLevel),
                             1)
        #self.greenTextFrames
        
        #  Draw the green text frames on the Zoom HUD.
        displaySurface.blit(self.greenTextFrames[random.randrange(0,5)],
                            (self.zoomedViewBoundary[0],
                             self.zoomedViewBoundary[1]))
        
        displaySurface.blit(self.greenTextFrames[random.randrange(0,5)],
                            (self.zoomedViewBoundary[2] - self.greenTextFrames[0].get_width(),
                             self.zoomedViewBoundary[3] - self.greenTextFrames[0].get_height()))

    #  Prepare Probot scan target, only set probots which are currently not in
    #  use.
    def setProbotsTarget(self, scanType):
        
        for bot in self.probot:
            
            if bot.scanType == -1:
                
                bot.scanType = scanType
                self.scanning[scanType] = True
            

    #  Check if Scanning and launch probots if not.
    #  Also check to make sure we are not launching Probots if we already
    #  have data.
    def scanAndLaunch(self, scanType):

        if self.testScanData():
            
            return #  Exit immediately if we have all the scan data.
        
#        isScanning = False
        
        #  A probot scan can be interrupted, so we need to check the scanned
        #  value carefully.
        
        #  Check to see if we are scanning something.
#        for check in self.scanning:
                    
#            if check:
                        
#                isScanning = True
        
        #  Only launch Probots when data remains to be scanned.
#        if isScanning:
                
            #  Do not launch the Probots twice for the same thing.
#            if self.scanned[scanType] <= 1 and self.scanning[scanType] != True:
                
#                self.scanning[scanType] = True
#                self.setProbotsTarget(scanType)
#                self.launchProbots()
                
#        else:
            
        if self.scanned[scanType] <= 1:
        
            # Attempt to send bots.
            self.setProbotsTarget(scanType)
            self.launchProbots()
            
        else:
            
            self.scanning[scanType] = False  #  Have all data.


    # Handle mouse events for user interaction.
    # Note: IronSeed was created during the days of no mouse wheel.
    # It might be interesting to add context support for it to the
    # data window.
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
            
            self.resetScanner()
                        
            self.systemState = 10
            #  Reset scanner stage and enter main screen system state.
            
        
        #  Display the next lines of data in the lower data window for
        #  a given category.
        elif self.next.within(currentPosition):
            
            if self.scanningComplete:
                
                pass
        
        
        #  Display the previous lines of data in the lower data window for
        #  a given category.
        elif self.previous.within(currentPosition):
            
            if self.scanningComplete:
                
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
            
            self.retrieveAnomalies()
        
        elif self.planetMap.within(currentPosition):
            
            # The position clicked on the screen needs to be adjusted for the
            # relative texture position.
            
            AdjustedPositionX = currentPosition[0] - self.mainViewBoundary[0]
            AdjustedPositionY = currentPosition[1] - self.mainViewBoundary[1]
            
            self.setZoomBoundaries([AdjustedPositionX, AdjustedPositionY])
            self.setZoomTexture()
        
        return self.systemState


    #  Draw a micro version of the planet on a probot monitor.
    #  TODO:  This actually sweeps in from the right, and zooms in until
    #  it is centred in the monitor.
    def drawMicroPlanet(self, displaySurface, bot):
        
        displaySurface.blit(self.miniPlanetAnimation[bot.stageTimeElapsed()],
                            bot.BoundingBoxScaled)


    #  Draw a segment of the landscape texture on a probot monitor.
    def drawLandscapeProbot(self, displaySurface, bot):
        
        #  Ensure original background graphic is wiped
        self.drawProbotMonitor(displaySurface, bot, True)
        
        displaySurface.blit(self.planetTextureScaled,
                            bot.BoundingBoxScaled,
                            (bot.planetPosition[0]-self.mainViewBoundary[0]-(int((g.width/320)*(31/2))),
                             bot.planetPosition[1]-self.mainViewBoundary[1]-(int((g.height/200)*(24/2))),
                             int((g.width/320)*31),
                             int((g.height/200)*24)))


    #  Draw text and a graphic on a Probot Monitor.
    def drawTextAndGraphic(self, displaySurface, graphic, bot, showGraphic=True):
        
        if showGraphic:
            
            displaySurface.blit(graphic, bot.BoundingBoxScaled)
            
        h.renderText([bot.probotFeedback[bot.status]],
                     g.font, displaySurface, g.WHITE, 0,
                     bot.textPosition[0],
                     bot.textPosition[1])


    #  Draw a probot status monitor.
    #  stage is the probot frame to draw.
    #  destination is a pygame rect
    #  Status, in order from 0:
    #  Docked, Deployed, Orbiting, Gathering, Analyzing, Returning,
    #  Refueling.
    #  TODO:  transit, complex planet resize required.
    def drawProbotMonitor(self, displaySurface, bot, blank=False):
        
        if blank == True:
            
            displaySurface.blit(self.probotEmptyScaled, bot.BoundingBoxScaled)
            return

        if bot.status == 0:
            
            self.drawTextAndGraphic(displaySurface,
                                    self.probotDockedScaled,
                                    bot)

        elif bot.status == 1 or bot.status == 2 or bot.status == 5:
            
            displaySurface.blit(self.probotEmptyScaled, bot.BoundingBoxScaled)
            
            if bot.status == 2:
                
                self.drawMicroPlanet(displaySurface, bot)
                
            self.drawTextAndGraphic(displaySurface,
                                    self.probotTransitScaled,
                                    bot)

        elif bot.status == 3 or bot.status == 4:  #  Overlay on landscape
        
            self.drawLandscapeProbot(displaySurface, bot)

            displaySurface.fill(g.RED,
                                (bot.BoundingBoxScaled[0] + int(((g.width/320)*31)/2),
                                bot.BoundingBoxScaled[1] + int(((g.height/200)*24)/2),
                                int((g.width/320)*1),
                                int((g.height/200)*1)))
            
            if bot.status == 3:
                
                self.drawTextAndGraphic(displaySurface,
                                        self.probotScanningScaled,
                                        bot, False)
                
            elif bot.status == 4:
                
                self.drawTextAndGraphic(displaySurface,
                                        self.probotScanningScaled,
                                        bot)
                displaySurface.blit(self.greenTextFrames[random.randrange(0,5)],
                                    (bot.BoundingBoxScaled[2] - self.greenTextFrames[0].get_width(),
                                     bot.BoundingBoxScaled[3] - self.greenTextFrames[0].get_height()))
                         
        elif bot.status == 6:

            self.drawTextAndGraphic(displaySurface,
                                    self.probotRefuelScaled,
                                    bot)
                         
        else:

             displaySurface.blit(self.probotEmptyScaled, bot.BoundingBoxScaled)

    #  Draw planet scan progress; drawn while data is being collected from the
    #  planet.
    def drawScanDataSummary(self, displaySurface):
                
        textToRender = [self.scanDataText[0]]
        
        for count in range(5):
            
            textToRender.append(self.scanDataText[count+1])
            
            if self.scanned[count] == 0:
                
                textToRender[count+1] += self.scanDataText[6]
            
                #textToRender.append(self.scanDataText[6])
            
            elif self.scanned[count] == 1:
                
                textToRender[count+1] += self.scanDataText[7]
                
            else:
                
                textToRender[count+1] += self.scanDataText[8]
        
        h.renderText(textToRender, g.font, displaySurface, g.WHITE,
                     g.offset, int((g.width/320)*6), int((g.height/200)*147))
        

    #  Draw planet summary information; this is drawn after all data
    #  from the planet is collected.
    def drawPlanetDataSummary(self, displaySurface):
        
        pass
    
    #  Draw the data summary panel for a given type of data, like atmosphere.
    #  Depending on the amount of data, the display may be progressed line
    #  by line using the next and previous buttons.
    def drawDataPanelSummary(self, displaySurface):
        
        pass


    #  Draw the red dots for Probots deployed on Planet Surface.

    #  Draw the Planet Scanner interface and all current animations.
    def drawInterface(self, displaySurface):

        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.scanInterfaceScaled, (0, 0))
        
        if self.scanningComplete == False:
            
            displaySurface.blit(self.planetTextureScaled, self.mainViewBoundary)
        
        if self.scanningComplete == False or self.scanDisplay == 4:
            
            displaySurface.blit(self.zoomTextureScaled, self.zoomedViewBoundary)
            
        self.drawZoomHUD(displaySurface)
        
        
        #  Draw bounding rectangle on map view.
        rectangle = (self.zoomedViewSelected[0] + self.mainViewBoundary[0],
                     self.zoomedViewSelected[1] + self.mainViewBoundary[1],
                     int(self.zoomedViewSelected[2] / self.zoomLevel),
                     int(self.zoomedViewSelected[3] / self.zoomLevel))
        pygame.draw.rect(displaySurface, g.BLUE, rectangle, 1)

        #  Draw scan progress while data still outstanding.
        if self.testScanData() == False:
            
            self.drawScanDataSummary(displaySurface)

        if self.scanningComplete:
            
            if self.scanDisplay < 4:
                
                self.drawPlanetDataSummary(displaySurface)
                self.drawDataPanelSummary(displaySurface)
            
            elif self.scanDisplay == 4:
            
                #  Draw anomalies on map.
                #TODO: Make Strobe
                perPixel = pygame.PixelArray(displaySurface)
        
                for anomaly in self.anomalies:
            
                    perPixel[anomaly.locationX][anomaly.locationY] = g.ANOMALY


                perPixel.close()
                self.drawDataPanelSummary(displaySurface)
                
            else:
                
                self.drawPlanetDataSummary(displaySurface)

        #  Draw working probots on map.
        count = 1
        
        for bot in self.probot:
            
            if count <= self.probotCount:
                
                self.drawProbotMonitor(displaySurface, bot)
                
                # Check and draw movement pixel.  (scale?)
                if bot.shouldDraw():
                    
                    displaySurface.fill(g.RED, (bot.planetPosition[0],
                                                bot.planetPosition[1],
                                                int((g.width/320)*1),
                                                int((g.height/200)*1)))
                
            else:
                
                self.drawProbotMonitor(displaySurface,
                                       bot.BoundingBoxScaled, True)


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
            
            #  Generate the animation frames for the mini planet.
            self.prepareMiniPlanetFrames()
            
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
                
                self.dataCollected[dataValue] = 500 * self.scanned[dataValue]

        if self.scannerStage == 1:

            self.probotTick() # Run a tick update for the probots.
            self.drawInterface(displaySurface)

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()

        return self.systemState