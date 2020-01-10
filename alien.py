# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:54:40 2020
Aliens! : Stores much the same as a crewmember, but simplified with a few extras.
Alien Ships: The aliens live on ships as well, strange that.
@author: Nuke Bloodaxe
"""

Aliens = {} # All alien factions, can custom populate during game!
AlienConversations = {} # Alien conversation sets by type.

class AlienShip(object):
    
    def __init__(self, relativeX, relativeY, relativeZ, techLevel, skill,
                 shield, battery, shieldLevel, hullDamage,
                 destinationX, destinationY, destinationZ, maxHull,
                 maxAcceleration, regeneration, shipPicture, alien,
                 name = "Nostromo" ):
        self.relativeX = relativeX
        self.relativeY = relativeY
        self.relativeZ = relativeZ
        self.techLevel = techLevel
        self.skill = skill
        self.shield = shield
        self.battery = battery
        self.shieldLevel = shieldLevel
        self.hullDamage = hullDamage
        self.destinationX = destinationX
        self.destinationY = destinationY
        self.destinationZ = destinationZ
        self.maxHull = maxHull
        self.maxAcceleration = maxAcceleration
        self.regeneration = regeneration
        self.shipPicture = shipPicture
        self.alien = alien
        self.name = name
        self.damage = [0, 0, 0, 0, 0, 0, 0]
        self.gunNodes = [0, 0, 0, 0, 0]
        self.charges = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    

class Alien(object):
    def __init__(self, name = "FaceHugger", alienType = 0, techRange = (0,0),
                 Anger = 0, congeniality = 0, victory = 0, id = 0,
                 conversationSet = 0, atWar = False):
        
        pass
    
def loadAliens(file = ""):
    
    pass