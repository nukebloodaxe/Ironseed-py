# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:12:22 2019
Crewmember Datastructure
@author: Nuke Bloodaxe
"""
import io

levelData ={0:0,1:1000,2:3000,3:7000,4:11000,5:18000,6:29000,7:47000,8:76000,
            9:123000,10:200000,11:350000,12:500000,13:650000,14:800000,
            15:950000,16:1100000,17:1250000,18:1400000,19:1550000,20:1700000}

CrewData = [] #All crew members from disk.


class CrewMember(object):
    def __init__(self, name="UNNKNOWN", experience = 1000, level = 1, sex = "O",
                 position="UNKNOWN", physical=0, mental=0, emotion=0, bio=[""] ):
        self.name = name
        self.experience = experience
        self.level = level
        self.sex = sex
        self.position = position
        self.physical = physical
        self.mental = mental
        self.emotion = emotion
        self.bio = bio[:] # historically 10 lines at 52 chars
        #I'm sure we can do better than just this...
        #Although the concept of an ego synth is a little limiting.
        
    def checkLevel(self):
        if self.level == 20: return False
        levelUp = False
        if levelData[self.level+1] < self.experience:
            self.level += 1
            levelUp = True
        return levelUp
    
    
    
#Loads all crew data from the given file location.
def loadCrewData(file="Data_Generators\Other\IronPy_crew.tab"):
    crewFile = io.open(file, "r")
    crewName = ""
    crewDataString = []
    crewBioString = [] #Character Bio
    temp = ""
    while temp != "ENDF":
        crewName = crewFile.readline().split('\n')[0] #name line
        crewDataString = (crewFile.readline().split('\n')[0]).split('\t') #Data Line line
        temp = crewFile.readline().split('\n')[0]
        while temp != "END" and temp != "ENDF":
            crewBioString.append(temp)
            temp = crewFile.readline().split('\n')[0]
        crew = CrewMember(crewName,1000,crewDataString[3],crewDataString[5],
                          crewDataString[4],crewDataString[0],
                          crewDataString[1],crewDataString[2],
                          crewBioString)
        
        CrewData.append(crew) # add to global crew data table.
        # A crewmember has now been loaded.

    crewFile.close()
