# -*- coding: utf-8 -*-
"""
Created on Tues Dec 17 22:08:18 2019
Planets: Planet and Planet solar system related code.
These really deserve their own class and file.
@author: Nuke Bloodaxe
"""

#  State:
#  0: Gaseous, A:Nebula, B:Gas Giant, C:Heavy Atmosphere
#  1: Active, A: Volcanic, B: Semi-Volcanic, C: Land Formation
#  2: Stable, A: Land and Water, B: Slight Vegitation, C: Medium Vegitation (Tech 0)
#  3: Early Life, A: Heavy Vegitation (tech 0), B: Medium Vegitation (tech 1), C: Medium Vegitation (Tech 2)
#  4: Advanced Life, A: Medium Vegitation (tech 3), B:Slight Vegitation (tech 3), C: No Vegitation (Tech 5)
#  5: Dying, A:Ruins, B:Medium Vegitation, C:Dead Rock
#  6: Dead, A:Radiation, B:Asteroid, C:Null
#  7: Star, A:Yellow, B:Red, C:White

#  name, State, variation, Life/Technology level
#  Check utils2.pas, it contains most planet related details and old algos.
#  Explore.pas contains much of the graphics settings for colours and texturing.
#  Investigate how to integrate into the planet class.
#  Note:  System name and planet names combined = 1000 units.
#  Although the planet names appear to never have been used, it should be possible to 
#  add them and an extra 250 entries.  The 250 extra entries won't be cannon, but then
#  again I believe they will add more class to the game; quite why channel 7 never
#  used that file is a mystery for now.

import io, pygame, math, random, items
import helper_functions as h, global_constants as g

PlanetarySystems = {} #  Original code indicates these max out at 250.

Planets = {} #  Original code indicates these max out at 1000
ScanData = [] #  Holds the scan data definitions from scandata.tab.
#  ---> Planet state this way, planet grade down.
SystemData = []

