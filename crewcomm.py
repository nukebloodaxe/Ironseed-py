# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:01:01 2019
CrewComm - Communicate with crew members... poorly.
Note: I am very tempted to make this more sophisticated.
Note: * is now used in keywords files to indicate multi-word terms.
@author: Nuke Bloodaxe
"""

import io, pygame, random, global_constants as g, crew

CrewKeywords = {} #crewmember{}->Keyword->{event:reponse code,runtime event,list treatment-single/multiline etc}

CrewReplies = {} #crewmember{}->Key Respose Code->[responses]

#dictionary of key words->check event codes->check response requirement
#->pick response from list 

#Dictionary of replies, index by reponse code.  Contains lists.

class crewComm(object):
    def __init__(self,crew):
        self.crew = crew
        self.selectedCrew = 0 #nobody
        
        
    def update(self, displaySurface):
        return self.communicate(displaySurface)
    
    def communicate(self,displaySurface):
        
        return 6 # TODO, currently loops communication system for testing.
    
#load all crew comversation related data.
#file location and prefix, Number of files(file number), extension.
#Note: We have some advantages with the reposnse lines, as they are written
#to the crew terminal character by character, we can take advantage of the
#data formatting codes dynamically.
def loadCrewCommunications(file="Data_Generators\Other\crewcon",count=6,extension=".tab"):
    
    for index in range(1,count+1):
        commFile = io.open(file+str(index)+extension, "r")
        commDataString = []
        keyWords = []
        commResponseString = []
        CrewKeywords[index] = {}
        CrewReplies[index] = {}
        temp = [""]
        while temp[0] != "ENDF":
            commDataString = (commFile.readline().split('\n')[0]).split('\t') #Data Line
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
            
        # A crewmember's responses have now been loaded.

        commFile.close()