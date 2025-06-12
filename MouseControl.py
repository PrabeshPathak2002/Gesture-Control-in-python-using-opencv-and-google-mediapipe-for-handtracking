import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui
import time

# Configuration constants
WCAM, HCAM = 640, 480
SMOOTHENING = 10
CLICK_COOLDOWN = 0.3  # seconds
FRAME_R = 100  # Frame reduction for active region

def fingers_up(landmarks):
    """
    Returns a list indicating which fingers are up.
    [Thumb, Index, Middle, Ring, Pinky]
    """
    fingers = []
    # Thumb: compare tip and IP joint in x direction (for right hand)
    fingers.append(landmarks[4][1] > landmarks[3][1])
    # Fingers: compare tip and PIP joint in y direction
    for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
        fingers.append(landmarks[tip][2] < landmarks[pip][2])
    return fingers

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, WCAM)
    cap.set(4, HCAM)

    # Initialize hand detector
    detector = htm.HandTracking(max_num_hands=1)
    screen_w, screen_h = pyautogui.size()
    
    # Tracking variables
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    last_click_time = 0

    pTime = 0  # For FPS calculation

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Draw active region rectangle
        cv2.rectangle(frame, (FRAME_R, FRAME_R), (WCAM - FRAME_R, HCAM - FRAME_R), (255, 0, 255), 2)

        # Hand detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector.results = detector.hands.process(frame_rgb)
        landmarks = detector.findPosition(frame, draw=True)

        if landmarks and len(landmarks) >= 21:
            # Get finger positions
            x1, y1 = landmarks[8][1], landmarks[8][2]   # Index tip
            x2, y2 = landmarks[12][1], landmarks[12][2] # Middle tip

            # Detect which fingers are up
            fingers = fingers_up(landmarks)

            # Only move mouse if index finger is up and middle finger is down
            if fingers[1] and not fingers[2]:
                # Map coordinates to screen within reduced frame
                x3 = np.interp(x1, (FRAME_R, WCAM - FRAME_R), (0, screen_w))
                y3 = np.interp(y1, (FRAME_R, HCAM - FRAME_R), (0, screen_h))

                # Smooth movement
                clocX = plocX + (x3 - plocX) / SMOOTHENING
                clocY = plocY + (y3 - plocY) / SMOOTHENING

                # Update mouse position
                pyautogui.moveTo(int(screen_w - clocX), int(clocY))
                plocX, plocY = clocX, clocY

                # Visual feedback for index finger tip
                cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            # Click detection: both index and middle fingers up and close together
            if fingers[1] and fingers[2]:
                if np.hypot(x2 - x1, y2 - y1) < 40 and (time.time() - last_click_time) > CLICK_COOLDOWN:
                    pyautogui.click()
                    last_click_time = time.time()
                    # Visual click feedback
                    cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), 15, (0, 255, 0), cv2.FILLED)

        # FPS calculation and display
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow("Hand Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
