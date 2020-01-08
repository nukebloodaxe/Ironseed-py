# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:54:40 2020
Aliens! : Stores much the same as a crewmember, but simplified with a few extras.
Alien Ships: The aliens live on ships as well, strange that.
@author: Nuke Bloodaxe
"""

Aliens = {} # All alien factions, can custom populate during game!
AlienConversations = {} # Alien conversation sets by type.

class Alien(object):
    def __init__(self, name = "FaceHugger", alienType = 0, techRange = (0,0),
                 Anger = 0, congeniality = 0, victory = 0, id = 0,
                 conversationSet = 0, atWar = False):
        
        pass
    
def loadAliens(file = ""):
    
    pass