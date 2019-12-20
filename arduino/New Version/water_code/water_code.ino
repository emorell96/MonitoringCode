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
        bool debug = false;
        virtual int read() =0;
        virtual int set_pin(int i) = 0;
        void set_debug(bool deb){debug = deb;}
    protected:
        virtual int open() = 0;
        
       
};

class Multiplexer{
    //Class to interface with a Multiplexer of 4 bits
    public:
        std::array<std::pair<int, int>, 4> pins; //array with pairs (pin, status: HIGH, LOW)
        //Constructors:
        Multiplexer() = default;
        Multiplexer(std::array<int, 4> _pins, int default_state = LOW){
            this->set_pins(_pins, default_state);
        }
        //Methods:
        int set_pins(std::array<int, 4> _pins, int default_state = LOW){
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
                    Serial.println(F("Channel is wrong! Channel needs to be between 0 and 15."));
                    break;
            }
            this->set_pin(0, A);
            this->set_pin(1, B);
            this->set_pin(2, C);
            this->set_pin(3, D);
            success = 1;
            return success;

            }
        
        
    
    
        void set_pin(int n, int status){
            if(n>=4){
                Serial.println(F("Error! Pin is beyond the multiplexer pin number"));
                exit(EXIT_FAILURE);
            }
            pins[n].second = status;
            digitalWrite(pins[n].first, pins[n].second);
        }


};
class TempSensorAdafruit : public Sensor {
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
            if(debug){
                return random(15000,17000);
            }
            multiplexer.set_channel(channel);
            return ads_.readADC_Differential_2_3();
        }
        int set_pin(int chan){
            channel = chan;
            this->open();
            return 1;
        }
    protected:
        static Adafruit_ADS1115 ads_; //Object used to control adc
        static Multiplexer multiplexer; //Object used to control multiplexer
        int open(){
            ads_.begin();
            ads_.setGain(GAIN_TWOTHIRDS);
            return 1;
        };
        
};
//Definition of static multiplexer:
Multiplexer TempSensorAdafruit::multiplexer;
//Definition of static ads;
Adafruit_ADS1115 TempSensorAdafruit::ads_;
class FlowSensor : public Sensor{
    int pin;
    public:
        FlowSensor() = default;
        FlowSensor(int _pin){
            pin = _pin;
            open();
        }
        int set_pin(int _pin){
            pin = _pin;
            open();
        }
        int read(){
            if(debug){
                return random(1, 1023);
            }
            return analogRead(pin);
        }
    protected:
        int open(){
            pinMode(pin, INPUT);
            return 1;
        }
    
};
//  class Sensors //<std::array<SensorType, N>, ...>
// {
// private:
//     /* data */
// public:
//     Sensors(std::tuple structure)
//     void initialize(){
//         //iterate through
//     }
// };
//Temperature Sensor array:
//std::array<TempSensorAdafruit, 16> temp_sensors;
//FlowSensor array:
//std::array<FlowSensor, 8> flow_sensors;
//Sensors(std::make_tuple(std::make_tuple(TempSensorAdafruit, 16, ), std::make_tuple(FlowSensor, 8)) 


class SerialSensorInterface{
    
    public:
        char sol, eol, pollchar;
        bool recipient_ready = false;
        int baudrate;
        SerialSensorInterface(char _sol, char _eol, char _pollchar ,String _ready_msg, int _baudrate = 9600){
            begin(_sol, _eol, _pollchar,_ready_msg, _baudrate);
        }
        SerialSensorInterface() = default;
        void begin(char _sol, char _eol, char _pollchar, String _ready_msg, int _baudrate = 9600){
            sol = _sol;
            eol = _eol;
            pollchar = _pollchar;
            baudrate = _baudrate;
            Serial.begin(_baudrate);
            Serial.flush(); 
            send_msg(_ready_msg);
        }
        void polled(){
            //put inside loop()
            if(Serial.available()){
                char inChar = (char)Serial.read(); 
                if(inChar == pollchar){
                    //received the polling char:
                    //So send data
                    recipient_ready = true;
                }
            }
        }
        String format_msg(String msg){
            return sol+msg+eol;
        }
        void send_msg(String msg){
            Serial.print(format_msg(msg));
        }
        //template<size_t n>
        void ReadValues(Sensor* arr, size_t n){
            //It will only read values when asked by recipient.
            if(recipient_ready){
                for(auto i = arr; arr+n; ++i){
                    send_msg(String((i)->read()));
                }
            }
        }
};



//Temperature Sensor array:
std::array<TempSensorAdafruit, 16> temp_sensors;
//FlowSensor array:
std::array<FlowSensor, 8> flow_sensors;
SerialSensorInterface ser;

void setup(){
    ser.begin('\r','\n', '\n', F("Arduino is ready"));
    int i =0;
    for(auto&& tempsensor:temp_sensors){
        tempsensor.set_debug(true);
        tempsensor.set_pin(i);
        tempsensor.set_multiplexer_pins(47, 49, 51, 53);
        ++i;
    }
    i =0;
    for(auto&& flowsensor:flow_sensors){
        flowsensor.set_pin(i);
        ++i;
    }
};
void loop(){
    ser.polled();
    ser.ReadValues(temp_sensors.data(), temp_sensors.size()); //temp_sensors.size()
    ser.ReadValues(flow_sensors.data(), flow_sensors.size());
};
