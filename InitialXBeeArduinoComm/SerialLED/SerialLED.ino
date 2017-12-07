#define VERSION "1.00a0"
#include <Adafruit_NeoPixel.h>

#define LEDPIN    6
#define NUM_LEDS  1

char data;

// r g b w : Colors for Rainbow
int rainbow_color[14][4] = {
  {255, 0 , 0, 0}, // red
  {120, 30, 0, 25}, //faded orange
  {209, 148, 0, 15}, // goldish
  {75, 97, 0, 20}, // light green
  {63, 217, 0, 21}, // really green
  {0, 158, 0, 209}, // seafoam
  {0, 162, 97, 106}, // turquoise
  {0, 115, 72, 0}, // aqua
  {0, 122, 240, 41}, // cerulean
  {0, 50, 185, 0}, // ocean
  {0, 0, 255, 121}, // baby blue
  {255, 0, 255, 180}, // lilac
  {127, 0, 171, 0}, // iris
  {176, 0, 148, 56} // orchid
};

int mood_color[11][4] = {
  {255, 0 , 100, 0}, // fushia
  {153, 0, 153, 50}, //rose
  {176, 0, 148, 56}, // orchid
  {205, 0, 95, 50}, // baby pink
  {206, 0, 166, 0}, // Unicorn pink
  {140, 0, 0, 84}, // daisy
  {138, 0, 0, 75}, // Dusk
  {255, 20, 0, 60}, // sunset
  {120, 30, 0, 25}, // faded orange
  {255, 70, 0, 35}, // orange cream
  {165, 109, 0, 61} // ambient
};

//Pixel colors go GRB
Adafruit_NeoPixel LED = Adafruit_NeoPixel(NUM_LEDS, LEDPIN, NEO_RGBW);

void setup() {
  // Starts serial. XBee must be connected to RX and TX pins 0 and 1 and able to join the network
  Serial.begin(9600);
  LED.begin();
  LED.setBrightness(200);
  LED.show(); //Init all the LEDs to off
}

//TODO: Add functions here
void redflash()
{
  LED.setPixelColor(0, LED.Color(0, 255, 0, 0));
  LED.setPixelColor(1, LED.Color(0, 255, 0, 0));
  LED.show();
  //TODO: This may cause issues with how the system collects data. May need to figure out a way to get around that. Make nonblocking
  delay(500);
  LED.setPixelColor(0, LED.Color(0, 0, 0, 0));
  LED.setPixelColor(1, LED.Color(0, 0, 0, 0));
  LED.show();
}

void rainbow() 
{
  int r,g,b,w;
  // take lights through Color spectrum
  for (int x = 0; x < 14; x++){
    r = rainbow_color[x][0];
    g = rainbow_color[x][1];
    b = rainbow_color[x][2];
    w = rainbow_color[x][3];
    LED.setPixelColor(0, LED.Color(g, r, b, w));
    LED.setPixelColor(1, LED.Color(g, r, b, w));
    LED.show();
  }
}

void warmwhite()
{
  LED.setPixelColor(0, LED.Color(0, 0, 0, 255));
  LED.setPixelColor(1, LED.Color(0, 0, 0, 255));
  LED.show();
}

void candle()
{
  //Warm white with a bit more orange in there
  LED.setPixelColor(0, LED.Color(30, 50, 0, 175));
  LED.setPixelColor(1, LED.Color(30, 50, 0, 175));
  LED.show();
}

void mood()
{
  //Go from pink to red to orange and then back
  int r,g,b,w;
  for (int x = 0; x < 11; x++){
    r = mood_color[x][0];
    g = mood_color[x][1];
    b = mood_color[x][2];
    w = mood_color[x][3];
    LED.setPixelColor(0, LED.Color(g, r, b, w));
    LED.setPixelColor(1, LED.Color(g, r, b, w));
    LED.show();
    delay(20);
  }
}

void wave()
{
    int g = 80;
    int b = 255;
    for ( int i = 0; i < 25; i++)
    {
      LED.setPixelColor(0, LED.Color(g + 2, 0, b - 2, 0));
      LED.setPixelColor(1, LED.Color(g + 4, 0, b - 4, 0));
      LED.show();
    }
    for ( int i = 0; i < 25; i++)
    {
      LED.setPixelColor(0, LED.Color(g - 2, 0, b + 2, 0));
      LED.setPixelColor(1, LED.Color(g - 4, 0, b + 4, 0));
      LED.show();
    }
}

void loop() {
  //Check if data is available
  if (Serial.available())
  {
     //If so, store data in variable and echo the character as an OK
     data = Serial.read();
     Serial.write(data);
     delay(10);
  }

  //Read variable and run light associated. Make sure the variable stays long enough to run the program multiple times
  switch(data)
  {
    case 'r' : 
      //Run through the rainbow. See Color definition  above for values
      rainbow();
      break;
    case 'w': 
      //Display a warm white LED
      warmwhite();
      break;
    case 'c':
      //Run the warm white with some varying reds and oranges to create a more orange Color
      candle();
      break;
    case 'm':
      //Run through different reds and oranges in a mood lighting-esque fashion
      mood();
      break;
    case 'b':
      wave();
      break;
    default:
      //Set the basic command to just flash the red LED
      redflash();
  }
}


