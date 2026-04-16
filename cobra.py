import Tello
import cv2
import time

# --- CONFIGURATION ---
cobra_speed = 80      # Intensity of the climb (0-100)
surge_duration = 1.2  # Seconds spent in the "climb" phase
repeat_count = 3      # Number of times to repeat the whole sequence

# --- INITIALIZE DRONE ---
drone = Tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon() # Required for keyboard input window

def check_emergency():
    """Checks for the '.' key to trigger an immediate landing."""
    # Capture frame to keep the window alive
    frame_read = drone.get_frame_read()
    img = frame_read.frame
    cv2.imshow("Cobra Monitor", cv2.resize(img, (320, 240)))
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('.'):
        print("!!! EMERGENCY ABORT DETECTED !!!")
        drone.send_rc_control(0, 0, 0, 0)
        drone.land()
        return True
    return False

def sleep_with_check(seconds):
    """Replacement for time.sleep that stays alert for the stop button."""
    start_time = time.time()
    while time.time() - start_time < seconds:
        if check_emergency():
            return True
        time.sleep(0.05)
    return False

def perform_cobra():
    print("Executing Cobra Maneuver...")
    # 1. Forward Surge
    drone.send_rc_control(0, 40, 0, 0)
    if sleep_with_check(1): return True
    
    # 2. The Pull Up (The Cobra)
    drone.send_rc_control(0, cobra_speed, cobra_speed, 0)
    if sleep_with_check(surge_duration): return True
    
    # 3. The Stall/Level Out
    drone.send_rc_control(0, 0, 0, 0)
    if sleep_with_check(1): return True
    return False

try:
    drone.takeoff()
    if sleep_with_check(2): raise Exception("Abort during takeoff")

    for i in range(repeat_count):
        print(f"Sequence {i+1} of {repeat_count}")
        
        # Perform maneuver
        if perform_cobra(): break
        
        # Wait 3-4 seconds
        if sleep_with_check(3): break
        
        # 4. Flip and Reverse
        print("Flipping and Reversing Direction...")
        drone.flip("b") 
        if sleep_with_check(1): break
        
        drone.rotate_clockwise(180)
        if sleep_with_check(1): break

    print("Mission Complete or Aborted. Landing...")
    drone.land()

except Exception as e:
    print(f"Error encountered: {e}")
    drone.land()

finally:
    cv2.destroyAllWindows()