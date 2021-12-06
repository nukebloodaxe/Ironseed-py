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
        self.stringAvailable = False
        self.barString = ""
        self.barTextProgress = [h.rotatingLine(0)]
        self.title = title  # We need to see if this is a section title line.
        self.rotator = 0

    #  Rotate the rotating character.
    def progressRotator(self):

        # Keep the rotator turning with each update call.
        self.rotator += 1

        if self.rotator > 8:

            self.rotator = 0

        self.barTextProgress.pop()  # remove rotator character.
        self.barTextProgress.append(h.rotatingLine(self.rotator))

    # Set the progress bar to a new length, based on a percentage and
    # character limit.
    def setProgressBar(self, percentage, limit):

        stars = int(percentage * (limit/100))
        self.barTextProgress = []

        for char in range(stars):

            self.barTextProgress.append('*')

        if percentage < 100:

            self.barTextProgress.append('|')

        self.stringAvailable = False

    # Get the current progress bar as a string
    def getProgressBar(self):

        if not self.stringAvailable:

            self.barString = ""

            for char in self.barTextProgress:

                self.barString += char

            self.stringAvailable = True

        return self.barString


class initScreen(object):

    def __init__(self, displaySurface):

        self.loadingBars = InitData  # Progress bars and text for each section.
        self.step = 0  # We need to keep track of our process steps.
        self.barIndex = 0  # Index of first bar drawn on screen.

        # Graphics related section
        self.displaySurface = displaySurface
        self.backgroundScreen = pygame.image.load(os.path.join('Graphics_Assets', 'saver.png'))

        # Scaled Graphics
        self.scaledBackgroundScreen = pygame.transform.scale(self.backgroundScreen, (g.width, g.height))
        self.scaledBackgroundScreen.set_colorkey(g.BLACK)

        # Line and character limits for this resolution.
        self.lineLimit = h.textLinesWithin(0, g.height)
        self.characterLimit = h.charactersWithin(0, g.width)

    #  Add a new loading bar
    def addLoadingBar(self, leadGraphic, barColour, barText, title=False):

        self.loadingBars.append(loadingBar(leadGraphic, barColour, barText, title))

    #  Set the process step we are on.
    def setProcessStep(self, step):

        self.step = step

        # Check to see which step we need to render from, so we don't overshoot
        # the bottom of the screen.
        if self.step > self.lineLimit:

            self.barIndex = self.lineLimit - self.step

    #  Rendering routine, we use the default screen size.
    def screenRender(self):

        self.displaySurface.fill(g.BLACK)
        self.displaySurface.blit(self.scaledBackgroundScreen, (0, 0))

        # now coalate the text and render it.
        textToPrint = []

        for bar in self.loadingBars[self.barIndex:self.step+1]:

            textToPrint.append(bar.barText[0])
            textToPrint.append(bar.getProgressBar())
            #print(bar.barText)

        # Note: Very simple for now.
        h.renderText(textToPrint, g.font, self.displaySurface, g.WHITE, g.offset)
        pygame.display.update()

    #  Run the intialization routine, including graphics update functions.
    #  Progress is the % progress return from another object.
    def processData(self, progress):

        # Set completed bar length to progress.
        self.loadingBars[self.step].setProgressBar(progress, self.characterLimit)

        if progress < 100:

            self.loadingBars[self.step].progressRotator()

        if progress == 100:

            return False

        else:

            return True  # return true until all finished.

    #  Update loop.
    def update(self, progress):

        status = self.processData(progress)
        self.screenRender()
        return status


#  Loads all initialization screen data from the given file location.
#  Note: images are in numerical order for entries in IronPy_Initialization.tab
#  Note: Alpha formatted file support, allows mixed bar data.
def loadScreenData(file=os.path.join('Data_Generators', 'Other', 'IronPy_Initialization.tab')):

    initializationFile = io.open(file, "r")
    temp = ""  # Data Line

    while temp != "ENDF":

        barText = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
        #print("BarText", barText)

        if barText[0] == "ENDF":

            break

        barColour = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
#        print("BarColour", barColour)

        if barColour[0] == "EOD":  # Data entry is a section title.

            InitData.append(loadingBar(None, None, barText, True))

        elif barColour[0] == "EOO":  # Suggests Alpha formatted file.

            InitData.append(loadingBar(None, None, barText))

        else:

            barGraphic = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Data Line
            temp = (h.loadLineStripComment(initializationFile).split('\n')[0]).split('\t')  # Should capture EOO
            InitData.append(loadingBar(barGraphic, barColour, barText))

    initializationFile.close()
