import serial
from time import sleep

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 9600


def setup(delay):
    global ser
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1.0)
    sleep(delay)
    ser.reset_input_buffer()
    return ser


def flush():
    ser.flush()


def flush_input():
    ser.flushInput()


def flush_output():
    ser.flushOutput()


def get_data():
    response = ''
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').rstrip()
    return response


def send_data(data):
    data = data + "\n"
    ser.write(data.encode('utf-8'))


def change_port(_port):
    ser.setPort(_port)


def change_baudrate(_baudrate):
    ser.baudrate = _baudrate


def close():
    ser.close()