class Planet(object):
    def __init__(self):
        self.name = "UNKNOWN"
        self.systemName = "" #  Quicker for reverse lookups.
        self.index = 0 #  Normally our planet number.
        self.state = 0
        self.grade = 0 #  Appears to be "mode" in original code.
        self.size = 1
        self.radius = 0
        self.water = 0
        self.age = 0
        self.bots = [0, 0, 0] #  Mining, Fabricator, Manufactory.
        self.depleted = 0 #  Have bots completed mining/building/fabricating?
        self.notes = 0
        self.seed = 0 #  Seed used for procedural generation.
        self.cache = [] #  Item cache, limit of 7 items.
        # Visitation date related info:
        self.dateMonth = 0
        self.dateYear = 0
        self.visits = 0
        self.orbit = 0 #  set this during system generation.
        self.outpost = 0 #  Extra feature, is this an outpost?
        self.owned = 0 #  Extra feature, the owner of the planet.
        # Planet bitmap of terrain data.
        self.planetTerrain = [[0 for i in range(g.planetWidth)] for j in range(g.planetHeight)]
        
        #  Planet texture related data
        self.planetTexture = pygame.Surface((g.planetWidth, g.planetHeight), 0)
        self.planetTexture.set_colorkey(g.BLACK)
        #  self.createPlanet()
        #  Note: if you see a system with a star called 'Bug', then you have a problem.
        
        # Probot scan related Data points.
        # 1 for each hemesphere.  When value is 2, scan is complete.
        self.lithosphere = 0
        self.hydrosphere = 0
        self.atmosphere = 0
        self.biosphere = 0
        self.anomaly = 0
        
    # New game initialisation, this occurs during the generation phase.
    # Results are ultimately saved to save game file for new game.
    def generate(self, index, sun = False):
        
        self.index = index
        self.seed = random.randint(1,64000)
        random.seed(self.seed)
        self.size = random.randint(1, 5)
        
        if self.size == 0 or self.size == 1:
            self.radius = 900
            
        elif self.size == 2 or self.size == 3:
            self.radius = 1095
            
        else:
            self.radius = 3000
        
        if sun == True:
            self.age = random.randint(0,7)
            if self.age <=3:
                self.grade = 1
            elif self.age >= 4 and self.age <= 5:
                self.grade = 2
            else:
                self.grade = 3
            self.state = 7
            return
        
        self.state = random.randint(0,7)
        self.water = random.randint(0,50)
        
        if self.state == 0:
            self.age = random.randint(0, 5)
            if self.age <=3:
                self.grade = 1
            elif self.age >= 4 and self.age <= 5:
                self.grade = 2
            else:
                self.grade = 3
                
        elif self.state == 1:
            if self.age <=4:
                self.grade = 1
            elif self.age >= 8 and self.age <= 8:
                self.grade = 2
            else:
                self.grade = 3
        elif self.state == 2:
            self.age = random.randint(0, 64000)*7812
            if self.age <=200000000:
                self.grade = 1
            elif self.age <= 350000000 and self.age > 200000000:
                self.grade = 2
            else:
                self.grade = 3
        elif self.state == 3:
            self.age = random.randint(0, 15001)*1000
            if self.age <=150000000:
                self.grade = 1
            elif self.age <= 150005000 and self.age > 150000000:
                self.grade = 2
            else:
                self.grade = 3
        elif self.state == 4:
            self.age = random.randint(0, 5000)
            if self.age <=2000:
                self.grade = 1
            elif self.age <= 3000 and self.age > 2000:
                self.grade = 2
            else:
                self.grade = 3
        elif self.state == 5:
            self.age = random.randint(0, 5000)
            if self.age <=1500:
                self.grade = 1
            elif self.age <= 5500 and self.age > 1500:
                self.grade = 2
            else:
                self.grade = 3
        else: # State 6
            self.age = random.randint(0, 100)*1000
            if self.age >100000:
                self.grade = 1
            else:
                if random.randint(0, 2) == 0:
                    self.grade = 3
                else:
                    self.grade = 1
            
        self.age = random.randint(0, 2000)
    
    # Get the technology level of the planet.
    # Note: I'm not 100% sure how those values work.
    # It is possible that a bit-shift is intended, but that will
    # require more research.
    def getTechLevel(self):
        if self.orbit == 0:
            return 0 # We are a star... although, what about Dyson spheres?
        
        #if self.name == "mars":  #  Twilight zone, this check doesn't work?!?
        #    print("I am Mars")
        #    return 1500
        
        techLevel = -2
        if self.systemName in ["KODUH","OLEZIAS","IYNK","TEVIX","SEKA","WIOTUN"]:
            return 6*256 # Really...
        
        if self.systemName == "EXOPID":
            
            if 27 in g.eventFlags:
                return 0
            else:
                return 6*256
        
        if self.state == 2:
            if self.grade == 2:
                techLevel == -1
            elif self.grade == 3:
                techLevel += self.age / 15000000
        
        elif self.state == 3:
            techLevel = (self.state - 1) * 256
            if self.grade == 1:
                techLevel += self.age / 15000000
            elif self.grade == 2:
                techLevel += self.age / 1000
            elif self.grade == 3:
                techLevel += self.age / 800
        
        elif self.state == 4:
            techLevel = (self.state + 2) * 256
            if self.grade == 1:
                techLevel += self.age / 400
            elif self.grade == 2:
                techLevel += self.age / 200

        elif self.state == 5:
            if self.grade == 1:
                temp = self.age / 100000000
                if temp > 9:
                    temp = 9
                techLevel += temp
            elif self.grade == 2:
                techLevel = -1
        
        elif self.state == 6:
            if self.grade == 2: # Void Dwellers.
                techLevel = 6*256
        
        return techLevel
    
    # This effectively ages the planet based on the time since last visit.
    # If the planet state changes then all notes, bots and cache items are lost.
    def adjustPlanet(self, timePassed):

        if self.bots[0] > 0 or self.bots[1] > 0 or self.bots[2] > 0:
            if self.depleted == 0:
                self.addItems(7) # Historically limit is 7 items.
                self.depleted = 1 # Bots have completed job.
        
        self.age += timePassed
        oldState = self.state
        
        if self.state == 0:
        
            if self.grade == 1 or self.grade == 2:
                if self.age >= 1000000000:
                    age = 0
                    self.grade += 1
            
            elif self.grade == 3:
                if self.age > 500000000:
                    self.age = 0
                    self.grade = 1
                    self.state = 1
            
        elif self.state == 1:
            if self.grade == 1:
                if self.age >= 500000000:
                    self.age = 0
                    self.grade = 2
            
            elif self.grade == 2:
                if self.age >= 400000000:
                    self.age = 0
                    self.grade = 3
                    
            elif self.grade == 3:
                if self.age >= 300000000:
                    self.age = 0
                    self.grade = 1
                    self.state = 2
        
        elif self.state == 2:
            if self.grade == 1:
                if self.age >= 200000000:
                    self.age = 0
                    self.grade = 2
            
            elif self.grade == 2:
                if self.age >= 150000000:
                    self.age = 0
                    self.grade = 3
                    
            elif self.grade == 3:
                if self.age >= 150000000:
                    self.age = 0
                    self.grade = 1
                    self.state = 3
                
                if random.randrange(0,40) == 0:
                    self.age = 0
                    self.state = 5
                    self.grade = 2
        
        elif self.state == 3:
            if self.grade == 1:
                if self.age >= 15000000:
                    self.age = 0
                    self.grade = 2
                if random.randrange(0,40) == 0:
                    self.age = 0
                    self.state = 5
                    self.grade = 2                
            
            elif self.grade == 2:
                if self.age >= 10000:
                    self.age = 0
                    self.grade = 3
                    
            elif self.grade == 3:
                if self.age >= 8000:
                    self.age = 0
                    self.grade = 1
                    self.state = 4
        
        elif self.state == 4:
            if self.grade == 1:
                if self.age >= 4000:
                    self.age = 0
                    self.grade = 2
            
            elif self.grade == 2:
                if self.age >= 2000:
                    self.age = 0
                    self.grade = 3
                if random.randrange(0,40) == 0:
                    self.age = 0
                    self.state = 6
                    if random.randrange(0,2) == 0:
                        self.grade = 1
                    else:
                        self.grade = 2                
                    
            elif self.grade == 3:
                if self.age >= 4000:
                    self.age = 0
                    self.grade = 1
                    self.state = 5
                if random.randrange(0,40) == 0:
                    self.age = 0
                    self.grade = 5
                    self.state = 6
                    if random.randrange(0,2) == 0:
                        self.mode =1
                    else:
                        self.mode = 2                
            
        elif self.state == 5:
            if self.grade == 1:
                if self.age >= 3000:
                    self.age = 0
                    self.grade = 2
            
            elif self.grade == 2:
                if self.age >= 8000:
                    self.age = 0
                    self.grade = 3
                if random.randrange(0,40) == 0:
                    self.age = 0
                    self.state = 2
                    self.grade = 3
            #Ignore Grade 3.
            
        elif self.state == 6:
            if self.state == 1 and age >=100000:
                self.age = 0
                self.grade = 2
            
            
        # Planet changed, catastrophic loss of equipment and info.
        if (oldState != self.state):
            self.cache = []
            self.bots = [0, 0, 0]
            self.notes = 0
    
    # This function computes the quantities of elements required to make the
    # components of a final product (component, material, weapon, shield etc.)
    # If the quantities are sufficient to make the final item, return the
    # amount that can be produced.
    # Note: Evil function.
    def getSubQuantities(self, index, itemType, elements, materials):
        totalTech = 99
        itemName = items.getItemOfType(index, itemType)
        temp = items.itemConstructionDictionary[itemName]
        for something in range(1,4): # each item uses 3 things to make.
        
            if items.itemDictionary[temp[something]][2] == "ELEMENT":
                
                quantity = elements[items.findItemInPseudoArray(temp[0])]
            
            elif items.itemDictionary[temp[something]][2] == "MATERIAL":
            
                quantity = materials[items.findItemInPseudoArray(temp[0])]
            
            # This happens when we receive a final product, like a weapon...
            elif items.itemDictionary[temp[something]][2] == "COMPONENT":
                subIndex = items.findItemInPseudoArray(temp[something[0]])
                quantity = self.getSubQuantities(subIndex, "COMPONENT", 
                                                 elements, materials)
            if quantity < totalTech:
                totalTech = quantity
            
        return totalTech
    
    # Scans are predefined, so return quantities accordingly.
    # This relies on the predefined scan data file being loaded.
    def getItemAmounts(self):
        elements = []
        materials = []
        components = []
        for index in range(g.totalElements):
            elements.append(ScanData[index][self.state])
        
        for index in range(g.totalMaterials):
            totalTech = 99 # We don't want to shower the players with gifts.
            totalYield = 0
            item = items.getItemOftype("MATERIAL", index)
            temp = items.itemConstructionDictionary[item]
            for element in range(1,4): # each material uses 3 elements to make.
                quantity = elements[items.findItemInPseudoArray(temp[element])]
                totalYield += quantity
                if quantity < totalTech:
                    totalTech = quantity
            if totalTech > 0:
                materials.append(totalYield)
            else:
                materials.append(0)
                
        materials[0] = 0
        materials[20] = 0
        
        # We use the sub category function in here to determine if we have
        # enough materials to actually manufacture the component concerned.
        for index in range(g.totalComponents):
            components.append(self.getSubQuantities(index, "COMPONENT",
                                                    elements, materials))
        
        components[0] = 0
        components[21] = 0
        components[22] = 0
        
        return elements, materials, components
    
    # Add items to the planet, including results of surface mining/manufacturing.
    # These are added by name for ease of use in the dictionaries.
    # Note: A planet normally has only one bot type, I'm adding this for
    # the possibility of a "factory" planet.
    # TODO: Function calls need to be corrected to real versions.
    def addItems(self, quantityLimit):
        if not self.depleted:
            elements, materials, components = self.getItemAmounts()
            remaining = quantityLimit
            total = 0
            
            if self.bots[0] > 0:
                
                for element in elements:
                    total += element
                
                for index in range(1,7):
                    
                    if len(self.cache) < 7:
                        self.cache.append(items.getRandomItem("ELEMENT", g.totalElements))
                        remaining -= 1
                    if len(self.cache) == total or remaining <= 0:
                        break
            
            if self.bots[1] > 0:
                
                for material in materials:
                    total += material
                
                for index in range(1,7):
                    
                    if len(self.cache) < 7:
                        self.cache.append(items.getRandomItem("MATERIAL", g.totalMaterials))
                        remaining -= 1
                    if len(self.cache) == total or remaining <= 0:
                        break
                    
            if self.bots[2] > 0:
                
                for component in components:
                    total += component
                
                for index in range(1,7):
                    
                    if len(self.cache) < 7:
                        self.cache.append(items.getRandomItem("COMPONENT", g.totalComponents))
                        remaining -= 1
                    if len(self.cache) == total or remaining <= 0:
                        break
    
    # Create the planet bitmap, which uses the random pixel height-change
    # method to raise and lower terrain.
    # Areas where technology is present are represented as a bright pixel.
    # Note: Colour adjust later.  This function is used to draw the planet
    # to screen as well...
    def createPlanet(self):
        # Prepare texture for per-pixel adjustments.
        planetSurface = pygame.PixelArray(self.planetTexture)
        #print("I am creating a planet: ", self.name)
        currentX, currentY = 0, 0
        random.seed(self.seed)
        step = 0
        technologyLevel = self.getTechLevel()
        #print("Technology Level is: ", technologyLevel)
        for index in range(75000):
            step += 1
            currentX = currentX-1+random.randrange(0,3)
            currentY = currentY-1+random.randrange(0,3)
            if currentX > g.planetWidth-1:
                currentX = 0
            elif currentX < 1:
                currentX = g.planetWidth-1
            
            if currentY > g.planetHeight-1:
                currentY = 0
            elif currentY < 1:
                currentY = g.planetHeight-1
            
            if self.planetTerrain[currentY][currentX] < 240:
                self.planetTerrain[currentY][currentX] += 7
                
        #  Make bright spots representing buildings/tech.
        if technologyLevel > 0:
            #print("Tech Ahoy!: ", technologyLevel)
            technologyLevel = (int(technologyLevel) >> 4) * 10 + (int(technologyLevel) & 0x0F)
            technologyLevel = technologyLevel * technologyLevel / 10
            #print("Adjusted: ", technologyLevel)
            #  The above evilness is the nearest approximation I can get at the
            #  moment for what was happening in pascal.
            for index in range(int(technologyLevel)):
                currentX = random.randrange(0, g.planetWidth - 1)
                currentY = random.randrange(0, g.planetHeight - 1)
                if self.planetTerrain[currentY][currentX] > self.water:
                    self.planetTerrain[currentY][currentX] = 255
                    
        #  TODO: Convert height bitmap to planet graphic in self.planetTexture
        
    #  Create a swirl effect, usually for clouds on a gas giant.
    def createSwirl(self, currentX, currentY, size):
        
        currentPixel = 0
        
        if currentY <= g.height: # Southern Hemesphere.
            if size == 2:
                currentPixel = self.planetTerrain[currentY-1][currentX]
                self.planetTerrain[currentY-1][currentX] = self.planetTerrain[currentY][currentX+1] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+1] = currentPixel - random.randint(1,3)
            
            elif size == 3:
                currentPixel = self.planetTerrain[currentY-1][currentX]
                self.planetTerrain[currentY-1][currentX] = self.planetTerrain[currentY][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+1] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY-1][currentX+1]
                self.planetTerrain[currentY-1][currentX] = self.planetTerrain[currentY][currentX+1] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+1] = currentPixel - random.randint(1,3)
                
            elif size == 4:
                currentPixel = self.planetTerrain[currentY-1][currentX]
                self.planetTerrain[currentY-1][currentX] = self.planetTerrain[currentY][currentX+3] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+3] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY-1][currentX+1]
                self.planetTerrain[currentY-1][currentX+1] = self.planetTerrain[currentY][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+2] = currentPixel - random.randint(1,3)                
                currentPixel = self.planetTerrain[currentY-2][currentX+2]
                self.planetTerrain[currentY-2][currentX+2] = self.planetTerrain[currentY+1][currentX+1] - random.randint(1,3)
                self.planetTerrain[currentY+1][currentX+1] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY-2][currentX+1]
                self.planetTerrain[currentY-2][currentX+1] = self.planetTerrain[currentY+1][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY+1][currentX+2] = currentPixel - random.randint(1,3)
                
        else: # Northern Hemesphere.
            if size == 2:
                currentPixel = self.planetTerrain[currentY-1][currentX+1]
                self.planetTerrain[currentY-1][currentX+1] = self.planetTerrain[currentY][currentX] - random.randint(1,3)
                self.planetTerrain[currentY][currentX] = currentPixel - random.randint(1,3)
                
            elif size == 3:
                currentPixel = self.planetTerrain[currentY][currentX]
                self.planetTerrain[currentY][currentX] = self.planetTerrain[currentY-1][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY-1][currentX+2] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY-1][currentX+1]
                self.planetTerrain[currentY-1][currentX+1] = self.planetTerrain[currentY][currentX+1] - random.randint(1,3)
                self.planetTerrain[currentY][currentX+1] = currentPixel - random.randint(1,3)
                
            elif size == 4:            
                currentPixel = self.planetTerrain[currentY][currentX]
                self.planetTerrain[currentY][currentX] = self.planetTerrain[currentY-1][currentX+3] - random.randint(1,3)
                self.planetTerrain[currentY-1][currentX+3] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY][currentX+1]
                self.planetTerrain[currentY][currentX+1] = self.planetTerrain[currentY-1][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY-1][currentX+2] = currentPixel - random.randint(1,3)                
                currentPixel = self.planetTerrain[currentY-2][currentX+2]
                self.planetTerrain[currentY-2][currentX+2] = self.planetTerrain[currentY+1][currentX+1] - random.randint(1,3)
                self.planetTerrain[currentY+1][currentX+1] = currentPixel - random.randint(1,3)
                currentPixel = self.planetTerrain[currentY-2][currentX+1]
                self.planetTerrain[currentY-2][currentX+1] = self.planetTerrain[currentY+1][currentX+2] - random.randint(1,3)
                self.planetTerrain[currentY+1][currentX+2] = currentPixel - random.randint(1,3)
    
    # Create a Gas Planet bitmap.
    def createGasPlanet(self):
        currentX, currentY = 0
        random.seed(self.seed)
        #step = 0
        colours = [0,0,0]
        # You never know, there might be blimp people...
        #technologyLevel = self.getTechLevel(self.systemName)
        
        # What horrible colours shall we choose?
        if random.randint(0,2) > 0:
            colours[0] = 32
            colours[1] = 48
            colours[2] = 64
        else:
            colours[0] = 112
            colours[1] = 128
            colours[2] = 96
        # Create the atmospheric bands of "gas".  Who knows what the Blimp
        # People have been doing...
        areas = 1
        bandColour = 0
        
        for YPosition in range(int(g.height/2), 0, -1):
            areas -= 1
            if areas == 0:
                areas = (int(g.height/2) - abs(YPosition - int(g.height/2))) / 10
                areas = areas + 6 + random.randint(0, areas + 5)
                if (areas < YPosition) and ((areas + 5) > YPosition):
                    areas = YPosition >> 1 # bit shift by 1 right.
                bandColour = (bandColour + random.randint(0,2) + 1) % 3
                
                if bandColour == 0:
                    bandColour = colours[0] + 8 + random.randint(0,5)
                    
                elif bandColour == 1:
                    bandColour = colours[1] + 8 + random.randint(0,5)
                    
                else:
                    bandColour = colours[2] + 8 + random.randint(0,5)
        
            for XPosition in range(0, int(g.width)):
                
                self.planetTerrain[YPosition][XPosition] = bandColour + random.randint(0,2)
                self.planetTerrain[g.height-YPosition][XPosition] = bandColour + random.randint(0,2)
            
        # Create areas of turbulance between bands, aka the Jupiter look.
        for YPosition in range(3, g.height):
            
            if (self.planetTerrain[YPosition][1] & 0xF0) != (self.planetTerrain[YPosition-1][1] & 0xF0):
                
                XPosition = 1
                while XPosition <= g.width:
                    band = random.randint(0, 4) + 1
                    if band + XPosition > g.height:
                        band = g.height - XPosition
                    self.createSwirl(XPosition,YPosition,band)
                    XPosition += band
                YPosition += 2
                
        # Create Spots: this was pretty dire in the code...
        spotCount = 6 + random.randint(0,5)
        spotSize = 0
        for spot in range(1, spotCount):
            colour = random.randint(0,2)
            if colour == 0:
                colour = colours[0] + 2 + random.randint(0,4)
                
            elif colour == 1:
                colour = colours[1] + 2 + random.randint(0,4)
                
            else:
                colour = colours[2] + 2 + random.randint(0,4)
            
            if spot == 1:
                spotSize = 15 + random.randint(1,5)
            else:
                spotSize = 2 + random.randint(1,6)
            
            spotSize2 = spotSize * spotSize
            spotSize21 = (spotSize - 1) * (spotSize - 1)
            spotSize22 = (spotSize - 2) * (spotSize - 2)
            XPosition = random.randint(0, g.width)
            YPosition = random.randint(0, (g.height-10)-(2*spotSize)) + 5 + spotSize
            
            for X1 in range(spotSize*-1, spotSize):
                XX = X1 + XPosition
                X12 = X1 * X1
                if XX < 1:
                    XX += g.width
                
                elif XX > 240:
                    XX -= g.width
                diametre = round(math.sqrt(spotSize2 - X12))
                for Y1 in range(diametre*-1, diametre):
                    diametre2 = X12 * (Y1*Y1)
                    if diametre2 > spotSize21:
                        self.planetTerrain[Y1+YPosition][XX] += 1 + random.randint(1,2)
                    elif diametre2 > spotSize22:
                        self.planetTerrain[Y1+YPosition][XX] += colour - 1 - random.randint(1,2)
                    else:
                        self.planetTerrain[Y1+YPosition][XX] += colour + random.randint(1,2)
                    
        #TODO: After the horrendous mess we've just gone through, convert the
        # bitmap into a surface with the correct colours.
        
    # Create an Asteroid field bitmap.
    # Note: The original IS code uses an icon for this.
    def createAsteroidField(self):
        
        pass
    
    # Create a Nubula/Cloud Bitmap.
    # NOTE: Does not work yet.
    # TODO: Replace algo with something a bit nicer.
    def createCloud(self):
        currentX, currentY = 0
        random.seed(self.seed)
        steps = random.randint(0, 25) + 50
        size = 0
        colours = [0,0,0]
        # You never know, something might be running in the cloud...
        #technologyLevel = self.getTechLevel(self.systemName)
        for step in range(steps):
            if step == 1:
                size = random.randint(0, 50) + 50
                x = 160
                y = 70
            else:
                size = random.randint(0, 50) + 25
                x = size + 30 + random(260 - size*2)
                y = (size >> 1) + 10 + random.randint(0, 120 - size)
            
            # Note: I believe they were referencing the colour.
            colour = (random.randint(0, 48) + 32) & 0xF0
            for xWidth in range(-size, size):
                background1 = (0x7 * (size - abs(xWidth)) ) / size
                ySize = round(math.cos(xWidth*1.57/size) * (size << 1))
                for yHeight in range(-ySize, ySize):
                    if ySize > 0:
                        background = (background1 * (ySize - abs(yHeight))) * (ySize - abs(yHeight)) / ySize / ySize
                    else:
                        background = 0
                    currentX = x + xWidth
                    currentY = y + yHeight
                    # Note: Interact with background here.
                    # TODO: access background layer.
                    # Using foreground layer for now.
                    if (self.planetTerrain[currentY][currentX] > 143) or (random.randint(0,7) < background):
                        self.planetTerrain[currentY][currentX] = colour | background
                    
                    elif (self.planetTerrain[currentY][currentX] and 0xF) < background:
                        self.planetTerrain[currentY][currentX] = (self.planetTerrain[currentY][currentX] & 0xF0) | background
            
            for xWidth in range(0, 120):
                for yHeight in range(0, 240):
                    self.planetTerrain[yHeight][xWidth] = self.planetTerrain[yHeight+10][xWidth+40]


    #  Wrap a flat surface to a pseudo sphere.
    #  The idea is that we can take a defined area of a planet, a flat surface,
    #  and convert it into a "sphere" which we can rotate every so often.
    #  A rotation is an illusion, and all we are doing is advancing the start and
    #  end pixels by one.
    #  sphereSurface must be square and terrain start must be
    #  within or equil to the width of the planet surface.
    def planetBitmapToSphere(self, sphereSurface, terrainStart = 0, eclipse = True):
        
        eclipseCoverage = 0  #  Area covered by eclipse shadow.
        glowIndex = 4  #  It's glowing brightly.
        day, month, year, second = 0  #  For rotation calculations.
        
        #  Sort out the eclipse shadow settings.
        
        selectEclipsePhase = random.randint(0,3)
        
        if selectEclipsePhase == 0:
            eclipseCoverage = random.randint(0, 25) + 30
        
        elif selectEclipsePhase == 1:
            eclipseCoverage = 80 - random.randint(0, 25)
            
        elif selectEclipsePhase == 2:
            eclipseCoverage = 200 + random.randint(0, 25)
            
        else:
            eclipseCoverage = 250 - random.randint(0, 25)
        
        #  math.radians(degrees)
        #  width of terrain: len(self.planetTerrain[0][0])
        #  Height of surface sphereSurface.get_height()
        tempPlanet = pygame.Surface((g.planetHeight, g.planetHeight), 0)
        tempPlanet.set_colorkey(g.BLACK)
        tempPlanet2 = pygame.PixelArray(tempPlanet)
        #  360 degrees in a circle.
        
        for x in range(0, g.planetHeight):
            bitmapSafeX = h.safeWrap(g.planetWidth,x,terrainStart)
            safeX = h.safeWrap(g.planetHeight,x,0)
            for y in range(0, g.planetHeight):
                if self.water > self.planetTerrain[y][safeX]:
                    #  Water depth support...
                    #  TODO : preliminary support
                    #  Current blue is based on difference between water level and terrain
                    tempPlanet2[y][safeX] = (0, 0, self.water-self.planetTerrain[y][bitmapSafeX])
                
                #  Check for technology, if pixel = technology, then put bright
                #  yellow pixel.  This is based on tech level.
                
                elif self.planetTerrain[y][bitmapSafeX] == 255:
                
                    Technology = self.getTechLevel()
                
                    if Technology <= 1:
                        if Technology > 0:
                            tempPlanet2[y][safeX] = g.TECH1
                            
                    elif Technology <= 2:
                        tempPlanet2[y][safeX] = g.TECH2
                            
                    elif Technology <= 3:
                        tempPlanet2[y][safeX] = g.TECH3
                            
                    elif Technology <= 4:
                        tempPlanet2[y][safeX] = g.TECH4
                            
                    elif Technology <= 5:
                        tempPlanet2[y][safeX] = g.TECH5
                            
                    else:
                        tempPlanet2[y][safeX] = g.YELLOW
                            
                #  TODO : Green pixels based on life present.
                
                #  Check if we can do eclipse in same routine.
                #  TODO : light level due to eclipse.
                else:
                    # TODO:  Add the correct colours.
                    tempPlanet2[y][safeX] = (0,self.planetTerrain[y][bitmapSafeX],0)
        """       
        if tempPlanet.get_height() < 180:
            tempPlanetC = pygame.transform.smoothscale(tempPlanet,(180,180))
            tempPlanet = tempPlanetC
        
        sphereDiameter = tempPlanet.get_height()
        degreesPerPixel = 180/sphereDiameter
        sphereRadius = sphereDiameter/2
        print("Sphere Diameter: ", sphereDiameter)
        print("degreesPerPixel: ", degreesPerPixel)
        print("Sphere Radius: ", sphereRadius)
        print("tempPlanet Width: ", tempPlanet.get_width())
        print("Temp Planet Height: ", tempPlanet.get_height())
        """
        
        #  https://www.xarg.org/2017/07/how-to-map-a-square-to-a-circle/
        #  Thank you Robert, this is exactly what I was looking for!
        #  function map(x, y):
        #    return [ x * math.sqrt(1-y*y/2), y * math.sqrt(1-x*x/2)]
        #  Alternative approach start
        
        tempPlanet3 = pygame.Surface((g.planetHeight, g.planetHeight), 0)
        tempPlanet3.set_colorkey(g.BLACK)
        tempPlanet3.fill(g.BLACK)
        tempPlanet4 = pygame.PixelArray(tempPlanet3)
        
        #print("Total Data Points: ", g.planetHeight*g.planetHeight)
        #count = 0
        exceptions = 0
        for x in range(0, g.planetHeight):
            for y in range(0, g.planetHeight):
                
                try:
                    xLocus, yLocus = h.map(x, y, g.planetHeight, g.planetHeight)
                    tempPlanet4[yLocus][xLocus] = tempPlanet2[y][x]
                    #count += 1
                except:
                    exceptions += 1
        #print("Data Points Succeeded: ", count, " Exceptions: ", exceptions)
        tempPlanet2.close()
        tempPlanet4.close()
        
        #  Test texture surface, have a look at it when it is flat.
        #  Note: scale will be incorrect as target is smaller.  This is okay.
        self.planetTexture = tempPlanet
        #self.planetTexture.blit(tempPlanet,(0,0))
        sphereSurface.blit(tempPlanet3, (0,0))
        return tempPlanet3
        #  That's it!
        # Alternative approach finish.
    
    # Create a Star bitmap.
    def createStar(self):
        
        
        pass
    
    #  Render the planet : Calls other functions for special cases.
    #  This takes the planet texture and wraps it to a sphere,
    #  while also applying special effects such as water levels,
    #  eclipse shadow, clouds etc.
    #  Note: calls sub-functions for rendering.
    #  Note:  Most curious, old code has support for rotation based on the
    #  current time.  This, being cool, will be added.
    #  Note: might dispense with this function, the new create function is so
    #  much better.

    def renderPlanet(self, displaySurface, XPosition, YPosition,
                     step, time, eclipse=True):

        day, month, year, second = 0  #  For rotation calculations.
        c2, r2 = 0.0 #  c^2, r^2
        eclipseCoverage = 0
        glowIndex = 4  #  It's glowing brightly.
        roundPlanetTexture = pygame.PixelArray(self.planetTexture)
        # Prepare our planet texture for per-pixel blit.
        random.seed(self.seed) #  Ensure consistency each time drawn.
        
        #  Warning: Calculus ahead, c2, r2 and the like represent c^2, r^2 etc.
        if self.radius < 901:
            c2 = 1.2
        
        elif self.radius > 2000:
            c2 = 1.09
        
        else: 
            c2 = 1.16
        
        #  Sort out the eclipse shadow settings.
        
        selectEclipsePhase = random.randint(0,3)
        
        if selectEclipsePhase == 0:
            eclipseCoverage = random.randint(0, 25) + 30
        
        elif selectEclipsePhase == 1:
            eclipseCoverage = 80 - random.randint(0, 25)
            
        elif selectEclipsePhase == 2:
            eclipseCoverage = 200 + random.randint(0, 25)
            
        else:
            eclipseCoverage = 250 - random.randint(0, 25)
        
        r2 = math.round(math.sqrt(self.radius))
        offset = g.planetWidth-r2
        maxSphere = 2*r2+4
        sphere = maxSphere/2
        
        
        
    
    # Render a Gas Giant
    def renderGasGiant(self, displaySurface):
        
        pass
    
    # Render a star
    def renderStar(self, displaySurface):
        
        pass
    
    # Render an Asteroid field.
    def renderAsteroids(self, displaySurface):
        
        pass

    def renderCloud(self):
        
        pass

    # Update the planet, this is assuming there has been a change.
    def update(self):
        pass
    
    
        
