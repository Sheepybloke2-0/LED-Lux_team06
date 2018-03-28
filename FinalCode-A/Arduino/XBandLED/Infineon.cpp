#include "Infineon.h"
#include <Arduino.h> //needed for Serial.println
#include <inttypes.h>
#include <stddef.h>
#include <Wire.h>

Infineon::Infineon(void)
{


}


Infineon::~Infineon(void)
{
}





  unsigned int c[2] = {0};
  unsigned int d[4] = {0};
  unsigned int on = 0;
  unsigned int message = 0;

void Infineon::SETTIME(uint8_t Time)
{
	switch(Time)
	{ // R = warm G = cool B = always off
	case one:    I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x0, 0xFFF, 0x0);break; // all cool
	case two:    I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x1C7, 0xE38, 0x0);break;
	case three:  I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x38E, 0xC71, 0x0);break;
	case four:   I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x555, 0xAAA, 0x0);break;
	case five:   I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x71C, 0x8E3, 0x0);break;
  case middle: I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x7FF, 0x7FF, 0x0);break; // middle - reset value
	case six:    I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0x8E3, 0x71C, 0x0);break;
	case seven:  I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0xAAA, 0x555, 0x0);break;
	case eight:  I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0xC71, 0x38E, 0x0);break;
	case nine:   I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0xE38, 0x1C7, 0x0);break;
  case ten:    I2CWRITE6BYTES(ADDRESS, INTENSITY_RGB, 0xFFF, 0x0, 0x0);break; // all warm
  default: break;
	}
}
/* can poweron and poweroff be gradual? */
void Infineon::poweroff(){
  // turn off LEDs
  I2CWRITE6BYTES(ADDRESS, INTENSITY_RBG, 0x0, 0x0, 0x0);
}
void Infineon::poweron(){
  // turn on to middle time setting
  SETTIME(middle);
}
// Infineon functions follow
 /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - Defined I2C Commands i.e. INTENSITY_RED, INTENSITY_GREEN, INTENSITY_BLUE
                   unsigned int Data - 16bit data to be written to slave
  Parameters (OUT): None
  Return Value: None
  Description: This function will write 2 bytes of word to the I2C bus line
  */



void Infineon::I2CWRITE2BYTES (int Address, int Command, unsigned int Data)
  {
    unsigned int upperByte, lowerByte; // Separate 4 byte data into 2 byte values
    lowerByte = Data;
    upperByte = Data >> 8;

    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF); // Putting address into correct format
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD)); // Start I2C transmission
    Wire.write(uint8_t(lowerSLAD)); // address lower 8 bits of i2c address
    Wire.write(uint8_t(Command)); // write command
    Wire.write(uint8_t(upperByte)); // write data
    Wire.write(uint8_t(lowerByte));
    Wire.endTransmission(true);

  }
   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - Defined I2C Commands i.e. INTENSITY_RGB, CURRENT_RGB
                   unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree - Three 16bit data to be written to slave
  Parameters (OUT): None
  Return Value: None
  Description: This function will write 6 bytes of word to the I2C bus line
  */

void Infineon::I2CWRITE6BYTES (unsigned int Address, unsigned int Command, unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree) // DataOne: Red, DataTwo: Green, DataThree: Blue
  {
    unsigned int upperByte, lowerByte; // Split each Data parameter into upper and lower 8 bytes because I2C format sends 8 bytes of data each time
    lowerByte = DataOne;
    upperByte = DataOne >> 8;

    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF);
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD)); // Red
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command));
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));
    lowerByte = DataTwo;
    upperByte = DataTwo >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));
    lowerByte = DataThree;
    upperByte = DataThree >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));
    Wire.endTransmission(true);

  }

 /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - Defined I2C Commands i.e. DMX16Bit
                   unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree, usigned int DataFour, unsigned int DataFive - Three 16bit data to be written to slave
  Parameters (OUT): None
  Return Value: None
  Description: This function will write 12 bytes of word to the I2C bus line
  */

