#include <ArduinoJson.h>
#include <usbhid.h>
#include <usbhub.h>
#include <hiduniversal.h>
#include <hidboot.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // This is the 'maximum' pulse length count (out of 4096)

void setup(){
  Serial.begin(9600);

  pwm.begin();
  pwm.setPWMFreq(51);
}

void cont(int pin, int value){
  pwm.setPWM(pin,0,value);
}

void loop() {
  Serial.print("Input pin number: ");
  while(Serial.available() == 0) {}
  int pin = Serial.parseInt();
  Serial.println(pin);

  Serial.print("Input value: ");
  while(Serial.available() == 0) {}
  int value = Serial.parseInt();
  Serial.println(value);

  cont(pin,value);

  Serial.println("Input any key to continue..");
  while(Serial.available() == 0) {}

  pin = Serial.read();
  Serial.println(" ");
}
