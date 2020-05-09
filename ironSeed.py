# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:00:33 2019
Game state machine.
Handles the main render and tick loop.
@author: Nuke Bloodaxe
"""
import pygame, sys, pygame.sndarray, intro_main
import ship, crew, items, planets, weaponsAndShields, PlanetScanner
import mainMenu, saveAndLoad, EGOSynthManipulator, commandDeck
import GameGenerator as gen
import crewcomm as crewC
import global_constants as g
import helper_functions as h

class IronSeed(object):
    
    def __init__(self):
        
        self.state = 3  # Initilise with intro set, normally 3.

        self.creditText = ["1994 Channel 7, Destiny: Virtual",
                          "Released Under GPL V3.0 in 2013 by Jeremy D Stanton of IronSeed.net",
                          "2013 y-salnikov - Converted IronSeed to FreePascal and GNU/Linux",
                          "2016 Nuke Bloodaxe - Pascal Code Tidying/Prep",
                          "2020 Nuke Bloodaxe - Complete Python Refactor/Rewrite",
                          "All rights reserved."]
        self.versionText = ["Ironseed", g.version]
        
        # Set Window version and Display surface
        print("Initialise Screen.")
        self.displaySurface = pygame.display.set_mode(g.size)
        pygame.display.set_caption(self.versionText[0]+' '+self.versionText[1])
        
        # Initialise game objects
        print("Initilising IronSeed Game Time")
        g.starDate = [2, 3, 3784, 8, 75] # M,D,Y,H,M.
        g.gameDate = h.IronSeedTime()
        
        # Populate Item dictionaries
        print("Loading Items")
        items.loadItemData()
        print("Loading Scan Data")
        planets.loadScanData()
        print("Initialising Planets")
        planets.initialisePlanets()
        print("Loading Planetary Systems")
        planets.loadPlanetarySystems()
        print("Populating Planetary Systems")
        planets.populatePlanetarySystems()
        print("Loading Crew Data")
        crew.loadCrewData()
        print("Initialising Internal Objects:")
        weaponsAndShields.loadWeaponsAndShields()
        print("Crew Objects")
        self.crew = crew.Crew()
        print("Ship Objects")
        self.ship = ship.Ship()
        print("Intro Objects")
        self.intro = intro_main.IronseedIntro()
        print("Game Generator Objects")
        self.generator = gen.Generator(self.ship, self.crew)  # Settings at new-game state.
        print("Commnications System Objects")
        self.crewCom = crewC.crewComm(self.crew)  # Needs to have crew data set.
        print("Planet Scanner Objects")
        self.planetScanner = PlanetScanner.PlanetScanner(self.ship, self.crew)
        print("EGO Synth Manipulation System")
        self.EGOManipulation = EGOSynthManipulator.EGOManipulator(self.crew)
        print("Command Deck System")
        self.commandDeck = commandDeck.CommandDeck(self.ship, self.crew)
        print("Creating Main Menu")
        self.mainMenu = mainMenu.MainMenu()
        
        self.states = {1:self.generator.update,  # The crew + ship selection system.
                       2:self.mainMenu.update,  # Main menu.
                       3:self.intro.update,  # Game Intro - quite useful for testing.
                       4:"cargo",  # Ship cargo system, includes item assembly.
                       5:self.planetScanner.update,  # Planet surveys and drone ops.
                       6:"Communications",  # Comms between ships/planets
                       7:"Combat",  # Normal and simulated combat.
                       8:self.crewCom.update,  # "talk" with crew members.
                       9:self.EGOManipulation.update,  # Ego-synth manipulation.
                       10:self.commandDeck.update,  # Main game command deck.
                       11: "Load Game",
                       12: "Save Game" }
        
        self.interactive = {1:self.generator.interact,
                            2:self.mainMenu.interact,
                            3:self.intro.interact,
                            4:"cargo",
                            5:self.planetScanner.interact,
                            6:"Communications",
                            7:"Combat",
                            8:self.crewCom.interact,
                            9:self.EGOManipulation.interact,
                            10:self.commandDeck.interact,
                            11:"Load Game",
                            12:"Save Game"}
        print("We Are GO!")


    def main_loop(self):

        # Display copyright credits on start.
        self.displaySurface.fill(g.BLACK)
        h.renderText(self.creditText, g.font, self.displaySurface, g.WHITE, g.offset)
        pygame.display.update()

        # wait some seconds, approx 4.
        pygame.time.wait(4000)

        # enter main state and logic loop.
        while 1:
            
            for evt in pygame.event.get():
                
                if evt.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()
                    
                # Handle mouse input.
                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.state = self.interactive[self.state](evt.button)
                    
            g.gameDate.update()  #  Update game time in "realtime"
            self.state = self.states[self.state](self.displaySurface)
            # self.state(self.displaySurface)
            pygame.display.update()
