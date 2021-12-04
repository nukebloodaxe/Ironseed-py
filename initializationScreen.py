#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 14:57:49 2021
This is additional to the original version of IronSeed.
This offers a quality of life improvement, and displays an initialization
screen showing progress for each area of the game during load and generation.
@author: nuke_bloodaxe
"""

import global_constants as g
import helper_functions as h
import io
import os
import pygame

InitData = []  # All screen initialization related data from disk.


class loadingBar(object):

    def __init__(self, leadGraphic, barColour, barText, title=False):

        self.percent = 0
        self.sprite = leadGraphic
        self.barColour = barColour
        self.barText = barText
        self.title = title  # We need to see if this is a section title line.


class initializationScreen(object):

    def __init__(self):

        self.loadingBars = []  # Progress bars and text for each section.
        self.step = 0  # We need to keep track of our process steps.
        self.barIndex = 0  # Index of first bar drawn on screen.

        # Graphics related section
        self.backgroundScreen = pygame.image.load(os.path.join('Graphics_Assets', 'saver.png'))

    #  Rendering routine, we use the default screen size.
    def screenRender(self):

        pass

    #  Run the intialization routine, including graphics update functions.
    def processData(self):

        self.screenRender()
        return True  # return true until all finished.


#  Loads all initialization screen data from the given file location.
#  Note: images are in numerical order for entries in IronPy_Initialization.tab
#  Note: Alpha formatted file support, allows mixed bar data.
def loadScreenData(file=os.path.join('Data_Generators', 'Other', 'IronPy_Initialization.tab')):

    initializationFile = io.open(file, "r")
    temp = ""  # Data Line

    while temp != "ENDF":

        barText = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
#        print("BarText", barText)

        if barText[0] == "ENDF":

            break

        barColour = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
#        print("BarColour", barColour)

        if barColour[0] == "EOD":

            InitData.append(loadingBar(None, None, barText, True))

        elif barColour[0] == "EOO":  # Suggests Alpha formatted file.

            InitData.append(loadingBar(None, None, barText))

        else:

            barGraphic = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
            temp = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Should capture EOO
            InitData.append(loadingBar(barGraphic, barColour, barText))

    initializationFile.close()
