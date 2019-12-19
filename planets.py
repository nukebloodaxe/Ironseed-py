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

PlanetarySystems = {} #original code indicates these max out at 250.

Planets = {} #original code indicates these max out at 1000

class Planet(object):
    def __init__(self, name="Bug", state=0, grade='A', orbit = 0):
        self.name = name
        self.state = state
        self.grade = grade #could be "mode" in original code.
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
        #Note: if you see a system with a star called 'Bug', then you have a problem.
        
class PlanetarySystem(object):
    def __init__(self,  planets, systemName = "Buggy"):
        self.systemName = systemName
        #Visitation related info
        self.dateMonth = 0
        self.dateYear = 0
        self.visits = 0
        
        
        self.planets = planets
        
        self.orbits = [] #Add to list in orbit order.  0 should be star.
        #The provided planets may be out of order, so we play it safe.
        for count in range(len(planets)+1):
            self.orbits.append(0)

        for planet in planets:
            self.orbits[planet.orbit] = planet
        
def initialisePlanets(filename):
    #load planet files and populate planet structure
    #planet by name = (planet name, state, variation, tech level/life)
    Planets["mars"] = ("mars",4,'C',5)
    
def transformCheckPlanet(planet):
    name, state, grade, life = Planets[planet]
    # chance of transformation.
    
    #BIG ALGO HERE
    Planets[planet] = (name,state,grade)
    
