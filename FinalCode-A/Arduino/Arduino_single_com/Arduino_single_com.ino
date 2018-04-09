#include "SoftwareSerial.h"

char data[64];
uint8_t read_val;
int LED = 8;

//SoftwareSerial XBee(6,7);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available())
  {
    Serial.write(Serial.read());
    read_val = Serial.read();
    
    digitalWrite(LED, HIGH);
    delay(1000);
    digitalWrite(LED, LOW);
  }
}
