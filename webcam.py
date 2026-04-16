import cv2
import numpy as np
import time
import random

# --- SETTINGS ---
width, height = 320, 240
deadZone = 40 

# State Machine Constants
SEARCHING = "SEARCHING"
LOCKED_ON = "LOCKED_ON"
CLIMBING = "CLIMBING"

# --- INIT WEBCAM ---
cap = cv2.VideoCapture(1)

# --- TRACKBARS FOR CALIBRATION ---
def empty(a): pass
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",10,179,empty)
cv2.createTrackbar("SAT Min","HSV",120,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VALUE Min","HSV",70,255,empty)
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

# --- BEHAVIOR VARIABLES ---
current_state = SEARCHING
side_choice = random.choice(["LEFT", "RIGHT"])
last_flip_time = time.time()

def get_target_contour(img_dilated, current_side):
    contours, _ = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    best_cnt = None
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000: 
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                if cy < (height // 2):
                    if current_side == "LEFT" and cx < (width // 2):
                        best_cnt = cnt
                        break
                    elif current_side == "RIGHT" and cx > (width // 2):
                        best_cnt = cnt
                        break
    return best_cnt

while True:
    # 1. GET FRAME FROM WEBCAM
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (width, height))
    imgContour = img.copy()

    # 2. IMAGE PROCESSING
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHsv, lower, upper)

    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(mask, kernel, iterations=1)

    # 3. STATE MACHINE (VISUAL ONLY, NO MOVEMENT)
    if current_state == SEARCHING:
        cv2.putText(imgContour, f"SEARCHING {side_choice}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

        target = get_target_contour(imgDil, side_choice)

        if target is not None:
            current_state = LOCKED_ON
        else:
            if time.time() - last_flip_time > 2.0:
                side_choice = random.choice(["LEFT", "RIGHT"])
                last_flip_time = time.time()

    elif current_state == LOCKED_ON:
        target = get_target_contour(imgDil, side_choice)

        if target is not None:
            x, y, w, h = cv2.boundingRect(target)
            cx, cy = x + (w // 2), y + (h // 2)

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)

            error_x = cx - (width // 2)
            error_y = (height // 2) - cy 

            if abs(error_x) < deadZone and abs(error_y) < deadZone:
                current_state = CLIMBING
                climb_start_time = time.time()
        else:
            current_state = SEARCHING

    elif current_state == CLIMBING:
        cv2.putText(imgContour, "CLIMBING (SIMULATED)", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if time.time() - climb_start_time > 2.0:
            side_choice = random.choice(["LEFT", "RIGHT"])
            current_state = SEARCHING

    # 4. UI OVERLAY
    cv2.rectangle(imgContour,
                  (width//2-deadZone, height//2-deadZone),
                  (width//2+deadZone, height//2+deadZone),
                  (255, 255, 0), 1)

    cv2.imshow("Webcam Feed", imgContour)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()