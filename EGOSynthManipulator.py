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
        
        # Gradient as a list of tuples.
        self.redBar = h.colourLine(int((g.width/320)*63), g.RED)
        
        #  Prepare texture sections for monitor screen shrink and grow.
        
        #  Bars for copy: 217, 103, ends at 186
        
        self.screenBar = pygame.Surface((1, 84))
        self.screenBar.blit(self.EGOInterface, (0, 0), (217, 103, 1, 84))
        self.screenBarScaled = pygame.transform.scale(self.screenBar, (int((g.width/320)), int((g.height/200)*84)))
        self.screenBarScaled.set_colorkey(g.BLACK)
        
        #  movable screen edge: 194, 99 to 217 width.  190 end height.
        
        self.screenBracket = pygame.Surface((23, 94))
        self.screenBracket.blit(self.EGOInterface, (0, 0), (194, 99, 23, 94))
        self.screenBracketScaled = pygame.transform.scale(self.screenBracket, (int((g.width/320)*23), int((g.height/200)*94)))
        self.screenBracketScaled.set_colorkey(g.BLACK)
        
        #  Blanking rectangle.
        self.blankRectangle = (int((g.width/320)*127), int((g.height/200)*99), int((g.width/320)*90), int((g.height/200)*94))
        
        #  Image and evaluate toggle
        self.imageShow = True   #  When image is not showing we see the
                                #  Heartbeat style EGO status line.
        self.pulseColourCycle = 0
        
        #  Monitor shrink/grow flags/steps.
        self.extendScreen = False
        self.shrinkScreen = False
        self.screenStep = 0
        self.maxStep = int((g.width/320)*60)
        
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
        #  TODO: encode button required, but needs save facility.
        
    def update(self, displaySurface):
        return self.EGOInterfaceLoop(displaySurface)
    
    #  Drawing routine for shrinking and growing the in-game monitor screen.
    def drawMonitorMovement(self, displaySurface):
        
        barXY = (int((g.width/320)*217), int((g.height/200)*104))
        bracketXY = (int((g.width/320)*195), int((g.height/200)*99))
        
        #  194, 99  is top-left of monitor panel.
        
        if self.extendScreen:
            
            if self.screenStep < self.maxStep:
                
                self.screenStep += 1
        
        elif self.shrinkScreen:
            
            if self.shrinkScreen > 0:
                
                self.screenStep -= 1
        
        if self.screenStep != 0:
            
            #  Prepare surface for redraw.
            displaySurface.fill(g.BLACK, self.blankRectangle)
        
            for count in range(self.screenStep):
                # 217, 103
                displaySurface.blit(self.screenBarScaled, barXY)
                barXY = (barXY[0]-1, barXY[1])
                bracketXY = (bracketXY[0]-1, bracketXY[1])
            
        
            displaySurface.blit(self.screenBracketScaled, bracketXY)
            
            
    
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
    
    #  Draw the bars indicating the points total for each of the crew member's
    #  attributes.
    def drawAttributeBars(self, displaySurface):
        # 179 x,y 20,y 28,y 36,y 62 wide.
        barWidthRatio = ((g.width/320)*62)/100
        
        
        growingBar = h.createBar(self.redBar, int(barWidthRatio*self.crewPointer.skill), int((g.height/200)*3)+1)
        displaySurface.blit(growingBar, (int((g.width/320)*179), int((g.height/200)*20)))
        
        growingBar = h.createBar(self.redBar, int(barWidthRatio*self.crewPointer.performance), int((g.height/200)*3)+1)
        displaySurface.blit(growingBar, (int((g.width/320)*179), int((g.height/200)*28)))
        
        growingBar = h.createBar(self.redBar, int(barWidthRatio*self.crewPointer.sanity), int((g.height/200)*3)+1)
        displaySurface.blit(growingBar, (int((g.width/320)*179), int((g.height/200)*36)))
    
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
            self.extendScreen = False
            
        elif self.evaluate.within(currentPosition):
            
            self.imageShow = False
            self.extendScreen = True
            self.shrinkScreen = False
            
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
    
    #  TODO:  Checks for extending and shrinking image/heartbeat monitor.
    def drawInterface(self, displaySurface):
        
        displaySurface.fill(g.BLACK)
        self.drawAttributeBars(displaySurface)
        displaySurface.blit(self.EGOInterfaceScaled, (0, 0))
        
        if self.imageShow and self.screenStep == 0:
            
            displaySurface.blit(self.crewPointer.resizedImage, ((g.width/320)*210, (g.height/200)*110))
        else:
                        
            self.drawMonitorMovement(displaySurface)
            
            if self.screenStep == self.maxStep:
            
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
            
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            
            self.crewPointer.recalculateStatus()
            self.drawInterface(displaySurface)
            #  Run slow!
            pygame.time.wait(50)
        else:
            self.musicState = False
            self.manipulationStage = 0
            return 10  #  Return to Orbit view.
            #return 2  #  Go to main menu, but should be 10, for orbit.
        
        return self.systemState