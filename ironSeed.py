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
import cargoDeck, crewStatus, planetComms
import GameGenerator as gen
import crewcomm as crewC
import global_constants as g
import helper_functions as h

class IronSeed(object):

    def __init__(self):

        self.state = 3  # Initialise with intro set, normally 3.

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

        # init globals
        g.init(h.IronSeedTime())

        # Populate Item dictionaries
        print("Loading Items: ", end='')
        items.loadItemData()
        print("complete.")
        print("Loading Scan Data: ", end='')
        planets.loadScanData()
        print("complete.")
        print("Initialising Planets: ", end='')
        planets.initialisePlanets()
        print("complete.")
        print("Loading Planetary Systems: ", end='')
        planets.loadPlanetarySystems()
        print("complete.")
        print("Populating Planetary Systems: ", end='')
        planets.populatePlanetarySystems()
        print("complete.")
        print("Loading Crew Data: ", end='')
        crew.loadCrewData()
        print("complete.")
        print("Initialising Internal Objects.")
        print("Weapon and Shield Objects: ", end='')
        weaponsAndShields.loadWeaponsAndShields()
        print("complete.")
        print("Crew Objects: ", end='')
        self.crew = crew.Crew()
        print("complete.")
        print("Ship Objects: ", end='')
        self.ship = ship.Ship()
        print("complete.")
        print("Intro Objects: ", end='')
        self.intro = intro_main.IronseedIntro()
        print("complete.")
        print("Game Generator Objects: ", end='')
        self.generator = gen.Generator(self.ship, self.crew)  # Settings at new-game state.
        print("complete.")
        print("Communications System Objects: ", end='')
        self.crewCom = crewC.crewComm(self.crew)  # Needs to have crew data set.
        print("complete.")
        print("Planet Scanner Objects: ", end='')
        self.planetScanner = PlanetScanner.PlanetScanner(self.ship, self.crew)
        print("complete.")
        print("EGO Synth Manipulation System: ", end='')
        self.EGOManipulation = EGOSynthManipulator.EGOManipulator(self.crew)
        print("complete.")
        print("Cargo Deck Objects: ", end='')
        self.cargoDeck = cargoDeck.CargoDeck(self.ship)
        print("complete.")
        print("Crew Status Objects: ", end='')
        self.crewStatus = crewStatus.CrewStatus(self.crew)
        print("complete.")
        print("Plant Comms Objects: ", end='')
        self.planetComms = planetComms.PlanetComm(self.ship)
        print("complete.")
        print("Command Deck System: ", end='')
        self.commandDeck = commandDeck.CommandDeck(self.ship, self.crew)
        print("complete.")
        print("Creating Main Menu: ", end='')
        self.mainMenu = mainMenu.MainMenu()
        print("complete.")

        # Note:  While in Alpha, the below state list is not exhaustive.

        self.states = {1:self.generator.update,  # The crew + ship selection system.
                       2:self.mainMenu.update,  # Main menu.
                       3:self.intro.update,  # Game Intro - quite useful for testing.
                       4:self.cargoDeck.update,  # Ship cargo system - make mistakes fast.
                       5:self.planetScanner.update,  # Planet surveys and drone ops.
                       6:"Ship Hail",  # Comms between ships, with alien character portrait.
                       7:"Combat",  # Normal and simulated combat.
                       8:self.crewCom.update,  # "talk" with crew members.
                       9:self.EGOManipulation.update,  # Ego-synth manipulation.
                       10:self.commandDeck.update,  # Main game command deck.
                       11: "Load Game", # Load Game Screen
                       12: "Save Game", # Save Game Screen (exists?)
                       13: self.crewStatus.update, # Crew character status screen.
                       14: self.planetComms.update, # Ship to planet comms.
                       15: "Ship Logs", # Listing of all log files.
                       16: "Creation",  # really item assembly/disassembly.
                       17: "Sector Map" # Inter-Sector travel.
                       }

        self.interactive = {1:self.generator.interact,
                            2:self.mainMenu.interact,
                            3:self.intro.interact,
                            4:self.cargoDeck.interact,
                            5:self.planetScanner.interact,
                            6:"Communications",
                            7:"Combat",
                            8:self.crewCom.interact,
                            9:self.EGOManipulation.interact,
                            10:self.commandDeck.interact,
                            11:"Load Game",
                            12:"Save Game",
                            13: self.crewStatus.interact,
                            14: self.planetComms.interact,
                            15: "Ship Logs",
                            16: "Creation",
                            17: "Sector Map"
                            }
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


if __name__ == "__main__":
    game = IronSeed()
    game.main_loop()

