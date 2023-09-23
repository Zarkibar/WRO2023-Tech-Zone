import serial_comm
import utils
import threading
import cv2
import numpy as np
from PIL import Image
from time import sleep


def camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow, upper_yellow = utils.get_limits('yellow')
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        edges = cv2.Canny(mask, 75, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 5)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', edges)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def serial_communication():
    serial_comm.setup(3)
    while True:
        sleep(0.2)
        recved_data = serial_comm.recv_data()
        print(recved_data)


if __name__ == "__main__":
    # serial_thread = threading.Thread(target=serial_communication)
    camera_thread = threading.Thread(target=camera)
    camera_thread.start()