import Tello
import cv2
import time
import math

# --- CONFIGURATION ---
duration = 10.0       # How long to fly the helix (seconds)
frequency = 1.5       # Speed of the rotation (higher = faster spinning)
amplitude = 35        # Width of the spiral (0-100)
climb_speed = 20      # Constant upward velocity
start_test = 1        # 0 for Flight, 1 for Testing (no takeoff)

# --- INITIALIZE DRONE ---
drone = Tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()

def perform_helix(is_drone_two=False):
    """
    Performs a spiral climb.
    is_drone_two: If True, it starts 180 degrees out of phase to create the 'double' helix.
    """
    start_time = time.time()
    # Offset by Pi (180 degrees) for the second drone to create the "cross" effect
    phase_offset = math.pi if is_drone_two else 0
    
    print(f"Starting Helix Movement. Drone 2 Mode: {is_drone_two}")
    print("PRESS '.' TO EMERGENCY LAND")
    
    while time.time() - start_time < duration:
        t = time.time() - start_time
        
        # --- THE HELIX MATH ---
        # Left/Right (X) and Forward/Back (Y) use Sine/Cosine to move in a circle
        lr = int(amplitude * math.cos(frequency * t + phase_offset))
        fb = int(amplitude * math.sin(frequency * t + phase_offset))
        
        # Vertical (Z) stays constant for a steady climb
        ud = climb_speed
        
        # Send velocities to the drone
        drone.send_rc_control(lr, fb, ud, 0)
        
        # --- EMERGENCY STOP CHECK ---
        # We must read the frame and waitKey to capture the keyboard input
        frame_read = drone.get_frame_read()
        img = frame_read.frame
        cv2.imshow("Helix Monitor", cv2.resize(img, (320, 240)))
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('.'):
            print("EMERGENCY ABORT DETECTED!")
            drone.send_rc_control(0, 0, 0, 0)
            drone.land()
            return False # Signal that we aborted
            
        time.sleep(0.05)
    
    return True # Signal completion

# --- MAIN EXECUTION ---
try:
    if start_test == 0:
        drone.takeoff()
        time.sleep(2)
    
    # Run the helix (change to True for the second drone)
    completed = perform_helix(is_drone_two=False)
    
    if completed:
        print("Helix complete. Hovering...")
        drone.send_rc_control(0, 0, 0, 0)
        time.sleep(2)
        drone.land()

except Exception as e:
    print(f"Error: {e}")
    drone.send_rc_control(0, 0, 0, 0)
    drone.land()

finally:
    cv2.destroyAllWindows()

"""
How to Synchronize Two DronesTo get that perfect DNA look where the drones "cross" each other:
Drone 1 (is_drone_two=False): Starts at the $0$ position of the circle.
Drone 2 (is_drone_two=True): Starts at the $\pi$ (180°) position.
The Result: When Drone 1 moves Right, Drone 2 moves Left. 
When Drone 1 moves Forward, Drone 2 moves Backward. 
They will stay perfectly opposite each other as they climb.

Tips for the HelixSpace Requirement: This creates a circular "tube" of movement. 
Ensure you have about 2 meters of horizontal clearance in all directions.
Spinning vs. Moving: Notice I kept yaw = 0. 
This means the drone's "nose" always points the same way while it slides in a circle. 
This is much more stable than trying to rotate the drone while spiraling.
Smoothness: If the circle looks more like a square, increase the time.sleep(0.05) frequency (make the number smaller) to send updates faster.
"""