#include <Wire.h>
#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();
#define SERVOMIN  70 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define TRIG 9
#define ECHO 8

Servo servo;
const int servoPin=9;

//서보모터 기본 셋팅 각도
int servo_angle1 = 30;
int servo_angle2 = 50;
int servo_angle3 = 0;

//0번 서보모터 딜레이
int em_d=700, pet_d=1200, pp_d=1500,ps_d=2300;

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
  for(;servo_angle1 <= 30 || servo_angle2 >= 50;servo_angle1++,servo_angle2--){
    if(servo_angle1 <= 30){
      setARM(1,servo_angle1);
    }
    if(servo_angle2 >= 50){
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  setARM(3,30);
  delay(2000);
  //open_func();
}

void empty(){
  //회전
  servo.write(110);
  delay(em_d);

  //정지
  servo.write(90);
  delay(100);

  //손목 회전 & 원위치
  for(int i=30;i<180;i++){
    setARM(3,i);
    delay(10);
  }
  delay(2000);
  //delay(10000); detection 진행

  for(int i=180;i>30;i--){
    setARM(3,i);
    delay(10);
  }
  delay(1000);

  //center로 회전
  servo.write(75);
  delay(em_d);

  //정지
  servo.write(90);
}

void pet(){
  for(;servo_angle1 <= 30 || servo_angle2 >= 50;servo_angle1++,servo_angle2--){
    if(servo_angle1 <= 30){
      setARM(1,servo_angle1);
    }
    if(servo_angle2 >= 50){
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);

  servo.write(110);
  delay(pet_d);
  servo.write(90);
  delay(1000);
  servo.write(81.75);
  delay(pet_d);
 
  open_func();
  delay(1000);
}

void pp(){
  for(;servo_angle1 <= 30 || servo_angle2 >= 50;servo_angle1++,servo_angle2--){
    if(servo_angle1 <= 30){
      setARM(1,servo_angle1);
    }
    if(servo_angle2 >= 50){
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);

  servo.write(78.5);
  delay(pp_d);
  servo.write(90);
  delay(1000);
  servo.write(102);
  delay(pp_d);
 
  open_func();
  delay(1000);
}

void ps(){
  for(;servo_angle1 <= 30 || servo_angle2 >= 50;servo_angle1++,servo_angle2--){
    if(servo_angle1 <= 30){
      setARM(1,servo_angle1);
    }
    if(servo_angle2 >= 50){
      setARM(2,servo_angle2);
    }
    delay(15);
  }
  delay(1000);

  servo.write(78);
  delay(ps_d);
  servo.write(90);
  delay(1000);
  servo.write(102.95);
  delay(ps_d+200);
 
  open_func();
  delay(1000);
}

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
  servo.write(90);//초기 손 고정은 어쩌면 좋지

  //pinMode(TRIG, OUTPUT);
  //pinMode(ECHO, INPUT);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  center();
  Serial.println("setting success");

  delay(10);
}

void loop() {
    Serial.println("empty");
    //empty();
    ps();
    exit(0);
}
