import Tello
import cv2
import numpy as np
import time
import random

# --- CONFIGURATION ---
width, height = 320, 240
deadZone = 45        # Increase this (e.g., to 60) if drone wobbles too much
speed_gain = 0.4     # Sensitivity: lower (0.2) is smoother, higher (0.6) is faster
startCounter = 1     # 0 for Flight, 1 for Testing (motor-off)

# State Machine Constants
SEARCHING = "SEARCHING"
LOCKED_ON = "LOCKED_ON"
CLIMBING = "CLIMBING"

# --- INITIALIZE DRONE ---
drone = Tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()

# --- TRACKBARS (HSV Calibration) ---
def empty(a): pass
cv2.namedWindow("HSV")
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",10,179,empty)
cv2.createTrackbar("SAT Min","HSV",120,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VALUE Min","HSV",70,255,empty)
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

# --- LOGIC VARIABLES ---
current_state = SEARCHING
side_choice = random.choice(["LEFT", "RIGHT"])
last_flip_time = time.time()
search_attempts = 0  
show_mask = False  

def get_nearest_target(img_dilated, current_side):
    """Finds the stone on the correct side/height closest to the center crosshair."""
    contours, _ = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    best_cnt = None
    min_dist = float('inf')
    cx_screen, cy_screen = width // 2, height // 2

    for cnt in contours:
        if cv2.contourArea(cnt) > 800: # Ignore noise
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx_obj = int(M["m10"] / M["m00"])
                cy_obj = int(M["m01"] / M["m00"])
                
                # Rule 1: Must be in the Top Half to ensure we climb UP
                if cy_obj < cy_screen:
                    # Rule 2: Must match the "Coin Flip" side
                    if (current_side == "LEFT" and cx_obj < cx_screen) or \
                       (current_side == "RIGHT" and cx_obj > cx_screen):
                        
                        # Rule 3: Must be the closest to center among all candidates
                        dist = np.sqrt((cx_obj - cx_screen)**2 + (cy_obj - cy_screen)**2)
                        if dist < min_dist:
                            min_dist = dist
                            best_cnt = cnt
    return best_cnt

while True:
    # 1. CAPTURE & RESIZE
    frame_read = drone.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    
    # 2. AUTO-TAKEOFF
    if startCounter == 0:
        drone.takeoff()
        drone.send_rc_control(0, 0, 30, 0) # Initial climb
        time.sleep(2)
        startCounter = 1

    # 3. COLOR FILTERING
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([cv2.getTrackbarPos("HUE Min","HSV"), 
                      cv2.getTrackbarPos("SAT Min","HSV"), 
                      cv2.getTrackbarPos("VALUE Min","HSV")])
    upper = np.array([cv2.getTrackbarPos("HUE Max","HSV"), 
                      cv2.getTrackbarPos("SAT Max","HSV"), 
                      cv2.getTrackbarPos("VALUE Max","HSV")])
    mask = cv2.inRange(imgHsv, lower, upper)
    imgDil = cv2.dilate(mask, np.ones((5, 5)), iterations=1)

    # 4. TOGGLE VIEW PREPARATION
    if show_mask:
        display_img = cv2.cvtColor(imgDil, cv2.COLOR_GRAY2BGR)
        view_label = "VIEW: MASK"
    else:
        display_img = img.copy()
        view_label = "VIEW: FEED"

    # 5. DRONE BRAIN (State Machine)
    lr, ud, fb, yaw = 0, 0, 0, 0

    if current_state == SEARCHING:
        target = get_nearest_target(imgDil, side_choice)
        if target is not None:
            current_state = LOCKED_ON
            search_attempts = 0 
        else:
            if time.time() - last_flip_time > 2.0: # Flip every 2 seconds
                side_choice = random.choice(["LEFT", "RIGHT"])
                last_flip_time = time.time()
                search_attempts += 1
        
        # FINISH LINE CHECK
        if search_attempts >= 8:
            print("Mission Complete: No more stones found.")
            drone.land()
            break

    elif current_state == LOCKED_ON:
        target = get_nearest_target(imgDil, side_choice)
        if target is not None:
            x, y, w, h = cv2.boundingRect(target)
            cx, cy = x + (w // 2), y + (h // 2)
            cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Distance from Center
            error_x = cx - (width // 2)
            error_y = (height // 2) - cy 

            # Move if outside Deadzone
            if abs(error_x) > deadZone:
                lr = int(np.clip(error_x * speed_gain, -30, 30))
            if abs(error_y) > deadZone:
                ud = int(np.clip(error_y * speed_gain, -30, 30))

            # REQUISITE REACHED
            if abs(error_x) < deadZone and abs(error_y) < deadZone:
                current_state = CLIMBING
                climb_start_time = time.time()
        else:
            current_state = SEARCHING # Target lost, go back to searching

    elif current_state == CLIMBING:
        ud = 18 # Simulate upward reach
        if time.time() - climb_start_time > 2.0:
            side_choice = random.choice(["LEFT", "RIGHT"])
            current_state = SEARCHING

    # 6. UI OVERLAYS
    # Deadzone Box
    cv2.rectangle(display_img, (width//2-deadZone, height//2-deadZone), 
                  (width//2+deadZone, height//2+deadZone), (255, 255, 0), 1)
    cv2.putText(display_img, f"STATE: {current_state}", (10, 20), 1, 1, (0, 255, 0), 1)
    cv2.putText(display_img, f"SIDE: {side_choice}", (10, 40), 1, 1, (255, 255, 0), 1)
    cv2.putText(display_img, view_label, (width - 100, 20), 1, 0.8, (0, 255, 255), 1)

    # 7. MOTOR CONTROL & COMMANDS
    drone.send_rc_control(lr, fb, ud, yaw)
    cv2.imshow("Tello Bouldering Pilot", display_img)

    # 8. KEYBOARD INPUTS
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        show_mask = not show_mask
    elif key == ord('.'): # EMERGENCY ABORT
        print("EMERGENCY LANDING!")
        drone.send_rc_control(0,0,0,0)
        drone.land()
        break
    elif key == ord('q'):
        drone.land()
        break

cv2.destroyAllWindows()