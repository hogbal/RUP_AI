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
  Serial.println("test");
  pwm.begin();
  pwm.setPWMFreq(51);
}


void loop() {
  for(int i=0;i<6;i++){
    for(int value=SERVOMIN;value<SERVOMAX;value++){
    pwm.setPWM(i,0,value);
    }
  }
}
