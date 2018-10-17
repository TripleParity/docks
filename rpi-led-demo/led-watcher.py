from enum import Enum
from typing import List, Dict
import sys

import time

import docker

class Colour(Enum):
    WHITE = 18
    RED = 23
    GREEN = 24
    BLUE = 25

def colourStrToEnum(colourStr):
    if colourStr == 'white':
        return Colour.WHITE
    elif colourStr == 'red':
        return Colour.RED
    elif colourStr == 'green':
        return Colour.GREEN
    elif colourStr == 'blue':
        return Colour.BLUE
    
    return None

# Alternative to above function
# colour = colourToEnum.get(key, None)
#
colourToEnum = {
    'white': Colour.WHITE,
    'red': Colour.RED,
    'green': Colour.GREEN,
    'blue': Colour.BLUE
}

def findOff(previous, current):
    result = dict()

    for k, v in previous.items():
        if k not in current:
            result[k] = True

    return result

def findOn(previous, current):
    result = dict()

    for k, v in current.items():
        if k not in previous:
            result[k] = True

    return result

def turnOnColour(colour):
    print('Turning on: ', colour)
    TODO = 1

def turnOffColour(colour):
    print('Turning off: ', colour)
    TODO = 2

def turnOffAllColours():
    for k, v in colourToEnum.items():
        print('Turning off: ', k)
        TODO = 3

def handleColourUpdate(prevColours, colours):
    # Avoid potential flickering by calculating deltas
    turnOn = findOn(prevColours, colours)
    turnOff = findOff(prevColours, colours)

    for k, v in turnOn.items():
        turnOnColour(k)
        
    for k, v in turnOff.items():
        turnOffColour(k)

def createDockerClient():
    return docker.DockerClient(base_url='unix://var/run/docker.sock', version='1.37')

client = None
try:
    client = createDockerClient()
except:
    print('[ERROR] ', sys.exc_info()[0])
    client = None

prevColours = dict()

print('Starting LED watcher...')

while True:
    if (client):
        containers = None

        try:
            containers = client.containers.list()
        except:
            print('[ERROR] ', sys.exc_info()[0])
            handleColourUpdate(prevColours, dict())
            prevColours = dict()

        if (containers):
            colours = dict()

            for container in containers:
                if 'led_colour' in container.labels:
                    colourString = (str)(container.labels['led_colour'].strip())
                    colour = colourStrToEnum(colourString)

                    if colour != None:
                        colours[colour] = True
                    else:
                        print('[ERROR] Invalid colour: ' + colourString + ' on ' + container.name)

            handleColourUpdate(prevColours, colours)
            prevColours = colours
    else:
        try:
            client = createDockerClient()
        except:
            print('[ERROR] ', sys.exc_info()[0])
            client = None
            handleColourUpdate(prevColours, dict())
            prevColours = dict()
    
    time.sleep(1)
