# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:01:01 2019
CrewComm - Communicate with crew members... poorly.
Note: I am very tempted to make this more sophisticated.
Note: * is now used in keywords files to indicate multi-word terms.
@author: Nuke Bloodaxe
"""

import io
import os
import pygame
import random
import crew
import buttons
import global_constants as g
import helper_functions as h

CrewKeywords = {} #crewmember{}->Keyword->{event:reponse code,runtime event,list treatment-single/multiline etc}

CrewReplies = {} #crewmember{}->Key Respose Code->[responses]

#dictionary of key words->check event codes->check response requirement
#->pick response from list 

#Dictionary of replies, index by reponse code.  Contains lists.

class crewComm(object):

    def __init__(self, shipCrew):

        self.crewMembers = shipCrew
        self.selectedCrew = 6  # nobody
        self.crewPointer = "placeholder"  # For Sanity.
        self.state = 8
        self.commStage = 0  #  What Setup/Interaction stage are we at.
        # Prepare background image
        self.charCom = pygame.image.load(os.path.join('Graphics_Assets', 'charcom.png'))
        self.charComScaled = pygame.transform.scale(self.charCom,(g.width,g.height))
        # Prepare Character communication screen for blitting.
        self.charComScaled = pygame.transform.scale(self.charCom, (g.width, g.height))
        self.charComScaled.set_colorkey(g.BLACK)
        self.musicState = False  # Music playback?

        #  define button positions:  Scaling experiment.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        # height, width, (x,y) position
        self.EGOTank1 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*9), int((g.height/200)*30)))
        self.EGOTank2 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*9), int((g.height/200)*60)))
        self.EGOTank3 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*9), int((g.height/200)*90)))
        self.EGOTank4 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*235), int((g.height/200)*30)))
        self.EGOTank5 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*235), int((g.height/200)*60)))
        self.EGOTank6 = buttons.Button(int((g.height/200)*20),
                                       int((g.width/320)*76),
                                       (int((g.width/320)*235), int((g.height/200)*90)))
        
        # The exit button.
        self.Exit = buttons.Button(int((g.height/200)*19),
                                       int((g.width/320)*11),
                                       (int((g.width/320)*308), int((g.height/200)*153)))

    def update(self, displaySurface):

        return self.communicate(displaySurface)

    # Handle mouse events for user interaction.
    def interact(self, mouseButton):

        currentPosition = pygame.mouse.get_pos()

        if self.EGOTank1.within(currentPosition):

            self.selectedCrew = 0
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.EGOTank2.within(currentPosition):

            self.selectedCrew = 1
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.EGOTank3.within(currentPosition):

            self.selectedCrew = 2
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.EGOTank4.within(currentPosition):

            self.selectedCrew = 3
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.EGOTank5.within(currentPosition):

            self.selectedCrew = 4
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.EGOTank6.within(currentPosition):

            self.selectedCrew = 5
            self.crewPointer = self.crewMembers.crew[self.selectedCrew] # For Sanity.

        elif self.Exit.within(currentPosition):

            # click to exit.
            self.selectedCrew = 6
            self.systemState = 10  # Untrap us.

        return self.systemState

    # Compare the keyword against all event entries and check to see which
    # flags have been tripped, return the reply entry matching the highest
    # tripped flag number.
    def checkKeywordEventFlags(self, keyword = ""):

        pass

    # Parse the string of text looking for keywords present in the crewKeywords
    # Dictionary.  Returns a reply based on the best event flag for the text.
    def textInterpret(self, text=""):
    
        tokenisedText = text.split()
        pass

    # Draw the interface for the crew communicator.
    def drawInterface(self, displaySurface):

        displaySurface.fill(g.BLACK)
        displaySurface.blit(self.charComScaled,(0,0))  # Set background.

        if self.selectedCrew < 6:

            # Render crewmember image.
            displaySurface.blit(self.crewPointer.resizedImage,
                                ((g.width/320)*127, (g.height/200)*41))

        else:

            # Render static.
            primeStatic = h.makeFuzz(int((g.width/320)*68), int((g.height/200)*68))
            displaySurface.blit(primeStatic, ((g.width/320)*127, (g.height/200)*41))

    #  Main communication routine loop.
    def communicate(self,displaySurface):
        
        if self.commStage == 0:
            
            # We need to ensure our system state is set.
            self.systemState = 8
            
            # Start comm music
            if self.musicState is False:
                
                pygame.mixer.music.load(os.path.join('sound', 'CREWCOMM.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
                self.commStage += 1
            
            
        elif self.commStage == 1:
            
            self.drawInterface(displaySurface)

#            self.crewPointer = self.crew.crew[self.currentCrewMember]  # For Sanity.

            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():

                pygame.mixer.music.play()

        if self.systemState != 8:

            self.commStage = 0
            self.musicState = False

        return self.systemState #  loop for the moment.


# load all crew comversation related data.
# file location and prefix, Number of files(file number), extension.
# Note: We have some advantages with the reposnse lines, as they are written
# to the crew terminal character by character, we can take advantage of the
# data formatting codes dynamically.
def loadCrewCommunications(file=os.path.join('Data_Generators', 'Other', 'crewcon'), count=6, extension='.tab'):
    
    for index in range(1,count+1):
        
        commFile = io.open(file+str(index)+extension, "r")
        commDataString = []
        keyWords = []
        #  commResponseString = [""]
        CrewKeywords[index] = {}
        CrewReplies[index] = {}
        temp = [""]
        
        while temp[0] != "ENDF":
            
            commDataString = (commFile.readline().split('\n')[0]).split('\t') #Data Line
            #  print(commDataString) # for debug.
            keyWords = commDataString[4].split('*')
            
            for word in keyWords:
                
                try:
                    
                    CrewKeywords[index][word][commDataString[0]] = [commDataString[1],
                                                                    commDataString[2],
                                                                    commDataString[3]]
                except:
                    
                    CrewKeywords[index][word] = {}
                
                CrewKeywords[index][word][commDataString[0]] = [commDataString[1],
                                                                commDataString[2],
                                                                commDataString[3]]
            temp = (commFile.readline().split('\n')[0]).split('\t')
            
            while temp[0] != "EOD" and temp[0] != "ENDF":
                
                try:
                    
                    CrewReplies[index][temp[0]]
                    
                except:
                    
                    CrewReplies[index][temp[0]] = []
                    
                CrewReplies[index][temp[0]].append(temp[1])
                temp = (commFile.readline().split('\n')[0]).split('\t')
            
        #  A crewmember's responses have now been loaded.

        commFile.close()