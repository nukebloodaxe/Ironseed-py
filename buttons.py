# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:52:12 2019
Buttons: Handles all button graphics and stores the relative position
of where they are.  A button check handler can indicate if a given set of x/y
coordinates is within a given button, and return the index number for that
button.
@author: Nuke Bloodaxe
"""

import global_constants as g

class Button(object):
    def __init__(self, height, width): # Tuples of (X,Y)
        self.height
        self.width
        
        self.position = (0,0)
        
        # Store the values used to generate this button.
        self.resolutionX = g.width
        self.resolutionY = g.height
    
    # Set this position of the button on screen, we give the top left corner of
    # the button as a tuple of (x,y).
    def setPosition(position):
        self.position = position
    
    # Check if a given tuple of (x,y) is within the button area.
    # Note: given as screen position, so needs to be translated to button area.
    def within(position):
        
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
        