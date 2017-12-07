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


### 12/6/17 Adding LED support
First convert the old serial code to actually moving the Pixel LED. Start by using the
old pseudo code to pull together the basic structure, then add the serial work.

Supporting 5 different actions right now. here's the switch statement:
```
//Read variable and run light associated. Make sure the variable stays long enough to run the program multiple times
 switch(data)
 {
   case 'r' :
     //Run through the rainbow. See color definition  above for values
     rainbow();
     break;
   case 'w':
     //Display a warm white LED
     warmwhite();
     break;
   case 'c':
     //Run the warm white with some varying reds and oranges to create a more orange color
     candle();
     break;
   case 'm':
     //Run through different reds and oranges in a mood lighting-esque fashion
     mood();
     break;
   case 'd':
     //Dim and brighten the LEDs
     dim();
     break;
   default:
     //Set the basic command to just flash the red LED
     redflash();
 }
```
#####Connections!
**NOTE** Connect the Arduino and XBee like so
| XBee Connection | Arduino Pin |
----------------------------------
| Vcc Pin 1       | 3.3v        |
| GND Pin 10      | GND         |
| DOUT Pin 2      | RX Pin 0    |
| DIN Pin 3       | TX Pin 1    |

To flash the Arduino, you need to have the TX/RX pins disconnected, since the
board is flashed over serial and having connections in those pins overrides the
onboard serial. Once flashed, connect to an external power supply and it should work.


Found out that the NeoPixel doesn't have a dim command. The setBrightness command
should only be used once on initialization to limit current, not change brightness. :(
