# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:08:39 2019
Ironseed helper functions
@author: Nuke Bloodaxe
"""
import pygame, random, time, math
import global_constants as g

#  Create a colour gradient, from black to the colour in the given length.
#  The colour is expected to be a Tuple: (0, 0, 0)
#  The return is a list of tuples; provides max compatibility.
def colourGradient(length, colour):
    
    pixels = [(0, 0, 0)]
    step0 = colour[0]/length
    step1 = colour[1]/length
    step2 = colour[2]/length
    pixel0 = 0
    pixel1 = 0
    pixel2 = 0
    
    for pixel in range(length):
        
        pixel0 += step0
        pixel1 += step1
        pixel2 += step2
        pixels.append((int(pixel0), int(pixel1), int(pixel2)))
    
    return pixels

#  Create a line from the given colour, as a list of tuples.
#  The colour is expected to be a Tuple: (0, 0, 0)
#  The return is a list of tuples; provides max compatibility.
def colourLine(length, colour):
    
    pixels = [colour]

    for pixel in range(length):
        
        pixels.append(colour)
    
    return pixels

#  Create a bar using a colourGradient tuple list.
#  Length is the required element width from the tuple list.
#  Height is the amount of times the bar is repeated vertically.
#  Rounded indicates if the end of the bar needs to be drawn as
#  half a hemesphere with Height diameter.
#  Returns a pygame surface with the required elements added.
def createBar(tupleList=[], length=0, height=int((g.height/320)*2), rounded=False):
    
    bar = pygame.Surface((length, height))
    bar.set_colorkey(g.BLACK)
    barArray = pygame.PixelArray(bar)
    roundedY = 0
    roundStep = 0
    
    if rounded:
        
        roundedY = int(height/2)
        
    
    for x in range(length):
        
        for y in range(height):
            
            if rounded:
                
                if (length - roundedY) <= x:
                    
                    if y-(x-(length - roundedY)) > 0 and y < y+(x-(length - roundedY)):
                        
                        barArray[x][y] = tupleList[x]
                        
                else:
                    
                    barArray[x][y] = tupleList[x]
                    
            else:
                
                barArray[x][y] = tupleList[x]
                
    barArray.close()
    return bar

#  Create a targetting reticule from [quantity] circles and draw it on
#  passed [surface] at [x],[y], with [spacing] between circles.
#  Draw line of circle with [thickness] pixels and [colour].
def targettingReticule(surface, x, y, colour, quantity, spacing, thickness):
    
    for count in range(quantity):
    
        pygame.draw.circle(surface, colour, (x, y),
                           (spacing + count*spacing),
                           thickness)
    

#  Map a point on a square 2D array to a point on a 2D sphere.
#  Note:  No exception correction for math.sqrt(0)
#  BIG NOTE:  Complexity comes from ridiculous math.sqrt not handling negative
#             numbers...
def sphereMap(x, y, xWidth, yHeight):
    
    #  x * math.sqrt(1 - y * y / 2), y * math.sqrt(1 - x * x / 2)
    #  Determine in which quadrant circle unit value will appear.
    #  And convert x and y to temporary unit circle values
    radius = xWidth / 2
    sqrt = math.sqrt  #  Reduce lookups, this function needs to be FAST!
    unitCircleMultiplier = 1/radius
    xConverted = 0
    yConverted = 0
    quadrant = 1
    #  top right = 3, bottom right = 2, bottom left = 1, top left = 4.
    
    if x <= radius:
        
        if y <= radius:
            
            quadrant = 4 #  top left
            xConverted = -1 * (radius-x) * unitCircleMultiplier#x * unitCircleMultiplier
            yConverted = -1 * (radius-y) * unitCircleMultiplier#y * unitCircleMultiplier
            
        else:
            
            quadrant = 3 #  Top right - contains top right data.
            xConverted = -1 * (radius-x) * unitCircleMultiplier
            yConverted = (radius - y) * unitCircleMultiplier
    else:
        
        if y <= radius:
            
            quadrant = 1 #  bottom left?
            xConverted = (radius - x) * unitCircleMultiplier
            yConverted = -1 * (radius - y) * unitCircleMultiplier
            
        else:
            
            quadrant = 2  #  Appears to be bottom right data
            xConverted = -1*(radius - x) * unitCircleMultiplier
            yConverted = -1*(radius - y) * unitCircleMultiplier
            
    #print("X Converted: ", str(xConverted), "Y Converted: ", str(yConverted))
    #  By doing this temporary conversion, all x and y values are positive,
    #  as is the circle unit value.
    #  This is important, as the math.sqrt() function cannot handle 0 or
    #  negative values; just to make our lives harder.
    tempxUnit = 1 - (yConverted * yConverted) / 2
    tempyUnit = 1 - (xConverted * xConverted) / 2
    xUnit = 0
    yUnit = 0
    
    if tempxUnit < 0:
        
        xUnit = xConverted * (-1*sqrt(-1*tempxUnit))
        
    else:
        
        xUnit = xConverted * sqrt(tempxUnit)
    
    if tempyUnit < 0:
        
        yUnit = yConverted * (-1*sqrt(-1*tempyUnit))
        
    else:
        
        yUnit = yConverted * sqrt(tempyUnit)
        
    #yUnit = yConverted * math.sqrt(1 - (xConverted * xConverted) / 2)
    
    #print("X Unit: ", str(xUnit), "Y Unit: ", str(yUnit))
    
    xMap = xUnit * radius
    yMap = yUnit * radius
    
    #print("X Map: ", str(xMap), "Y Map: ", str(yMap))
    
    #  Convert to normal space values.
    xRealSpace = 0
    yRealSpace = 0
    
    if quadrant == 1:
        
        #  Bottom Left - confirmed working.
        xRealSpace = int(radius - xMap)
        yRealSpace = int(yMap + radius)
        
    elif quadrant == 2:  #  Bottom Right - Confirmed working.
        
        xRealSpace = int(xMap + radius)
        yRealSpace = int(yMap + radius)
        
    elif quadrant == 3:  #  Top right data - confirmed working.
        
        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = int(radius - yMap)
        
    else:  #  Top Left, confirmed correct.
    
        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = -1 * int(radius-yMap)
    
    #print("X: ", str(xRealSpace), "Y: ", str(yRealSpace))
    
    return xRealSpace, yRealSpace

#  Very simple stopwatch.

class StopWatch(object):

    def __init__(self):
        
        self.stopwatch = 0.0
        self.stopwatchSet = False
        self.time = 0.0

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
        
        if self.stopwatchSet is True:
            
            return self.stopwatch
        
        return time.time()

    #  Get seconds since stopwatch was set.
    def getElapsedStopwatch(self):
        
        return time.time() - self.stopwatch
    
    #  Reset StopWatch
    def resetStopwatch(self):
        
        self.stopwatchSet = False
        self.stopwatch = 0

#  Create a global stopwatch, this gets used all over the place.
GameStopwatch = StopWatch()  #  Very much needed.

#  Prefix a number with zeros for places width and return it as a string.
#  If the places figure is 0 or less, return the number as a string.
#  If the number is greater than the length of the places, return the number.
def zeroPrefix(self, number, places):
    
    if places <=0:
        
        return str(number)
    
    result = ''
    
    if len(str(number)) >= places:
        
        return str(number)
    
    prefixCount = places - len(str(number))
    
    for index in range(1, prefixCount):
        
        result += '0'
    
    result += str(number)
    
    return result

# Implement "game" time, this is IronSeed universe time.

class IronSeedTime(object):
    
    def __init__(self):

        #  Set stardate from global value.        
        self.starDateYear = g.starDate[0]
        self.starDateMonth = g.starDate[1]
        self.starDateDay = g.starDate[2]
        self.starDateHour = g.starDate[3]
        self.starDateMinute = g.starDate[4]
        self.internalTimer = StopWatch()
        self.internalTimer.setStopwatch()

    #  Load new values, usually from Save Game.        
    def loadNewDate(self, Year, Month, Day, Hour, Minute):
        
        self.starDateYear = Year
        self.starDateMonth = Month
        self.starDateDay = Day
        self.starDateHour = Hour
        self.starDateMinute = Minute

    #  Retrieve game time as list, for special displays and save game.
    def getGameTime(self):
        
        return [self.starDateYear, self.starDateMonth, self.starDateDay,
                self.starDateHour, self.starDateMinute]
    
    #  Return string of IronSeedTime, usually for display.
    #  Note:  For some reason time was in blue on black...
    def __str__(self):
        
        return zeroPrefix(self.starDateDay, 2)+'/'+zeroPrefix(self.starDateMonth, 2)+'/'+str(self.starDateYear)+'  '+zeroPrefix(self.starDateHour, 2)+':'+zeroPrefix(self.starDateMinute, 2)
    
    #  Update the time, this uses the default of 1 real-world
    #  second = 5 minutes.
    def update(self):
        
        if self.internalTimer.getElapsedStopwatch() >= 1.0:
            
            self.internalTimer.setStopwatch()
            self.incrementTime(False, False, False, False, True)
        
    
    #  Tick a unit of time
    def incrementTime(self, Year=False, Month=False,
                      Day=False, Hour=False, Minute=False):
        
        if Year:
            
            self.starDateYear += 1
        
        if Month:
            
            self.starDateMonth += 1
            
            if self.starDateMonth > 12:
                
                self.starDateMonth = 0
                self.incrementTime(True)
            
        if Day: #  Do this very simple, 30 days in the month.
            
            self.starDateDay += 1
            
            if self.starDateDay > 30:
                
                self.starDateDay = 0
                self.incrementTime(False, True)
            
        if Hour:
            
            self.starDateHour += 1
            
            if self.starDateHour > 24:
                
                self.starDateHour = 0
                self.incrementTime(False, False, True)
            
        if Minute:
            
            self.starDateMinute += 5
            
            if self.starDateMinute > 59:
                
                self.starDateMinute = 0
                self.incrementTime(False, False, False, True)
                


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
def safeWrap(width, step, current):
    
    whereAt = current+step
    
    if whereAt >= width:
        
        return whereAt % width
    
    return whereAt

#  Return a subset of a list, safely
#  Start is the start of the index in the list.
#  End is the ending index entry in the list.
#  We return what we can if the ending index is longer than the list.
def subsetList(theList, start, end):
    
    subSet = []
    count = 0
    
    for item in theList:
        
        if count >= start and count <= end:
            
            subSet.append(item)
        
        count += 1
        
        if count > end:
            
            break
        
    return subSet

#  Render the given text onto a surface.
#  With right justification, make sure you provide the width where the text
#  should end.
def renderText(text, font, Surface, colour=g.WHITE, offset=0, width=0, height=0, centred=False, justifyRight=False):
    
    position = 0
    
    for line in text:
        
        renderedText = font.render(line, True, colour)
        
        if centred:
            
            Surface.blit(renderedText, (width-(renderedText.get_width()/2), height+position))
            
        elif justifyRight:
            
            Surface.blit(renderedText, ((width-renderedText.get_width()), height+position))
            
        else:
            
            Surface.blit(renderedText, (width, height+position))
            
        position += offset

#  Print text at height+width of given surface, fading in.
def fadeInText(text, width, height, colour, surface, step=0, darken=False, centreText=True):
    
    comboSurface = pygame.Surface(g.size)
    finished = False
    
    if darken:
        
        fade = pygame.Surface(g.size)
        fade.fill(g.BLACK)
        fade.set_alpha(20)
        surface.blit(fade, (0, 0))
        
    renderText(text, g.font, comboSurface, colour, 20, width, height, True)
    comboSurface.set_alpha(step*10)
    safeSurface = pygame.PixelArray(surface)
    safeCombo = pygame.PixelArray(comboSurface)
    line = 0
    
    while line < g.height:
        
        for pixel in range(g.width):
            
            if safeCombo[pixel][line] != 0:
                
                safeSurface[pixel][line] = safeCombo[pixel][line]            

        line += 1

    #surface.blit(comboSurface,(0,0))
    del safeSurface
    del safeCombo
    
    if (step*10) >= 255:
        
        finished = True
        
    return finished


#  Fade out a given surface.
def fadeOut(width, height, surface, step, fillColour = g.BLACK):
    
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(fillColour)
    fade.set_alpha(step*5)
    surface.blit(fade, (0, 0))
    
    if step >= 55:
        
        finished = True
        
    return finished

#  Fade in a given surface.
def fadeIn(width, height, surface, step, fillColour = g.BLACK):
    
    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(g.BLACK)
    fade.set_alpha(255-step*5)
    surface.blit(fade, (0, 0))
    
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
    
    x1 = ((width*ratio)/8)*3.25#width/4#7*3.25
    x2 = ((width*ratio)/8)*6.50#(width/4)*2#7*6.50
    y1 = ((height*ratio2)/5)#/5)#height/4#7
    y2 = ((height*ratio2)/5)*2.5#/5)*2.5#(height/4)*2#7*3.5
    
    if darken:
        
        fade = pygame.Surface(g.size)
        fade.fill(g.BLACK)
        fade.set_alpha(10)
        surface.blit(fade, (0,0))
        
    renderText(text, font,surface, colour, offset, x1+step, y1+step, True)
    renderText(text, font,surface, colour, offset, x2-step, y1+step, True)
    renderText(text, font,surface, colour, offset, x1+step, y2-step, True)
    renderText(text, font,surface, colour, offset, x2-step, y2-step, True)
    
    if (int(x1+step) - int(x2-step)) <= 1 and (int(x1+step) - int(x2-step)) >= -1:
        
        centre = True
        
    return (centre, x1+step, y1+step)

#  Create TV Fuzz - Quickly, with stylish half-fill by default
#  Based off of David "Futility" Clark's Static filled TV text font.
#  Note: More shades required.
def makeFuzz(width, height, half=True):
        
    fuzzyScreen = pygame.Surface((width, height), 0)
    fuzzyScreen.fill(g.BLACK)
    colours = fuzzyScreen.map_rgb(g.BLACK), fuzzyScreen.map_rgb(g.WHITE)
    C = random.choice
    S = fuzzyScreen.set_at
    yrange = range(height)
    
    if half is True:
        
        yrange = range(0, height, 2)
        
    xrange = range(width)
    
    for y in yrange:
        
        #if y%2 == 0 or not half:
        #    for x in xrange:
        #        S((x,y),C(colours))
        
        for x in xrange:
            
            S((x, y), C(colours))
            
    return fuzzyScreen
