# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:26:00 2019
Ship Datastructure
@author: Nuke Bloodaxe
"""

import io, pygame, crew, items, random, global_constants as g

# The ship our crew are haunting...
class Ship(object):
    def __init__(self):
        self.guns = []
        self.cargo = []
        self.maxfuel = 0
        self.mass = 0
        self.acceleration = 0
        self.hullMax = 0
        #self.Crew() # debating about storing this here...
    
    