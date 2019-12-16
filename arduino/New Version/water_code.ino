#include <array>
#include <avr/wdt.h> //Watchdog timer (WDT) library
#include <Wire.h> //Wire library needed for ADC communication
#include <Adafruit_ADS1015.h> //Adafruit ADC communication library


//ARDUINO_LI_v4
//Based on code by K. Fujiwara, Updated by E. Morell.
//12/16/2019

class Sensor{
    //Base class for Sensors.
    //The aim of this class is to standarize the way we talk to sensors using the arduino.
    //It will have a 
    public:
        virtual int get_value() = 0;
    private:
        virtual int open() = 0;
        virtual int read() =0;
       
}

template<int N>
class Multiplexer{
    //Class to interface with a Multiplexer of N bits
    public:
        std::array<std::pair<int, int>, N> pins; //array with pairs (pin, status: HIGH, LOW)
        Multiplexer(std::array<int, N> _pins, int default_state = LOW){
            int count = 0;
            for(auto&& pin: _pins){
                pins[count].first = pin;
                pins[count].second = default_state;
                ++count;
            }
        }
        int choose_channel(int channel){
            switch (N) //Different truth table depending on how many bits the multiplexer has. Default is not implemented so error.
            {
            case /* constant-expression */:
                /* code */
                break;
            
            default:
                break;
            }
        }
    
    private:
        void set_pin(int n, int status){
            if(n>=N){
                Serial.println("Error! Pin is beyond the multiplexer pin number");
                exit(EXIT_FAILURE);
            }
            pins[n].second = status;
        }

}
class TempSensorAdafruit : Sensor {
    Mu
    public:

    private:
        int read()
}