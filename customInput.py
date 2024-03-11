import time
import pyautogui
import pydirectinput
import settings
import os
from images import getConfidence
import random

VERBOSE = settings.VERBOSE
#SAFE_SPACE = (settings.androidSize[0] + 100, int(settings.androidSize[1] / 2))
#CLICK_DELAY = 0.5
"""
max_x = settings.androidSize[0]
max_y = settings.androidSize[1] + settings.barWidth
region=(0, 0, max_x, max_y)
"""

# # TODO: uncomment this out in prod
# #pyautogui.FAILSAFE=False

special_characters = {
    '~':'`',
    '!':'1',
    '@':'2',
    '#':'3',
    '$':'4',
    '%':'5',
    '^':'6',
    '&':'7',
    '*':'8',
    '(':'9',
    ')':'0',
    '_':'-',
    '+':'=',
    '{':'[',
    '}':']',
    '|':'\\',
    ':':';',
    '"':"'",
    '<':',',
    '>':'.',
    '?':'/'
}

class customInput:

    def __init__(self, safe_space, click_delay, region, pathToImages):
        self.safe_space = safe_space
        self.click_delay = click_delay
        self.region = region
        self.pathToImages = pathToImages

    #waits until image is on screen or until max time limit is reached
    def wait_until(self, description, max=20, wait=0, visible=True):
        startTime = time.time()
        while True:
            test = self.find(description)

            if test and visible:
                if VERBOSE: print(f"found {description}")
                break
            
            if not test and not visible:
                if VERBOSE: print(f"didnt find {description}")
                break

            if (time.time() - startTime) > max:
                if visible and VERBOSE: print(f"Couldn't find {description} after {max} seconds")
                if not visible and VERBOSE: print(f"{description} still found on screen after {max} seconds")
                return False
            time.sleep(0.5)
        
        if wait:
            time.sleep(wait)
        
        return test


    def locate(self, object):
        x = int(object[0] + object[2] / 2)
        y = int(object[1] + object[3] / 2)
        return x, y


    def move_back(self):
        pyautogui.moveTo(self.safe_space[0], self.safe_space[1])


    #click and move back
    def click(self, object=None, button="left", wait=0, back=True, confidence=None):
        if VERBOSE: print(f"Attempting to click {object}")
        if not object:
            print("ERROR: could not find object to click")
            return object
        if type(object) == tuple:
            x, y = object
        elif object:
            if type(object) == str:
                object = self.find(object, confidence=confidence)
                if not object:
                    print("ERROR: could not find object to click")
                    return object
            x, y = self.locate(object)
        else:
            if VERBOSE: print("WARNING: clicking without any object specified")
            x, y = pyautogui.position()
        if VERBOSE: print(f"Moving to {x}, {y}")
        pyautogui.moveTo(x=x, y=y)
        time.sleep(self.click_delay)
        pydirectinput.mouseDown(button=button)
        time.sleep(0.075 + random.random() / 50)    #average mouse click lasts 85ms, with Q3 = 95ms, Q1= 75ms;
        pydirectinput.mouseUp(button=button)
        if back:
            self.move_back()
        if wait:
            time.sleep(wait)
        return True


    def moveTo(self, object, duration=0):
        if object == None:
            print("ERROR: cannot move to None - probably couldn't find object")
        if type(object) == tuple:
            x, y = object
        else:
            if type(object) == str:
                object = self.find(object)
            x, y = self.locate(object)
        pyautogui.moveTo(x, y, duration=duration)


    def find(self, description, confidence=None, grayscale=False):
        imgPath = f"{os.path.join(self.pathToImages, description)}.png"

        if not confidence:
            confidence = getConfidence(description)

        if self.region:
            try:
                return pyautogui.locateOnScreen(imgPath, confidence=confidence, region=self.region, grayscale=grayscale)
            except:
                return False
        else:
            return pyautogui.locateOnScreen(imgPath, confidence=confidence, grayscale=grayscale)

    def press(self, key, presses=1, interval=0.1):
        for i in range(presses):
            if key in special_characters.keys():
                self.hotkey(key)
            elif key.isupper():
                self.hotkey('shift', key)
            else:
                pydirectinput.press(key)
            time.sleep(interval)


    def write(self, message, interval=0.1, end=""):
        for letter in message:
            self.press(letter, interval=interval)
        if end:
            self.press(end)


    def hotkey(self, *keys):
        for key in keys:
            if key in special_characters.keys():
                pydirectinput.keyDown('shift')
                time.sleep(0.1)
                pydirectinput.keyDown(special_characters[key])
            else:
                pydirectinput.keyDown(key)
        time.sleep(0.1)
        for key in keys[::-1]:
            if key in special_characters.keys():
                pydirectinput.keyUp(special_characters[key])
                time.sleep(0.1)
                pydirectinput.keyUp('shift')
            else:
                pydirectinput.keyUp(key)



    #swipe functions
    def swipe(self, ctrl, duration=.25):
        if ctrl == "up":
            x = int(settings.androidSize[0] / 2)
            y = settings.barWidth + settings.androidSize[1] - 5
            pyautogui.moveTo(x, y)
            y = settings.barWidth + int(1 * settings.androidSize[1] / 4)
        
        if ctrl == "down":
            x = int(settings.androidSize[0] / 2)
            y = settings.barWidth + 5
            pyautogui.moveTo(x, y)
            y = settings.barWidth + int(3 * settings.androidSize[1] / 4)

        if ctrl == "left":
            x = 5
            y = settings.barWidth + int(settings.androidSize[1] / 2)
            pyautogui.moveTo(x, y)
            x = int(3 * settings.androidSize[0] / 4)

        if ctrl == "right":
            x = settings.androidSize[0] - 5
            y = settings.barWidth + int(settings.androidSize[1] / 2)
            pyautogui.moveTo(x, y)
            x = int(1 * settings.androidSize[0] / 4)

        time.sleep(1)
        pyautogui.dragTo(x, y, duration)
        self.move_back()



    def scroll(self, direction, min_interval=0.04):
        if VERBOSE: print(f"Scrolling {direction}")
        self.moveTo((settings.androidSize[0] / 2, settings.androidSize[1] / 2 + settings.barWidth))
        if direction == "up": direction = 100
        if direction == "down": direction = -100
        for i in range(20):
            pyautogui.scroll(direction)
            time.sleep(min_interval + (random.random() * 0.02))
        self.move_back()


