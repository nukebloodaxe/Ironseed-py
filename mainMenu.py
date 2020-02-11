# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:25:11 2020
Ironseed Main Menu.
@author: Nuke Bloodaxe
"""
import pygame, buttons, sys, os
import helper_functions as h
import global_constants as g

class MainMenu(object):
    def __init__(self):
        self.menuStage = 0  #  Current menu state.
        self.rollingStarfield = 0  #  Pixel index for the background starfield.
        self.starField = pygame.image.load(os.path.join('Graphics_Assets', 'cloud.png'))
        self.musicState = False
        
        #  Prepare starfield for blitting.
        self.starFieldScaled = pygame.transform.scale(self.starField, (g.width, g.height))
        
        #  Main Menu Graphics
        self.menuGraphic = pygame.image.load(os.path.join('Graphics_Assets', 'intro5.png'))
        
        #  Prepare menu graphic for blitting
        self.menuGraphicScaled = pygame.transform.scale(self.menuGraphic, (g.width, g.height))
        
        #  Positional buttons for the screen options.
        self.newGame = buttons.Button(35, 237,(71, 367))  # Based on 640x480
        self.intro = buttons.Button(35, 191, (107, 415))
        self.quitGame = buttons.Button(35, 177, (336, 416))
        self.loadGame = buttons.Button(35, 209, (336, 367))
        
    #  Mouse interactions, click on a menu item and make it work.
    def interact(self, mouseButton):
        currentPosition = pygame.mouse.get_pos()
        if self.newGame.within(currentPosition):
            print("New Game")
            self.musicState = False
            return 1
        elif self.intro.within(currentPosition):
            print("Rerun Intro")
            self.musicState = False
            return 3
        elif self.quitGame.within(currentPosition):  #  Quit game viciously.
            print("Exit")
            pygame.quit()
            sys.exit()
        elif self.loadGame.within(currentPosition):
            print("Load Game")
            self.musicState = False
            return 11  #  Should be 11, others are test values.
            #  Note:  Running load game after begin game allows all
            #  necessary data to be setup before testing a different state.
        
        return 3  #  Restart the intro as a failsafe.
    
    #  Update state routine
    def update(self, displaySurface):
        return self.MainMenuLoop(displaySurface)
    
    def MainMenuLoop(self, displaySurface):
        #  Start main intro music
        if self.menuStage == 0:
            pygame.mixer.music.load(os.path.join('sound', 'INTRO2.OGG'))
            pygame.mixer.music.play()
            self.musicState = True
            self.menuStage = 1 #  normally 1, use other stages for debug.
            
        if self.menuStage == 1:
            
            if self.musicState == False:
                pygame.mixer.music.load(os.path.join('sound', 'INTRO2.OGG'))
                pygame.mixer.music.play()
                self.musicState = True
            
            # rewind and start music playing again if track end reached.
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            
            #  Blit starfield.
            
            starFieldBlit = pygame.PixelArray(self.starFieldScaled)
            displaySurfaceBlit = pygame.PixelArray(displaySurface)
            
            #  Advance and wrap the starfield at 15 pixels per frame.
            self.rollingStarfield += 15
            
            if self.rollingStarfield >= g.width:
                self.rollingStarfield = 0
            
            for x in range(0, g.width):
                
                bitmapSafeX = h.safeWrap(g.width, x, self.rollingStarfield)
                safeX = h.safeWrap(g.width, x, 0)
                
                for y in range(0, g.height):
                    
                    displaySurfaceBlit[safeX][y] = starFieldBlit[bitmapSafeX][y]

            starFieldBlit.close()
            displaySurfaceBlit.close()
            
            displaySurface.blit(self.menuGraphicScaled, (0, 0))
            
        return 2