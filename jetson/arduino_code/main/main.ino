#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  70 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define TRIG 10
#define ECHO 11

Servo servo;
const int servo0 = 9;
const int servo1 = 1;
const int servo2 = 2;
const int servo3 = 3;
const int servo4 = 4;

int servo_angle1 = 35;
int servo_angle2 = 40;

int em_d=700, pet_d=1200, pp_d=1500,ps_d=2300;

void setARM(int num,int angle){
  int value = map(angle,0,180,SERVOMIN,SERVOMAX);
  pwm.setPWM(num,0,value);
}

void open_func(){
  setARM(servo4,0);
}

void close_func(){
  setARM(servo4,50);
}

void center(){
  int angle1 = 35;
  int angle2 = 40;
  for(;servo_angle1 >= angle1 || servo_angle2 >= angle2;servo_angle1--,servo_angle2--){
    if(servo_angle1 >= angle1){
      setARM(servo1,servo_angle1);
    }
    if(servo_angle2 >= angle2){
      setARM(servo2,servo_angle2);
    }
    delay(15);
  }
  
  setARM(servo3,30);
  delay(2000);
  open_func();
}

void empty(){
  /*
  servo.write(110);
  delay(em_d);

  servo.write(90);
  delay(100);
  */

  for(int i=30;i<140;i++){
    setARM(servo3,i);
    delay(10);
  }
  delay(2000);

  for(int i=140;i>30;i--){
    setARM(servo3,i);
    delay(10);
  }
  delay(1000);
  /*
  servo.write(75);
  delay(em_d);
  
  servo.write(90);
  */
}

void pet(){
  servo.write(113);
  delay(pet_d);

  servo.write(90);
  delay(500);

  int angle1 = 60;
  int angle2 = 65;
  for(;servo_angle1 <= angle1 || servo_angle2 <= angle2;servo_angle1++,servo_angle2++){
    if(servo_angle1 <= angle1){
      setARM(servo1,servo_angle1);
    }
    if(servo_angle2 <= angle2){
      setARM(servo2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);
  
  open_func();
  delay(1000);
  
  servo.write(74);
  delay(pet_d);
  servo.write(90);
  
  delay(1000);
}

void pp(){
  servo.write(75.5);
  delay(pp_d);
  
  servo.write(90);
  delay(500);

  int angle1 = 60;
  int angle2 = 65;
  for(;servo_angle1 <= angle1 || servo_angle2 <= angle2;servo_angle1++,servo_angle2++){
    if(servo_angle1 <= angle1){
      setARM(servo1,servo_angle1);
    }
    if(servo_angle2 <= angle2){
      setARM(servo2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);
  
  open_func();
  delay(1000);
  
  servo.write(108);
  delay(pp_d);
  servo.write(90);
  delay(1000);
}

void ps(){  
  servo.write(107.5);
  delay(ps_d);
  
  servo.write(90);
  delay(500);

  int angle1 = 35;
  int angle2 = 40;
  for(;servo_angle1 >= angle1 || servo_angle2 >= angle2;servo_angle1--,servo_angle2--){
    if(servo_angle1 >= angle1){
      setARM(servo1,servo_angle1);
    }
    if(servo_angle2 >= angle2){
      setARM(servo2,servo_angle2);
    }
    delay(15);
  }
  
  delay(1000);
  
  open_func();
  delay(1000);

  servo.write(80);
  delay(ps_d);
  
  servo.write(90);
  delay(1000);
}


void setup() {
  Serial.begin(9600);
  servo.attach(servo0);
  servo.write(90);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  center();
  Serial.println("setting success");

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
