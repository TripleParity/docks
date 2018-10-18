from enum import Enum
from typing import List, Dict
import sys
import os

import time

import docker
from gpiozero import PWMLED

hostname = "10.0.0.2" # Manager

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

whiteLed = PWMLED(Colour.WHITE.value)
redLed = PWMLED(Colour.RED.value)
greenLed = PWMLED(Colour.GREEN.value)
blueLed = PWMLED(Colour.BLUE.value)

# whiteLed.value = 0.2
# redLed.value = 0.5
# blueLed.value = 0.2

colourToLed = {
    Colour.WHITE: whiteLed,
    Colour.RED: redLed,
    Colour.GREEN: greenLed,
    Colour.BLUE: blueLed
}

def turnOffAllColours():
    # colourToLed[Colour.WHITE].off()
    colourToLed[Colour.RED].off()
    colourToLed[Colour.GREEN].off()
    colourToLed[Colour.BLUE].off()

# turnOffAllColours()

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
    if (colour != Colour.GREEN):
        colourToLed[colour].value = 0.2
    else:
        colourToLed[colour].value = 1

def turnOffColour(colour):
    print('Turning off: ', colour)
    colourToLed[colour].value = 0

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
prevResponse = 1

print('Starting LED watcher...')

while True:
    response = os.system("ping -c 1 " + hostname + " > /dev/null")

    if response == 0:
        # print hostname, 'is up!'
        if prevResponse != 0:
            turnOnColour(Colour.WHITE)
    else:
        # print hostname, 'is down!'
        if prevResponse == 0:
            turnOffColour(Colour.WHITE)

    prevResponse = response

    if (client):
        containers = None

        try:
            containers = client.containers.list(filters={'status': 'running'})
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
                        print(colours)
                    else:
                        print('[ERROR] Invalid colour: ' + colourString + ' on ' + container.name)

            handleColourUpdate(prevColours, colours)
            prevColours = colours
        else:
            handleColourUpdate(prevColours, dict())
            prevColours = dict()
    else:
        try:
            client = createDockerClient()
        except:
            print('[ERROR] ', sys.exc_info()[0])
            client = None
            handleColourUpdate(prevColours, dict())
            prevColours = dict()
    
    time.sleep(2)
