import pydirectinput
import pyautogui
import time
import mss
import operator
from PIL import Image
import numpy as np

def main():
    print("Collecting Click Center")
    input()
    clickCenter = pydirectinput.position()

    print("Collecting Map Center")
    input()
    mapCenter = pydirectinput.position()
    mapX, mapY = mapCenter

    print("Collecting Hire Center")
    input()
    hireCenter = pydirectinput.position()

    print("Collecting Scroll Down")
    input()
    scrollDown = pydirectinput.position()

    print("Collecting Death Numbers Top Left Corner")
    input()
    deathNumStart = pydirectinput.position()

    print("Collecting Death Numbers Bottom Right Corner")
    input()
    deathNumEnd = pydirectinput.position()

    deathW, deathH = tuple(map(operator.sub, deathNumEnd, deathNumStart))

    print(deathW, deathH)

    # Starting screenshotting object
    sct = mss.mss()
    mssRegion = {"mon": 1, "top": deathNumStart[1], "left": deathNumStart[0], "width": deathW, "height": deathH}
    sctImgOG = Image.fromarray(np.array(sct.grab(mssRegion)))


    clCentX, clCentY = clickCenter

    moveModifier = 8
    clBox = 8 * moveModifier
    clCentX, clCentY = clCentX - clBox, clCentY - clBox


    clBoxCur = 0
    lvlUpgrade = 10
    lvlTracker = 0
    timer = 0
    bossLvl = False
    while True:
        pydirectinput.click()

        if clBoxCur > 1000:
            pydirectinput.moveTo(*hireCenter)
            pydirectinput.click()

            pydirectinput.moveTo(mapX + 100, mapY)
            pydirectinput.click()

            clBoxCur = 0
            lvlTracker += 1

            if bossLvl:
                if (time.time() - timer) >= 30:
                    sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
                    if pyautogui.locate(sctImg, sctImgOG, grayscale=True, confidence=.4) == None:
                        pydirectinput.moveTo(mapX - 100, mapY)
                        pydirectinput.click()
                        clBoxCur = -10000

                    bossLvl = False

            else:
                sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
                if pyautogui.locate(sctImg, sctImgOG, grayscale=True, confidence=.4) == None:
                    bossLvl = True
                    timer = time.time()

            pydirectinput.moveTo(*clickCenter)
            time.sleep(2)


        # if lvlTracker == lvlUpgrade:
        #     pydirectinput.moveTo(mapX + 100, mapY)
        #     pydirectinput.click()

        clBoxCur += moveModifier


# Runs the main function
if __name__ == '__main__':
    main()
