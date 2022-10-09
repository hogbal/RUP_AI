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

  servo_init();

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
}

void loop() {
  open_met(pet);
  delay(2000);
  close_met(pet);
  delay(2000);
  open_met(pp);
  delay(2000);
  close_met(pp);
  delay(2000);
  open_met(ps);
  delay(2000);
  close_met(ps);
  delay(2000);
}
