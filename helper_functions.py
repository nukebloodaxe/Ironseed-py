# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:08:39 2019
Ironseed helper functions
@author: Nuke Bloodaxe
"""
import global_constants as g
import math
import cmath
import pygame
import random
import time


# Load a line of text data from a file, stripping comments marked with a #.
def loadLineStripComment(file):

    temp = '#'

    while temp[0] == '#':

        temp = file.readline()

#    print("temp is: ", temp)

    return temp


# Create a rotating line based on 9 points of movement.
def rotatingLine(position=0):

    rotator = ['|', '/', '-', '\\', '|', '/', '-', '\\', '|']

    return rotator[position]


# Based on a starting position, how many lines of text can we print before we
# reach a defined vertical pixel limit.
# Note:  It's expected that you check your start and finish limits are sane.
def textLinesWithin(topY, bottomY):

    return int((bottomY - topY)/g.offset)


# Based on a starting position, how many characters can we print before we
# reach a defined horizontal pixel limit.
# Note: I know this is a little silly right now, but it'll get better later.
def charactersWithin(leftX, rightX):

    return int((rightX-leftX)/g.offset)


# Create a colour gradient, from black to the colour in the given length.
# An optional increment can be added, to have a gradient without black.
# The colour is expected to be a Tuple: (0, 0, 0)
# The return is a list of tuples; provides max compatibility.
def colourGradient(length, colour, invert=False, increment=0):

    pixels = [(0, 0, 0)]

    if invert:

        step0 = -1*((colour[0] - increment)/length)
        step1 = -1*((colour[1] - increment)/length)
        step2 = -1*((colour[2] - increment)/length)
        pixel0 = colour[0]
        pixel1 = colour[1]
        pixel2 = colour[2]

    else:

        step0 = (colour[0]/length)
        step1 = (colour[1]/length)
        step2 = (colour[2]/length)
        pixel0 = (0 + increment)
        pixel1 = (0 + increment)
        pixel2 = (0 + increment)

    for pixel in range(length):

        pixel0 += step0
        pixel1 += step1
        pixel2 += step2
        pixels.append((int(pixel0), int(pixel1), int(pixel2)))

    return pixels


# Rotate the elements of an array left by 1 and return the result.
def shiftArrayLeft(array):

    return array[1:] + [array[0]]


# Rotate the elements of an array right by 1 and return the result.
def shiftArrayRight(array):

    return [array[-1]] + array[:-1]


# Create a line from the given colour, as a list of tuples.
# The colour is expected to be a Tuple: (0, 0, 0)
# The return is a list of tuples; provides max compatibility.
def colourLine(length, colour):

    pixels = [colour]

    for pixel in range(length):

        pixels.append(colour)

    return pixels


# Create a bar using a colourGradient tuple list.
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
#  Note:  In the original game the cicles go towards the center.
#  TODO:  True/False for draw circles from center or draw inwards from border.
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

    return x * cmath.sqrt(1 - y * y / 2).real, y * cmath.sqrt(1 - x * x / 2).real

    #  x * math.sqrt(1 - y * y / 2), y * math.sqrt(1 - x * x / 2)
    #  Determine in which quadrant circle unit value will appear.
    #  And convert x and y to temporary unit circle values
    radius = xWidth / 2
    sqrt = math.sqrt  # Reduce lookups, this function needs to be FAST!
    unitCircleMultiplier = 1/radius
    xConverted = 0
    yConverted = 0
    quadrant = 1
    #  top right = 3, bottom right = 2, bottom left = 1, top left = 4.

    if x <= radius:

        if y <= radius:

            quadrant = 4  # top left
            # x * unitCircleMultiplier
            xConverted = -1 * (radius-x) * unitCircleMultiplier
            # y * unitCircleMultiplier
            yConverted = -1 * (radius-y) * unitCircleMultiplier

        else:

            quadrant = 3  # Top right - contains top right data.
            xConverted = -1 * (radius-x) * unitCircleMultiplier
            yConverted = (radius - y) * unitCircleMultiplier
    else:

        if y <= radius:

            quadrant = 1  # bottom left?
            xConverted = (radius - x) * unitCircleMultiplier
            yConverted = -1 * (radius - y) * unitCircleMultiplier

        else:

            quadrant = 2  # Appears to be bottom right data
            xConverted = -1*(radius - x) * unitCircleMultiplier
            yConverted = -1*(radius - y) * unitCircleMultiplier

    # print("X Converted: ", str(xConverted), "Y Converted: ", str(yConverted))

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

    # Convert to normal space values.
    xRealSpace = 0
    yRealSpace = 0

    if quadrant == 1:

        # Bottom Left - confirmed working.
        xRealSpace = int(radius - xMap)
        yRealSpace = int(yMap + radius)

    elif quadrant == 2:  # Bottom Right - Confirmed working.

        xRealSpace = int(xMap + radius)
        yRealSpace = int(yMap + radius)

    elif quadrant == 3:  # Top right data - confirmed working.

        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = int(radius - yMap)

    else:  # Top Left, confirmed correct.

        xRealSpace = -1 * int(radius-xMap)
        yRealSpace = -1 * int(radius-yMap)

    #print("X: ", str(xRealSpace), "Y: ", str(yRealSpace))

    return xRealSpace, yRealSpace


#  Map a point on a square 2D array to a point on a 2D sphere.
#  Note:  No exception correction for cmath.sqrt(0)
#  BIG NOTE:  This is a cmath version of the prior sphereMap function.
#             It should be treated as highly experimental.
#  Convention Note: This could be divided into further functions, but this
#                   would increase the execution and lookup time too much.
def cSphereMap(x, y, xWidth, yHeight):

    #  x * math.sqrt(1 - y * y / 2), y * math.sqrt(1 - x * x / 2)
    #  Determine in which quadrant circle unit value will appear.
    #  And convert x and y to temporary unit circle values
    radius = xWidth / 2
    sqrt = cmath.sqrt  # Reduce lookups, this function needs to be FAST!
    unitCircleMultiplier = 1 / radius
    xConverted = 0
    yConverted = 0
    xComplex = 0
    yComplex = 0
    quadrant = 1

    # top right = 3, bottom right = 2, bottom left = 1, top left = 4.

    # Initial conversion calculations before quadrant mapping.
    # We perform the unit circle conversion here.
    xConverted = (radius - x) * unitCircleMultiplier
    yConverted = (radius - y) * unitCircleMultiplier

    # We change the sign coordinate according to its graphical quadrant.
    if x <= radius:

        if y <= radius:

            quadrant = 4  # top left
            xConverted *= -1
            yConverted *= -1

        else:

            quadrant = 3  # Top right - contains top right data.
            xConverted *= -1

    else:

        if y <= radius:

            quadrant = 1  # bottom left?
            yConverted *= -1

        else:

            quadrant = 2  # Appears to be bottom right data
            xConverted *= -1
            yConverted *= -1

    # print("xConverted = ", str(xConverted), "yConverted = ", str(yConverted))

    # We derive the complex number here for the pixel position on the circle.
    # Notice how the prior conversion produces a real result for simplicity?
    xComplex = xConverted * sqrt(1 - yConverted * yConverted / 2).real
    yComplex = yConverted * sqrt(1 - xConverted * xConverted / 2).real

    # print("X Complex: ", str(xComplex), "Y Complex: ", str(yComplex))

    # We now scale the X and Y values from cicle units to our real x and y.
    xMap = xComplex * radius
    yMap = yComplex * radius

    # print("X Map: ", str(xMap), "Y Map: ", str(yMap))

    # Convert to normal space values, so it maps to the texture.
    xRealSpace = 0
    yRealSpace = 0

    if quadrant == 1:

        # Bottom Left - confirmed working.
        xRealSpace = int(radius - xMap)
        yRealSpace = int(yMap + radius)

    elif quadrant == 2:  # Bottom Right - Confirmed working.

        xRealSpace = int(xMap + radius)
        yRealSpace = int(yMap + radius)

    elif quadrant == 3:  # Top right data - confirmed working.

        xRealSpace = -1 * int(radius - xMap)
        yRealSpace = int(radius - yMap)

    else:  # Top Left, confirmed correct.

        xRealSpace = -1 * int(radius - xMap)
        yRealSpace = -1 * int(radius - yMap)

    # print("X: ", str(xRealSpace), "Y: ", str(yRealSpace))

    return xRealSpace, yRealSpace


# Very simple stopwatch.
class StopWatch(object):

    def __init__(self):

        self.stopwatch = 0.0
        self.stopwatchSet = False
        self.time = 0.0

    # Get the current time - Real World.
    def getTime(self):

        self.time = time.time()
        return self.time

    # Set Stopwatch - Real World
    def setStopwatch(self):

        self.stopwatchSet = True
        self.stopwatch = time.time()

    # Get Stopwatch time  - Real World
    # Should result in current time and later calc of 0 in other calling
    # functions.
    def getStopwatch(self):

        if self.stopwatchSet is True:

            return self.stopwatch

        return time.time()

    # Get seconds since stopwatch was set.
    def getElapsedStopwatch(self):

        return time.time() - self.stopwatch

    # Reset StopWatch
    def resetStopwatch(self):

        self.stopwatchSet = False
        self.stopwatch = 0


#  Create a global stopwatch, this gets used all over the place.
GameStopwatch = StopWatch()  # Very much needed.


#  Prefix a number with zeros for places width and return it as a string.
#  If the places figure is 0 or less, return the number as a string.
#  If the number is greater than the length of the places, return the number.
def zeroPrefix(number, places):

    if places <= 0:

        return str(number)

    result = ''

    if len(str(number)) >= places:

        return str(number)

    prefixCount = places - len(str(number))

    for index in range(0, prefixCount):

        result += '0'

    result += str(number)

    return result


# Implement "game" time, this is IronSeed universe time.
class IronSeedTime(object):

    def __init__(self):

        #  Set stardate from global value. M,D,Y,H,M
        self.starDateYear = g.starDate[2]
        self.starDateMonth = g.starDate[0]
        self.starDateDay = g.starDate[1]
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

        return str(zeroPrefix(self.starDateDay, 2)+'/'+zeroPrefix(self.starDateMonth, 2)+'/'+zeroPrefix(self.starDateYear, 5)+'  '+zeroPrefix(self.starDateHour, 2)+':'+zeroPrefix(self.starDateMinute, 2))

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

        if Day:  # Do this very simple, 30 days in the month.

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

    if text == []:

        return  # Nothing to render

    position = 0

    for line in text:

        renderedText = font.render(line, True, colour)

        if centred:

            Surface.blit(
                renderedText, (width-(renderedText.get_width()/2), height+position))

        elif justifyRight:

            Surface.blit(
                renderedText, ((width-renderedText.get_width()), height+position))

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
def fadeOut(width, height, surface, step, fillColour=g.BLACK):

    finished = False
    fade = pygame.Surface(g.size)
    fade.fill(fillColour)
    fade.set_alpha(step*5)
    surface.blit(fade, (0, 0))

    if step >= 55:

        finished = True

    return finished


#  Fade in a given surface.
def fadeIn(width, height, surface, step, fillColour=g.BLACK):

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

    # Find text centre
    widthHeightDifference = int((g.width - g.height)/2)
    longestText = ""

    for line in text:

        if len(line) > len(longestText):

            longestText = line

    demoText = font.render(longestText, True, colour)
    textCentreWidth = int(demoText.get_width()/2)
    centre = False

    #  New method.
    x1 = widthHeightDifference + textCentreWidth
    #print("Text Centre Width:", str(x1))
    x2 = g.width - widthHeightDifference - textCentreWidth
    #print("Text Centre Width 2:", str(x2))
    y1 = 0  # textCentreHeight
    #print("Text Centre Height:", str(y1))
    y2 = x2-x1
    #print("Text Centre Height 2:", str(y2))

    if darken:

        fade = pygame.Surface(g.size)
        fade.fill(g.BLACK)
        fade.set_alpha(10)
        surface.blit(fade, (0, 0))

    renderText(text, font, surface, colour, offset, x1+step, y1+step, True)
    renderText(text, font, surface, colour, offset, x2-step, y1+step, True)
    renderText(text, font, surface, colour, offset, x1+step, y2-step, True)
    renderText(text, font, surface, colour, offset, x2-step, y2-step, True)

    if (int(x1+step) - int(x2-step)) <= 1 and (int(x1+step) - int(x2-step)) >= -1:

        centre = True

    return (centre, x1+step, y1+step)


#  Create TV Fuzz - Quickly, with stylish half-fill by default
#  Based off of David "Futility" Clark's Static filled TV text font.
#  Note: More shades of grey required; no, not 50...
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


#  Prepare an animation array by taking frame definition data, and
#  using it to extract x rows and x columns of frames into a returned array.
#  The texture is the graphic containing the frames.
#  The Frame dimensions are defined using the following format:
#  ((x,y)(width,height)(columns,rows))
#  By default, frames are resized to current resolution, but this can be
#  turned off by using False as the last parameter.
def prepareAnimationArray(texture, frameDefinitions, resize=True):

    frames = []

    for column in range(0, frameDefinitions[2][0]):

        for row in range(0, frameDefinitions[2][1]):

            sourceRectangle = ((frameDefinitions[0][0] + (frameDefinitions[1][0]*column)),
                               (frameDefinitions[0][1] +
                                (frameDefinitions[1][1]*row)),
                               frameDefinitions[1][0], frameDefinitions[1][1])

            frame = pygame.Surface((frameDefinitions[1][0],
                                    frameDefinitions[1][1]))
            frame.blit(texture, (0, 0), sourceRectangle)
            frames.append(frame)

    if resize:

        frames = resizeGraphicArray(frames)

    return frames


#  Resize an array of frames for an animation or similar to the current
#  resolution.
def resizeGraphicArray(graphicArray):

    resizedFrames = []

    for frame in graphicArray:

        newFrame = pygame.transform.scale(frame, (int(
            (g.width/320)*frame.get_width()), int((g.height/200)*frame.get_height())))
        resizedFrames.append(newFrame)

    return resizedFrames


#  Create a pie graph from a given set of values in %.
#  The values are expected to be in size order, largest to smallest.
#  The pie graph is drawn to the given surface.
#  an array of colours is returned, representing the assigned colours for each
#  value.  This is provided in value order, from the passed array.
#  centre is a tuple(x, y), colour is an 8-bit tuple (r,g,b)
#  An optional increment gives a different gradient colour start position.
#  Note:  Might need to make this return both the values and a surface to work.
def drawPieGraph(surface, centre, radius, colour, values, increment=0):

    #  Generate the pie segment colours, invert colour gradient.
    pieGraphColours = colourGradient(len(values)+increment, colour, True)

    currentAngle = 270  # Polar co-ordinates, want graph to start at top.
    colourIndex = 0

    #  Draw the largest value as a circle, other values will overlay.
    pygame.draw.circle(surface, pieGraphColours[0+increment], centre, radius)

    for segment in values:

        targetArc = [centre]

        for degree in range(int(currentAngle), int(currentAngle+((360/100)*segment))):

            targetArc.append((centre[0]+(radius*math.cos((degree*math.pi)/180)),
                             centre[1]+(radius*math.sin((degree*math.pi)/180))))

        targetArc.append(centre)

        if len(targetArc) > 2:

            pygame.draw.polygon(
                surface, pieGraphColours[colourIndex+increment], targetArc)

        currentAngle += (360/100)*segment
        colourIndex += 1

    return pieGraphColours


# Take an input texture, and based on the current step, create a frame of an
# animation where pixels are sprayed vertically, top to bottom, left to right,
# from a central point to form the final image.
# Note: Centre is an x, y coordinate as a tuple.
# The buffer is a preexisting predrawn surface, and the haveBuffer indicator
# tells the funtion to use it if present.  We always return a buffer image.
def drawSprayFrame(texture, centre, increment=0, buffer=object,
                   haveBuffer=False, priorXY=(0, 0)):

    # The surface which will be returned.
    sprayResult = object

    currentX = priorXY[0]
    currentY = priorXY[1]

    # Use a preexisting buffer?
    if haveBuffer and increment == 0:

        sprayResult = pygame.Surface(texture.get_size(), 0)
        sprayResult.set_colorkey(g.BLACK)
        sprayResult.fill(g.BLACK)
        sprayResult.set_at((currentX, currentY), texture.get_at((currentX, currentY)))
        buffer = sprayResult.copy()

    else:

        buffer.set_at((currentX, currentY), texture.get_at((currentX, currentY)))
        sprayResult = buffer.copy()

    #print("Current X: ", currentX, "Current Y: ", currentY)
    #print("Texture-Width: ", buffer.get_width(),
    #      "Texture-Height: ", buffer.get_height())

    if (currentY < (texture.get_height() - 1)):

        currentY += 1

    else:

        currentY = 0
        currentX += 1

    #print("currentX = ", currentX, "currentY = ", currentY)

    # Draw a line the same colour as the origin pixel.
    pygame.draw.line(sprayResult, texture.get_at((currentX, currentY)), centre,
                     (currentX, currentY))

    return sprayResult, buffer, (currentX, currentY)
