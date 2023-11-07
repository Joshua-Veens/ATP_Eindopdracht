#include <iostream>
#include "BH1750.hpp"

int main(){
    BH1750Library bh1750Sensor(0x23); // Create an instance of the BH1750Library

    // Example: Read light level from BH1750 sensor
    int lightLevel = bh1750Sensor.readLightLevel();
    std::cout << "Light level: " << lightLevel << std::endl;

    return 0;
}