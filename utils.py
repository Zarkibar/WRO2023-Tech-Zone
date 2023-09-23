from time import sleep, time
import numpy as np


def get_limits(color):
    if color == 'red':
        lower_limit = [0, 200, 200]
        upper_limit = [6, 255, 255]
    elif color == 'green':
        lower_limit = [40, 100, 100]
        upper_limit = [80, 255, 255]
    elif color == 'blue':
        lower_limit = [81, 100, 100]
        upper_limit = [130, 255, 255]
    elif color == 'yellow':
        lower_limit = [18, 94, 140]
        upper_limit = [48, 255, 255]
    elif color == 'black':
        lower_limit = [30, 37, 0]
        upper_limit = [100, 255, 78]

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
