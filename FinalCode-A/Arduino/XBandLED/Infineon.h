#ifndef INFINION_H
#define INFINION_H

#include <Arduino.h> //needed for Serial.println
#include <inttypes.h>
#include <stddef.h>

 #define ADDRESS                    0x15EUL

  #define INTENSITY_RED              0x11U
  #define INTENSITY_GREEN            0x12U
  #define INTENSITY_BLUE	           0x13U
  #define INTENSITY_RGB              0x14U
  #define CURRENT_RED                0x21U
  #define CURRENT_GREEN              0x22U
  #define CURRENT_BLUE               0x23U
  #define CURRENT_RGB                0x24U
  #define OFFTIME_RED                0x41U
  #define OFFTIME_GREEN              0x42U
  #define OFFTIME_BLUE		           0x43U
  #define WALKTIME                   0x50U
  #define DIMMINGLEVEL               0x60U
  #define FADERATE                   0x61U

  #define READ_INTENSITY_RED         0x81U
  #define READ_INTENSITY_GREEN       0x82U
  #define READ_INTENSITY_BLUE        0x83U
  #define READ_CURRENT_RED           0x84U
  #define READ_CURRENT_GREEN         0x85U
  #define READ_CURRENT_BLUE          0x86U
  #define READ_OFFTIME_RED           0x87U
  #define READ_OFFTIME_GREEN         0x88U
  #define READ_OFFTIME_BLUE          0x89U
  #define READ_WALKTIME              0x8AU
  #define READ_DIMMINGLEVEL          0x8BU
  #define READ_FADERATE              0x8CU


  #define SAVEPARAMETERS             0xA0U

  #define BCCUMODID                  0x50030008U
  #define CHIPID                     0x40010004U
  #define REDINTS                    0x500300A0U // BCCU_CH5
  #define REDINT                     0x500300A4U
  #define BLUEINTS                   0x50030078U
  #define STARTWALK                  0x50030018U

typedef enum  {one, two, three, four, five, middle, six, seven, eight, nine, ten} Time; //changed from colors to Times

class Infineon
{
public:
	Infineon(void);
	~Infineon(void);

	unsigned int on;
  unsigned int message;

	void SETTIME(uint8_t Time);

	void I2CWRITE2BYTES (int Address, int Command, unsigned int Data);
	void I2CWRITE6BYTES (unsigned int Address, unsigned int Command, unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree);
	void I2CWRITE12BYTES (unsigned int Address, unsigned int Command, unsigned int DataOne, unsigned int DataTwo, unsigned int DataThree, unsigned int DataFour, unsigned int DataFive, unsigned int DataSix);
	unsigned int I2CREAD (unsigned int Address, unsigned int Command);
	unsigned long I2CREAD_DIRECTACCESS (unsigned int Address, unsigned int Command, unsigned long registerAddress);
	void I2CWRITE_DIRECTACCESS (unsigned int Address, unsigned int Command, unsigned long registerAddress, unsigned long Data);
	void CHANGEADDRESS (unsigned int Address, unsigned int newAddress);
	void I2CDMX (unsigned int Address, unsigned int Command);
	void I2CSAVEPARAM (unsigned int Address);
  void poweron(uint8_t ime);
  void poweroff();




};


#endif // Infineon.h
