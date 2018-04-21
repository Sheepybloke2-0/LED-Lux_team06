char data;
int LED = 6;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available())
  {
    Serial.write(Serial.read());
    data = Serial.read();
    if(data != NULL)
    {
         digitalWrite(LED, HIGH);
         delay(1000);
         digitalWrite(LED, LOW);
    }
    
    delay(10);
  }

}
