#include <ArduinoSTL.h>
#include <array>
//#include <avr/wdt.h> //Watchdog timer (WDT) library
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
        virtual int read() =0;
    private:
        virtual int open() = 0;
        
       
};

template<int N>
class Multiplexer{
    //Class to interface with a Multiplexer of N bits
    public:
        std::array<std::pair<int, int>, N> pins; //array with pairs (pin, status: HIGH, LOW)
        //Constructors:
        Multiplexer() = default;
        Multiplexer(std::array<int, N> _pins, int default_state = LOW){
            this.set_pins(_pins, default_state);
        }
        //Methods:
        int set_pins(std::array<int, N> _pins, int default_state = LOW){
            int count = 0;
            for(auto&& pin: _pins){
                pins[count].first = pin;
                pins[count].second = default_state;
                pinMode(pin, OUTPUT);//initialize the digital out pins as outputs
                ++count;
            }
            return 1;
        }
        
        int set_channel(int channel){
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
                    Serial.println("Channel is wrong! Channel needs to be between 0 and 15.");
                    break;
                }
                this->set_pin(0, A);
                this->set_pin(1, B);
                this->set_pin(2, C);
                this->set_pin(3, D);
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


};
class TempSensorAdafruit : Sensor {
    int channel;
    public:
        TempSensorAdafruit() = default;
        TempSensorAdafruit(int chan){
            channel = chan;
            open();
        }
        int set_multiplexer_pins(int S0, int S1, int S2, int S3){
            multiplexer.set_pins((std::array<int, 4>){S0, S1, S2, S3});
        }
        int read(){
            multiplexer.set_channel(channel);
            return 2;
        }
        int set_channel(int chan){
            channel = chan;
            this->open();
        }
    protected:
        Adafruit_ADS1115 ads; //Object used to control adc
        Multiplexer<4> multiplexer; //Object used to control multiplexer
    private:
        
       
        int open(){
            ads.begin();
            ads.setGain(GAIN_TWOTHIRDS);
            return 1;
        };
        
};

void setup(){
TempSensorAdafruit(1);
//Temperature Sensor array:
//TempSensorAdafruit::set_multiplexer_pins(47, 49, 51, 53);
std::array<TempSensorAdafruit, 16> temp_sensors;
int i =0;
for(auto&& tempsensor:temp_sensors){
    tempsensor.set_channel(i);
    tempsensor.set_multiplexer_pins(47, 49, 51, 53);
    ++i;
}

};

void loop(){

};
