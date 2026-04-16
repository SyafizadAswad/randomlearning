import cv2
import numpy as np

# Init cam
cap = cv2.VideoCapture(1)

# 0 = normal view, 1 = mask view
view_mode = 0

def get_display_frame(frame, mask, mode):
    if mode == 0:
        return frame
    elif mode == 1:
        # convert mask to 3-channel so it can be displayed like a normal frame
        return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # Convert to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red ranges
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    lower_pink = np.array([140, 70, 80])
    upper_pink = np.array([170, 255, 255])

    # Create masks (combine both ranges for better red detection)
    mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)
    mask2 = cv2.inRange(hsv_frame, lower_pink, upper_pink)
    mask = mask1 + mask2

    # Morphology
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    red_objects_counts = 0

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            red_objects_counts += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Red Object", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # UI
    text = f"Red Objects: {red_objects_counts}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2

    cv2.rectangle(frame, (width - 250, height - 50), (width, height), (0, 0, 0), cv2.FILLED)

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = width - text_w - 20
    text_y = height - 20

    cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

    # Get display frame depending on mode
    display_frame = get_display_frame(frame, mask, view_mode)

    cv2.imshow("Red color tracking", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('m'):
        view_mode = 1 - view_mode  # toggle between 0 and 1

cap.release()
cv2.destroyAllWindows()