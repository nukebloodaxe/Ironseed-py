# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:00:33 2019
Game state machine.
Handles the main render and tick loop.
@author: Nuke Bloodaxe
"""
import cargoDeck
import commandDeck
import crew
import crewcomm as crewC
import crewStatus
import EGOSynthManipulator
import GameGenerator as gen
import global_constants as g
import helper_functions as h
import intro_main
import initializationScreen
import items
import mainMenu
import os
import planetComms
import planets
import PlanetScanner
import pygame
import pygame.sndarray
import saveAndLoad
import ship
import sys
import weaponsAndShields


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

        #  Initialise music system and pygame
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        # Note: Font should resize according to resolution, but logic needed.
        # Note: This should really be externalised into a conf file.
        #  Fonts:  this is a temporary google font, get it from them.
        g.font = pygame.font.Font(os.path.join('Fonts', 'Inconsolata-ExtraBold.ttf'), 14)
        g.offset = 15
        # Note: temporary doubling, for the command deck.
        g.font2 = pygame.font.Font(os.path.join('Fonts', 'Inconsolata-ExtraBold.ttf'), 28)

        # Set Window version and Display surface
        print("Initialize Screen.")
        self.displaySurface = pygame.display.set_mode(g.size)
        pygame.display.set_caption(self.versionText[0]+' '+self.versionText[1])

        # Initialize game objects
        print("Initilizing IronSeed Game Time")
        g.starDate = [2, 3, 3784, 8, 75]  # M,D,Y,H,M.
        g.gameDate = h.IronSeedTime()

        # Prepare initilization screen.
        initializationScreen.loadScreenData()
        # Note:  We can now reset the entire session with another call.
        self.loadAndSetup = initializationScreen.initScreen(self.displaySurface)

        # Populate Item dictionaries
        items.loadItemData(self.loadAndSetup)
        planets.loadScanData(self.loadAndSetup)
        planets.initialisePlanets(self.loadAndSetup)
        planets.loadPlanetarySystems(self.loadAndSetup)
        planets.populatePlanetarySystems(self.loadAndSetup)
        crew.loadCrewData(self.loadAndSetup)

        # Populate graphics precalculation tables.
        planets.precalculatePlanetSphereMapping()

        # Section title.

        self.loadAndSetup.setProcessStep(6)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        #  Initialising Internal Objects.

        weaponsAndShields.loadWeaponsAndShields(self.loadAndSetup)
        self.crew = crew.Crew()
        self.loadAndSetup.setProcessStep(8)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.ship = ship.Ship()
        self.loadAndSetup.setProcessStep(9)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.intro = intro_main.IronseedIntro()
        self.loadAndSetup.setProcessStep(10)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.generator = gen.Generator(self.ship, self.crew, self.loadAndSetup, True)  # Settings at new-game state.
        self.loadAndSetup.setProcessStep(11)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.crewCom = crewC.crewComm(self.crew)  # Needs to have crew data set.
        self.loadAndSetup.setProcessStep(12)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.planetScanner = PlanetScanner.PlanetScanner(self.ship, self.crew)
        self.loadAndSetup.setProcessStep(13)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.cargoDeck = cargoDeck.CargoDeck(self.ship)
        self.loadAndSetup.setProcessStep(14)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.crewStatus = crewStatus.CrewStatus(self.crew)
        self.loadAndSetup.setProcessStep(15)  # Title.
        self.loadAndSetup.update(100)  # Box the title.
        
        self.planetComms = planetComms.PlanetComm(self.ship)
        self.loadAndSetup.setProcessStep(16)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.EGOManipulation = EGOSynthManipulator.EGOManipulator(self.crew)
        self.loadAndSetup.setProcessStep(17)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.commandDeck = commandDeck.CommandDeck(self.ship, self.crew)
        self.loadAndSetup.setProcessStep(18)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        self.mainMenu = mainMenu.MainMenu()
        self.loadAndSetup.setProcessStep(19)  # Title.
        self.loadAndSetup.update(100)  # Box the title.

        # Note:  While in Alpha, the below state list is not exhaustive.

        self.states = {1: self.generator.update,  # The crew + ship selection system.
                       2: self.mainMenu.update,  # Main menu.
                       3: self.intro.update,  # Game Intro - quite useful for testing.
                       4: self.cargoDeck.update,  # Ship cargo system - make mistakes fast.
                       5: self.planetScanner.update,  # Planet surveys and drone ops.
                       6: "Ship Hail",  # Comms between ships, with alien character portrait.
                       7: "Combat",  # Normal and simulated combat.
                       8: self.crewCom.update,  # "talk" with crew members.
                       9: self.EGOManipulation.update,  # Ego-synth manipulation.
                       10: self.commandDeck.update,  # Main game command deck.
                       11: "Load Game",  # Load Game Screen
                       12: "Save Game",  # Save Game Screen (exists?)
                       13: self.crewStatus.update,  # Crew character status screen.
                       14: self.planetComms.update,  # Ship to planet comms.
                       15: "Ship Logs",  # Listing of all log files.
                       16: "Creation",  # really item assembly/disassembly.
                       17: "Sector Map"  # Inter-Sector travel.
                       }

        self.interactive = {1: self.generator.interact,
                            2: self.mainMenu.interact,
                            3: self.intro.interact,
                            4: self.cargoDeck.interact,
                            5: self.planetScanner.interact,
                            6: "Communications",
                            7: "Combat",
                            8: self.crewCom.interact,
                            9: self.EGOManipulation.interact,
                            10: self.commandDeck.interact,
                            11: "Load Game",
                            12: "Save Game",
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

        Initializing = True
        progress = 0  # progress %

        # Enter substate, initialization screen with pretty/retro graphics.
        while Initializing:

            # We'll still handle quit routines here.
            for evt in pygame.event.get():

                if evt.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            #Initializing = self.loadAndSetup.update(progress)
            pygame.display.update()  # update displayed frames.
            break  # skip for now.

        # create and initialise the game engine clock.
        #runningSpeed = pygame.time.Clock()

        # Enter main state and logic loop.
        while 1:

            for evt in pygame.event.get():

                if evt.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                # Handle mouse input.
                elif evt.type == pygame.MOUSEBUTTONDOWN:

                    self.state = self.interactive[self.state](evt.button)

            g.gameDate.update()  # Update game time in "realtime"
            self.state = self.states[self.state](self.displaySurface)
            # self.state(self.displaySurface)
            pygame.display.update()
            #runningSpeed.tick(60)  # Run at 60fps.
