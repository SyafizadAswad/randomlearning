import Tello
import cv2
import numpy as np
import time
import math

# --- CONFIGURATION ---
duration = 5.0        # How long to perform the pendulum (seconds)
frequency = 2.0       # How fast it swings back and forth
amplitude_x = 40      # How wide the swing is (0-100)
amplitude_y = 20      # How deep the "arc" dip is (0-100)
forward_speed = 10    # Slow forward movement during the swing

# --- INITIALIZE DRONE ---
drone = Tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()

def perform_pendulum(reverse=False):
    """
    Performs an arc-shaped pendulum motion.
    To reverse the direction for a 2nd drone, we multiply the X-axis by -1.
    """
    direction_modifier = -1 if reverse else 1
    start_time = time.time()
    
    print(f"Starting Pendulum. Reverse: {reverse}")
    
    while time.time() - start_time < duration:
        # Calculate elapsed time
        t = time.time() - start_time
        
        # --- THE PENDULUM MATH ---
        # Horizontal swing: Back and forth
        # Multiply by direction_modifier to reverse start side (Left vs Right)
        lr = int(amplitude_x * math.sin(frequency * t) * direction_modifier)
        
        # Vertical arc: We use abs(cos) or cos(2t) to ensure it goes DOWN then UP 
        # for every single half-swing of the X axis.
        ud = int(-amplitude_y * abs(math.cos(frequency * t / 2)))
        
        # Forward creep
        fb = forward_speed
        
        # Send the combined vector to the drone
        drone.send_rc_control(lr, fb, ud, 0)
        
        # Small delay to prevent flooding the Tello with commands
        time.sleep(0.05)
        
        # Emergency abort during flight
        if cv2.waitKey(1) & 0xFF == ord('.'):
            break

    # Stop movement after duration
    drone.send_rc_control(0, 0, 0, 0)

# --- MAIN EXECUTION ---
try:
    drone.takeoff()
    time.sleep(2)
    
    # FOR 1ST DRONE: Set reverse=False
    # FOR 2ND DRONE: Set reverse=True to have them swing in opposite directions
    perform_pendulum(reverse=False) 
    
    print("Motion Complete. Hovering...")
    time.sleep(2)
    drone.land()

except Exception as e:
    print(f"Error: {e}")
    drone.send_rc_control(0, 0, 0, 0)
    drone.land()

finally:
    cv2.destroyAllWindows()