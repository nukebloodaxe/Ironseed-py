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
        self.imageShow = True  #  When image is not showing we see the
                                #  Heartbeat style EGO status line.
        self.pulseColourCycle = 0
        
        self.extendScreen = False
        self.extendScreenStep = 0
        
        self.shrinkScreen = False
        self.shrinkScreenStep = 0
        
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
        #  encode button required, but needs save faciliy.
        
    def update(self, displaySurface):
        return self.EGOInterfaceLoop(displaySurface)
    
    #  Draw the sine-wave status line.
    #  I have a feeling the randomness in Python is much higher than that in
    #  the pascal implementation, which is making it difficult to produce a
    #  waveform that is similar to the original.
    def drawStatusLine(self, displaySurface):
        
        random.seed(99)  #  Fix the generation, to provide consistency.
        #  For Sanity.
        self.crewPointer = self.crew.crew[self.currentCrewmember]
        #  Quicken Python namespace lookups
        physical = self.crewPointer.physical
        mental = self.crewPointer.mental
        emotional = self.crewPointer.emotion
        radiusMultiplier = ((g.height/200)*34)/100  #  (based on original 200 pixel height screen)
        lineStart = int((g.width/320)*145)
        lineFinish = int((g.width/320)*285)
        lineTop = int((g.height/200)*111)
        lineBottom = int((g.height/200)*179)
        pulseWidth = int((g.height/200)*145)  #  Mid-point of monitor.
        oldXY = (lineStart, lineTop+radiusMultiplier)  # start at 0.
        
        if self.pulseColourCycle == 0:
            
            self.pulseColourCycle = 255
        else:
            self.pulseColourCycle -= 15
        
        #print("Physical ", physical, " Emotional ", emotional, " Mental ", mental)
        
        for x in range(lineStart, lineFinish, int((g.width/320)*4)):  #  2 pixel steps 
            
            #currentColour = (0, 0, ((x-16)%32)+128)  #  Really... it's blue.
            currentColour = (0, 0, (x+self.pulseColourCycle)%255)  #  Really... it's blue.
            #  I'm wondering if the colour changes are not agressive enough...
            
            randomNumber = random.choice([0, 1, 2, 3, 4, 5])
            
            randY = 0  #  Our random y position.
            if randomNumber == 0:
                randY = physical * radiusMultiplier
                
            if randomNumber == 1:
                randY = mental * radiusMultiplier
            
            if randomNumber == 2:
                randY = emotional * radiusMultiplier
        
            if randomNumber == 3:
                randY = -1 * (physical * radiusMultiplier)
                
            if randomNumber == 4:
                randY = -1 * (mental * radiusMultiplier)
                
            if randomNumber == 5:
                randY = -1 * (emotional * radiusMultiplier)
            
            randY += pulseWidth
            
            pygame.draw.line(displaySurface, currentColour, oldXY, (x, randY), 1)
            
            oldXY = (x, randY)
    
        random.seed()  #  Make random random again ;)
    
    #  Mouse handling routines, handles all button press logic.
    #  The original did not have support for scrolling, but it could
    #  be introduced if the up and down arrows were converted to sliders.
    def interact(self, mouseButton):
        

        currentPosition = pygame.mouse.get_pos()
        #  Do you see what I mean by code sanity?
        self.crewPointer = self.crew.crew[self.currentCrewmember]
        
        if self.image.within(currentPosition):
            
            self.imageShow = True
            self.shrinkScreen = True
            
        elif self.evaluate.within(currentPosition):
            
            self.imageShow = False
            self.extendScreen = True
            
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
    
    #  TODO:  Checks for extending and shrinking screen.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.EGOInterfaceScaled, (0, 0))
        if self.imageShow:
            displaySurface.blit(self.crewPointer.resizedImage, ((g.width/320)*210, (g.height/200)*110))
        else:
            self.drawStatusLine(displaySurface)
    
    def EGOInterfaceLoop(self, displaySurface):
        
        #  Preparation routine
        if self.manipulationStage == 0:
            
            self.crewPointer = self.crew.crew[self.currentCrewmember]
            
            #  Start main intro music
            if self.musicState == False:
                
                pygame.mixer.music.load("sound\\PSYEVAL.OGG")
                pygame.mixer.music.play()
                self.musicState = True
                self.manipulationStage += 1
        
        elif self.manipulationStage == 1:
            
            self.drawInterface(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
        else:
            self.musicState = False
            self.manipulationStage = 0
            return 10  #  Return to Orbit view.
            #return 2  #  Go to main menu, but should be 10, for orbit.
        
        return self.systemState