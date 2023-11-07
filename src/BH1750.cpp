#include <iostream>
#include <random>
#include <vector>
#include <pybind11/pybind11.h>

class BH1750Library {

private:
   int bh1750Address = 0x23;
   uint16_t lightLevel = 25000;
   int currentHour = 10;
   int lightLevels [24] = { 20, 50, 100, 300, 500, 900, 3200, 19000, 29000, 30000, 29000, 28000, 26000, 18000, 17000, 6000, 1200, 800, 300, 200, 100, 50, 30, 20 };

public:
   BH1750Library(){}

   int simulateLightLevel(){   
      unsigned int tmp = 0;
      tmp = (uint8_t)((lightLevel >> 8) & 0xFF);
      tmp <<= 8;
      tmp |= (uint8_t)(lightLevel & 0xFF);
      return tmp;
   }


   int readLightLevel() {
      return simulateLightLevel() / 1.2;
   }

   void setLightLevel(int lightLevel_){
      lightLevel = lightLevel_;
   }

   void generateSimulatedLightLevel() {
      std::random_device rd;
      std::mt19937 gen(rd());
      std::uniform_real_distribution<double> noise(-10, 10);
      double noise_value = noise(gen);

      if (currentHour == 23){
         currentHour = 0;
      }

      lightLevel = lightLevels[currentHour];
      currentHour++;

      lightLevel += static_cast<int>(noise_value);
    }

};


namespace py = pybind11;

PYBIND11_MODULE(BH1750, handle) {
    handle.doc() = "BH1750Library Python wrapper";

    py::class_<BH1750Library>(handle, "BH1750Library")
        .def(py::init<>())
        .def("readLightLevel", &BH1750Library::readLightLevel)
        .def("setLightLevel", &BH1750Library::setLightLevel)
        .def("generateSimulatedLightLevel", &BH1750Library::generateSimulatedLightLevel);
}