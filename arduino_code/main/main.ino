#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  70 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define TRIG 10
#define ECHO 11

const int PET = 1;
const int PP = 2;
const int PS = 3;

void setARM(int num,int angle){
  int value = map(angle,0,180,SERVOMIN,SERVOMAX);
  pwm.setPWM(num,0,value);
}

void servo_init(){
  setARM(PET, 10);
  setARM(PP, 10);
  setARM(PS, 10);
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
  for(int i = 90;i>=10;i--){
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

  bool detection = false;
  unsigned long duration = pulseIn(ECHO,HIGH);
  float distance = ((float)(340*duration)/10000)/2;

  if(distance <= 10){
    delay(500);
    
    Serial.println("Detection");

    int met = 0;
    while(true) {
      if(Serial.available()){
        met = Serial.read() - '0';
        if(met != 0){
          detection = true;
          open_met(met);
          delay(10000);
          break;
        }
        else if(met == 0){
          break;
        }
      }
    }
    if(detection){
      close_met(met);
      detection = false;
      Serial.println("End");
    }
  }
}