class PlanetarySystem(object):
    def __init__(self, systemName="Buggy", positionX=0.0, positionY=0.0, positionZ=0.0):
        self.systemName = systemName # Don't forget to assign to planets too.
        #Visitation related info
        self.dateMonth = g.starDate[0]
        self.dateYear = g.starDate[2]
        self.visits = 0
        self.positionX = positionX
        self.positionY = positionY
        self.positionZ = positionZ
        self.notes = 0
        self.starGrade = 0 # quick lookup of the type of star.
        self.numberOfPlanets = 0 # how many planets this system has.
        self.planets = [] # Max 9 including star(at 0).
            
    # Get the tech level for a particular planet.
    def getTechLevel(self, orbit):
        self.planets[orbit].getTechLevel(self.systemName)
    
    # Determine amount of planets this system has.
    def createPlanetCount(self):
        self.numberOfPlanets = 3 + random.randint(1,3)
    
    # Update the system, which is normally based on time passed since last visit.
    # Run once only for each visit!
    def updateSystem(self):
        self.visits += 1 # It is HIGHLY unlikely we'll roll this over...
        self.dateMonth = g.starDate[0]
        self.dateYear = g.starDate[2]
        
    # A trick to show the name as "UNKNOWN" when a system has not been visited.
    def getName(self):
        if self.visits > 0:
            return self.systemName
        return "UNKNOWN"

