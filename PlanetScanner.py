# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:35:51 2019
Planet Scanner
@author: Nuke Bloodaxe
"""

# This requires rather a lot of things to be working beforehand.
# However, it also is the best way to test the planet related code.

import buttons, planets, pygame, items, ship, global_constants as g, helper_functions as h
import random, math, io, time

# This class is essentially a self-contained game called "The planet scanner" ;)
class PlanetScanner(object):
    
    def __init__(self):
        
        self.scannerStage = 0 # what we are doing.
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
    # Launch probots for a scan
    def launchProbots(self):
        
        pass
    
    # The planet we will scan for anomalies etc.
    def scanPlanet(self, planet):
        
        pass
    
    # Retrieve anomalies and put into ship cargo.
    def retrieveAnomalies(self, ship, planet):
        
        pass
    
    def update(self, displaySurface):
        self.runScanner(displaySurface)
        pass
    
    def runScanner(self, displaySurface):
        
        pass