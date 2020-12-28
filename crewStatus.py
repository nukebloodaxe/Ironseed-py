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
        self.currentCrewMember = 0
        self.crewPointer = "placeholder"  # For Sanity.
        self.crewPositions = ["", "PSYCHOMETRY", "ENGINEERING", "SCIENCE", "SECURITY", "ASTROGATION", "MEDICAL"]
        
        #  Graphics related
        self.crewInterface = pygame.image.load(os.path.join('Graphics_Assets', 'char2.png'))
        self.crewInterfaceScaled = pygame.transform.scale(self.crewInterface, (g.width, g.height))
        self.crewInterfaceScaled.set_colorkey(g.BLACK)
        
        self.frameCount = 0  #  For keeping track of animation frames.
        self.titleFrameCount = 0  #  For keeping track of title frames.
        self.pseudoTextCount1 = 0  #  For keeping track of pseudo text frames.
        self.pseudoTextCount2 = 1  #  For keeping track of pseudo text frames.
        
        #  Create individual graphical elements.
        
        #  left, top, width, height
        #  Handle display area of the crew heartbeat line.
        self.pulseDisplayArea = pygame.Rect((int((g.width/320)*16),
                                             int((g.height/200)*14)),
                                            (int((g.width/320)*180),
                                             int((g.height/200)*76)))
        
        #  Handle display area of horizontal pulse line.
        self.pulseLineArea = pygame.Rect((int((g.width/320)*42),
                                          int((g.height/200)*122)),
                                         (int((g.width/320)*38),
                                          int((g.height/200)*2)))
        
        #  Handle display area of the sanity bar; red.
        self.sanityBarArea = pygame.Rect((int((g.width/320)*309),
                                          int((g.height/200)*26)),
                                         (int((g.width/320)*2),
                                          int((g.height/200)*68)))
        
        #  Handle the blanking area to clear texture elements.
        self.blankDisplayArea = pygame.Rect((int((g.width/320)*5),
                                             int((g.height/200)*130)),
                                            (int((g.width/320)*259),
                                             int((g.height/200)*67)))
        
        #  Location of green crew pips when crewmember selected.
        self.greenCrewLEDLocation = [(303, 142),(303, 145),(303, 148),
                                     (310, 142),(310, 145),(310, 148)]
        
        self.currentGreenLED = pygame.Rect((int((g.width/320)*303),
                                            int((g.height/200)*142)),
                                           (int((g.width/320)*2),
                                            int((g.height/200)*2)))
        
        #  Tuple list for the Sanity bar.
        self.sanityBar = h.colourGradient(self.sanityBarArea.height, g.RED)
        
        #  Tuple list for micro pulse line.
        self.pulseLine = h.colourGradient(self.pulseLineArea.width, g.RED)
        
        #  Animation array for text displayed in window above buttons.
        self.titleText = []
        self.pseudoText = []
        
        self.titleTextDraw = pygame.Rect((int((g.width/320)*273),
                                          int((g.height/200)*121)),
                                          (int((g.width/320)*38),
                                           int((g.height/200)*9)))
        
        self.pseudoTextDraw1 = pygame.Rect((int((g.width/320)*273),
                                            int((g.height/200)*132)),
                                           (int((g.width/320)*18),
                                            int((g.height/200)*9)))
        
        self.pseudoTextDraw2 = pygame.Rect((int((g.width/320)*292),
                                            int((g.height/200)*132)),
                                           (int((g.width/320)*18),
                                            int((g.height/200)*9)))
        
        
        # formatted (x,y)(width,height)(columns,rows)
        self.textTitleLocations = ((9, 144), (39, 10), (3, 2))
        self.pseudoTextLocations = ((129, 145), (20, 8), (2, 4))
        
        #  Scaled animation arrays for screen text.
        self.scaledTitleText = []
        self.scaledPseudoText = []
        
        #  Load in above textures.
        self.prepareAnimationFrames()
        
        #  Scale above textures
        self.scaleAnimationFrames()
        
        #  Define button positions scaled from a 320x200 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.exit = buttons.Button(int((g.height/200)*14),
                                   int((g.width/320)*9),
                                   (int((g.width/320)*302),
                                    int((g.height/200)*155)))
        
        self.up = buttons.Button(int((g.height/200)*14),
                                   int((g.width/320)*17),
                                   (int((g.width/320)*280),
                                    int((g.height/200)*146)))
        
        self.down = buttons.Button(int((g.height/200)*14),
                                   int((g.width/320)*17),
                                   (int((g.width/320)*280),
                                    int((g.height/200)*162)))
    
    
    #  Prepare all animation frames from the screen graphic.
    def prepareAnimationFrames(self):
        
        self.titleText = h.prepareAnimationArray(self.crewInterface,
                                                 self.textTitleLocations,
                                                 False)
        
        self.pseudoText = h.prepareAnimationArray(self.crewInterface,
                                                  self.pseudoTextLocations,
                                                  False)

    
    #  Scale animation frames to current resolution.
    def scaleAnimationFrames(self):
        
        self.scaledTitleText = h.resizeGraphicArray(self.titleText)
        self.scaledPseudoText = h.resizeGraphicArray(self.pseudoText)

    
    #  Reset the Crew Status system back to default starting values.
    def resetCrewStatus(self):
        
        self.crewStatusStage = -1  # Forces reset when we return.
        self.pulseColourCycle = 255
        self.musicState = False
    
    
    #  Update loop.
    #  Note:  This is one of the basics of polymorphism, where functions
    #  have common names across diffrent classes.  The idea being to simplify
    #  overall coding.
    def update(self, displaySurface):

        return self.crewInterfaceLoop(displaySurface)
        
        
        
    #  Mouse handling routines, handles all button press logic.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.up.within(currentPosition):
            
            self.currentCrewMember += 1
            
            if self.currentCrewMember > 5:
                
                self.currentCrewMember = 0
                
            self.crewPointer = self.crew.crew[self.currentCrewMember] # For Sanity.
            
            self.currentGreenLED = pygame.Rect((int((g.width/320)*self.greenCrewLEDLocation[self.currentCrewMember][0]),
                                                int((g.height/200)*self.greenCrewLEDLocation[self.currentCrewMember][1])),
                                               (int((g.width/320)*2),
                                                int((g.height/200)*2)))
                
        elif self.down.within(currentPosition):
            
            self.currentCrewMember -= 1
            
            if self.currentCrewMember < 0:
                
                self.currentCrewMember = 5
                
            self.crewPointer = self.crew.crew[self.currentCrewMember] # For Sanity.
            
            self.currentGreenLED = pygame.Rect((int((g.width/320)*self.greenCrewLEDLocation[self.currentCrewMember][0]),
                                                int((g.height/200)*self.greenCrewLEDLocation[self.currentCrewMember][1])),
                                               (int((g.width/320)*2),
                                                int((g.height/200)*2)))
        
        elif self.exit.within(currentPosition):
            
            self.resetCrewStatus()
                        
            self.systemState = 10
            #  Reset crew status stage and enter command deck state.
        
        return self.systemState
    
    
    #  Interface drawing routine.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.crewInterfaceScaled, (0, 0))
        
        #  Render heartbeat pulse line in red.
        self.crewPointer.drawStatusLine(displaySurface, self.pulseDisplayArea, 0)
        
        #  Render small pulse line in red.
        pulse = h.createBar(self.pulseLine, len(self.pulseLine), self.pulseLineArea.height)
        displaySurface.blit(pulse, self.pulseLineArea)
        
        #  Make pulse rotate right after each frame.
        self.pulseLine = h.shiftArrayRight(self.pulseLine)
        
        #  Render crewmember image.
        displaySurface.blit(self.crewPointer.resizedImage,
                            ((g.width/320)*220, (g.height/200)*16))
        
        #  Render green LED for selected crew member.
        displaySurface.fill(g.GREEN, self.currentGreenLED)
        
        #  Calculate sanity bar length
        sanityBarLength = int((self.sanityBarArea.height/100)*self.crewPointer.sanity)
        
        #  Create sanity bar tuple list.
        sanityBar = h.colourGradient(sanityBarLength, g.RED)
        
        #  Render sanity bar for selected crew member.
        adjustedSanityBar = h.createBar(sanityBar,
                                        sanityBarLength,
                                        self.sanityBarArea.height)
        rotatedSanityBar = pygame.transform.rotate(adjustedSanityBar, -90)
        scaledSanityBar = pygame.transform.scale(rotatedSanityBar,
                                                 (self.sanityBarArea.width,
                                                  sanityBarLength))
        displaySurface.blit(scaledSanityBar, self.sanityBarArea)
        
        #  Render pretty graphics in mini-monitor for ambiance.
        
        displaySurface.blit(self.scaledTitleText[self.titleFrameCount],
                            self.titleTextDraw)
        
        displaySurface.blit(self.scaledPseudoText[self.pseudoTextCount1],
                            self.pseudoTextDraw1)
        
        displaySurface.blit(self.scaledPseudoText[self.pseudoTextCount2],
                            self.pseudoTextDraw2)
        
        #  Adjust frame counters and timers.
        if self.frameCount >= 20:
            
            self.titleFrameCount += 1
            
            if self.titleFrameCount >= len(self.scaledTitleText):
                
                self.titleFrameCount = 0
            
            self.frameCount = 0
        
        elif self.frameCount in [0, 5, 10, 15, 20]:
            
            self.pseudoTextCount1 += 1
            self.pseudoTextCount2 += 1
            
            if self.pseudoTextCount1 >= len(self.scaledPseudoText):
                
                self.pseudoTextCount1 = 0
            
            if self.pseudoTextCount2 >= len(self.scaledPseudoText):
                
                self.pseudoTextCount2 = 0
        
        self.frameCount += 1
        
        #  Clear text area.
        displaySurface.fill(g.BLACK, self.blankDisplayArea)
        
        #  Render Bio column of text.
        h.renderText(self.crewPointer.bio, g.font, displaySurface, g.WHITE, 15, (g.width/320)*6, (g.height/200)*131)
        
        #  Render Character Level text.
        h.renderText([str(self.crewPointer.level)], g.font, displaySurface, g.WHITE, 15, (g.width/320)*154, (g.height/200)*120)
        
        #  Render Character Experience points.
        h.renderText([str(self.crewPointer.experience)], g.font, displaySurface, g.WHITE, 15, (g.width/320)*190, (g.height/200)*120)
        
        #  Render Character Name.  Note, using 180 for x as is centre of text field.
        h.renderText([str(self.crewPointer.name)], g.font, displaySurface, g.WHITE, 15, (g.width/320)*180, (g.height/200)*103, True)
        
    #  Our main interface loop, here we run all setup and stage checks.
    def crewInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.crewStatusStage == 0:
            
            #  We need to ensure our system state is set.
            self.systemState = 13
            self.crewPointer = self.crew.crew[self.currentCrewMember] # For Sanity.
            
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