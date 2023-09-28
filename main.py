import serial_comm
import image_processing
import utils
import threading
import cv2
from time import sleep
from gpiozero import Button

on_button = Button(12)

SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 19200

MAX_WALL_DISTANCE = 90
TOLERANCE = 10


def camera():
    cap = cv2.VideoCapture(0)
    sleep(2)

    try:
        while True:
            sleep(0.001)
            ret, frame = cap.read()
            frame = cv2.resize(frame, (400, 300))
            frame = image_processing.line_detection(frame, 'yellow')

            lower_limit, upper_limit = utils.get_limits('green')
            mask = cv2.inRange(frame, lower_limit, upper_limit)

            cv2.imshow('frame', frame)
            cv2.imshow('mask', mask)

    except KeyboardInterrupt:
        print("Keyboard Interrupted")
        cap.release()
        cv2.destroyAllWindows()


def serial_communication():
    serial_comm.setup(SERIAL_PORT, BAUDRATE, 3)
    serial_comm.setDTR(True)
    global servo_state
    global distance_left, distance_right
    distance_left = 0
    distance_right = 0
    servo_state = 0

    serial_comm.send_data("F")

    while True:
        sleep(0.005)
        recved_data = serial_comm.recv_data()

        # Get and save the servo values
        if recved_data.startswith("Sl"):
            distance_left = int(recved_data[2:])
        elif recved_data.startswith("Sr"):
            distance_right = int(recved_data[2:])

        # Movement

        if (distance_left - distance_right) > TOLERANCE and servo_state != -1:
            serial_comm.send_data("L")
            servo_state = -1
        elif (distance_right - distance_left) > TOLERANCE and servo_state != 1:
            serial_comm.send_data("R")
            servo_state = 1
        elif (distance_left - distance_right) < TOLERANCE and (distance_right - distance_left) < TOLERANCE and servo_state != 0:
            serial_comm.send_data("Ss")
            servo_state = 0

        print("dl: " + str(distance_left) + "\ndr: " + str(distance_right))


if __name__ == "__main__":
    on_button.wait_for_active()

    serial_thread = threading.Thread(target=serial_communication)
    camera_thread = threading.Thread(target=camera)
    serial_thread.start()
    camera_thread.start()
