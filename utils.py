import RPi.GPIO as GPIO
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

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def get_sonar_distance(sonar_trigger1, sonar_echo1, sonar_trigger2, sonar_echo2, sonar_trigger3, sonar_echo3):
    # SERVO 1
    # set Trigger to HIGH
    GPIO.output(sonar_trigger1, True)

    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(sonar_trigger1, False)

    StartTime1 = time()
    StopTime1 = time()

    # save StartTime
    while GPIO.input(sonar_echo1) == 0:
        StartTime1 = time()

    # save time of arrival
    while GPIO.input(sonar_echo1) == 1:
        StopTime1 = time()

    # time difference between start and arrival
    TimeElapsed1 = StopTime1 - StartTime1
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_left = (TimeElapsed1 * 34300) / 2

    # SERVO 2
    # set Trigger to HIGH
    GPIO.output(sonar_trigger2, True)

    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(sonar_trigger2, False)

    StartTime2 = time()
    StopTime2 = time()

    # save StartTime
    while GPIO.input(sonar_echo2) == 0:
        StartTime2 = time()

    # save time of arrival
    while GPIO.input(sonar_echo2) == 1:
        StopTime2 = time()

    # time difference between start and arrival
    TimeElapsed2 = StopTime2 - StartTime2
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_right = (TimeElapsed2 * 34300) / 2

    # SERVO 3
    # set Trigger to HIGH
    GPIO.output(sonar_trigger3, True)

    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    GPIO.output(sonar_trigger3, False)

    StartTime3 = time()
    StopTime3 = time()

    # save StartTime
    while GPIO.input(sonar_echo3) == 0:
        StartTime3 = time()

    # save time of arrival
    while GPIO.input(sonar_echo3) == 1:
        StopTime3 = time()

    # time difference between start and arrival
    TimeElapsed3 = StopTime3 - StartTime3
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_front = (TimeElapsed3 * 34300) / 2

    return distance_left, distance_right, distance_front
