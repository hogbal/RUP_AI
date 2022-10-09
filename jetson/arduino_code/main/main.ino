#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  70 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define TRIG 10
#define ECHO 11

const int pet = 1;
const int pp = 2;
const int ps = 3;

void setARM(int num,int angle){
  int value = map(angle,0,180,SERVOMIN,SERVOMAX);
  pwm.setPWM(num,0,value);
}

void servo_init(){
  setARM(pet, 0);
  setARM(pp, 0);
  setARM(ps, 0);
}

void open_met(int servo){
  setARM(servo, 0);
  for(int i = 0;i<=90;i++){
    setARM(servo, i);
    delay(10);
  }
}

void close_met(int servo){
  setARM(servo, 90);
  for(int i = 90;i>=0;i--){
    setARM(servo, i);
    delay(10);
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  servo_init();

  delay(10);
}

void loop() {
  digitalWrite(TRIG,LOW);
  digitalWrite(ECHO,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG,LOW);

  unsigned long duration = pulseIn(ECHO,HIGH);
  float distance = ((float)(340*duration)/10000)/2;

  if(distance <= 10){
    delay(500);
    close_func();
    delay(500);
    
    empty();
    Serial.println("Detection");

    while(true) {
      if(Serial.available()){
        char data = Serial.read();
        if(data == '1') {
          pet();
          break;
        }
        else if(data == '2'){
          pp();
          break;
        }
        else if(data == '3'){
          ps();
          break;
        }
        else if(data == '0'){
          //detect error
          break;
        }
      }
    }
    center();
    while(true) {
      if(Serial.available()){
        char data = Serial.read();
        if(data == 'e') {
          break;
        }
      }
    }
  }
}
