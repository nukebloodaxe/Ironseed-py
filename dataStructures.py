# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:10:18 2019
DataStructures
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

planets = {}

def initialisePlanets(filename):
    #load planet files and populate planet structure
    #planet by name = (planet name, state, variation, tech level/life)
    planets["mars"] = ("mars",4,'C',5)
    
def transformCheckPlanet(planet):
    name, state, variation, life = planets[planet]
    # chance of transformation.
    
    #BIG ALGO HERE
    planets[planet] = (name,state,variation,life)
    