# Note: Original code had name of planet based on orbit.
# ALPHA, BETA, GAMMA, DELTA, EPISILON, ZETA, ETA, THETA
def initialisePlanets(fileName=""):
    # Load planet files and populate planet structure
    # Planet by name = (planet name, state, variation, tech level/life)
    Planets["mars"] = Planet() # For intro.
    Planets["mars"].generate("mars")
    Planets["mars"].name = "mars"
    Planets["mars"].seed = 37337
    Planets["mars"].state = 4
    Planets["mars"].grade = 3
    Planets["mars"].water = 10
    Planets["mars"].age = 1000000
    Planets["mars"].orbit = 4
    Planets["mars"].createPlanet()
    
    for newPlanet in range(0,1001):
        Planets[newPlanet] = Planet()
        Planets[newPlanet].seed = random.random()
        Planets[newPlanet].generate(newPlanet)
        
    
def transformCheckPlanet(planet):
    name, state, grade, life = Planets[planet]
    # chance of transformation.
    #TODO
    #BIG ALGO HERE
    Planets[planet] = (name,state,grade)
    

# Render a planet using an approximation of the old IronSeed Algorithm.
# Note: I'm thinking high-quality pre-renders might be a better choice.
# landtype= array[1..240,1..120] of byte;
# Enhancement: Generate, save to disk in savegame, and then load in later
# playthroughs.
def renderPlanet(width, height, planetType, surface, step=0):
    comboSurface = pygame.Surface(g.size)
    finished = False
    # comboSurface.set_alpha(step*10)
    safeSurface = pygame.PixelArray(surface)
    safeCombo = pygame.PixelArray(comboSurface)
    # we create the planet first, then blit the pixels onto the original
    # surface.  Unfortunately, the creation process is not fast.
    
    
    
    # Now to the copy, taking into account the transparency layer.
    line = 0
    while line<g.height:
        for pixel in range(g.width):
            if safeCombo[pixel][line] != 0:
                safeSurface[pixel][line]=safeCombo[pixel][line]            
            
        line += 1
            
    # surface.blit(comboSurface,(0,0))
    del safeSurface
    del safeCombo
    if (step*10) >= 255:
        finished = True
    return finished

