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
   for(int value=SERVOMIN;value<SERVOMAX;value++){
      pwm.setPWM(0,0,value);
      Serial.println(value);
      delay(30);
   }
}
