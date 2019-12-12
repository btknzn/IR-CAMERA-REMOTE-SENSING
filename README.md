# IR-CAMERA-REMOTE-SENSING
 Aim of this project to undestanding how many people in one room with Thermal Image Processing.I made one system which can detect %76 Percent(0 person, 1 person, 2 people and 3 people in room). Please read PDF(IR CAMERA DETECTİON REPORT AND SYSTEM DESCRİPTİON AND CODE DESCRİPTİON 6.pdf) to understand your project. You can also find 3D printer Design for camera and also electronic parts. 

 In our project, we selected Teensy 3.6 as an our Micro-controller because of its ARM cortex processer (32bit 180MHZ). It is fast and in our Project we are going to make a lot of mathematical calculation with big sized arrays. For this reason, Teensy 3.6 is perfect selection for us. 
 

Sparkfun Qwiic IR Array MLX90640 is selected as IR camera in our project because of its wide angle detectin(110-70 degrees). It is wide area and it is perfect selection for our project

 
Sprakfun Qwiic IR Array MLX90640 (110x75 degrees)

Lastly, we needed to save our data in our project and we found best way as wireless connection with one server and send this data to this server. Because of that, we need  one wireless module and  Adafruit Airlift Wifi is selected in our project. It has  a very nice pre-written library.
 
Adafruit Airlift Wifi
After that we needed a box to put our microcontroller and camera. The box is designed in Fusion 360 and printed as 3-D. 


 We made SPI communication between Teensy with Airlift-WİFİ.  ADAFRUİT AİRLİFT WİFİ is connected to Teensy 3.6 for SPI Communuicaition like that: 13.Teensy pin to  SCK , 12 Teensy pin to MISO 11.Teensy pin to MOSI 5.Teensy pin to CS 9.Teensy pin to BUSY 6.Teensy pin to REST and  ground to ground,  Vin to 3.3V. We used prewritten code for this communication.
We also made I2C communication between Teensy with MLX90640 SPARKFUN IR CAMERA. MLX90640 SPARKFUN IR CAMERA is connected like that: 18.Teensy pin to SDA and 19.Teensy pin to SCL and ground to ground, 3.3V to 3.3V. We used also prewritten code for this communication.


If you want to learn my Image processing algorithm and also Machine Learning algorithm, you need to read PDF document(IR CAMERA DETECTİON REPORT AND SYSTEM DESCRİPTİON AND CODE DESCRİPTİON 6.pdf).

If you have question, Please do not hesitate to ask:
E-mail:ozenbatukaan@gmail.com
