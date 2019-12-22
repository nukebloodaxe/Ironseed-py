# -*- coding: utf-8 -*-
"""
Created on Tues Dec 17 22:08:18 2019
Planets
These really deserve their own class and file.
@author: Nuke Bloodaxe
"""

#State:
#0: Gaseous, A:Nebula, B:Gas Giant, C:Heavy Atmosphere
#1: Active, A: Volcanic, B: Semi-Volcanic, C: Land Formation
#2: Stable, A: Land and Water, B: Slight Vegitation, C: Medium Vegitation (Tech 0)
#3: Early Life, A: Heavy Vegitation (tech 0), B: Medium Vegitation (tech 1), C: Medium Vegitation (Tech 2)
#4: Advanced Life, A: Medium Vegitation (tech 3), B:Slight Vegitation (tech 3), C: No Vegitation (Tech 5)
#5: Dying, A:Ruins, B:Medium Vegitation, C:Dead Rock
#6: Dead, A:Radiation, B:Asteroid, C:Null
#7: Star, A:Yellow, B:Red, C:White

#name, State, variation, Life/Technology level
#Check utils2.pas, it contains most planet related details and old algos.

import io, pygame, global_constants as g

PlanetarySystems = {} #original code indicates these max out at 250.

Planets = {} #original code indicates these max out at 1000

class Planet(object):
    def __init__(self, name="Bug", state=0, grade='A', orbit = 0):
        self.name = name
        self.state = state
        self.grade = grade #Appears to be "mode" in original code.
        self.size = 1
        self.water = 0
        self.age = 0
        self.bots = 0
        self.notes = 0
        self.seed = 0 #seed used for procedural generation.
        self.cache = [] #item cache, limit of 7 items.
        #Visitation date related info:
        self.dateMonth = 0
        self.dateYear = 0
        self.visits = 0
        self.outpost = 0 #Extra feature, is this an outpost?
        self.owned = 0 #Extra feature, the owner of the planet.
        self.orbit = orbit
        
        #Planet texture related data
        planetTexture = pygame.Surface((g.planetHeight, g.planetWidth), 0)
        self.createPlanet()
        #Note: if you see a system with a star called 'Bug', then you have a problem.
    
    #Get the technology level of the planet.
    def getTechLevel(self, system):
        if self.orbit == 0:
            return 0 #We are a star... although, what about Dyson spheres?
        techLevel = -2
        if system in ["KODUH","OLEZIAS","IYNK","TEVIX","SEKA","WIOTUN"]:
            return 6*256 #Really...
        
        if system == "EXOPID":
            
            if 27 in g.eventFlags:
                return 0
            else:
                return 6*256
        
        if self.state == 2:
            if self.grade == 2:
                techLevel == -1
            elif self.grade == 3:
                techLevel += self.age / 15000000
        
        elif self.state == 3:
            techLevel = (self.state - 1) * 256
            if self.grade == 1:
                techLevel += self.age / 15000000
            elif self.grade == 2:
                techLevel += self.age / 1000
            elif self.grade == 3:
                techLevel += self.age / 800
        
        elif self.state == 4:
            techLevel = (self.state + 2) * 256
            if self.grade == 1:
                techLevel += self.age / 400
            elif self.grade == 2:
                techLevel += self.age / 200

        elif self.state == 5:
            if self.grade == 1:
                temp = self.age / 100000000
                if temp > 9:
                    temp = 9
                techLevel += temp
            elif self.grade == 2:
                techLevel = -1
        
        elif self.state == 6:
            if self.grade == 2: #Void Dwellers.
                techLevel = 6*256
        
        return techLevel
    
    #This effectively ages the planet based on the time since last visit.
    def adjustPlanets(self):
        pass
    
    #This function handles materials and components for display.
    def getSubQuantities(self):
        
        pass
    
    #Scans are predefined, so populate the planet item cache accordingly.
    def getItemAmounts(self):
        
        pass
    
    #Add items to the planet, including results of surface mining/manufacturing.
    def addItems(self):
        
        pass
    
    #Create the planet texture, which uses the random pixel height-change
    #method to raise and lower terrain.
    def createPlanet(self):
        planetSurface = pygame.PixelArray(self.planetTexture)
        
        
        
        pass

    #Update the planet, this is assuming there has been a change.
    def update(self):
        pass
    
    
        
class PlanetarySystem(object):
    def __init__(self,  planets, systemName = "Buggy"):
        self.systemName = systemName
        #Visitation related info
        self.dateMonth = 0
        self.dateYear = 0
        self.visits = 0
        self.positionX = 0
        self.positionY = 0
        self.positionZ = 0
        
        
        self.planets = planets
        
        self.orbits = [] #Add to list in orbit order.  0 should be star.
        #The provided planets may be out of order, so we play it safe.
        for count in range(len(planets)+1):
            self.orbits.append(0)

        for planet in planets:
            self.orbits[planet.orbit] = planet
            
    #Get the tech level for a particular planet.
    def getTechLevel(orbit):
        self.orbits[orbit].getTechLevel(self.systemName)
        
    #Update the system, which is normally based on time passed since last visit.
    def updateSystem(self):
        pass


def initialisePlanets(fileName):
    #load planet files and populate planet structure
    #planet by name = (planet name, state, variation, tech level/life)
    Planets["mars"] = ("mars",4,'C',5)


#Note: Make sure you initialise the planets!
def initialiseSystems(fileName="Data_Generators\Other\Ironpy_SystemData.tab")

    pass
    
def transformCheckPlanet(planet):
    name, state, grade, life = Planets[planet]
    # chance of transformation.
    
    #BIG ALGO HERE
    Planets[planet] = (name,state,grade)

#Render a planet using an approximation of the old IronSeed Algorithm.
#Note: I'm thinking high-quality pre-renders might be a better choice.
#landtype= array[1..240,1..120] of byte;
def renderPlanet(width, height, planetType, surface, step=0):
    comboSurface = pygame.Surface(g.size)
    finished = False
    #comboSurface.set_alpha(step*10)
    safeSurface = pygame.PixelArray(surface)
    safeCombo = pygame.PixelArray(comboSurface)
    #we create the planet first, then blit the pixels onto the original
    #surface.  Unfortunately, the creation process is not fast.
    
    
    
    # Now to the copy, taking into account the transparency layer.
    line = 0
    while line<g.height:
        for pixel in range(g.width):
            if safeCombo[pixel][line] != 0:
                safeSurface[pixel][line]=safeCombo[pixel][line]            
            
        line += 1
            
    #surface.blit(comboSurface,(0,0))
    del safeSurface
    del safeCombo
    if (step*10) >= 255:
        finished = True
    return finished