# Load in system data, which includes co-ordinates.
# Planet quantities and orbits + types are determined via random generation.
# This makes Ironseed somewhat roguelike, making no game the same twice.
# Note: Might be interesting to see if we can implement the travelling salesman
# Algo for working out shortest distance between systems on the starmap.
def loadPlanetarySystems(planetarySystemsFile="Data_Generators\Other\IronPy_SystemData.tab"):
    systemsFile = io.open(planetarySystemsFile, "r")
    systemDataString = (systemsFile.readline().split('\n')[0]).split('\t') #Data Line line
    while systemDataString[0] != "ENDF":
        SystemData.append([systemDataString[0], float(systemDataString[1]),
                           float(systemDataString[2]), float(systemDataString[3])])
        #systemDataString = temp.split('\t')
        # A scan entry line has now been loaded.
        systemDataString = (systemsFile.readline().split('\n')[0]).split('\t') #Data Line line

    # Populate the Planetary Systems Dictionary.
    
    for system in SystemData:
        PlanetarySystems[system[0]] = PlanetarySystem(system[0], system[1],
                                                      system[2], system[3])

    systemsFile.close()

# Here we use a python generator to iterate over the planets dictionary.
# This produces a noticible improvement to both speed and comprehension of
# what the code is doing.
# Note: support function for populatePlanetary systems, run it nowhere else.
def iteratePlanetDictionary():
    count = 0
    while 1:
        count = 0
        for planet in Planets:
            count += 1
            if count > 1000:
                break
            yield Planets[planet], count

