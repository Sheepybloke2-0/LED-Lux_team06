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
    data = Serial.read();
    Serial.write(data);
    if( data == 'r')
    {
      digitalWrite(LED, HIGH);
      Serial.write("LED on \n");
      delay(1000);
      digitalWrite(LED, LOW);
    }
    
    delay(10);
  }

}
