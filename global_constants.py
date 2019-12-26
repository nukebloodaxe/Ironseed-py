# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:26:54 2019
Global Constants, used everywhere.
@author: Nuke Bloodaxe
"""
import pygame

size = width, height = 640, 480 # screen dimensions
#Planet texture constants.
planetHeight = 120
planetWidth = 240
version = "IronPython 0.01 - FrigidSnake Alpha"

# Initialise music system and pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

#colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

#fonts
font = pygame.font.Font('Fonts\\NotoSansTC-Regular.otf', 12)
offset = 20 # for this font.

# Totals for items
totalElements = 17
totalMaterials = 21
totalComponents = 22
totalDevices = 13
totalShields = 14
totalWeapons = 57
maxCargo = totalElements + totalMaterials + totalMaterials + totalComponents
maxCargo += totalDevices + totalShields + totalWeapons + 1


#game related constants; will be class integrated later.
gameStatus = 0

eventFlags = [] # Having the events system as flags makes things much simpler.

systemsVisited = []

starDate = [2,3,3784,8,75] #M,D,Y,H,M, Default entry here is for new game.