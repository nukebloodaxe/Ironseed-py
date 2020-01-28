# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:25:11 2020
Ironseed Main Menu.
@author: Nuke Bloodaxe
"""
import pygame
import helper_functions as h
import global_constants as g

class MainMenu(object):
    def __init__(self):
        self.menuStage = 0  #  Current menu state.
        self.rollingStarfield = 0  #  Pixel index for the background starfield.
        self.starField = pygame.image.load("Graphics_Assets\\cloud.png")
        
        #  Prepare starfield for blitting.
        self.starFieldScaled = pygame.transform.scale(self.starField, (g.width, g.height))
        
        #  Main Menu Graphics
        self.menuGraphic = pygame.image.load("Graphics_Assets\\intro5.png")
        
        #  Prepare menu graphic for blitting
        self.menuGraphicScaled = pygame.transform.scale(self.menuGraphic, (g.width, g.height))
        
    #  Mouse interactions, click on a menu item and make it work.
    def interact(self, mouseButton):
        #  TODO
        return 3  #  Restart the intro for now.
    
    #  Update state routine
    def update(self, displaySurface):
        return self.MainMenuLoop(displaySurface)
    
    def MainMenuLoop(self, displaySurface):
        #  Start main intro music
        if self.menuStage == 0:
            pygame.mixer.music.load("sound\\INTRO2.OGG")
            pygame.mixer.music.play()
            self.menuStage = 1 #  normally 1, use other stages for debug.
            
        if self.menuStage == 1:
            #  TODO: blit starfield.
            
            starFieldBlit = pygame.PixelArray(self.starFieldScaled)
            displaySurfaceBlit = pygame.PixelArray(displaySurface)
            
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