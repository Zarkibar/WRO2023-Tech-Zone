import utils
import cv2
import numpy as np


def line_detection(frame, color):
    frame_gaussed = cv2.GaussianBlur(frame, (1, 1), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(frame_gaussed, cv2.COLOR_BGR2HSV)

    lower_yellow, upper_yellow = utils.get_limits(color)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            frame = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return frame


# UNCOMPLETED
def distance_estimation(frame, known_width, focal_length):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([160, 100, 100])
    upper_red = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([75, 255, 255])
    mask3 = cv2.inRange(hsv, lower_green, upper_green)

    # Combine the masks
    mask = mask1 + mask2

    # Apply morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    mask3 = cv2.morphologyEx(mask3, cv2.MORPH_OPEN, kernel1)
    # Find contours of the red objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c, j = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            distance = (known_width * focal_length) / w
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    for contour in c:
        a = cv2.contourArea(contour)
        if a > 100:
            x, y, w, h = cv2.boundingRect(contour)
        dis = (known_width * focal_length) / w
        # print(w)

    return distance