void Infineon::I2CWRITE12BYTES (unsigned int Address, unsigned int Command, unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree, unsigned int DataFour, unsigned int DataFive, unsigned int DataSix) // DataOne: Red, DataTwo: Green, DataThree: Blue
  {
    unsigned int upperByte, lowerByte;
    lowerByte = DataOne;
    upperByte = DataOne >> 8;

    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF);
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command)); // write command
    Wire.write(uint8_t(upperByte)); // write 2 uint8_ts
    Wire.write(uint8_t(lowerByte));

    lowerByte = DataTwo;
    upperByte = DataTwo >> 8;
    Wire.write(uint8_t(upperByte)); // write next two bytes
    Wire.write(uint8_t(lowerByte));

    lowerByte = DataThree;
    upperByte = DataThree >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));

    lowerByte = DataFour;
    upperByte = DataFour >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));

    lowerByte = DataFive;
    upperByte = DataFive >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));

    lowerByte = DataSix;
    upperByte = DataSix >> 8;
    Wire.write(uint8_t(upperByte));
    Wire.write(uint8_t(lowerByte));
    Wire.endTransmission(true);

  }

   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - Defined read I2C Commands i.e. READ_INTENSITY_RED, READ_INTENSITY_GREEN, READ_INTENSITY_BLUE
  Parameters (OUT): None
  Return Value: Requested data from Shield will be sent back
  Description: This function will request 2 bytes of word from the shield
  */

unsigned int Infineon::I2CREAD (unsigned int Address, unsigned int Command) // Returns data sent by slave
  {
    int i = 0;
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF);
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79;

    Wire.beginTransmission(uint8_t(upperSLAD)); // Red
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command));
    Wire.endTransmission(false); // false for Repeated Start

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.requestFrom(upperSLAD, 2, true);
    unsigned int data = 0;

    while(Wire.available())    // slave may send less than requested. Print out received data byte
    {
      message = 1;
      c[i] = Wire.read(); // receive a byte as character
      i++;

    }
    Wire.endTransmission(true);

    data = c[1]; // write data to serial monitor. c[1] is higher byte
    data = (data << 8) | c[0];  // shift left and combine with lower byte
    Serial.print("0x");
    if (data < 0x1000)
        Serial.print("0");
    Serial.println(data, HEX);
    return data;
  }

   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - DIRECTACCESS_READ
  Parameters (OUT): None
  Return Value: Requested data from the Shield will be returned
  Description: This function will request 4 bytes of data from shield.
  */

unsigned long Infineon::I2CREAD_DIRECTACCESS (unsigned int Address, unsigned int Command, unsigned long registerAddress)
  {
    int i = 0;
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF); // sending command + address
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command));

    unsigned int firstByte, secondByte, thirdByte, fourthByte;
    firstByte = registerAddress >> 24; // top byte
    secondByte = registerAddress >> 16;
    thirdByte = registerAddress >> 8;
    fourthByte = registerAddress; // bottom byte

    Wire.write(uint8_t(firstByte));
    Wire.write(uint8_t(secondByte));
    Wire.write(uint8_t(thirdByte));
    Wire.write(uint8_t(fourthByte));

    Wire.endTransmission(false); // false for Repeated Start

    Wire.beginTransmission(uint8_t(upperSLAD)); // request for read
    Wire.write(uint8_t(lowerSLAD));
    Wire.requestFrom(upperSLAD, 4, true);
    unsigned long data = 0;

    while(Wire.available())    // slave may send less than requested. Print out received data byte
    {
      d[i] = 0;
      d[i] = Wire.read(); // receive a byte as character
      i++;
    }

    Wire.endTransmission(true);

    data = d[3]; // combining into one variable. Highest byte received first
    data = (data << 8) | d[2];
    data = (data << 8) | d[1];
    data = (data << 8) | d[0];
    Serial.print("0x");
    if (data < 0x10000000)
        Serial.print("0");
    Serial.println(data, HEX);
    return data;
  }
   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   int Command - Defined I2C Commands i.e. DIRECTACCESS_OR, DIRECTACCESS_AND, DIRECTACCESS_MOVE
                   unsigned long registerAddress - address of target register
                   unsigned long Data - 32 bits data to be written to register
  Parameters (OUT): None
  Return Value: None
  Description: This function will write 4 bytes of data to specified register
  */
