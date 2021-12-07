# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:26:54 2019
Global Constants, used everywhere.
Note:  The constant bit refers to the naming...
@author: Nuke Bloodaxe
"""
import pygame, os


# Simple objects is declared and initialized here,
# class object types is declared here and initialized in the init method.

size = width, height = 640, 480  # screen dimensions
#  Planet texture constants.
planetHeight = 240  # 120
planetWidth = 480  # 240
#  It's certainly not a lively python...
version = "IronPython 0.02 - Frigid Snake Alpha"

#  Colours
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
VILE_PINK = (255, 0, 255)

ANOMALY = (0, 235, 0)

TECH1 = (50, 50, 0)
TECH2 = (100, 100, 0)
TECH3 = (150, 150, 0)
TECH4 = (200, 200, 0)
TECH5 = (250, 250, 0)

font: object
offset = 15  # for this font.

#  Totals for items
totalElements = 17
totalMaterials = 21
totalComponents = 22
totalDevices = 13
totalShields = 14
totalWeapons = 57
totalArtifacts = 911  #  Effectively unique items.
maxCargo = totalElements + totalMaterials + totalMaterials + totalComponents
maxCargo += totalDevices + totalShields + totalWeapons + 1


#  Game related constants; will be class integrated later.
gameStatus = 0

eventFlags = []  #  Having as event list of flags makes things much simpler

systemsVisited = []

starDate = [2, 3, 3784, 8, 75]  # M,D,Y,H,M, Default entry here is for new game.
gameDate: object  #  The game time needs to be accessible everywhere.


# Class objects need a separate init function
def init(init_game_date):
    #  Initialise music system and pygame
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    global font
    # Note: Font should resize according to resolution, but logic needed.
    #  Fonts:  this is a temporary google font, get it from them.
    font = pygame.font.Font(os.path.join('Fonts', 'Inconsolata-ExtraBold.ttf'), 14)

    # Initialise game objects
    global gameDate
    gameDate = init_game_date
