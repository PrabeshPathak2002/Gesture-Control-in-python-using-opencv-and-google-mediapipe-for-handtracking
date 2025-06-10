import cv2
import HandTrackingModule as htm
import time
import pyautogui
import numpy as np

wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wcam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hcam)
pTime = 0

detector = htm.HandTracking()

last_action_time = 0
action_delay = 1  # seconds

def fingers_up(lmlist):
    # Returns a list of 1 (up) or 0 (down) for each finger
    tips = [4, 8, 12, 16, 20]
    fingers = []
    if lmlist and len(lmlist) == 21:
        # Thumb: check x for right hand
        fingers.append(1 if lmlist[4][1] > lmlist[3][1] else 0)
        # Other fingers: tip y < pip y means finger is up
        for tip in tips[1:]:
            fingers.append(1 if lmlist[tip][2] < lmlist[tip-2][2] else 0)
    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detector.results = detector.hands.process(imgRGB)

    lmlist = detector.findPosition(img, draw=True)

    current_time = time.time()
    if lmlist and len(lmlist) == 21:
        fingers = fingers_up(lmlist)
        totalFingers = sum(fingers)
        if totalFingers == 5 and current_time - last_action_time > action_delay:
            pyautogui.press('playpause')
            last_action_time = current_time
            cv2.putText(img, "Play/Pause", (400, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
        elif totalFingers == 0 and current_time - last_action_time > action_delay:
            pyautogui.press('playpause')
            last_action_time = current_time
            cv2.putText(img, "Play/Pause", (400, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
detector.release()