void Infineon::I2CWRITE_DIRECTACCESS (unsigned int Address, unsigned int Command, unsigned long registerAddress, unsigned long Data) // For accessing registers directly
  {
    int i = 0;
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF); // sending command + address
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command));

    unsigned int firstByte, secondByte, thirdByte, fourthByte; // Send address of register first
    firstByte = registerAddress >> 24; // top byte
    secondByte = registerAddress >> 16;
    thirdByte = registerAddress >> 8;
    fourthByte = registerAddress; // bottom byte

    Wire.write(uint8_t(firstByte));
    Wire.write(uint8_t(secondByte));
    Wire.write(uint8_t(thirdByte));
    Wire.write(uint8_t(fourthByte));

    firstByte = Data >> 24; // top byte
    secondByte = Data >> 16;
    thirdByte = Data >> 8;
    fourthByte = Data; // bottom byte

    Wire.write(uint8_t(firstByte)); // send 4 bytes of data
    Wire.write(uint8_t(secondByte));
    Wire.write(uint8_t(thirdByte));
    Wire.write(uint8_t(fourthByte));
    Wire.endTransmission(true);

  }
   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   unsigned int newAddress - Address the shield should change to
  Parameters (OUT): None
  Return Value: None
  Description: This function will change the I2C address of the slave
  */

void Infineon::CHANGEADDRESS (unsigned int Address, unsigned int newAddress)
  {
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF);
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79; // First 5 bits 11110 and last bit '1' for a write

    Wire.beginTransmission(uint8_t(upperSLAD)); // Red
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(0x70)); // Command to change address
    lowerSLAD = (unsigned int) (newAddress & 0x00FF);
    upperSLAD = newAddress >> 7; // Split address into 2 bytes
    upperSLAD |= 0xF0; // 10 bit addressing: First 5 bits have to be 11110.
    upperSLAD &= 0xFE;
    Wire.write(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.endTransmission(true);
  }

   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
                   unsigned int Command - DMXON, DMXOFF
  Parameters (OUT): None
  Return Value: None
  Description: This function will enable or disable DMX512 control on shield
  */

void Infineon::I2CDMX (unsigned int Address, unsigned int Command) // Switch off / on the DMX
  {
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF); // Putting address into correct format
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79;

    Wire.beginTransmission(uint8_t(upperSLAD)); // Start I2C transmission
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(Command));
    Wire.endTransmission(true);

  }
   /*
  Parameters (IN): int Address - Address of RGB LED Shield, Default 0x15E
  Parameters (OUT): None
  Return Value: None
  Description: This function will request the shield to save configurations to flash memory
  */

void Infineon::I2CSAVEPARAM (unsigned int Address)
  {
    int i = 0;
    unsigned int lowerSLAD = (unsigned int) (Address & 0x00FF);
    unsigned int upperSLAD = Address >> 8;
    upperSLAD |= 0x79;

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD));
    Wire.write(uint8_t(SAVEPARAMETERS)); // write SAVEPARAMETERS command
    Wire.endTransmission(false); // false for Repeated Start

    Wire.beginTransmission(uint8_t(upperSLAD));
    Wire.write(uint8_t(lowerSLAD)); // write to address lower 8 bits of slave address
    Wire.requestFrom(upperSLAD, 2, true);  // send READ request with upper slave address
    unsigned int data = 0;

    while(Wire.available())    // slave may send less than requested. Print out received data byte
    {
      message = 1;
      c[i] = Wire.read(); // receive a byte as character
      i++;
    }
    Wire.endTransmission(true); // STOP condition

    data = c[1]; // print the data on serial monitor
    data = (data << 8) | c[0];
    Serial.print("0x");
    if (data < 0x1000)
        Serial.print("0");
    Serial.println(data, HEX);

  }
