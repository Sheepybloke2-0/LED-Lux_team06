// Arduino Code for LED drivers
#include "Infineon.h"
#include <XBee.h>
#define VERSION "1.00a0"

/* global vars */
uint8_t data = 0;
uint8_t lightState;
/* ZB response stuff */
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
// create reusable response objects for responses we expect to handle
Rx16Response rx16 = Rx16Response();
Rx64Response rx64 = Rx64Response();
// create reusable response objects for responses we expect to handle
ZBRxResponse rx = ZBRxResponse();

Infineon driver;

void loop() {
  xbee.readPacket();

  if (xbee.getResponse().isAvailable()) {
    // got something

    if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
      // got a zb rx packet
      // now fill our zb rx class
      xbee.getResponse().getZBRxResponse(rx);
      data = rx.getData(0);
    }
    else {
      // not something we were expecting
      data = 0; // sets data to default value
    }
    switch(data){
     case "avg" :
       // middle time setting, middle brightness setting
       lightState = middle;
       driver.SETTIME(lightState);
       break;
     case "pt": // plus time
       //more yellow
       if (lightState >= 11){
         lightState += lightState;
       }
       driver.SETTIME(lightState);
       data = 0; // don't want this to happen every loop
       break;
     case "mt": // minus time
       // more blue
       if (lightState <= 0){
         lightState -= lightState;
       }
       driver.SETTIME(lightState);
       data = 0;
       break;
     case "off":
       // turn off lights
       driver.poweroff();
       break;
     case "on":
       // turn on lights
       driver.poweron();
       break;
     default:
       // it should stay doing whatever it's doing
  }} else if (xbee.getResponse().isError()) {
      data = 0;
}
