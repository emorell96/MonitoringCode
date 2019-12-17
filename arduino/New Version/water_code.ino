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
        virtual int read() =0;
    private:
        virtual int open() = 0;
        
       
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
        Multiplexer() = default;
        int choose_channel(int channel){
            int success = 0;
            switch (N) //Different truth table depending on how many bits the multiplexer has. Default is not implemented so error.
            {
            case 4:
                int A = LOW, B = LOW, C = LOW, D = LOW;
                switch (channel)
                {
                case 0:
                    A=LOW;
                    B=LOW;
                    C=LOW;
                    D=LOW;
                    break;
                case 1:
                    A=HIGH;
                    B=LOW;
                    C=LOW;
                    D=LOW;
                    break;
                case 2:
                    A=LOW;
                    B=HIGH;
                    C=LOW;
                    D=LOW;
                    break;
                case 3:
                    A=HIGH;
                    B=HIGH;
                    C=LOW;
                    D=LOW;
                    break;
                case 4:
                    A=LOW;
                    B=LOW;
                    C=HIGH;
                    D=LOW;
                    break;
                case 5:
                    A=HIGH;
                    B=LOW;
                    C=HIGH;
                    D=LOW;
                    break;
                case 6:
                    A=LOW;
                    B=HIGH;
                    C=HIGH;
                    D=LOW;
                    break;
                case 7:
                    A=HIGH;
                    B=HIGH;
                    C=HIGH;
                    D=LOW;
                    break;
                case 8:
                    A=LOW;
                    B=LOW;
                    C=LOW;
                    D=HIGH;
                    break;
                case 9:
                    A=HIGH;
                    B=LOW;
                    C=LOW;
                    D=HIGH;
                    break;
                case 10:
                    A=LOW;
                    B=HIGH;
                    C=LOW;
                    D=HIGH;
                    break;
                case 11:
                    A=HIGH;
                    B=HIGH;
                    C=LOW;
                    D=HIGH;
                    break;
                case 12:
                    A=LOW;
                    B=LOW;
                    C=HIGH;
                    D=HIGH;
                    break;
                case 13:
                    A=HIGH;
                    B=LOW;
                    C=HIGH;
                    D=HIGH;
                    break;
                case 14:
                    A=LOW;
                    B=HIGH;
                    C=HIGH;
                    D=HIGH;
                    break;
                case 15:
                    A=HIGH;
                    B=HIGH;
                    C=HIGH;
                    D=HIGH;
                    break;
                default:
                    Serial.println("Channel is wrong! Channel needs to be between 0 and 15.")
                    break;
                }
                this.set_pin(0, A);
                this.set_pin(1, B);
                this.set_pin(2, C);
                this.set_pin(3, D);
                success = 1;
                break;
            
            default:
                return success;
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
            digitalWrite(pins[n].first, pins[n].second);
        }


}
class TempSensorAdafruit : Sensor {
    int channel;
    public:
        TempSensorAdafruit(int chan){
            this.channel = chan;
        }

    private:
        static Multiplexer<4> multiplexer; //Object used to control multiplexer
        static Adafruit_ADS1115 ads; //Object used to control adc
        void open(){
            ads.begin();
            ads.setGain(GAIN_TWOTHIRDS);
        }
        void read()
}
