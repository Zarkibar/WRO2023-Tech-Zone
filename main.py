import utils
import cv2
from PIL import Image
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import Motor

MAX_WALL_DISTANCE = 15
MAX_FRONT_WALL_DISTANCE = 10
MAX_SIDE_WALL_DISTANCE = 5
SERVO_DEFAULT_ROTATION = 7
SERVO_MAX_ROTATION = 8.4
SERVO_MIN_ROTATION = 5.4
MOTOR_SPEED = 0.6

SERVO_PIN = 18
SERVO_PWM_HERTZ = 50
MOTOR_FORWARD_PIN = 17
MOTOR_BACKWARD_PIN = 27
MOTOR_ENABLE_PIN = 22
# set GPIO Pins
SONAR_TRIGGER1 = 23
SONAR_ECHO1 = 24
SONAR_TRIGGER2 = 19
SONAR_ECHO2 = 26
SONAR_TRIGGER3 = 6
SONAR_ECHO3 = 13

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, SERVO_PWM_HERTZ)
motor = Motor(forward=MOTOR_FORWARD_PIN, backward=MOTOR_BACKWARD_PIN, enable=MOTOR_ENABLE_PIN)

# set GPIO direction (IN / OUT)
GPIO.setup(SONAR_TRIGGER1, GPIO.OUT)
GPIO.setup(SONAR_ECHO1, GPIO.IN)
GPIO.setup(SONAR_TRIGGER2, GPIO.OUT)
GPIO.setup(SONAR_ECHO2, GPIO.IN)
GPIO.setup(SONAR_TRIGGER3, GPIO.OUT)
GPIO.setup(SONAR_ECHO3, GPIO.IN)

if __name__ == '__main__':
    servo_pwm.start(0)
    servo_pwm.ChangeDutyCycle(SERVO_DEFAULT_ROTATION)
    cap = cv2.VideoCapture(0)

    sleep(3)
    motor.forward(MOTOR_SPEED)

    try:
        while True:
            sleep(0.1)
            ret, frame = cap.read()
            frame = cv2.resize(frame, (400, 300))

            hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # For detecting Red
            red_lower_limit, red_upper_limit = utils.get_limits(color='red')
            red_mask = cv2.inRange(hsvImage, red_lower_limit, red_upper_limit)

            red_mask_ = Image.fromarray(red_mask)
            red_bbox = red_mask_.getbbox()
            if red_bbox is not None:
                isRedInView = True
                x1, y1, x2, y2 = red_bbox
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
            else:
                isRedInView = False

            # For detecting Green
            green_lower_limit, green_upper_limit = utils.get_limits(color='green')
            green_mask = cv2.inRange(hsvImage, green_lower_limit, green_upper_limit)

            green_mask_ = Image.fromarray(green_mask)
            green_bbox = green_mask_.getbbox()
            if green_bbox is not None:
                isGreenInView = True
                x1, y1, x2, y2 = green_bbox
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            else:
                isGreenInView = False

            cv2.imshow('frame', frame)

            # MOVEMENT
            if isGreenInView:
                servo_pwm.ChangeDutyCycle(SERVO_MAX_ROTATION)
                sleep(0.5)
            elif isRedInView:
                servo_pwm.ChangeDutyCycle(SERVO_MIN_ROTATION)
                sleep(0.5)

            distance_left, distance_right, distance_front = utils.get_sonar_distance(SONAR_TRIGGER1, SONAR_ECHO1, SONAR_TRIGGER2, SONAR_ECHO2, SONAR_TRIGGER3, SONAR_ECHO3)
            print(f"Distance1: {distance_left}\ndistance2:{distance_right}\ndistance3:{distance_front}")
            if distance_front <= MAX_FRONT_WALL_DISTANCE:
                motor.stop()
                motor.backward(0.4)
                servo_pwm.ChangeDutyCycle(SERVO_MAX_ROTATION)
                sleep(1)
                motor.forward(MOTOR_SPEED)
            elif distance_left <= MAX_SIDE_WALL_DISTANCE:
                motor.stop()
                motor.backward(0.4)
                servo_pwm.ChangeDutyCycle(SERVO_MIN_ROTATION)
                sleep(1)
                motor.forward(MOTOR_SPEED)
            elif distance_right <= MAX_SIDE_WALL_DISTANCE:
                motor.stop()
                motor.backward(0.4)
                servo_pwm.ChangeDutyCycle(SERVO_MAX_ROTATION)
                sleep(1)
                motor.forward(MOTOR_SPEED)

            if distance_left <= MAX_WALL_DISTANCE:
                servo_pwm.ChangeDutyCycle(SERVO_MAX_ROTATION)
            elif distance_right <= MAX_WALL_DISTANCE:
                servo_pwm.ChangeDutyCycle(SERVO_MIN_ROTATION)
            else:
                servo_pwm.ChangeDutyCycle(SERVO_DEFAULT_ROTATION)

    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except:
        print("Error Occurred")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        motor.stop()
        servo_pwm.stop()
        GPIO.cleanup()