# Add in planets to all systems.  Breakout when all planets used up.
# Note: I might dispense with the planet limit later.
# Note: the code claims OBAN is system 145, however a check of the
# system lines shows that OBAN is line 127; I will use "OBAN" as the
# planetary system value.
# Note: run this function only Once!
def populatePlanetarySystems():
    
    lastPlanet = False
    count = 0
    
    for pSystem in PlanetarySystems:
        system = PlanetarySystems[pSystem]
        system.createPlanetCount()
        
        if system.systemName == "OBAN":
            system.numberOfPlanets = 3 # including the star
        
        # Add Sun Here.
        #TODO: Random orbits for the count of planets.
        for orbit in range(0, system.numberOfPlanets):
            
            # planet, count = iteratePlanetDictionary()
            # planet.index = count # Possible: adjust index to dictionary order.
            Planets[count].orbit = orbit
            Planets[count].systemName = system.systemName
            
            if system.systemName == "OBAN":
                
                if orbit == 1:
                    
                    Planets[count].state = 2
                    Planets[count].grade = 3
                    Planets[count].orbit = 2
                    Planets[count].age = 2000
                
                elif orbit == 2:

                    Planets[count].state = 5
                    Planets[count].grade = 3
                    Planets[count].orbit = 4
                    Planets[count].age = 2000
                    
            system.planets.append(Planets[count])
            
            if orbit == 0:
                Planets[count].generate(count, True) # activate sun code.
                system.starGrade = Planets[count].state
            
            count += 1
            
            if count >= 1000:
                lastPlanet = True
                break
            
        if lastPlanet == True:
            break

# Load in scanData, used during planet scans.
def loadScanData(scannerFile="Data_Generators\Other\IronPy_scandata.tab"):
    scanFile = io.open(scannerFile, "r")
    scanDataString = (scanFile.readline().split('\n')[0]).split('\t') #Data Line line
    while scanDataString[0] != "ENDF":
        convertedLine = []
        for value in scanDataString:
            convertedLine.append(int(value))
        ScanData.append(convertedLine[:])
        # A scan entry line has now been loaded.
        scanDataString = (scanFile.readline().split('\n')[0]).split('\t') #Data Line line

    scanFile.close()