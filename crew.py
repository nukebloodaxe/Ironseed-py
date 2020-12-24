# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:12:22 2019
Crewmember Datastructure
@author: Nuke Bloodaxe
"""
#  TODO: Levelup messaging system, and crew messages in general.

import io, os, pygame, random, global_constants as g

levelData ={0:0,1:1000,2:3000,3:7000,4:11000,5:18000,6:29000,7:47000,8:76000,
            9:123000,10:200000,11:350000,12:500000,13:650000,14:800000,
            15:950000,16:1100000,17:1250000,18:1400000,19:1550000,20:1700000}

CrewData = [] #  All crew members from disk.

#  Insanity Index :)  Remember kids, don't do drugs.
#  ^ was '+chr(n+64)+'
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

#  Base crewmember class, all crew file data ultimately goes here.
class CrewMember(object):
    
    def __init__(self, name="UNNKNOWN", level = 1, sex = "O",
                 position="UNKNOWN", physical=0, mental=0, emotion=0, bio=[""],
                 image=0):
        
        self.name = name
        self.experience = levelData[int(level)]
        self.level = int(level)
        self.sex = sex #  Freeform field; some are robots originally.
        self.position = position
        self.physical = int(physical)
        self.mental = int(mental)
        self.emotion = int(emotion)
        self.pulseColourCycle = 255  #  Used for the status heart-pulse line.
        self.bio = bio[:] # Historically 10 lines at 52 chars
        #  I'm sure we can do better than just this...
        #  Although the concept of an ego synth is a little limiting.
        self.image = image # hacky, but works ;)
        #  Resizing logic should be handled in another function.
        
        if image < 10:
            
            self.image = pygame.image.load(os.path.join('Graphics_Assets', 'image0'+str(image)+'.png'))
            
        else:
            
            self.image = pygame.image.load(os.path.join('Graphics_Assets', 'image'+str(image)+'.png'))
            
        #self.resizedImage = self.image # placeholder
        self.resizedImage = pygame.transform.scale(self.image, ( int((g.width/320)*self.image.get_width()), int((g.height/200)*self.image.get_height())))
        
        #  Internal calculated parameters: careful, these are fully dynamic!
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
                
            self.recalculateStatus()
                
        return levelUp
    
    #  Add experience and check to see if we leveled up.
    def addXP(self, amount):
        
        levelUp = False
        
        if self.experience < 25000000:
        
            self.experience += amount
            levelUp = self.checkLevel()
            
        return levelUp
    
    #  Resize the crew graphic according to the provided parameters.
    def resizeCrewImage(self, x = g.width, y = g.height):
        
        self.resizedImage = pygame.transform.scale(self.image, (x, y))
    
    #  Display the resized crew image at given coordinates.
    #  Note: Never display the internal self.image data, it won't be scaled right.
    def displayCrewImage(self, displaySurface, x, y):
        
        displaySurface.blit(self.resizedImage,(x, y))
        
    #  Draw the sine-wave status line.
    #  I have a feeling the randomness in Python is much higher than that in
    #  the pascal implementation, which is making it difficult to produce a
    #  waveform that is similar to the original.
    #  displayArea is a pygame rectangle object, prescaled.
    #  Colours = 0=red, 1=green, 2=blue
    #  TODO: Add colour changes based on stats.
    def drawStatusLine(self, displaySurface, displayArea, colour=2):
        
        #print(displayArea)
        random.seed(99)  #  Fix the generation, to provide consistency.
        #  Quicken Python namespace lookups
        radiusMultiplier = (displayArea.height/2)/100  #  (based on original 200 pixel height screen)
        lineStart = int(displayArea.x)
        lineFinish = int((displayArea.x+displayArea.width))
        lineTop = int(displayArea.y)
        lineBottom = int(displayArea.y+displayArea.height)
        pulseWidth = int(displayArea.height/2)+lineTop  #  Mid-point of monitor.
        oldXY = (lineStart, lineTop+radiusMultiplier)  # start at 0.
        
        if self.pulseColourCycle == 0:
            
            self.pulseColourCycle = 255
        else:
            self.pulseColourCycle -= 15
        
        #print("Physical ", physical, " Emotional ", emotional, " Mental ", mental)
        
        for x in range(lineStart, lineFinish, int((g.width/320)*4)):  #  2 pixel steps
        
            currentColour = (0,0,0) # placeholder.
            
            if colour == 0:
                
                currentColour = ((x+self.pulseColourCycle)%255, 0, 0) # Red
                
            elif colour == 1:
                
                currentColour = (0, (x+self.pulseColourCycle)%255, 0) # Green
            
            else:
                
                currentColour = (0, 0, (x+self.pulseColourCycle)%255)  # Blue
                
            #  I'm wondering if the colour changes are not agressive enough...
            
            randomNumber = random.choice([0, 1, 2, 3, 4, 5])
            
            randY = 0  #  Our random y position.
            if randomNumber == 0:
                randY = self.physical * radiusMultiplier
                
            if randomNumber == 1:
                randY = self.mental * radiusMultiplier
            
            if randomNumber == 2:
                randY = self.emotion * radiusMultiplier
        
            if randomNumber == 3:
                randY = -1 * (self.physical * radiusMultiplier)
                
            if randomNumber == 4:
                randY = -1 * (self.mental * radiusMultiplier)
                
            if randomNumber == 5:
                randY = -1 * (self.emotion * radiusMultiplier)
            
            randY += pulseWidth
            
            pygame.draw.line(displaySurface, currentColour, oldXY, (x, randY), 1)
            
            oldXY = (x, randY)
            #print (oldXY)
    
        random.seed()  #  Make random random again ;)
        
    #  The temporary insanity system is... odd.
    def tempInsanity(self):
        
        # there is a 1 in 6 change of this happening.
        if int(random.randint(0, 5)) == 0:
            
            return "" # Nothing happens
        
        return insanityIndex[random.randrange(0, 19)]
    
    #  Ego Synths are a bit "unstable", given they are lacking physical forms.
    #  So, sanity checks are bad news all around, as the EGO is decaying.
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
        
        self.recalculateStatus()
        
        if random.randint(1, 80) > self.sanity:
            
            return self.tempInsanity()
        
        
        return "" # Nothing special happens.

    #  Perform a crewmember skill check, which can also be bad...
    #  returns a boolean declaring skill check success or failure.
    #  Failure causes Ego to decay, like a melting snowflake.
    def skillCheck(self):
        
        skillSuccess = random.randint(1, 80)
        skillCheck = False
        sanityReport = ""
        
        #  You need to roll under the skill level, like D&D, to be successful.
        if skillSuccess > self.skill:
            
            skillSuccess = random.randint(1, 80)
            
            #  Now we roll to see how bad things get.
            if skillSuccess > self.performance:
                
                if self.performance > 0: self.performance -= 1
                
                if self.mental > 1:
                    
                    self.mental -= 2
                else:
                    self.mental = 0
                    
                if self.physical > 0: self.physical -= 1
                
                if self.emotion < 99: self.emotion += 1
                
            #  Check to see if we've lost the plot completely.
            if self.performance == 0:
                
                sanityReport = self.sanityCheck()
                #  TODO
                if self.skill > 0: self.skill -= 1
                
                if self.physical > 1:
                    
                    self.physical -= 2
                    
                else:
                    
                    self.physcial = 0
                    
                if self.emotion > 0: self.emotion -= 1
                
                if self.mental < 99: self.mental += 1 #destroying things is cathartic
                
        else:
            
            skillCheck = True
            
        self.recalculateStatus()
            
        return skillCheck, sanityReport
    
    #  Crewmember message, add colour parameter later.
    def crewMessage(self, message):
        
        return self.position + ': ' + message
    
    #  Increase Mental by one point.
    def increaseMental(self):
        
        if self.mental == 99 or self.emotion < 2 or self.physical == 99:
            
                pass
            
        else:
            
            self.mental += 1
            self.physical += 1
            self.emotion -= 2
        
        self.recalculateStatus()
                
    #  Decrease Mental by one point.
    def decreaseMental(self):
        
        if self.mental == 0 or self.emotion > 97 or self.physical == 0:
            
                pass
            
        else:
            
            if self.mental > 0:
                
                self.mental -= 1
            
            if self.physical > 0:
            
                self.physical -= 1
            
            self.emotion += 2
        
        self.recalculateStatus()

    #  Increase Physical by one point.
    def increasePhysical(self):
        
        if self.mental < 2 or self.emotion == 99 or self.physical == 99:
        
            pass
        
        else:
            
            self.mental -= 2
            self.physical += 1
            self.emotion += 1
            
        self.recalculateStatus()
            
    #  Decrease Physical by one point.
    def decreasePhysical(self):
        
        if self.mental > 97 or self.emotion == 0 or self.physical == 0:
        
            pass
        
        else:
            
            self.mental += 2
            
            if self.physical > 0:
            
                self.physical -= 1
            
            if self.emotion > 0:
                
                self.emotion -= 1
        
        self.recalculateStatus()
    
    #  Increase emotion by one point.
    def increaseEmotion(self):
        
        if self.mental == 99 or self.emotion == 99 or self.physical < 2:
            
            pass
        
        else:
            
            self.mental += 1
            self.physical -= 2
            self.emotion += 1
        
        self.recalculateStatus()

    #  Decrease emotion by one point.
    def decreaseEmotion(self):
        
        if self.mental == 0 or self.emotion == 0 or self.physical > 97:
            
            pass
        
        else:
            
            if self.mental > 0:
                
                self.mental -= 1
            
            self.physical += 2
            
            if self.emotion > 0:
                
                self.emotion -= 1
                
        self.recalculateStatus()

    #  Recalculate the EGO's derived snaity/performace/skill values.
    #  This needs to be called every time a change is made to the EGO's
    #  base values.
    def recalculateStatus(self):
        
        self.sanity = self.emotion*0.6 + self.mental*0.4 - self.physical*0.2
        self.performance = self.mental*0.6 + self.physical*0.4 - self.emotion*0.2
        self.skill = self.physical*0.6 + self.emotion*0.4 - self.mental*0.2
    
#  Crew module for main game, our selected crew members live here, along with
#  all crew game-tick related functions.
class Crew(object):
    
    #  IronSeed has 6 roles, as given, this could be upped in Mods.
    def __init__(self):
        
        self.prime = 0 #  Player Role, traditionally Role 0, name "PRIME".
        #  Note: Although IronSeed keeps this anonymous, no reason why we can't
        #  have a player name here.
        #  These are placeholders.
        self.psychometry = 1 #  Role 1 
        self.engineering = 2 #  Role 2
        self.science = 3 #  Role 3
        self.security = 4 #  Role 4
        self.astrogation = 5 #  Role 5
        self.medical = 6 #  Role 6
        #  Placeholder, simpler for numerical random lookups.
        self.crew = []
        self.crewMessages = [] #  new internal feature, Messages from crew
                                #  members that need printing can be queued
                                #  for display later.
                                
    #  Setup the internal objects to the actual crewmember objects we are using.
    def setCrew(self, psychometry, engineering, science, security, astrogation, medical):
        
        self.psychometry = psychometry #  Role 1 
        self.engineering = engineering #  Role 2
        self.science = science #  Role 3
        self.security = security #  Role 4
        self.astrogation = astrogation #  Role 5
        self.medical = medical #  Role 6
        self.crew = [self.psychometry, self.engineering, self.science,
                     self.security, self.astrogation, self.medical]
        
    #  Add a message to the pending messages queue, these are printed onscreen
    #  later.  crewMember is the EGO Synth containment unit number.
    def addMessage(self, message, crewMember):
        
        self.crewMessages.append((message, crewMember))
    
    #  Get a message from the pending messages queue.  Returns an empty string
    #  when no messages are pending.
    def getMessage(self):
        
        if len(self.crewMessages) == 0:
            
            return ("",-1) # No message.
        
        return self.crewMessages.pop()
    
    #  EGO sanity failure.  Returns text output of insane EGO, or blank string
    #  if it's still holding it together.
    def sanityFailure(self, crewMember):
        sanityResult = ""
        
        if (crewMember.mental < 10) or (crewMember.emotion < 10) or (crewMember.physical < 10):
            
            sanityResult = crewMember.tempInsanity()
            
        d8Roll = random.randint(1, 8)
        
        if (d8Roll == 1) and (crewMember.mental > 0):
            
            crewMember.mental -= 1
            
        elif (d8Roll == 2) and (crewMember.physical > 0):
            
            crewMember.physcial -= 1
            
        elif (d8Roll == 4) and (crewMember.emotion > 0):
            
            crewMember.emotion -= 1
            
        crewMember.recalculateStatus()
                
        return sanityResult
    
    #  Perform Sanity Test on crewMember.  This is effectively a D8 roll
    #  with an added difficulty value.
    def sanityTest(self, crewMember, difficulty):
        
        sanityResult = False
        sanity = crewMember.sanity
        diff = difficulty
        
        if crewMember.sanity <= 5:
            
            sanity = 5
            
        if diff <= 0:
            
            diff = 1
            
        if random.randint(1, int(sanity+diff)) < sanity:
            
            sanityResult = True
        
        return sanityResult
    
    #  Stress test crewMember.  Failure increments game stress level.
    #  Note: this almost looks like a primative form of the modern game director.
    def crewStress(self, crewMember, difficulty):
        
        diff = difficulty - crewMember.performance
        
        if not self.sanityTest(crewMember, diff):
            
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
            
        if random.randint(1, int(perf+diff)) < perf:
            
            performanceResult = True
        
        return performanceResult


    def performanceRange(self, crewMember, difficulty):
        
        perf = crewMember.performance
        diff = difficulty
        
        if perf <= 5:
            
            perf = 5
            
        if diff <= 0:
            
            diff = 1
        
        return random.randint(1, int(perf)) - random.randint(1, int(diff))
    
    #  Perform a skill check on a crewmember, return if they succeed or fail.
    def skillTest(self, crewMember, difficulty, learn):
        
        skillResult = False
        skill = crewMember.skill
        diff = difficulty
        
        if skill <= 5:
            
            skill = 5
            
        if diff <= 0:
            
            diff = 1
            
        if random.randint(1, int(skill+diff)) < skill:
            
            skillResult = True
            self.crewStress(crewMember, 0)
            
        else:
            
            self.crewStress(crewMember, abs(diff-skill))
            
        if random.randint(1, 1000) < learn:
            
            if crewMember.addXP(difficulty):
                
                self.addMessage(crewMember.crewMessage('Increased knowledge base.'))
                
        return skillResult
    
    #  Perform a skill check on a crewmember, return resulting effort.
    def skillRange(self, crewMember, difficulty, learn):
        
        skill = int(crewMember.skill)
        diff = difficulty
        
        if skill <= 5:
            
            skill = 5
            
        if diff <= 0:
            
            diff = 1
            
        if random.randint(1, 1000) < learn:
            
            if crewMember.addXP(difficulty):
                
                self.addMessage(crewMember.crewMessage('Increased knowledge base.'))
                
        self.crewStress(crewMember, int((100*diff)/skill))
        return random.randint(1, skill) - random.randint(1, diff)
    
    
    
    #  Crew update tick function.
    def update(self):
        
        #  TODO:  Crew tick, check everything.
        
        pass

#  Navigate the CrewData array.  Allows us to go back and forward, safely, by
#  by a given type of crew member.
#  Forward, False, by default.  Backward, True.
def findCrew(crewType, currentIndex, backward = False):
    
    notFound = True
    
    while notFound:
    
        if backward:
            
            if currentIndex == 0:
                
                currentIndex = len(CrewData) - 1
                
            else:
                
                currentIndex -= 1
            
        else:
            
            if currentIndex == len(CrewData) - 1:
                
                currentIndex = 0
                
            else:
                
                currentIndex += 1
                
        if CrewData[currentIndex].position == crewType:
            
            return currentIndex
    

#  Loads all crew data from the given file location.
#  Note: Crew images are in numerical order for entries in IronPy_crew.tab
def loadCrewData(file=os.path.join('Data_Generators', 'Other', 'IronPy_crew.tab')):
    
    crewFile = io.open(file, "r")
    crewName = ""
    crewDataString = []
    temp = ""
    count = 1 #  Image file names start at 01 (e.g. image01.png)
    
    while temp != "ENDF":
        
        crewName = crewFile.readline().split('\n')[0] #name line
        crewDataString = (crewFile.readline().split('\n')[0]).split('\t') #Data Line line
        temp = crewFile.readline().split('\n')[0]
        crewBioString = [] #  Character Bio
        
        while temp != "END" and temp != "ENDF":
            
            crewBioString.append(temp)
            temp = crewFile.readline().split('\n')[0]
            
        crew = CrewMember(crewName,crewDataString[3],crewDataString[5],
                          crewDataString[4],crewDataString[0],
                          crewDataString[1],crewDataString[2],
                          crewBioString, count)
        
        CrewData.append(crew) #  add to global crew data table.
        count += 1
        #  A crewmember has now been loaded.

    crewFile.close()
