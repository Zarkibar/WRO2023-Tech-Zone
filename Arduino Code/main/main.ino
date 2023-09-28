#include <Servo.h>

Servo servo;

#define motor_in1 12
#define motor_in2 11
#define motor_speed_pin 10
int motor_speed = 255;

#define TRIGGER_PIN_LEFT 9
#define ECHO_PIN_LEFT 8
#define TRIGGER_PIN_RIGHT 5
#define ECHO_PIN_RIGHT 4

int duration_left;
int distance_left;
int duration_right;
int distance_right;

int BAUDRATE = 19200;
int SERVO_MIN_POS = 58;
int SERVO_MAX_POS = 108;
int SERVO_DEFAULT_POS = 78

void setup(){
  Serial.begin(BAUDRATE);
  servo.attach(A0);

  pinMode(TRIGGER_PIN_LEFT,OUTPUT);
  pinMode(ECHO_PIN_LEFT,INPUT);
  pinMode(TRIGGER_PIN_RIGHT,OUTPUT);
  pinMode(ECHO_PIN_RIGHT,INPUT);

  pinMode(motor_in1,OUTPUT);
  pinMode(motor_in2,OUTPUT);
  pinMode(motor_speed_pin,OUTPUT);
  analogWrite(motor_speed_pin, motor_speed);
  servo.write(78);
  delay(1000); 
  while (!Serial) {}
}

void loop()
{
  CalculateDistance();

  if (Serial.available() > 0){
    String message = Serial.readStringUntil('\n');

  if (message == "F"){
    digitalWrite(motor_in1, HIGH);
    digitalWrite(motor_in2, LOW);
  }
  else if (message == "B"){
    digitalWrite(motor_in1, HIGH);
    digitalWrite(motor_in2, LOW);
  }
  else if (message == "Sm"){
    digitalWrite(motor_in1, LOW);
    digitalWrite(motor_in2, LOW);
  }
   else if (message == "L"){
    servo.write(SERVO_MIN_POS);
  }
   else if (message == "R"){
    servo.write(SERVO_MAX_POS);
  }
  else if (message == "Ss"){
    servo.write(SERVO_DEFAULT_POS);
  }
 }
}

void CalculateDistance()
{
  digitalWrite(TRIGGER_PIN_LEFT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN_LEFT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN_LEFT, LOW);

  duration_left = pulseIn(ECHO_PIN_LEFT, HIGH);
  distance_left = duration_left/58.8;

  digitalWrite(TRIGGER_PIN_RIGHT, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN_RIGHT, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN_RIGHT, LOW);

  duration_right = pulseIn(ECHO_PIN_RIGHT, HIGH);
  distance_right = duration_right/58.8;

  Serial.print("Sl");
  Serial.println(distance_left);
  Serial.print("Sr");
  Serial.println(distance_right);

  delay(25);


}
