import cv2
import numpy as np
import HandTracking as htm
import time
import autopy
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
frameR = 100 #Frame Reduction
smoothening = 8

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1, detectionCon=0.7)
wScr, hScr = autopy.screen.size()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]


vol = 0
volBar = 400
volPer = 0

while True:
    #1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    if len(lmlist)!=0:
        #print(x1, y1, x2, y2)

        #3.Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        if fingers[1]==1 and fingers[0]==1:
            while fingers[4]!=1:
                # 1. Find hand Landmarks
                success, img = cap.read()
                img = detector.findHands(img)
                lmlist, bbox = detector.findPosition(img)

                # 2. Get the tip of the index and middle finger
                if len(lmlist) != 0:
                    x1, y1 = lmlist[8][1:]
                    x2, y2 = lmlist[12][1:]

                    # print(x1, y1, x2, y2)

                    # 3.Check which fingers are up
                    fingers = detector.fingersUp()
                    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                    # print(fingers)

                    # 4. Only Index Finger: Moving Mode
                    if fingers[1] == 1 and fingers[2] == 0:
                        # 5. Convert Co-ordinates

                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                        # 6. Smoothen Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
                        # 7. Move Mouse
                        autopy.mouse.move(wScr - clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY

                    # 8. Both Index and Middele Fingers are up: Clicking Mode
                    if fingers[1] == 1 and fingers[2] == 1:
                        # 9. Find Distance between Fingers
                        length, img, lineInfo = detector.findDistance(8, 12, img)
                        print(length)
                        # 10. Click mouse if distance is short
                        if length < 40:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()

                # 11. Frame Rate
                cTime = time.time()
                try:
                    fps = 1 / (cTime - pTime)
                except:
                    continue
                pTime = cTime
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                # 12. Display
                cv2.imshow("Image", img)
                cv2.waitKey(1)
        if fingers[3] == 1:
            while (fingers[4]!=1):
                fingers = detector.fingersUp()
                success, img = cap.read()
                img = detector.findHands(img)
                lmlist, _ = detector.findPosition(img, draw=False)
                if len(lmlist) != 0:
                    x1, y1 = lmlist[4][1], lmlist[4][2]
                    x2, y2 = lmlist[8][1], lmlist[8][2]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)
                    # print(length)

                    # Hand Range 30-200
                    # Volume Range -65 - 0

                    vol = np.interp(length, [30, 200], [minVol, maxVol])
                    volBar = np.interp(length, [30, 200], [400, 150])
                    volPer = np.interp(length, [30, 200], [0, 100])
                    #print(int(length), vol)
                    volume.SetMasterVolumeLevel(vol, None)

                    if length < 50:
                        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

                cTime = time.time()
                try:
                    fps = 1 / (cTime - pTime)
                except:
                    continue
                pTime = cTime
                cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

                cv2.imshow("Image", img)
                cv2.waitKey(1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)