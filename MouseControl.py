import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui
import time

# Configuration constants
WCAM, HCAM = 640, 480
SMOOTHENING = 10
CLICK_COOLDOWN = 0.3  # seconds

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

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Hand detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector.results = detector.hands.process(frame_rgb)
        landmarks = detector.findPosition(frame, draw=True)

        if landmarks and len(landmarks) >= 21:
            # Get finger positions
            x1, y1 = landmarks[8][1], landmarks[8][2]   # Index tip
            x2, y2 = landmarks[12][1], landmarks[12][2] # Middle tip

            # Map coordinates to screen
            x3 = np.interp(x1, (0, WCAM), (0, screen_w))
            y3 = np.interp(y1, (0, HCAM), (0, screen_h))

            # Smooth movement
            clocX = plocX + (x3 - plocX) / SMOOTHENING
            clocY = plocY + (y3 - plocY) / SMOOTHENING

            # Update mouse position
            pyautogui.moveTo(int(screen_w - clocX), int(clocY))
            plocX, plocY = clocX, clocY

            # Visual feedback for index finger tip
            cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            # Click detection
            if np.hypot(x2 - x1, y2 - y1) < 40 and (time.time() - last_click_time) > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = time.time()
                # Visual click feedback
                cv2.circle(frame, ((x1 + x2) // 2, (y1 + y2) // 2), 15, (0, 255, 0), cv2.FILLED)

        cv2.imshow("Hand Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
