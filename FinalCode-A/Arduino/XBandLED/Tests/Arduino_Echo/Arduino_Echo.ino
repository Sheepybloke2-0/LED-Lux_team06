//Arduino UNO XBee Test Code
//#include <XBee.h>
int led = 13;
int led2 = 4;
uint8_t data = 0;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  //xbee.setSerial(Serial);
  //Serial.flush();
}

void loop() {
//    xbee.readPacket();
//    
//    if (xbee.getResponse().isAvailable()) {
//      // got something
//      
//      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
//        // got a zb rx packet
//        // now fill our zb rx class
//        xbee.getResponse().getZBRxResponse(rx);
//        data = rx.getData(0);
//     }} else if (xbee.getResponse().isError()) {
      //nss.print("Error reading packet.  Error code: ");  
      //nss.println(xbee.getResponse().getErrorCode());
      // or flash error led
  //  } 
  if(Serial.available()){
    Serial.write(Serial.read());
    digitalWrite(led, HIGH);
    digitalWrite(led2, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    digitalWrite(led2, LOW);
    delay(100);
  }
}
