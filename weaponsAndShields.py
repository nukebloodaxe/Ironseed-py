# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:40:58 2019
All classes and methods related to weapons and shields.
@author: Nuke Bloodaxe
"""

import io, os

weapons = {}
shields = {}

class Weapon(object):
    def __init__(self, name, energyUse, totalDamage, PsychiDamage,
                 particleDamage, inertialDamage, energyDamage, weaponRange):
        #The different types of damage are in percentages.
        self.name = name
        self.energyUse = energyUse
        self.totalDamage = totalDamage
        self.psychiDamage = PsychiDamage
        self.particleDamage = particleDamage
        self.inertialDamage = inertialDamage
        self.energyDamage = energyDamage
        self.weaponRange = weaponRange

class Shield(Weapon):
    def __init__(self, name, energyUse, totalDamage, PsychiDamage,
                 particleDamage, inertialDamage, energyDamage, weaponRange=0):
        Weapon.__init__(self, name, energyUse, totalDamage, PsychiDamage,
                        particleDamage, inertialDamage, energyDamage,
                        weaponRange)
        
def loadWeaponsAndShields(loadAndSetup,
                          file=os.path.join('Data_Generators', 'Other', 'IronPy_WeaponsAndShields.tab')):

    # 100% increments on progress bar.
    progress = 0
    loadAndSetup.setProcessStep(7)

    weaponShieldFile = io.open(file, "r")
    temp = [""]
    # Clear the first 5 lines, as these are formatting info.

    while temp[0] != "BEGINWEAPONS":

        loadAndSetup.update(progress)
        temp[0] = weaponShieldFile.readline().split('\n')[0]

    temp = (weaponShieldFile.readline().split('\n')[0]).split('\t') #Data Line
    progress = 33

    while temp[0] != "BEGINSHIELDS":

        #print(temp)
        loadAndSetup.update(progress)

        try:

           weapons[temp[0]] = Weapon(temp[0],int(temp[1]), int(temp[2]),
                                      int(temp[3]), int(temp[4]),
                                      int(temp[5]), int(temp[6]), int(temp[7]))
        except:

           print("Absolutely fatal Error loading weapon data!")

        temp = (weaponShieldFile.readline().split('\n')[0]).split('\t') #Data Line
        loadAndSetup.update(progress)

    temp = (weaponShieldFile.readline().split('\n')[0]).split('\t') #Data Line
    progress = 66

    while temp[0] != "ENDF":

        loadAndSetup.update(progress)

        try:

            shields[temp[0]] = Shield(temp[0],int(temp[1]), int(temp[2]),
                                      int(temp[3]), int(temp[4]),
                                      int(temp[5]), int(temp[6]), int(temp[7]))

        except:

            print("Absolutely fatal Error loading shield data!")

        temp = (weaponShieldFile.readline().split('\n')[0]).split('\t') #Data Line

    progress = 100
    loadAndSetup.update(progress)

    #All weapon and shield data has now been loaded.
    weaponShieldFile.close()