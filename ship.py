# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:26:00 2019
Ship Datastructure
@author: Nuke Bloodaxe
"""

import io, pygame, crew, items, random, global_constants as g
import weaponsAndShields

#  The engineering repair teams, historically there are three.
class RepairTeam(object):
    def __init__(self):
        self.job = 0 # system in damage array being worked on.
        self.timeLeft = 0
        self.jobType = 0
        self.extra = 0

#  The ship our crew are haunting...
#  At this level we use game start values.  On game load all of this is expected
#  to be overwritten with the conents of the save file.
class Ship(object):
    
    def __init__(self):
        
        self.name = "De Bug"
        self.gunNodes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.gunMax = 0
        self.armed = False
        self.cargo = {}
        self.cargoMax = 0
        self.maxFuel = 0
        self.fuel = 0
        self.battery = 0
        self.mass = 0
        self.acceleration = 0
        self.accelerationMax = 0
        self.hullDamage = 0
        self.hullMax = 0
        self.fittedShield = ""
        self.shieldLevel = 0
        self.shieldMax = 15
        self.shieldOptions = [0, 0 ,0]
        self.frontHull = 1
        self.centerHull = 1
        self.rearHull = 1
        self.options = [1, 20, 1, 1, 2, 1, 0, 1, 64, 0] #New Game start values.
        #self.Crew() # debating about storing this here...
        
        #  Planetary System related variables: initialised to New Game values.
        self.orbiting = 2  #  Icarus.
        self.positionX = 16.6
        self.positionY = 22.6
        self.positionZ = 3.3
        
        #  Engineering related variables
        self.systemDamage = [25, 15, 2, 3, 16, 55, 22]#New game start values.
        #  Power Supply, Shield Control, Weapons Control, Engine,
        #  Life Support, Communications, Computer AI.
        self.engineeringTaskDescription = ["Idle", "Power Supply",
                                           "Shield Control",  "Weapons Control",
                                           "Engine", "Life Support",
                                           "Communications", "Computer AI",
                                           "Hull Damage", "Shield", "Weapon",
                                           "Device", "Component", "Material",
                                           "Artifact", "Other"]
        self.repairType = ["Power Supply", "Shield Control", "Weapons Control",
                           "Engine", "Life Support", "Communications",
                           "Computer AI", "Hull Damage"]
        self.engineeringTeam = [RepairTeam(),RepairTeam(),RepairTeam()]
        
        #  Prepare initial engineering job after new game start.
        self.engineeringTeam[0].timeLeft = self.systemDamage[6]*70+random.randrange(1,30)
        self.engineeringTeam[0].job = 6 # Area we are working on.
        self.engineeringTeam[0].jobType = 0 #Repairing
        
        self.research = 0
        
        #  Populate Cargo with initial items.
        self.cargo["Probot"] = ["Probot", 2]
        self.cargo["Dirk"] = ["Dirk", 1]
        self.cargo["Minebot"] = ["Minebot", 1]
        self.cargo["Manufactory"] = ["Manufactory", 1]
        
        #  Ship messages that need printing, not role specific.
        self.shipMessages = []
    
    #  Get our current position as x,y,z values.
    def getPosition(self):
        
        return self.positionX, self.positionY, self.positionZ
    
    #  Get our orbit.
    def getOrbit(self):
        
        return self.orbiting
    
    #  Add a message to the pending messages queue, these are printed onscreen
    #  later.  CrewMember is the EGO Synth containment unit number.
    def addMessage(self, message, crewMember):
        
        self.shipMessages.append((message, crewMember))
        
    
    #  Get a message from the pending messages queue.  Returns an empty string
    #  when no messages are pending.
    def getMessage(self):
        
        if len(self.shipMessages) == 0:
            
            return ("",-1) # No message.
        
        return self.shipMessages.pop()
    
    #  Add an item to cargo, different to original.
    #  I've dispensed with the item limit, and am looking at the possibility
    #  of having items left behind if the hold fills.  This eliminates the
    #  random loss of a cargo type if we overfill the hold.
    #  Returns cargo added success as boolean, alongside the remainder.
    def addCargo(self, itemName, quantity):
        
        cargoAdded = False
        itemWeight = items.itemDictionary[itemName].cargoSize
        totalWeight = itemWeight * quantity
        usedCargo = self.totalCargoSize()
        quantityLeft = quantity
        
        #  TODO: Force Artifacts to add regardless of size.
        if usedCargo + totalWeight > self.cargoMax:
            
            while usedCargo + itemWeight <= self.cargoMax:
                
                #  Try to add as many possible into cargo hold.
                try:
                    
                    self.cargo[itemName][1] += 1
                    
                except:
                    
                    self.cargo[itemName] = [itemName, 1]
                    
                usedCargo = self.totalCargoSize()
                quantityLeft -= 1
                cargoAdded = True
                
        else:
            
            try:
                
                self.cargo[itemName][1] += quantity
                
            except:
                
                self.cargo[itemName] = [itemName, quantity]
                
            cargoAdded = True
            quantityLeft = 0
        
        if quantityLeft > 0:
            
            quantity = quantityLeft # Experiment.
            
            if cargoAdded == False:
                
                self.addMessage("Cargo Full!", 2)
                self.addMessage(str(usedCargo)+'/'+str(self.cargoMax)+' used.', 2)
            
            else:
                
                self.addMessage("Cargo Filled During Transfer!", 2)
                self.addMessage(str(usedCargo)+'/'+str(self.cargoMax)+' used.', 2)
                self.addMessage(str(quantity)+" units were left behind!", 2)
                
        return cargoAdded, quantityLeft
                
    #  Remove a quantity of cargo, returning True and the quantity remaining on
    #  success, else False and quantity removed.
    def removeCargo(self, itemName, quantity ):
        
        cargoRemoved = False
        quantityLeft = quantity
        items = 0
        
        try:
            
            items = self.cargo[itemName][1]
            
        except:
            
            self.cargo[itemName] = [itemName, 0]
            items = 0
        
        if items >= quantity:
            
            quantityLeft = items - quantity
            cargoRemoved = True
            
        elif items == 0:
            
            self.addMessage("No " + itemName + " found in cargo!", 2)
            quantityLeft = 0
            
        else:
            
            quantityLeft -= self.cargo[itemName][1]
            self.cargo[itemName][1] = 0
        
        return cargoRemoved, quantityLeft
    
    #  Get Item Count for a given item possibly in cargo.
    def getItemQuantity(self, itemName):
        
        try:
            
            return self.cargo[itemName][1]
        
        except:
            
            self.addMessage("No " + itemName + " found in cargo!", 2)
            return 0
        
    #  Find total cubic meters of all cargo in hold.
    def totalCargoSize(self):
        
        totalSize = 0
        
        for item in self.cargo:
            
            if item[1] >= 1:
                
                count = item[1]
                
                while count > 0:
                    
                    totalSize += items.itemDictionary[item[0]].cargoSize
                    count -= 1
                    
        return totalSize  #  This function does not judge...
    
    #  Check to see if we are overweight.  Background switch determines
    #  if this is in the lower left corner log window, or somewhere else.
    def checkOverweight(self, background = False):
        
        overweight = False
        #  Role 2 for messages.
        weight = self.totalCargoSize()
        #  Print a big dialogue message if it happens in the background.
        #  As to how that would happen... Tribbles?
        
        if weight > self.cargoMax:
            
            #  Big dialogue box!
            if background:
                
                #  TODO: Big Box functionality.
                pass
            
            else:
                
                self.addMessage("Cargo Full!", 2)
                self.addMessage(str(weight)+'/'+str(self.cargoMax)+' used.', 2)
                self.addMessage('Must Jettison cargo.', 2)
                
            overweight = True
            
        return overweight #  This function does judge...
    
    #  Check to see if adding an item is possible.
    def willThisFit(self, item):
        
        estimate = self.totalCargoSize() + items.itemDictionary[item].cargoSize
        possible = True
        
        if estimate > self.cargoMax:
            
            possible = False
            
        return possible
            
        
    #  Apply damage to the ship, mitigating it with the shield first.
    #  if Life Support fails, you die there and then.
    def receiveDamage(self, totalDamage, PsychiDamage, particleDamage,
                      inertialDamage, energyDamage):
        #  TODO: Everything.
        #  First, find out how much damage the shield can absorb.
        pass
        
    
    #  Apply power drain to battery
    #  Note: Apply weapons first, then the shield.
    #  Enhancement Possible: Power allocation % could be added.
    def dischargeBattery(self):
        
        pass
    
    #  Setup the ship stats according to the selected ship type and variation.
    #  Note: used during generation at the start of game.
    def initialiseShip(self):
        
        self.cargoMax = 0
        self.name = ""
        self.gunMax = 0
        self.mass = 0
        self.maxFuel = 0
        self.hullMax = 0
        
        if self.frontHull == 1:
            
            self.name = "Heavy "
            self.gunMax = 2
            self.mass = 334
            self.maxFuel = 200
            self.hullMax = 200
            
        elif self.frontHull == 2:
            
            self.name = "Light "
            self.gunMax = 1
            self.mass = 334
            self.maxFuel = 250
            self.cargoMax = 50
            self.hullMax = 150
            
        else:
            
            self.name = "Strategic "
            self.gunMax = 3
            self.mass = 501
            self.maxFuel = 200
            self.hullMax = 100
            self.cargoMax = 0
            
        if self.centerHull == 1:
            
            self.name += "Shuttle "
            self.gunMax += 3
            self.mass += 501
            self.maxFuel += 350
            self.cargoMax += 50
            self.hullMax += 700
            
        elif self.centerHull == 2:
            
            self.name += "Assault "
            self.gunMax += 4
            self.mass += 668
            self.maxFuel += 300
            self.cargoMax += 100
            self.hullMax += 600
            
        else:
            
            self.name += "Storm "
            self.gunMax += 5
            self.mass += 835
            self.maxFuel += 300
            self.cargoMax += 50
            self.hullMax += 600
            
        if self.rearHull == 1:
            
            self.name += "Transport"
            self.gunMax += 0  #  ?
            self.cargoMax += 100
            self.hullMax += 100
            
        elif self.rearHull == 2:
            
            self.name += "Frigate"
            self.gunMax += 1
            self.mass += 167
            self.cargoMax += 50
            self.hullMax += 100
            
        else:
            
            self.name += "Cruiser"
            self.gunMax += 2
            self.mass += 330
            self.cargoMax += 50
        
        self.acceleration = 270000/self.mass
        
    
    #  Recalculate the ship stats, normally used when checking after mass
    #  changes or the application of upgrades.
    def recalculateShipStats(self):
        
        pass