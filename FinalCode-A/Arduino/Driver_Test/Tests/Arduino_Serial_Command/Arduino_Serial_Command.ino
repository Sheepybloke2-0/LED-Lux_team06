// Arduino_Serial_Command
// SecondNode

int led = 13; // status LED
uint8_t readVal = 0; // what is read
char data[64]; // command

void setup(){
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop(){
  while(Serial.available()){
    readVal = Serial.read();
    if(readVal == '\n'){
      break
    }
    
  }
}
