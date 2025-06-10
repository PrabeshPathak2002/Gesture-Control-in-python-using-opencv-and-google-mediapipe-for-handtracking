import cv2
import HandTrackingModule as htm
import time
import numpy as np
import screen_brightness_control as sbc

wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wcam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hcam)
pTime = 0

detector = htm.HandTracking()

while True:

    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detector.results = detector.hands.process(imgRGB)

    lmlist = detector.findPosition(img, draw=True, landmark_ids=[4,8])

    brightness = 50  # Default brightness percentage

    if lmlist and len(lmlist) >= 2:
        # Get the coordinates of the thumb and index finger tips
        x1, y1 = lmlist[0][1], lmlist[0][2]  # Thumb tip
        x2, y2 = lmlist[1][1], lmlist[1][2]  # Index finger tip

        # Draw a line between the thumb and index finger tips
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (0, 255, 0), cv2.FILLED)

        # Calculate distance
        length = np.hypot(x2 - x1, y2 - y1)

        # Map the length to brightness percentage (0 to 100)
        brightness = int(np.interp(length, [30, 200], [0, 100]))

        # Set the device brightness
        try:
            sbc.set_brightness(brightness)
        except Exception as e:
            print(f"Could not set brightness: {e}")

        # Display the brightness level
        brightBar = np.interp(length, [30, 200], [400, 150])
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(brightBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Brightness: {brightness}%', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

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


