# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:26:54 2019
Global Constants, used everywhere.
Note:  The constant bit refers to the naming...
@author: Nuke Bloodaxe
"""
import pygame, os

size = width, height = 640, 480  # screen dimensions
#  Planet texture constants.
planetHeight = 240  # 120
planetWidth = 480  # 240
#  It's certainly not a lively python...
version = "IronPython 0.01 - Frigid Snake Alpha"

#  Initialise music system and pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

#  Colours
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

ANOMALY = (0, 235, 0)

TECH1 = (50, 50, 0)
TECH2 = (100, 100, 0)
TECH3 = (150, 150, 0)
TECH4 = (200, 200, 0)
TECH5 = (250, 250, 0)

#  Fonts:  this is a temporary google font, get it from them.
font = pygame.font.Font(os.path.join('Fonts', 'Inconsolata-ExtraBold.ttf'), 14)
offset = 20  # for this font.

#  Totals for items
totalElements = 17
totalMaterials = 21
totalComponents = 22
totalDevices = 13
totalShields = 14
totalWeapons = 57
maxCargo = totalElements + totalMaterials + totalMaterials + totalComponents
maxCargo += totalDevices + totalShields + totalWeapons + 1


#  Game related constants; will be class integrated later.
gameStatus = 0

eventFlags = []  #  Having as event list of flags makes things much simpler

systemsVisited = []

starDate = [2, 3, 3784, 8, 75]  #M,D,Y,H,M, Default entry here is for new game.
gameDate = "Placeholder"  #  The game time needs to be accessible everywhere.