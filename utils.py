from time import sleep, time

import cv2
import numpy as np


def get_limits(color):
    if color == 'red':
        bgr_color = np.uint8([[[0, 0, 255]]])
    elif color == 'green':
        bgr_color = np.uint8([[[0, 255, 0]]])
    elif color == 'blue':
        bgr_color = np.uint8([[[255, 0, 0]]])
    elif color == 'yellow':
        bgr_color = np.uint8([[[255, 255, 0]]])
    elif color == 'black':
        bgr_color = np.uint8([[[0, 0, 0]]])
    else:
        print("COLOR " + color + " NOT RECOGNIZABLE")
        bgr_color = np.uint8([[[0, 0, 0]]])

    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    lower_limit = np.uint8([[[(hsv_color[0, 0, 0] - 10), 100, 100]]])
    upper_limit = np.uint8([[[(hsv_color[0, 0, 0] + 10), 255, 255]]])

    return lower_limit, upper_limit


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
