import cv2
import numpy as np
import time

print("Starting camera...")
cap = cv2.VideoCapture(0)

time.sleep(3)
print("Capturing background... Please stay out of the frame")

# Capture background
for i in range(60):
    ret, background = cap.read()

background = np.flip(background, axis=1)

print("Background captured! You can enter the frame with a red cloth.")

while cap.isOpened():

    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Red color detection
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    # Remove noise
    mask = cv2.medianBlur(mask,5)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask = cv2.dilate(mask, np.ones((3,3),np.uint8))

    mask_inv = cv2.bitwise_not(mask)

    # Replace cloak with background
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(img, img, mask=mask_inv)

    final_output = cv2.addWeighted(res1,1,res2,1,0)

    cv2.imshow("Invisible Cloak", final_output)

    # Press ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
