# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:08:39 2019
Ironseed helper functions
@author: Nuke Bloodaxe
"""
import pygame, random, time, math
import global_constants as g

#  Map a point on a square 2D array to a point on a 2D sphere.
#  Note:  No exception correction for math.sqrt(0)
#  BIG NOTE:  Complexity comes from ridiculous math.sqrt not handling negative
#             numbers...
def map(x, y, xWidth, yHeight):
    #  x * math.sqrt(1 - y * y / 2), y * math.sqrt(1 - x * x / 2)
    #  Determine in which quadrant circle unit value will appear.
    #  And convert x and y to temporary unit circle values
    radius = xWidth / 2
    unitCircleMultiplier = 1/radius
    xConverted = 0
    yConverted = 0
    quadrant = 1
    # top right = 3, bottom right = 2, bottom left = 1, top left = 4.
    
    if x <= radius:
        if y <= radius:
            quadrant = 4 # top left
            xConverted = -1 * (radius-x) * unitCircleMultiplier#x * unitCircleMultiplier
            yConverted = -1 * (radius-y) * unitCircleMultiplier#y * unitCircleMultiplier
        else:
            quadrant = 3 # Top right - contains top right data.
            xConverted = -1 * (radius-x) * unitCircleMultiplier
            yConverted = (radius - y) * unitCircleMultiplier
    else:
        if y <= radius:
            quadrant = 1 # bottom left?
            xConverted = (radius - x) * unitCircleMultiplier
            yConverted = -1 * (radius - y) * unitCircleMultiplier
        else:
            quadrant = 2  #  Appears to be bottom right data
            xConverted = -1*(radius - x) * unitCircleMultiplier
            yConverted = -1*(radius - y) * unitCircleMultiplier
            
    #print("X Converted: ", str(xConverted), "Y Converted: ", str(yConverted))
    # By doing this temporary conversion, all x and y values are positive,
    # as is the circle unit value.
    # This is important, as the math.sqrt() function cannot handle 0 or
    # negative values; just to make our lives harder.
    tempxUnit = 1 - (yConverted * yConverted) / 2
    tempyUnit = 1 - (xConverted * xConverted) / 2
    xUnit = 0
    yUnit = 0
    
    if tempxUnit < 0:
        xUnit = xConverted * (-1*math.sqrt(-1*tempxUnit))
    else:
        xUnit = xConverted * math.sqrt(tempxUnit)
    
    if tempyUnit < 0:
        yUnit = yConverted * (-1*math.sqrt(-1*tempyUnit))
    else:
        yUnit = yConverted * math.sqrt(tempyUnit)
    #yUnit = yConverted * math.sqrt(1 - (xConverted * xConverted) / 2)
    
    #print("X Unit: ", str(xUnit), "Y Unit: ", str(yUnit))
    
    xMap = xUnit * radius
    yMap = yUnit * radius
    
    #print("X Map: ", str(xMap), "Y Map: ", str(yMap))
    
    # Convert to normal space values.
    xRealSpace = 0
    yRealSpace = 0
    if quadrant == 1:
        # Bottom Left - confirmed working.
        xRealSpace = int(radius - xMap)
        yRealSpace = int(yMap + radius)
        
    elif quadrant == 2: # Bottom Right - Confirmed working.
        
        xRealSpace = int(xMap + radius)
        yRealSpace = int(yMap + radius)
        
    elif quadrant == 3: # Top right data - confirmed working.
        
        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = int(radius - yMap)
        
    else: # Top Left, confirmed correct.
        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = -1 * int(radius-yMap)
    
    #print("X: ", str(xRealSpace), "Y: ", str(yRealSpace))
    
    return xRealSpace, yRealSpace

#  Very simple stopwatch.

class StopWatch(object):

    def __init__(self):
        self.stopwatch = 0
        self.stopwatchSet = False
        self.time = 0

    #  Get the current time - Real World.
    def getTime(self):
        self.time = time.time()
        return self.time

    #  Set Stopwatch - Real World
    def setStopwatch(self):
        self.stopwatchSet = True
        self.stopwatch = time.time()

    #  Get Stopwatch time  - Real World
    #  Should result in current time and later calc of 0 in other calling
    #  functions.
    def getStopwatch(self):
        if self.stopwatchSet == True:
            return self.stopwatch
        return time.time()

    #  Get seconds since stopwatch was set.
    def getElapsedStopwatch(self):
        return time.time() - self.stopwatch
    
    # Reset StopWatch
    def resetStopwatch(self):
        self.stopwatchSet = False
        self.stopwatch = 0

GameStopwatch = StopWatch()  #  Very much needed.

# Increment "game" time, this is IronSeed universe time.



#  Check event flags to see if the event has been tripped.
#  Note: negative events and events above 20000 always return true.
def checkEvent(event):
    if event < 0 or event >= 20000:
        return True
    
    if event >= 8192:
        return False
    
    if event in g.eventFlags:
        return True
    else:
        return False

#  Safe wrapping at a given step and number
def safeWrap(width,step,current):
    whereAt = current+step
    if whereAt >= width:
        return whereAt%width
    return whereAt

#  Render the given text onto a surface.
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


#  Fade out a given surface.
def fadeOut(width, height, surface, step):
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(g.BLACK)
    fade.set_alpha(step*5)
    surface.blit(fade,(0,0))
    if step >= 55:
        finished = True
    return finished

#  Fade in a given surface.
def fadeIn(width, height, surface, step):
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(g.BLACK)
    fade.set_alpha(255-step*5)
    surface.blit(fade,(0,0))
    if step >= 55:
        finished = True
    return finished

#  Take a piece of text and converge it on a central location from 4
#  different directions, with god-ray effects.
#  step indicates which step of the transformation to illustrate.
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

#  Create TV Fuzz - Quickly, with stylish half-fill by default
#  Based off of David "Futility" Clark's Static filled TV text font.
#  Note: More shades required.
def makeFuzz(width, height, half=True):
        
    fuzzyScreen = pygame.Surface((width, height), 0)
    fuzzyScreen.fill(g.BLACK)
    colours = fuzzyScreen.map_rgb(g.BLACK),fuzzyScreen.map_rgb(g.WHITE)
    C = random.choice
    S = fuzzyScreen.set_at
    yrange = range(height)
    xrange = range(width)
    for y in yrange:
        if y%2 == 0 or not half:
            for x in xrange:
                S((x,y),C(colours))
    return fuzzyScreen
