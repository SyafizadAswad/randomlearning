import Tello
import cv2
import numpy as np
import time
import random

# --- SETTINGS ---
width, height = 320, 240
deadZone = 40 
startCounter = 0 # 0 for Flight, 1 for Testing (no takeoff)

# State Machine Constants
SEARCHING = "SEARCHING"
LOCKED_ON = "LOCKED_ON"
CLIMBING = "CLIMBING"

# --- INITIALIZE DRONE ---
drone = Tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()

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

# Global variables for the behavior
current_state = SEARCHING
side_choice = random.choice(["LEFT", "RIGHT"])
last_flip_time = time.time()

def get_target_contour(img_dilated, current_side):
    """Filters contours to find a stone on the chosen side in the upper half of the view."""
    contours, _ = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    best_cnt = None
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000: 
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Priority: Look at stones in the TOP HALF to keep climbing up
                if cy < (height // 2):
                    if current_side == "LEFT" and cx < (width // 2):
                        best_cnt = cnt
                        break
                    elif current_side == "RIGHT" and cx > (width // 2):
                        best_cnt = cnt
                        break
    return best_cnt

while True:
    # 1. GET FRAME
    frame_read = drone.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    imgContour = img.copy()
    
    # 2. FLIGHT STARTUP
    if startCounter == 0:
        drone.takeoff()
        # Give it a bit of height to see the first stones
        drone.send_rc_control(0, 0, 30, 0)
        time.sleep(2)
        drone.send_rc_control(0, 0, 0, 0)
        startCounter = 1

    # 3. IMAGE PROCESSING
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
    
    # Clean up detection with dilation
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(mask, kernel, iterations=1)

    # 4. BEHAVIOR LOGIC
    lr, ud, fb, yaw = 0, 0, 0, 0

    if current_state == SEARCHING:
        cv2.putText(imgContour, f"SEARCHING {side_choice}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        target = get_target_contour(imgDil, side_choice)
        
        if target is not None:
            current_state = LOCKED_ON
        else:
            # Coin flip logic: if nothing found for 2 seconds, switch sides
            if time.time() - last_flip_time > 2.0:
                side_choice = random.choice(["LEFT", "RIGHT"])
                last_flip_time = time.time()

    elif current_state == LOCKED_ON:
        target = get_target_contour(imgDil, side_choice)
        if target is not None:
            x, y, w, h = cv2.boundingRect(target)
            cx, cy = x + (w // 2), y + (h // 2)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Error calculation relative to center
            error_x = cx - (width // 2)
            error_y = (height // 2) - cy 

            # Movement (Adjust 0.5 to change responsiveness)
            if abs(error_x) > deadZone:
                lr = int(np.clip(error_x * 0.5, -25, 25))
            if abs(error_y) > deadZone:
                ud = int(np.clip(error_y * 0.5, -25, 25))

            # If inside the center box, stone is "reached"
            if abs(error_x) < deadZone and abs(error_y) < deadZone:
                current_state = CLIMBING
                climb_start_time = time.time()
        else:
            current_state = SEARCHING 

    elif current_state == CLIMBING:
        cv2.putText(imgContour, "STAYING AT STONE", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Briefly move up to simulate reaching for the next hold
        ud = 15 
        if time.time() - climb_start_time > 2.0:
            side_choice = random.choice(["LEFT", "RIGHT"]) 
            current_state = SEARCHING

    # 5. EXECUTE MOVEMENT
    drone.send_rc_control(lr, fb, ud, yaw)

    # 6. UI OVERLAY
    # Draw the center deadzone box
    cv2.rectangle(imgContour, (width//2-deadZone, height//2-deadZone), 
                  (width//2+deadZone, height//2+deadZone), (255, 255, 0), 1)
    
    cv2.imshow("Drone Feed", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break

cv2.destroyAllWindows()