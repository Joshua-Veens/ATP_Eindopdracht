#include <pybind11/pybind11.h>
#include <windows.h>
#include "pin.cpp"


class A4988 {
private:
    pin stepPin{3, false};
    pin dirPin{4, false};

public:
    A4988(){}

    void takeStep(){
        stepPin.digitalWrite(true);
        Sleep(1);
        stepPin.digitalWrite(false);
        Sleep(1);
    }

    void takeSteps(int n){
        for ( unsigned int i = 0; i < n; i++){
            takeStep();
        }
    }

    void setDirection(bool lr){
        dirPin.digitalWrite(lr);
    }

};

namespace py = pybind11;

PYBIND11_MODULE(A4988, handle) {
    handle.doc() = "A4988Library Python wrapper";

    py::class_<A4988>(handle, "A4988Library")
        .def(py::init<>())
        .def("takeSteps", &A4988::takeSteps)
        .def("setDirection", &A4988::setDirection);
}