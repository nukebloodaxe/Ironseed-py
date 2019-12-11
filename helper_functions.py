# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:08:39 2019
Ironseed helper functions
@author: Nuke Bloodaxe
"""
import pygame, random
import global_constants as g

#Safe wrapping at a given step and number
def safeWrap(width,step,current):
    whereAt = current+step
    if whereAt >= width:
        return whereAt%width
    return whereAt

# Render the given text onto a surface.
def renderText(text, font, Surface, colour, offset, width=0, height=0, centred=False):
    position = 0
    for line in text:
        renderedText = font.render(line, True, colour)
        if centred:
            Surface.blit(renderedText,(width-(renderedText.get_width()/2),height+position))
        else:
            Surface.blit(renderedText,(width,height+position))
        position += offset

#Print text at height+width of given surface, fading in.
def fadeInText(text, width, height, colour, surface, step=0, darken=False, centreText=True):
    comboSurface = pygame.Surface(g.size)
    finished = False
    if darken:
        fade = pygame.Surface(g.size)
        fade.fill(g.BLACK)
        fade.set_alpha(20)
        surface.blit(fade,(0,0))
    renderText(text, g.font, comboSurface, colour, 20, width, height, True)
    comboSurface.set_alpha(step*10)
    safeSurface = pygame.PixelArray(surface)
    safeCombo = pygame.PixelArray(comboSurface)
    line = 0
    while line<g.height:
        for pixel in range(g.width):
            if safeCombo[pixel][line] != 0:
                safeSurface[pixel][line]=safeCombo[pixel][line]            
            
        line += 1
            
    #surface.blit(comboSurface,(0,0))
    del safeSurface
    del safeCombo
    if (step*10) >= 255:
        finished = True
    return finished


#fade out a given surface.
def fadeOut(width, height, surface, step):
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(g.BLACK)
    fade.set_alpha(step*5)
    surface.blit(fade,(0,0))
    if step >= 100:
        finished = True
    return finished

#fade out a given surface.
def fadeIn(width, height, surface, step):
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(g.BLACK)
    fade.set_alpha(255-step*5)
    surface.blit(fade,(0,0))
    if step >= 100:
        finished = True
    return finished

#Take a piece of text and converge it on a central location from 4
#different directions, with god-ray effects.
#step indicates which step of the transformation to illustrate.
def convergeText(text, font, offset, colour, width, height, surface, step=0, darken=True):
    ratio = height/width
    ratio2 = width/height
    centre = False
    
    x1 = ((width*ratio)/7)*3.25#width/4
    x2 = ((width*ratio)/7)*6.50#(width/4)*2
    y1 = ((height*ratio2)/7)#height/4
    y2 = ((height*ratio2)/7)*3.5#(height/4)*2
    
    if darken:
        fade = pygame.Surface(g.size)
        fade.fill(g.BLACK)
        fade.set_alpha(10)
        surface.blit(fade,(0,0))
    renderText(text,font,surface,colour,offset,x1+step,y1+step,True)
    renderText(text,font,surface,colour,offset,x2-step,y1+step,True)
    renderText(text,font,surface,colour,offset,x1+step,y2-step,True)
    renderText(text,font,surface,colour,offset,x2-step,y2-step,True)
    if (int(x1+step) - int(x2-step)) <= 1 and (int(x1+step) - int(x2-step)) >=-1:
        centre = True
    return (centre, x1+step, y1+step)

#Create TV Fuzz - Quickly, with stylish half-fill by default
#Based off of David "Futility" Clark's Static filled TV text font.
#Note: More shades required.
def makeFuzz(width, height, half=True):
        
    fuzzyScreen = pygame.Surface((width, height), 0)
    fuzzyScreen.fill(g.BLACK)
    colours = fuzzyScreen.map_rgb(g.BLACK),fuzzyScreen.map_rgb(g.WHITE)
    C = random.choice
    S = fuzzyScreen.set_at
    yrange = range(height)
    for x in range(width):
        for y in yrange:
            if y%2 == 0 or not half:
                S((x,y),C(colours))
    return fuzzyScreen

"""TODO"""
#Render a planet using an approximation of the old IronSeed Algorithm.
#Note: I'm thinking high-quality pre-renders might be a better choice.
def renderPlanet(width, height, planetType, surface, step=0,):
    comboSurface = pygame.Surface(g.size)
    finished = False
    comboSurface.set_alpha(step*10)
    safeSurface = pygame.PixelArray(surface)
    safeCombo = pygame.PixelArray(comboSurface)
    #we create the planet first, then blit the pixels onto the original
    #surface.  Unfortunately, the creation process is not fast.
    
    
    
    # Now to the copy, taking into account the transparency layer.
    line = 0
    while line<g.height:
        for pixel in range(g.width):
            if safeCombo[pixel][line] != 0:
                safeSurface[pixel][line]=safeCombo[pixel][line]            
            
        line += 1
            
    #surface.blit(comboSurface,(0,0))
    del safeSurface
    del safeCombo
    if (step*10) >= 255:
        finished = True
    return finished