# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:12:22 2019
Crewmember Datastructure
@author: Nuke Bloodaxe
"""
#TODO: Levelup messaging system, and crew messages in general.

import io, pygame, random, global_constants as g

levelData ={0:0,1:1000,2:3000,3:7000,4:11000,5:18000,6:29000,7:47000,8:76000,
            9:123000,10:200000,11:350000,12:500000,13:650000,14:800000,
            15:950000,16:1100000,17:1250000,18:1400000,19:1550000,20:1700000}

CrewData = [] #All crew members from disk.

#Insanity Index :)  Remember kids, don't do drugs.
# ^ was '+chr(n+64)+'
insanityIndex = {0:'Out of memory error on brain ^.',
                 1:'Brain ^ not a supported device.',
                 2:'Read error on brain ^ incompatible media.',
                 3:'CRC checksum error on brain ^.',
                 4:'Brain ^ has been upgraded to patch level 3.',
                 5:'Segmentation error on brain ^. Reboot?',
                 6:'Mentation error, corpse dumped.',
                 7:'Network error on brain ^. Abandom, Retry, Apologize?',
                 8:'Brain ^ is not a system brain.',
                 9:'Runtime error in LIFE.BIN.',
                 10:'Runtime error 226 in LIFE.BIN exceeded 10.',
                 11:'Divide by zero error in brain ^.',
                 12:'Write protection fault on core sector 02AF^.',
                 13:'Runtime error 1 in program CHECKING.BIN.',
                 14:'Underflow error in CHECKING.EXE.',
                 15:'Overflow in TOWELETBOWEL.EXE. Flush stack?',
                 16:'Interrupt vector table restored.',
                 17:'Default settings.',
                 18:'Power fluxuation detected on brain ^.'}

#Base crewmember class, all crew file data ultimately goes here.
class CrewMember(object):
    def __init__(self, name="UNNKNOWN", level = 1, sex = "O",
                 position="UNKNOWN", physical=0, mental=0, emotion=0, bio=[""],
                 image=0):
        self.name = name
        self.experience = levelData[int(level)]
        self.level = int(level)
        self.sex = sex #Freeform field; some are robots originally.
        self.position = position
        self.physical = int(physical)
        self.mental = int(mental)
        self.emotion = int(emotion)
        self.bio = bio[:] # Historically 10 lines at 52 chars
        #I'm sure we can do better than just this...
        #Although the concept of an ego synth is a little limiting.
        self.image = image # hacky, but works ;)
        #Resizing logic should be handled in another function.
        if image < 10:
            self.image = pygame.image.load("Graphics_Assets\\image0"+str(image)+".png")
        else:
            self.image = pygame.image.load("Graphics_Assets\\image"+str(image)+".png")
        self.resizedImage = self.image # placeholder
        
        #Internal calculated parameters: careful, these are fully dynamic!
        self.sanity = self.emotion*0.6 + self.mental*0.4 - self.physical*0.2
        self.performance = self.mental*0.6 + self.physical*0.4 - self.emotion*0.2
        self.skill = self.physical*0.6 + self.emotion*0.4 - self.mental*0.2
        
    def printDebug(self):
        print(self.name)
        print(self.experience)
        print(self.level)
        print(self.sex)
        print(self.position)
        print(self.physical)
        print(self.mental)
        print(self.emotion)
        print(self.bio)
        
    def checkLevel(self):
        if self.level == 20: return False
        levelUp = False
        if levelData[self.level+1] < self.experience:
            self.level += 1
            levelUp = True
            
            if self.mental < 99:
                self.mental += 1
            if self.emotion < 99:
                self.emotion += 1
            if self.physical < 99:
                self.physical += 1
                
        return levelUp
    
    #Add experience and check to see if we leveled up.
    def addXP(self, amount):
        levelUp = False
        if self.experience < 25000000:
        
            self.experience += amount
            levelUp = self.checkLevel()
            
        return levelUp
    
    #Resize the crew graphic according to the provided parameters.
    def resizeCrewImage(self, x = g.width, y = g.height):
        self.resizedImage = pygame.transform.scale(self.image, (x, y))
    
    #Display the resized crew image at given coordinates.
    #Note: Never display the internal self.image data, it won't be scaled right.
    def displayCrewImage(self, displaySurface, x, y):
        displaySurface.blit(self.resizedImage,(x, y))
        
    #The temporary insanity system is... odd.
    def tempInsanity(self):
        # there is a 1 in 6 change of this happening.
        if int(random.random(5)) == 0:
            return "" # Nothing happens
        return insanityIndex[random.random(19)]
    
    #Ego Synths are a bit "unstable", given they are lacking physical forms.
    #So, sanity checks are bad news all around, as the EGO is decaying.
    def sanityCheck(self):
        
        if self.sanity > 0:
            self.sanity -= 1
            
        if self.emotion > 1:
            self.emotion -= 2
        else:
            self.emotion = 0
            
        if self.mental > 0:
            self.mental -= 1
        
        if self.physical < 99:
            self.physical += 1
        
        if random.random(80 > self.sanity):
            return self.tempInsanity()
        
        return "" # Nothing special happens.

    #Perform a crewmember skill check, which can also be bad...
    #returns a boolean declaring skill check success or failure.
    #Failure causes Ego to decay, like a melting snowflake.
    def skillCheck(self):
        skillSuccess = random.random(80)
        skillCheck = False
        sanityReport = ""
        # You need to roll under the skill level, like D&D, to be successful.
        if skillSuccess > self.skill:
            skillSuccess = random.random(80)
            #now we roll to see how bad things get.
            if skillSuccess > self.performance:
                if self.performance > 0: self.performance -= 1
                
                if self.mental > 1:
                    self.mental -= 2
                else:
                    self.mental = 0
                    
                if self.physical > 0: self.physical -= 1
                if self.emotion < 99: self.emotion += 1
            #Check to see if we've lost the plot completely.
            if self.performance == 0:
                sanityReport = self.sanityCheck()
                #TODO
                if self.skill > 0: self.skill -= 1
                if self.physical > 1:
                    self.physical -= 2
                else:
                    self.physcial = 0
                if self.emotion > 0: self.emotion -= 1
                if self.mental < 99: self.mental += 1 #destroying things is cathartic
        else:
            skillCheck = True
        return skillCheck, sanityReport
    
    #Crewmember message, add colour parameter later.
    def crewMessage(self, message):
        return self.position + ': ' + message
    
#Crew module for main game, our selected crew members live here, along with
#all crew game-tick related functions.
class Crew(object):
    #IronSeed has 6 roles, as given, this could be upped in Mods.
    def __init__(self, psychometry, engineering, science, security, astrogation, medical,):
        self.prime = 0 # Player Role, traditionally Role 0, name "PRIME".
        #Note: Although IronSeed keeps this anonymous, no reason why we can't
        #have a player name here.
        self.psychometry = psychometry # Role 1 
        self.engineering = engineering # Role 2
        self.science = science # Role 3
        self.security = security # Role 4
        self.astrogation = astrogation # Role 5
        self.medical = medical # Role 6
        # simpler for numerical random lookups.
        self.crew = [self.psychometry, self.engineering, self.science,
                     self.security, self.astrogation, self.medical]
        self.crewMessages = [] # new internal feature, Messages from crew
                                # members that need printing can be queued
                                # for display later.
    
    # Add a message to the pending messages queue, these are printed onscreen
    # later.
    def addMessage(self, message):
        self.crewMessages.append(message)
    
    #Get a message from the pending messages queue.  Returns an empty string
    #when no messages are pending.
    def getMessage(self):
        if len(self.crewMessages) == 0:
            return ""
        return self.crewMessages.pop()
    
    #EGO sanity failure.  Returns text output of insane EGO, or blank string
    #if it's still holding it together.
    def sanityFailure(self, crewMember):
        sanityResult = ""
        if (crewMember.mental < 10) or (crewMember.emotion < 10) or (crewMember.physical < 10):
            sanityResult = crewMember.tempInsanity()
        d8Roll = random.random(8)
        if (d8Roll == 1) and (crewMember.mental > 0):
            crewMember.mental -= 1
        elif (d8Roll == 2) and (crewMember.physical > 0):
            crewMember.physcial -= 1
        elif (d8Roll == 4) and (crewMember.emotion > 0):
            crewMember.emotion -= 1
                
        return sanityResult
    
    #Perform Sanity Test on crewMember.  This is effectively a D8 roll
    #with an added difficulty value.
    def sanityTest(self, crewMember, difficulty):
        sanityResult = False
        sanity = crewMember.sanity
        diff = difficulty
        if crewMember.sanity <= 5:
            sanity = 5
        if diff <= 0:
            diff = 1
        if random.random(sanity+diff) < sanity:
            sanityResult = True
        
        return sanityResult
    
    #Stress test crewMember.  Failure increments game stress level.
    #Note: this almost looks like a primative form of the modern game director.
    def crewStress(self, crewMember, difficulty):
        diff = difficulty - crewMember.performance
        
        if not self.sanityTest(crewMember,diff):
            if g.gameStatus < 99:
                g.gameStatus += 1
    
    def performanceTest(self, crewMember, difficulty):
        perf = crewMember.performance
        diff = difficulty
        performanceResult = False
        if perf <= 5:
            perf = 5
        if diff <= 0:
            diff = 1
        if random.random(perf+diff) < perf:
            performanceResult = True
        
        return performanceResult


    def performanceRange(self, crewMember, difficulty):
        perf = crewMember.performance
        diff = difficulty
        if perf <= 5:
            perf = 5
        if diff <= 0:
            diff = 1
        
        return random.random(perf) - random.random(diff)
    
    
    def skillTest(self, crewMember, difficulty, learn):
        skillResult = False
        skill = crewMember.skill
        diff = difficulty
        if skill <= 5:
            skill = 5
        if diff <= 0:
            diff = 1
        if random.random(skill+diff) < skill:
            skillResult = True
            self.crewStress(crewMember, 0)
        else:
            self.crewStress(crewMember,abs(diff-skill))
        if random(1000) < learn:
            if crewMember.addXP(difficulty):
                self.addMessage(crewMember.crewMessage('Increased knowledge base.'))
        return skillResult
    
    def skillRange(self, crewMember, difficulty, learn):
        skill = crewMember.skill
        diff = difficulty
        if skill <= 5:
            skill = 5
        if diff <= 0:
            diff = 1
        if random(1000) < learn:
            if crewMember.addXP(difficulty):
                self.addMessage(crewMember.crewMessage('Increased knowledge base.'))
        self.crewStress(crewMember,(100*diff)/skill)
        return random.random(skill)-random.random(diff)
    
    
    
    #Crew update tick function.
    def update(self):
        
        pass

    
#Loads all crew data from the given file location.
#Note: Crew images are in numerical order for entries in IronPy_crew.tab
def loadCrewData(file="Data_Generators\Other\IronPy_crew.tab"):
    crewFile = io.open(file, "r")
    crewName = ""
    crewDataString = []
    temp = ""
    count = 1 # image file names start at 01 (e.g. image01.png)
    while temp != "ENDF":
        crewName = crewFile.readline().split('\n')[0] #name line
        crewDataString = (crewFile.readline().split('\n')[0]).split('\t') #Data Line line
        temp = crewFile.readline().split('\n')[0]
        crewBioString = [] #Character Bio
        while temp != "END" and temp != "ENDF":
            crewBioString.append(temp)
            temp = crewFile.readline().split('\n')[0]
        crew = CrewMember(crewName,crewDataString[3],crewDataString[5],
                          crewDataString[4],crewDataString[0],
                          crewDataString[1],crewDataString[2],
                          crewBioString, count)
        
        CrewData.append(crew) # add to global crew data table.
        count += 1
        # A crewmember has now been loaded.

    crewFile.close()
