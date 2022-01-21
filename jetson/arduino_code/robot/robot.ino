#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  70 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  518 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define TRIG 9
#define ECHO 8

int servo_angle0 = 0;
int servo_angle1 = 165;
int servo_angle2 = 90;
int servo_angle3 = 0;

void setup(){
  Serial.begin(9600);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
}

void setARM(int num,int angle){
  int value = map(angle,0,180,SERVOMIN,SERVOMAX);
  pwm.setPWM(num,0,value);
}

void open_func(){
  setARM(4,0);
}

void close_func(){
  setARM(4,50);
}

void center(){
  for(;servo_angle1 <= 165 || servo_angle2 >= 90;servo_angle1++,servo_angle2--){
    if(servo_angle1 <= 165){
      setARM(1,servo_angle1);
    }
    if(servo_angle2 >= 90){
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  setARM(3,0);
  open_func();
}

void detection(){
  for(;servo_angle1 >= 135 || servo_angle2 <= 130;servo_angle1--,servo_angle2++){
    if(servo_angle1 >= 135) {
      setARM(1,servo_angle1);
    }
    if(servo_angle2 <= 130) {
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  setARM(3,150);
  close_func();
}

void pet(){
  for(;servo_angle1 >= 135 || servo_angle2 <= 130;servo_angle1--,servo_angle2++){
    if(servo_angle1 >= 135) {
      setARM(1,servo_angle1);
    }
    if(servo_angle2 <= 130) {
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);
  open_func();
}

void loop() {
  center();
  delay(1000);

  long duration, distance;

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duration = pulseIn (ECHO, HIGH);
  distance = duration * 17 / 1000;

  if(distance < 10){
    close_func();
    delay(1000);
    
    detection();
    delay(10000);

    center();
    delay(1000);
    
    pet();
    delay(3000);
  }
}
