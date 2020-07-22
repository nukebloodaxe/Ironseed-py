# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:32:51 2019
Item Datastructures
@author: Nuke Bloodaxe
"""
import io, os, random
import global_constants as g

itemDictionary = {}
itemConstructionDictionary = {}

# Items are divided into the following types:
# Weapons, Shields, Devices, Components, Materials, Elements, Artifacts.
# Artifacts will be implmented later, they are a special case.

# Base object parameters.
#  Note:  The dictionary is working so well I might dispense with this.
class Item(object):
    
    def __init__(self, name, cargoSize, worth, levels, itemType):
        
        self.name = name
        self.cargoSize = cargoSize
        self.worth = worth
        self.levels = levels # These appear to be the level requirements
                             # for each type of crew member. [6 crew, 6 levels.]
        # [psychometry, engineering, science, security, astrogation, medical]
        self.description # Item description.
        self.itemType # The item type.

# This data should be added to a dictionary, by name, on load.
# By tradition, the Iron Seed three items requirement is used.
class createItem(Item):
    
    def __init__(self, name, cargoSize, worth, levels, part1, part2, part3):
        
        self.part1 = part1
        self.part2 = part2
        self.part3 = part3
        Item.__init__(self,name,cargoSize,worth,levels)

# Find a random item of a given "type" category at the limit in items.
# Returns the item's name.
def getRandomItem(itemType, limit):
    
    rando = random.randint(1, limit)
    foundTypeCount = 0
    
    for item in itemDictionary:
        
        if itemDictionary[item][2] == itemType:
            
            foundTypeCount += 1
            
            if foundTypeCount == rando:
                
                return item

# Get the item name of "type" at "count" position, this effectively acts as 
# primative array traversal.
def getItemOfType(itemType, count):
    
    foundTypeCount = 0
    
    for item in itemDictionary:
        
        if itemDictionary[item][2] == itemType:
            
            foundTypeCount += 1
            
            if foundTypeCount == count:
                
                return item
            
# We look for the item and return the position as though the dictionary was an
# array.  We are assuming the item exists.
def findItemInPseudoArray(item):
    
    itemType = itemDictionary[item][2]
    foundTypeCount = 0
    
    for searchItem in itemDictionary:
        
        if itemDictionary[searchItem][2] == itemType:
            
            foundTypeCount += 1
            
            if searchItem == item:
                
                return foundTypeCount - 1
            
# Find the item and return a valid random alternate name for the item.
# If there is no alternate name, return normal item name.
# We assume the item exists in dictionary.
def getAlternateName(item):
    
    name = ""
    #print("Item: ", item)
    try:
        
        alternateNames = itemDictionary[item][6]
        name = random.choice(alternateNames)
        
    except IndexError:
        
        name = itemDictionary[item][0]
        
    except KeyError:
        
        name = "" # Unknown Item.
        
    return name

# Generate all artifacts from the names Given in an array.
# Also generate fixed special artifacts.
def generateArtifacts(names):
    
    for count in range(900): # IronSeed has 900 generated elements.
        
        #print(count)
    
        if count > 500:
            
            name = names[int((((count-501)/10))%19+41)]+' '+names[int(((count-501)%10)+50)]
        
        else:
            
            name = names[int((count/20)+1)]+' '+names[int(count%20+21)]
        
        size = int(count%40)+1
        
        #print(name)
        
        try:
                
            itemDictionary[name] = [name,
                                    size,
                                    "ARTIFACT",
                                    0,[1,1,1,1,1,1]]
        except:
                
            print("Tried Key: ", name)
            # Usually indicates the file we are loading is incorrectly
            # formatted.  If you are modding, double-check your tabs.
            print("Absolutely fatal error on creating Artifacts")  

    #  Append hard-coded artifacts, these are special plot items.
    itemDictionary["Shunt Drive"] = ["Shunt Drive",
                                     0,
                                     "ARTIFACT",
                                     0,[1,1,1,1,1,1]]
    itemDictionary["Channeler"] = ["Channeler",
                                   0,
                                   "ARTIFACT",
                                   0,[1,1,1,1,1,1]]
    itemDictionary["Iron Seed"] = ["Iron Seed",
                                   0,
                                   "ARTIFACT",
                                   0,[1,1,1,1,1,1]]
    itemDictionary["Homing Device"] = ["Homing Device",
                                       0,
                                       "ARTIFACT",
                                       0,[1,1,1,1,1,1]]
    itemDictionary["Detonator"] = ["Detonator",
                                   0,
                                   "ARTIFACT",
                                   0,[1,1,1,1,1,1]]
    itemDictionary["Thermal Plating"] = ["Thermal Plating",
                                         0,
                                         "ARTIFACT",
                                         0,[1,1,1,1,1,1]]
    itemDictionary["Ermigen Data Tapes"] = ["Ermigen Data Tapes",
                                            0,
                                            "ARTIFACT",
                                            0,[1,1,1,1,1,1]]
    itemDictionary["Glyptic Scythe"] = ["Glyptic Scythe",
                                        0,
                                        "ARTIFACT",
                                        0,[1,1,1,1,1,1]]
    itemDictionary["Multi-Imager"] = ["Multi-Imager",
                                      0,
                                      "ARTIFACT",
                                      0,[1,1,1,1,1,1]]
    itemDictionary["Ylinth Mutagenics"] = ["Ylinth Mutagenics",
                                           0,
                                           "ARTIFACT",
                                           0,[1,1,1,1,1,1]]
    itemDictionary["Goolas"] = ["Goolas",
                                0,
                                "ARTIFACT",
                                0,[1,1,1,1,1,1]]


# End of get random item functions.  These exist to make things easier.

# Populate the item and item construction dictionaries.
# we load from two different data files to do this, tab delimited.
# Data Order: Name, cargosize, worth, part1, part2, part3, levels
def loadItemData(file1=os.path.join('Data_Generators', 'Other', 'IronPy_items.tab'),
                 file2=os.path.join('Data_Generators', 'Other', 'IronPy_itemdata.tab'),
                 file3=os.path.join('Data_Generators', 'Other', 'IronPy_iteminfo.tab'),
                 file4=os.path.join('Data_Generators', 'Other', 'IronPy_alternateItemNames.tab'),
                 file5=os.path.join('Data_Generators', 'Other', 'IronPy_anomalyNames.tab')):
    
    itemFile = io.open(file1, "r")
    itemString = itemFile.readline() # title line
    itemString = itemFile.readline() # spacer line
    itemString = itemFile.readline() # real data
    constructFile = io.open(file2, "r")
    constString = constructFile.readline() # title line
    constString = constructFile.readline() # spacer line
    constString = constructFile.readline() # real data
    iteminfoFile = io.open(file3, "r")
    iteminfoString = iteminfoFile.readline() # immediate real data
    alternateNamesFile = io.open(file4, "r")
    alternateNamesString = alternateNamesFile.readline() # immediate real data.
    anomalyNamesFile = io.open(file5, "r")
    anomalyNamesFileString = anomalyNamesFile.readline() # immediate real data.
    S1 = itemString # used plenty, so must be short, is read string from file.
    S2 = constString # Used plenty, so must be short, is read string from file.
    S3 = iteminfoString # Used plenty, so must be short, is read string from file.
    S4 = alternateNamesString # Used plenty, so must be short, is read string from file.
    S5 = anomalyNamesFileString
    
    while S2 != "":
        
        decodedConst = S2.split('\t')
        requiredCrewLevels = [] # remove the \n and make elements ints.
        
        for integer in decodedConst[5:]:
            
            if integer != '\n':
                
                requiredCrewLevels.append(int(integer))
                
        # Item to create, Part 1, Part 2, Part 3, Worth, Required crew levels.
        itemConstructionDictionary[decodedConst[0]] = [decodedConst[0],
                                                       decodedConst[1],
                                                       decodedConst[2],
                                                       decodedConst[3],
                                                       int(decodedConst[4]),
                                                       requiredCrewLevels]
        S2 = constructFile.readline()
        
    while S1 != "":
        
        decodedItem = S1.split('\t')
        dump = decodedItem[2].split('\n') # removing newline
        decodedItem[2] = dump[0]
        # Name, Cargo Size, Item Type, Item Worth, Required Crew Levels.
        
        try:
            
            itemDictionary[decodedItem[0]] = [decodedItem[0],
                                              int(decodedItem[1]),
                                              decodedItem[2],
                                              itemConstructionDictionary[decodedItem[0]][4],
                                              itemConstructionDictionary[decodedItem[0]][5]]
        except KeyError:
            
            # We don't care about missing items.
            # We set these up as singular instances.
            try:
                
                itemDictionary[decodedItem[0]] = [decodedItem[0],
                                                  int(decodedItem[1]),
                                                  decodedItem[2],
                                                  0,[1,1,1,1,1,1]]
            except:
                
                print("Tried Key: ", decodedItem[0])
                # Usually indicates the file we are loading is incorrectly
                # formatted.  If you are modding, double-check your tabs.
                print("Absolutely fatal error on creating items")    
            
        S1 = itemFile.readline()
    
    # Add item descriptions.
    while S3 != "ENDF":
        
        itemName = S3.split('\n')[0]
        S3 = iteminfoFile.readline().split('\n')[0]
        itemDescription = []
        
        while S3 != "EOD" and S3 != "ENDF":
            
            itemDescription.append(S3)
            S3 = iteminfoFile.readline().split('\n')[0]
            
        try:
            
            itemDictionary[itemName].append(itemDescription)
            
        except KeyError:
            
            print("Tried Key: ", itemName)
            # Usually indicates the file we are loading is incorrectly
            # formatted.  If you are modding, double-check your item
            # files, as you may have a spelling mistake in the key names.
            print("Absolutely fatal error on adding item description.")    
        
        # An Item Description has now been loaded.
        S3 = iteminfoFile.readline()
    
    # Add alternate item names.
    while S4 != "ENDF":
        
        itemName, alternateName = "", ""
        alternateNames = []
        
        while S4 != "EOD" and S4 != "ENDF":
            #print(S4)
            itemName, alternateName = S4.split('\n')[0].split('\t', 1)
            #print("Item Name: ", itemName, "Alternate Name: ", alternateName)
            alternateNames.append(alternateName)
            S4 = alternateNamesFile.readline().split('\n')[0]
        
        try:
            
            itemDictionary[itemName].append(alternateNames)
            
        except KeyError:
            
            print("Tried Key: ", itemName)
            # Usually indicates the file we are loading is incorrectly
            # formatted.  If you are modding, double-check your item
            # files, as you may have a spelling mistake in the key names.
            print("Absolutely fatal error on adding item alternate Names.")    
        
        # An Item Description has now been loaded.
        S4 = alternateNamesFile.readline().split('\n')[0]
    
    # Add Artifact names.
    artifactSubNamesArray = []
    
    while S5 != "ENDF":
        
        artifactSubNamesArray.append(S5)
        S5 = anomalyNamesFile.readline().split('\n')[0]
    
    generateArtifacts(artifactSubNamesArray)
    
    itemFile.close()
    constructFile.close()
    iteminfoFile.close()
    alternateNamesFile.close()
    anomalyNamesFile.close()