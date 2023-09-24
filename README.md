# WRO2023 Tech Zone
 This is the official repository of the team "Tech Zone" for World Robot Olympiad 2023 Panama in the Future Engineer category. At this repository you can see all of our Codes, Components that were used, Team Photo, Robot's Photos etc.

## File Description
We have used two microcontrollers in our robot. 
- An Arduino Uno for controlling the hardware like Motors, Ultrasonic Sensors, Servos etc 
- A Rapberry Pi 3B for Image Processing and other internal processings. 

Raspberry Pi and Arduino will be communication with Serial Communication. Raspberry Pi has four files:

- ``main.py``
- ``serial_comm.py``
- ``utils.py``
- ``image_processing.py``

## main.py

This is the main script for Raspberry Pi. This file will always listen for a push button press. The button is in the top of the Raspberry Pi which will start the main code.


## serial_comm.py

This file contains code for communicating between Arduino and Raspberry Pi. It has the functions needed for Serial Communications like sending or receiving data. `main.py` will use this class for receiving and sending data from Raspberry to Arduino. 


## image_processing.py

This script holds many necessary functions for other scripts like the HSV Range of many colors that `main.py` or `image_processing.py` need to detect.


## utils.py

This script contains code for Image Processing functions that will be used by `main.py`. This script includes functions like Line Detection and Distance Estimation.