# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 21:11:00 2020
EGO Synth Manipulation System
This system allows you to manipulate the EGO synths, shifting stats around
in an attempt to keep them both stable and productive.
@author: Nuke Bloodaxe
"""
import crew, buttons, pygame, random
import global_constants as g
import helper_functions as h

#  Main class for the system, which is effectively another minigame.
class EGOManipulator(object):
    
    def __init__(self, crewMembers):
        
        self.crew = crewMembers
        self.systemState = 9
        self.musicState = False
        self.currentCrewmember = 0
        self.crewPointer = 0  #  For code sanity!
        self.manipulationStage = 0
        #  Proposed figures from manipulation.
        self.proposedEmotion = 0
        self.proposedPhysical = 0
        self.proposedMental = 0
        self.maxBubbles = 50  #  Historical Max is 50.
        self.EGOInterface = pygame.image.load("Graphics_Assets\\psyche.png")
        self.EGOInterfaceScaled = pygame.transform.scale(self.EGOInterface, (g.width, g.height))
        self.EGOInterfaceScaled.set_colorkey(g.BLACK)
        
        #  Image and evaluate toggle
        self.imageShow = False  #  When image is not showing we see the
                                #  Heartbeat style EGO status line.
        
        #  define button positions for a 640x480 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen buttons.
        self.image = buttons.Button(15, 50, (360, 100)) # Based on 640x480
        self.evaluate = buttons.Button(15, 66, (416, 100))
        self.mentalUp = buttons.Button(12, 15, (502, 45))
        self.mentalDown = buttons.Button(12, 15, (616, 45))
        self.physicalUp = buttons.Button(12, 15, (502, 64))
        self.physicalDown = buttons.Button(12, 15, (616, 64))
        self.emotionalUp = buttons.Button(12, 15, (502, 84))
        self.emotionalDown = buttons.Button(12, 15, (616, 84))
        self.previous = buttons.Button(15, 35, (525, 100))
        self.next = buttons.Button(15, 35, (574, 100))
        self.exit = buttons.Button(42, 19, (597, 378))
        
    def update(self, displaySurface):
        return self.EGOInterfaceLoop(displaySurface)
    
    #  Mouse handling routines, handles all button press logic.
    #  The original did not have support for scrolling, but it could
    #  be introduced if the up and down arrows were converted to sliders.
    def interact(self, mouseButton):
        

        currentPosition = pygame.mouse.get_pos()
        #  Do you see what I mean by code sanity?
        self.crewPointer = self.crew.crew[self.currentCrewmember]
        
        if self.image.within(currentPosition):
            
            self.imageShow = True
            
        elif self.evaluate.within(currentPosition):
            
            self.imageShow = False
            
        elif self.mentalUp.within(currentPosition):
            
            if self.crewPointer.mental == 99 or self.crewPointer.emotion < 2 or self.crewPointer.physical == 99:
            
                pass
            
            else:
                self.crewPointer.mental += 1
                self.crewPointer.physical += 1
                self.crewPointer.emotion -= 2
                
        elif self.mentalDown.within(currentPosition):
            
            if self.crewPointer.mental == 0 or self.crewPointer.emotion > 97 or self.crewPointer.physical == 0:
            
                pass
            
            else:
                
                if self.crewPointer.mental > 0:
                    
                    self.crewPointer.mental -= 1
                
                if self.crewPointer.physical > 0:
                
                    self.crewPointer.physical -= 1
                
                self.crewPointer.emotion += 2
                    
        elif self.physicalUp.within(currentPosition):
            
            if self.crewPointer.mental < 2 or self.crewPointer.emotion == 99 or self.crewPointer.physical == 99:
            
                pass
            
            else:
                self.crewPointer.mental -= 2
                self.crewPointer.physical += 1
                self.crewPointer.emotion += 1
            
        elif self.physicalDown.within(currentPosition):
            
            if self.crewPointer.mental > 97 or self.crewPointer.emotion == 0 or self.crewPointer.physical == 0:
            
                pass
            
            else:
                self.crewPointer.mental += 2
                
                if self.crewPointer.physical > 0:
                
                    self.crewPointer.physical -= 1
                
                if self.crewPointer.emotion > 0:
                    
                    self.crewPointer.emotion -= 1
            
        elif self.emotionalUp.within(currentPosition):
            
            if self.crewPointer.mental == 99 or self.crewPointer.emotion == 99 or self.crewPointer.physical < 2:
            
                pass
            
            else:
                
                self.crewPointer.mental += 1
                self.crewPointer.physical -= 2
                self.crewPointer.emotion += 1
                    
        elif self.emotionalDown.within(currentPosition):
            
            if self.crewPointer.mental == 0 or self.crewPointer.emotion == 0 or self.crewPointer.physical > 97:
            
                pass
            
            else:
                if self.crewPointer.mental > 0:
                    
                    self.crewPointer.mental -= 1
                
                self.crewPointer.physical += 2
                
                if self.crewPointer.emotion > 0:
                    
                    self.crewPointer.emotion -= 1
                    
        elif self.previous.within(currentPosition):
            
            if self.currentCrewmember > 0:
                
                self.currentCrewmember -= 1
                
            else:
                self.currentCrewmember = 5
                
            self.crewPointer = self.crew.crew[self.currentCrewmember]
            
        elif self.next.within(currentPosition):
            
            if self.currentCrewmember == 5:
                
                self.currentCrewmember = 0
                
            else:
                self.currentCrewmember += 1
                
            self.crewPointer = self.crew.crew[self.currentCrewmember]
            
        elif self.exit.within(currentPosition):
            
            self.manipulationStage += 1
        
        return self.systemState
    
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.EGOInterfaceScaled, (0, 0))
    
    def EGOInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.manipulationStage == 0:
            
            #  Start main intro music
            if self.musicState == False:
                
                pygame.mixer.music.load("sound\\PSYEVAL.OGG")
                pygame.mixer.music.play()
                self.musicState = True
                self.manipulationStage += 1
        
        elif self.manipulationStage == 1:
            
            self.drawInterface(displaySurface)
            
        else:
            self.musicState = False
            self.manipulationStage = 0
            return 10  #  Return to Orbit view.
            #return 2  #  Go to main menu, but should be 10, for orbit.
        
        return self.systemState