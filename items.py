# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:32:51 2019
Item Datastructures
@author: Nuke Bloodaxe
"""
import io, random, global_constants as g

itemDictionary = {}
itemConstructionDictionary = {}

# Items are divided into the following types:
# Weapons, Shields, Devices, Components, Materials, Elements, Artifacts.
# Artifacts will be implmented later, they are a special case.

# Base object parameters.
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
        if item[2] == itemType:
            foundTypeCount += 1
            if foundTypeCount == rando:
                return item[0]

# Get the item name of "type" at "count" position, this effectively acts as 
# primative array traversal.
def getItemOfType(itemType, count):
    foundTypeCount = 0
    for item in itemDictionary:
        if item[2] == itemType:
            foundTypeCount += 1
            if foundTypeCount == count:
                return item[0]
            
# We look for the item and return the position as though the ditionary was an
# array.  We are assuming the item exists.
def findItemInPseudoArray(item):
    itemType = itemDicitonary[item][2]
    foundTypeCount = 0
    for searchItem in itemDictionary:
        if searchItem[2] == itemType:
            foundTypeCount += 1
            if searchItem[0] == item:
                return foundTypeCount


# End of get random item functions.  These exist to make things easier.

# Populate the item and item construction dictionaries.
# we load from two different data files to do this, tab delimited.
# Data Order: Name, cargosize, worth, part1, part2, part3, levels
def loadItemData(file1="Data_Generators\Other\IronPy_items.tab",
                 file2="Data_Generators\Other\IronPy_itemdata.tab",
                 file3="Data_Generators\Other\IronPy_iteminfo.tab"):
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
    S1 = itemString # used plenty, so must be short, is read string from file.
    S2 = constString # Used plenty, so must be short, is read string from file.
    S3 = iteminfoString # Used plenty, so must be short, is read string from file.
    
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
                                                  decodedItem[1],
                                                  decodedItem[2],
                                                  0,[1,1,1,1,1,1]]
            except:
                print("Tried Key:", decodedItem[0])
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
            print("Tried Key:", itemName)
            # Usually indicates the file we are loading is incorrectly
            # formatted.  If you are modding, double-check your item
            # files, as you may have a spelling mistake in the key names.
            print("Absolutely fatal error on adding item description.")    
        
        # An Item Description has now been loaded.
        S3 = iteminfoFile.readline()
    
    itemFile.close()
    constructFile.close()
    iteminfoFile.close()