import pydirectinput
import pyautogui
import time
import mss
import operator
from PIL import Image
import numpy as np
import win32api


def main():
    """
    Main function for the program
    """

    # Getting the main clicking position
    print("Collecting Click Center")
    input()
    clickCenter = pydirectinput.position()

    # Getting the center of the level map
    print("Collecting Map Center")
    input()
    mapCenter = pydirectinput.position()
    mapX, mapY = mapCenter

    # Item 1 to buy
    print("Collecting Hire Center 1")
    input()
    hireCenter1 = pydirectinput.position()

    # Item 2 to buy
    print("Collecting Hire Center 2")
    input()
    hireCenter2 = pydirectinput.position()

    # Item 3 to buy
    print("Collecting Hire Center 3")
    input()
    hireCenter3 = pydirectinput.position()

    # Getting empty bottom area of the shop
    print("Collecting Bottom of Shop Top Left")
    input()
    shopTL = pydirectinput.position()

    # Getting empty bottom area of the shop
    print("Collecting Bottom of Shop Bootom Right")
    input()
    shopBR = pydirectinput.position()

    # Getting scroll down button
    print("Collecting Scroll Down")
    input()
    scrollDown = pydirectinput.position()

    # Getting the Boss Clock top left
    print("Collecting Boss Clock Top Left Corner")
    input()
    bossClockTL = pydirectinput.position()

    # Getting the Boss Clock bottom right
    print("Collecting Boss Clock Bottom Right Corner")
    input()
    bossClockBR = pydirectinput.position()

    # Getting the Width & Height for the boss clock icon and Shop icon
    bossClockW, bossClockH = tuple(map(operator.sub, bossClockBR, bossClockTL))
    shopW, shopH = tuple(map(operator.sub, shopBR, shopTL))

    # Starting screenshotting object
    sct = mss.mss()

    # Setting up the regions needed to screenshot
    bossClockRegion = {"mon": 1, "top": bossClockTL[1], "left": bossClockTL[0], "width": bossClockW, "height": bossClockH}
    shopRegion = {"mon": 1, "top": shopTL[1], "left": shopTL[0], "width": shopW, "height": shopH}

    # Taking the Original screenshot
    sctBossClockOG = Image.fromarray(np.array(sct.grab(bossClockRegion)))
    sctShopOG = Image.fromarray(np.array(sct.grab(shopRegion)))

    # Setting up inital variables
    curClicks = 0
    cycleClickAmount = 200
    bossGrindSetback = cycleClickAmount * -5
    otherMapDist = 100
    timer = 0
    bossLvl = False

    # Keep playing until you press the Q key
    while win32api.GetAsyncKeyState(ord('Q')) == 0:

        # Click
        pydirectinput.click()

        # If the current click is over the Cycle amount
        if curClicks > cycleClickAmount:

            # Take a screenshot of the shop region
            sctImg = Image.fromarray(np.array(sct.grab(shopRegion)))

            # Compare screenshot against the OG version (For scrolling down)
            if pyautogui.locate(sctImg, sctShopOG, grayscale=True, confidence=.8) == None:
                # scroll down for .5 secs
                pydirectinput.moveTo(*scrollDown)
                pydirectinput.mouseDown()
                time.sleep(.5)
                pydirectinput.mouseUp()

            # Click hire/lvl up button 3
            pydirectinput.moveTo(*hireCenter3)
            pydirectinput.click()

            # Click hire/lvl up button 2
            pydirectinput.moveTo(*hireCenter2)
            pydirectinput.click()

            # Click hire/lvl up button 1
            pydirectinput.moveTo(*hireCenter1)
            pydirectinput.click()

            # Click on the next level
            pydirectinput.moveTo(mapX + otherMapDist, mapY)
            pydirectinput.click()

            # If boss lvl is active
            if bossLvl:

                # fight the boss for 30 secs
                if (time.time() - timer) >= 30:

                    # Screenshot the boss clock area
                    sctImg = Image.fromarray(np.array(sct.grab(bossClockRegion)))

                    # If boss clock is still there
                    if pyautogui.locate(sctImg, sctBossClockOG, grayscale=True, confidence=.4) != None:
                        # Go to previous level
                        pydirectinput.moveTo(mapX - otherMapDist, mapY)
                        pydirectinput.click()
                        curClicks = bossGrindSetback

                    # Turn off boss lvl
                    bossLvl = False

            # If boss lvl is not active
            else:
                # Screenshot boss clock area
                sctImg = Image.fromarray(np.array(sct.grab(bossClockRegion)))

                # If boss clock is there
                if pyautogui.locate(sctImg, sctBossClockOG, grayscale=True, confidence=.4) != None:
                    # Start tracking boss lvl
                    bossLvl = True
                    timer = time.time()

            # reset click tracking and move to the click center
            curClicks = 0
            pydirectinput.moveTo(*clickCenter)

        # Add click to the tracker
        curClicks += 1


# Runs the main function
if __name__ == '__main__':
    main()
