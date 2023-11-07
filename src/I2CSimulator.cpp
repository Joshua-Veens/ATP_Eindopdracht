#ifndef I2CSimulator_HPP
#define I2CSimulator_HPP

#include <iostream>
#include <random>

class BH1750I2CSimulator {
private:
    uint16_t lightLevel = 25000;
    bool transmitting = false;
    bool actuatorActive = false;


    uint16_t generateSimulatedLightLevel() {
        // Seed the random number generator with the current time
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<double> noise(-50, 50); // Adjust the range as needed

        // Add noise to the humidity within the specified deviation
        double noiseLight = noise(gen);
        uint16_t noisyLightLevel = lightLevel + noiseLight;

        // Generate a random number within the specified range
        if(actuatorActive){
            noisyLightLevel = noisyLightLevel / 100;
        }
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

#endif