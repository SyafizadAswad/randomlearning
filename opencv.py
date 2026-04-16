import cv2
import numpy as np

#Init cam
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # get frame dimensions for positioning UI
    height, width, _ = frame.shape

    # 1. convert the frame from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. define range off red color in HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    lower_pink = np.array([140, 70, 80])
    upper_pink = np.array([170, 255, 255])

    # 3. create a mask (turns red pixels white and the rest black)
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # 1. Define a 'kernel' (a 5x5 square matrix)
    kernel = np.ones((5, 5), np.uint8)

    # 2. Remove small white noise (dots) from the background
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 3. Close the gaps between fragments of the actual object
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


    # 4. find the contours *outlines* of the white shape in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    red_objects_counts = 0

    for cnt in contours:
        # filter out ssmall noise by checking the area size
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            red_objects_counts += 1
            # draw a green rectangle around the detected red object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Red Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # -- UI section --
    text = (f"Red Objects: {red_objects_counts}")
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (255, 255, 255)
    bg_color = (0, 0, 0)
    
    # calculate tect size to position it perfetly at bottom right
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # coordinates for the text (with 20px padding from the edge)
    text_x = width - text_w - 20
    text_y = height - 20

    # put text on top
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

    #display the resulting frame
    cv2.imshow("Red color tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()