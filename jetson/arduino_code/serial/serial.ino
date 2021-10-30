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

boolean result = false;
String str = "";
 
StaticJsonDocument<200> doc;

class MyParser : public HIDReportParser {
  public:
    MyParser();
    void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf);
  protected:
    uint8_t KeyToAscii(bool upper, uint8_t mod, uint8_t key);
    virtual void OnKeyScanned(bool upper, uint8_t mod, uint8_t key);
    virtual void OnScanFinished();
};

MyParser::MyParser() {}

void MyParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) {
  // If error or empty, return
  if (buf[2] == 1 || buf[2] == 0) return;

  for (uint8_t i = 7; i >= 2; i--) {
    // If empty, skip
    if (buf[i] == 0) continue;

    // If enter signal emitted, scan finished
    if (buf[i] == UHS_HID_BOOT_KEY_ENTER) {
      OnScanFinished();
      result = true;
    }

    // If not, continue normally
    else {
      // If bit position not in 2, it's uppercase words
      OnKeyScanned(i > 2, buf, buf[i]);
    }
    return;
  }
}

uint8_t MyParser::KeyToAscii(bool upper, uint8_t mod, uint8_t key) {
  // Letters
  if (VALUE_WITHIN(key, 0x04, 0x1d)) {
    if (upper) return (key - 4 + 'A');
    else return (key - 4 + 'a');
  }

  // Numbers
  else if (VALUE_WITHIN(key, 0x1e, 0x27)) {
    return ((key == UHS_HID_BOOT_KEY_ZERO) ? '0' : key - 0x1e + '1');
  }

  return 0;
}

void MyParser::OnKeyScanned(bool upper, uint8_t mod, uint8_t key) {
  uint8_t ascii = KeyToAscii(upper, mod, key);
  Serial.print((char)ascii);
}

void MyParser::OnScanFinished() {
  Serial.println();
}

USB          Usb;
USBHub       Hub(&Usb);
HIDUniversal Hid(&Usb);
MyParser     Parser;

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

void set_arm(float X, float Y, float Z, float GRIP_DEGREE, int _GRIPPER, int de) {
  float Pi = 3.14159;
  float BASE_HEIGHT = 100.0;
  float SHOULDER_LENGTH = 95.0;
  float ARM_LENGTH = 30.0;
  float GRIP_LENGTH = 30.0;

  float BASE_ANGLE = atan(Y/X);
  float R = sqrt((X*X) + (Y*Y));
  float GRIP_ANGLE = radians(GRIP_DEGREE);
  float RSIN = sin(GRIP_ANGLE) * GRIP_LENGTH;
  float R1 = R - RSIN;
  float ZCOS = cos(GRIP_ANGLE) * GRIP_LENGTH;
  float Z1 = Z - BASE_HEIGHT + (ZCOS * GRIP_LENGTH);
  float A = sqrt((Z*Z) * (R*R)) / 2;
  float ELBOW_ANGLE = asin(A / ARM_LENGTH) * 2;
  float SHOULDER_ANGLE = atan2(Z1, R1) + ((Pi - ELBOW_ANGLE) / 2);
  float WRIST_ANGLE = Pi + GRIP_ANGLE - SHOULDER_ANGLE - ELBOW_ANGLE;

  BASE_ANGLE = constrain(map(degrees(BASE_ANGLE), 0, 180, 150, 600), 150, 600);
  SHOULDER_ANGLE = constrain(map(degrees(SHOULDER_ANGLE), 0, 180, 150, 600), 150, 600);
  ELBOW_ANGLE = constrain(map(degrees(ELBOW_ANGLE), 0, 180, 150, 600), 150, 600);
  WRIST_ANGLE = constrain(map(degrees(WRIST_ANGLE), 0, 180, 150, 600), 150, 600);
  GRIP_DEGREE = constrain(map(degrees(GRIP_DEGREE), 0, 180, 150, 600), 150, 600);
  _GRIPPER = constrain(map(degrees(_GRIPPER), 0, 180, 150, 600), 150, 600);
 
  pwm.setPWM(0,0,BASE_ANGLE);
  pwm.setPWM(1,0,SHOULDER_ANGLE);
  pwm.setPWM(2,0,ELBOW_ANGLE);
  pwm.setPWM(3,0,WRIST_ANGLE);
  pwm.setPWM(4,0,GRIP_DEGREE);
  pwm.setPWM(5,0,_GRIPPER);
}



void setup(){
  Serial.begin(9600);


  if (Usb.Init() == -1) {
    Serial.println("OSC did not start.");
  }

  delay( 200 );

  Hid.SetReportParser(0, &Parser);
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
    result = false;
    /*
    while(true) {
      Usb.Task();
      if(result == true) break;
    }
    */
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
