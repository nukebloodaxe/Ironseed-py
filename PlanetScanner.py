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
        self.scanning = [False, False, False, False, False]
        # lithosphere, hydrosphere, atmosphere, biosphere, anomaly
        
        # Up to 4 probots can be partaking in a scan
        Probot1 = [0,0] # red dot position
        Probot2 = [0,0]
        Probot3 = [0,0]
        Probot4 = [0,0]
        
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
        self.mainViewBoundary = (int((g.width/320)*28), int((g.height/200)*13), int((g.width/320)*239), int((g.height/200)*119))
        
        #  Zoomed view bounding area for planet texture.
        self.zoomedViewBoundary = (int((g.width/320)*206), int((g.height/200)*139), int((g.width/320)*59), int((g.height/200)*59))
        
        #  Selected zone for zoomedViewBoundary; default = top left corner.
        self.zoomedViewBoundary = (int((g.width/320)*28), int((g.height/200)*13), int((g.width/320)*59), int((g.height/200)*59))
        
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
    
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.scanInterfaceScaled, (0, 0))
        displaySurface.blit(self.thePlanet.planetTexture, self.mainViewBoundary)
    
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
        
        if self.scannerStage == 1:
            
            self.drawInterface(displaySurface)
            
        
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                    
                pygame.mixer.music.play()

        return self.systemState