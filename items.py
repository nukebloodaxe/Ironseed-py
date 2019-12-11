# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:32:51 2019
Item Datastructures
@author: Nuke Bloodaxe
"""
import io

itemDictionary = {}
itemConstructionDictionary = {}

#Base object parameters.
class Item(object):
    def __init__(self, name, cargoSize, worth, levels):
        self.name = name
        self.cargoSize = cargoSize
        self.worth = worth
        self.levels = levels

# This data should be added to a dictionary, by name, on load.
class createItem(Item):
    def __init__(self, name, cargoSize, worth, levels, part1, part2, part3):
        self.part1 = part1
        self.part2 = part2
        self.part3 = part3
        Item.__init__(self,name,cargoSize,worth,levels)

#Populate the item and item creation dictionaries.
#we load from two different data files to do this, tab delimited.
# Data Order: Name, cargosize, worth, part1, part2, part3, levels
def loadItemData(file1,file2):
    itemFile = io.open("Data_Generators\Other\IronPy_items.tab", "r")
    itemString = itemFile.readline() #title line
    itemString = itemFile.readline() #spacer line
    itemString = itemFile.readline() #real data
    constructFile = io.open("Data_Generators\Other\IronPy_itemdata.tab", "r")
    constString = constructFile.readline() #title line
    constString = constructFile.readline() #spacer line
    constString = constructFile.readline() #real data    
    S1 = itemString #used plenty, so must be short, is read string from file.
    S2 = constString #Used plenty, so must be short, is read string from file.
    
    while S2 != "":
        decodedConst = S2.split('\t')
        temp = [] # remove the \n and make elements ints.
        for integer in decodedConst[5:]:
            if integer != '\n':
                temp.append(int(integer))
        itemConstructionDictionary[decodedConst[0]] = [decodedConst[0],
                                                       decodedConst[1],
                                                       decodedConst[2],
                                                       decodedConst[3],
                                                       int(decodedConst[4]),
                                                       temp]
        S2 = constructFile.readline()
        
    while S1 != "":
        decodedItem = S1.split('\t')
        dump = decodedItem[1].split('\n') # removing newline
        decodedItem[1] = int(dump[0])
        try:
            itemDictionary[decodedItem[0]] = [decodedItem[0],
                                              decodedItem[1],
                                              itemConstructionDictionary[decodedItem[0]][4],
                                              itemConstructionDictionary[decodedItem[0]][5]]
        except KeyError:
            #We don't care about missing items.
            #We set these up as singular instances.
            try:
                itemDictionary[decodedItem[0]] = [decodedItem[0],
                                                  decodedItem[1],
                                                  0,[0,0,0,0,0,0]]
            except:
                print("Absolutely fatal error on creating items")    
            
        S1 = itemFile.readline()
        
    itemFile.close()
    constructFile.close()