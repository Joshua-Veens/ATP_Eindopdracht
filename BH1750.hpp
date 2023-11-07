#ifndef BH1750_HPP
#define BH1750_HPP

#include <iostream>
#include <random>


std::random_device rdev;
std::mt19937 rgen(rdev());
std::uniform_int_distribution<int> idist(0,10); //(inclusive, inclusive)


class BH1750I2CSimulator {
private:
   uint16_t lightLevel;
   bool transmitting = false;


   uint16_t generateSimulatedLightLevel() {
      // Seed the random number generator with the current time
      std::random_device rd;
      std::mt19937 gen(rd());
      std::uniform_real_distribution<double> noise(-200, 200); // Adjust the range as needed
      std::uniform_int_distribution<uint16_t> dist(1, 65535);

      // Add noise to the humidity within the specified deviation
      uint16_t randomLightLevel = dist(gen);
      double noiseLight = noise(gen);
      uint16_t noisyLightLevel = randomLightLevel + noiseLight;

      // Generate a random number within the specified range
      return noisyLightLevel;
   }

public:
   void write(uint8_t data){
      if( transmitting ){
         if ( data == 0x20 ){
            lightLevel = generateSimulatedLightLevel();
         }
         // else ..... 
         // other methods not implemented.
      }
   }

   uint16_t read(){
      return lightLevel;
   }

   void beginTransmission(){
      transmitting = true;
   }

   void endTransmission(){
      transmitting = false;
   }

};


class BH1750Library {

private:
   int bh1750Address = 0x23;
   BH1750I2CSimulator I2CSimulator;

public:
   BH1750Library(uint8_t address): 
      bh1750Address(address) 
      {}

   int readLightLevel() {
      I2CSimulator.beginTransmission();
      I2CSimulator.write(0x20); // Command to set sensor in high-resolution mode 1lux
      I2CSimulator.endTransmission();

      // delay(250); // Wait for measurement

      int lightLevel = I2CSimulator.read();
      return lightLevel;

   }
};

#endif