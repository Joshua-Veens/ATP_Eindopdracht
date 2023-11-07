#include "A4988.cpp"
#include <unistd.h>
#include <iostream>

int main() {
    A4988 motorDriver;
    motorDriver.setDirection(true);

    while( true ){
        motorDriver.takeSteps(100);
        sleep(5);
        std::cout << std::endl;
    }

    return 0;
}