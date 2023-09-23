int BAUDRATE = 115200;

void setup()
{
  Serial.begin(BAUDRATE);
  while (!Serial) {}
}

void loop()
{
  if (Serial.available() > 0){
    String message = Serial.readStringUntil('\n');
    Serial.println(message);
  }
}