# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:52:12 2019
Buttons: Handles all button graphics and stores the relative position
of where they are.  A button check handler can indicate if a given set of x/y
coordinates is within a given button, and return the index number for that
button.
@author: Nuke Bloodaxe
"""

import global_constants as g, helper_functions as h
import pygame

#  Buttons are square.
class Button(object):
    def __init__(self, height, width, position = (0, 0)): # Tuples of (X,Y)
        self.height = height
        self.width = width
        
        self.position = position  # Top left corner.
        
        # Store the values used to generate this button.
        self.resolutionX = g.width
        self.resolutionY = g.height
    
    # Set this position of the button on screen, we give the top left corner of
    # the button as a tuple of (x,y).
    def setPosition(self, position):
        self.position = position
    
    # Check if a given tuple of (x,y) is within the button area.
    # Note: given as screen position, so needs to be translated to button area.
    def within(self, position):
        
        isWithin = False
        
        if (position[0]>=self.position[0]) and (position[0]<=self.position[0]+self.width):
            if (position[1]>=self.position[1]) and (position[1]<=self.position[1]+self.height):
                isWithin = True
                
        return isWithin
    
    # Scale button to new current resolution.
    # The position of the button is also scaled.
    # Note: Call only if there has been a resolution change.
    def scale(self):
        
        multiplierX = 0
        multiplierY = 0
        
        if self.resolutionX < g.width:
            multiplierX = g.width / self.resolutionX 
        else:
            multiplierX = self.resolutionX / g.width
            
        if self.resolutionY < g.height:
            multiplierY = g.height / self.resolutionY 
        else:
            multiplierY = self.resolutionY / g.width

        self.width = int(self.width*multiplierX)
        self.height = int(self.height*multiplierX)
        
        self.position = (int(self.position[0]*multiplierX), int(self.position[1]*multiplierY))
        
        self.resolutionX = g.width
        self.resolutionY = g.height
        
# Ironseed has these big dialogue boxes that appear, we can handle those here.
class BigDialogueBox(Button):
    
    #  In this case the height and width dictate the full size of the main
    #  panel.
    def __init__(self, height, width, position, crewMember, message):

        Button.__init__(height, width, position)
        self.crewMember = crewMember
        self.message = message
        self.okButton = Button(int(self.height/5),
                               int(self.width/6),
                               (int((self.height/5)*4), int(self.width/3)))
    
    #  Untested work in progress.
    def drawDialogueBox(self, displaySurface):
        
        # Draw main Background rectangle 
        displaySurface.draw.fill(g.GREY, (int((g.height/200)*self.position[0]),
                                          int((g.width/320)*self.position[1]),
                                          int((g.height/200)*self.height),
                                          int((g.width/320)*self.width)))
        
        # Draw Highlight rim
        pygame.draw.rect(displaySurface,
                         (g.GREY[0]-20, g.GREY[1]-20, g.GREY[2]-20),
                         (int((g.height/200)*self.position[0]),
                          int((g.width/320)*self.position[1]),
                          int((g.height/200)*self.height),
                          int((g.width/320)*self.width)),
                         1)
        
        # Draw OK button Highlight Rim.  We use an optical illusion here.
        pygame.draw.rect(displaySurface,
                         (g.GREY[0]-20, g.GREY[1]-20, g.GREY[2]-20),
                         (int((g.height/200)*(self.position[0]+self.okButton.position[0])),
                          int((g.width/320)*(self.position[1]+self.okButton.position[1])),
                          int((g.height/200)*self.okButton.height),
                          int((g.width/320)*self.okButton.width)),
                         1)
        
        # Draw OK text.
        h.renderText(["OK"], g.font, displaySurface, g.BLACK, 0,
                     int((g.width/320)*(self.position[1]+self.okButton.position[1])),
                     int((g.height/200)*(self.position[0]+self.okButton.position[0])))
        
    
    def checkButtonClicked(self, position):

        return self.okButton.within(position)
