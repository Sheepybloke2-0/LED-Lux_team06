###Notes 12/5
Base serial that works:
```
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
```

To flash the arduino, disconnect TX and RX (0,1), since they confilct with the serial cable.
Then connect individually to the power supply and it works.

Current configs: Comes from [[https://alselectro.wordpress.com/2017/01/23/zigbee-xbee-s2c-how-to-configure-as-coordinator-router-end-device/|here]]
```
NODE 1:
PanID 12
Coordinator: Enabled[1]
DH: 0
DL: FFFF

NODE 2:
PanID: 12
Coordinator: Disabled[0]
Channel Verification: Enabled[1]
```
Now test with checking for from the terminal
```
    if(data == 'r')
    {
         digitalWrite(LED, HIGH);
         delay(1000);
         digitalWrite(LED, LOW);
    }
```
Not working so far. Maybe it has to do with the order. It could be that the serial
is being read in, then not available for the  `data` variable to capture.

That was the issue! This code flashes an LED when `r` is sent:
```
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
    //Grab data so that all processes can use it
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
```
Now, it's onto continuing the growths!
