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


#define TRIG 9
#define ECHO 8
#define LED 7

void throw_away_rup(){
/*
  for (uint16_t pulselen = SERVOMIN; pulselen < 500; pulselen++) {
    pwm.setPWM(5, 0, pulselen);
  }
  delay(1000);
*/
  for (uint16_t pulselen = 500; pulselen < SERVOMIN; pulselen--) {
    pwm.setPWM(5, 0, pulselen);
  }
  delay(1000);

  for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    pwm.setPWM(4, 0, pulselen);
  }
  delay(1000);
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
    pwm.setPWM(4, 0, pulselen);
  }
  delay(1000);
}

void setup(){
  Serial.begin(9600);

  pinMode(TRIG,OUTPUT);
  pinMode(ECHO,INPUT);

  pwm.begin();
  pwm.setPWMFreq(51);

  pwm.setPWM(5,0,150);
  pwm.setPWM(4,0,540);
  pwm.setPWM(3,0,250);
  pwm.setPWM(2,0,150);
  pwm.setPWM(1,0,350);
  pwm.setPWM(0,0,150);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}

void loop() {
  digitalWrite(TRIG,LOW);
  digitalWrite(ECHO,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG,HIGH);delayMicroseconds(10);
  digitalWrite(TRIG,LOW);

  unsigned long duration = pulseIn(ECHO,HIGH);
  float distance = ((float)(340*duration)/10000)/2;
  
  if(distance >= 10 && distance <= 30){
    //throw_away_rup();
    Serial.println("Detection");

    while(true){
      if(Serial.available()){
        char data = Serial.read();
        if(data == '1') {
          digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(1000);                       // wait for a second
          digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
          delay(1000);
          break;                    // wait for a second
        }
        else if(data == '2'){
          digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(2000);                       // wait for a second
          digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
          delay(2000);                       // wait for a second
          break;
          
        }
        else if(data == '3'){
          digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
          delay(3000);                       // wait for a second
          digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
          delay(3000);                       // wait for a second
          break;
        }
      }
    }
  }
  else {
    //Serial.println("0");
  }
}
