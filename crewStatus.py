# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:02:17 2020

The Crew Status viewer for Ironseed.
Here you can see XP, crew bio readouts, their profile etc.

@author: Nuke Bloodaxe
"""

import buttons, pygame, os
import global_constants as g
import helper_functions as h

#  Main class for the Crew Status screen, which is yet another minigame.
class CrewStatus(object):
    
    def __init__(self, theCrew):
        
        self.crew = theCrew
        self.systemState = 13
        self.musicState = False
        self.crewStatusStage = 0  #  Setup/interaction stage.
        self.pulseColourCycle = 255  #  for Ego Bio Status line.  Red Pulse.
        self.currentCrewMember = 1
        self.crewPositions = ["", "PSYCHOMETRY", "ENGINEERING", "SCIENCE", "SECURITY", "ASTROGATION", "MEDICAL"]
        
        #  Graphics related
        self.crewInterface = pygame.image.load(os.path.join('Graphics_Assets', 'char2.png'))
        self.crewInterfaceScaled = pygame.transform.scale(self.crewInterface, (g.width, g.height))
        self.crewInterfaceScaled.set_colorkey(g.BLACK)
        
        #  Create individual graphical elements.
        
        
        #  Handle display area of the crew heartbeat line.
        self.pulseDisplayArea = pygame.Rect((int((g.width/320)*16),
                                             int((g.height/200)*14)),
                                            (int((g.width/320)*180),
                                             int((g.height/200)*76)))
        
        #  Define button positions scaled from a 320x200 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.exit = buttons.Button(int((g.height/200)*14),
                                   int((g.width/320)*9),
                                   (int((g.width/320)*302),
                                    int((g.height/200)*155)))
        
    
    #  Reset the Crew Status system back to default starting values.
    def resetCrewStatus(self):
        
        self.crewStatusStage = -1  # Forces reset when we return.
        self.pulseColourCycle = 255
        self.musicState = False
    
    
    #  Update loop.
    def update(self, displaySurface):

        return self.crewInterfaceLoop(displaySurface)
        
        
        
    #  Mouse handling routines, handles all button press logic.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.exit.within(currentPosition):
            
            self.resetCrewStatus()
                        
            self.systemState = 10
            #  Reset crew status stage and enter command deck state.
        
        return self.systemState
    
    
    #  Interface drawing routine.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.crewInterfaceScaled, (0, 0))
        self.crew.crew[self.currentCrewMember].drawStatusLine(displaySurface, self.pulseDisplayArea, 0)
        
    #  Our main interface loop, here we run all setup and stage checks.
    def crewInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.crewStatusStage == 0:
            
            #  We need to ensure our system state is set.
            self.systemState = 13
            
            #  Start main intro music
            if self.musicState == False:
                
                pygame.mixer.music.load(os.path.join('sound', 'CREWCOMM.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.crewStatusStage += 1
        
        elif self.crewStatusStage == 1:
            
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                
                pygame.mixer.music.play()
            
            self.drawInterface(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
            
        if self.systemState != 13:
            
            self.crewStatusStage = 0
            self.musicState = False
        
        return self.systemState