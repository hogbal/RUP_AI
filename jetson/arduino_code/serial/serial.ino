#include <ArduinoJson.h>
 
String str = "";
 
StaticJsonDocument<200> doc;
 
void setup() {
  Serial.begin(9600);
  Serial.begin(19200);
}
 
void loop() {
  if(Serial.available())
  {
    str = Serial.readStringUntil('\n');
    DeserializationError error = deserializeJson(doc, str);
 
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }
  }
 
  int test = doc["test"];
  Serial.println(test);
  delay(10);
}
