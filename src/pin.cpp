
class pin {
private:
    int n;
    bool io;
    bool hl = false;

public:
    pin(int n_, bool io_):
    n(n_),
    io(io_)
    {}

    void digitalWrite(bool highLow){
        hl = highLow;
    }
};