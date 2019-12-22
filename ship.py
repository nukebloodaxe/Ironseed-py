# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:26:00 2019
Ship Datastructure
@author: Nuke Bloodaxe
"""

import io, pygame, crew, items, random, global_constants as g
import weaponsAndShields

#The engineering repair teams, historically there are three.
class RepairTeam(object):
    def __init__(self):
        self.job = 0 # system in damage array being worked on.
        self.timeLeft = 0
        self.jobType = 0
        self.extra = 0

# The ship our crew are haunting...
# At this level we use game start values.  On game load all of this is expected
# to be overwritten with the conents of the save file.
class Ship(object):
    def __init__(self):
        self.name = "De Bug"
        self.gunNodes = [0,0,0,0,0,0,0,0,0,0]
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
        self.shieldOptions = [0,0,0]
        self.frontHull = 1
        self.centreHull = 1
        self.rearHull = 1
        self.options = [1,20,1,1,2,1,0,1,64,0] #New Game start values.
        #self.Crew() # debating about storing this here...
        
        #planetary System related variables: initialised to New Game values.
        self.orbiting = 1
        self.positionX = 166
        self.positionY = 226
        self.positionZ = 33
        
        #Engineering related variables
        self.systemDamage = [25,15,2,3,16,55,22]#New game start values.
        #Power Supply, Shield Control, Weapons Control, Engine,
        #Life Support, Communications, Computer AI.
        self.engineeringTeam = [RepairTeam(),RepairTeam(),RepairTeam()]
        
        #Prepare initial engineering job after new game start.
        self.engineeringTeam[0].timeLeft = self.systemDamage[6]*70+random.randrange(1,30)
        self.engineeringTeam[0].job = 6 # Area we are working on.
        self.engineeringTeam[0].jobType = 0 #Repairing
        
        self.research = 0
        
        #populate Cargo with initial items.
        self.cargo["Probot"] = ["Probot", 2]
        self.cargo["Dirk"] = ["Dirk", 1]
        self.cargo["Minebot"] = ["Minebot", 1]
        self.cargo["Manufactory"] = ["Manufactory", 1]
    
    #Apply damage to the ship, mitigating it with the shield first.
    def receiveDamage(totalDamage, PsychiDamage, particleDamage,
                      inertialDamage, energyDamage):
        #First, find out how much damage the shield can absorb.
        shield
        pass
    
    #Apply power drain to battery
    def dischargeBattery():
        
        pass
    
    #Setup the ship stats according to the selected ship type and variation.
    #Note: used during generation at the start of game.
    def initialiseShip(self, front, centre, rear):
        if front == 1:
            self.name = "Heavy "
            self.gunMax = 2
            self.mass = 334
            self.maxFuel = 200
            self.hullMax = 200
            
        elif front == 2:
            self.name = "Light "
            self.gunMax = 1
            self.mass = 334
            self.maxFuel = 250
            self.cargo = self.cargo+50
            self.hullMax = 150            
        else:
            self.name = "Strategic "
            self.gunMax = 3
            self.mass = 501
            self.maxFuel = 200
            self.hullMax = 100
            
        if centre == 1:
            self.name = self.name + "Shuttle "
            self.gunMax = self.gunMax + 3
            self.mass = self.mass + 501
            self.maxFuel = self.maxFuel + 350
            self.cargo = self.cargo+50
            self.hullMax = self.hullMax + 700
        elif centre == 2:
            self.name = self.name + "Assault "
            self.gunMax = self.gunMax + 4
            self.mass = self.mass + 668
            self.maxFuel = self.maxFuel + 300
            self.cargo = self.cargo + 100
            self.hullMax = self.hullMax + 600
        else:
            self.name = self.name + "Storm "
            self.gunMax = self.gunMax + 5
            self.mass = self.mass + 835
            self.maxFuel = self.maxFuel + 300
            self.cargo = self.cargo+50
            self.hullMax = self.hullMax + 600
            
        if rear == 1:
            self.name = self.name + "Transport"
            self.gunMax = self.gunMax + 0
            self.cargo = self.cargo+100
            self.hullMax = self.hullMax + 100            
        elif rear == 2:
            self.name = self.name + "Frigate"
            self.gunMax = self.gunMax + 1
            self.mass = self.mass + 167
            self.cargo = self.cargo+50
            self.hullMax = self.hullMax + 100
        else:
            self.name = self.name + "Cruiser"
            self.gunMax = self.gunMax + 2
            self.mass = self.mass + 330
            self.cargo = self.cargo+50
        
        self.acceleration = 270000/self.mass
            
    
    #Recalculate the ship stats, normally used when checking after mass
    #changes or the application of upgrades.
    def recalculateShipStats(self):
        pass