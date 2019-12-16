#include <avr/wdt.h> //Watchdog timer (WDT) library
#include <math.h> 
//Basics: Ctrl-Shift-M run; Crtl-U upload code;

//ARDUINO_LI_v3
//K. Fujiwara
//2016/12/15
// Redid RTD box to conform with better system designed for the
// Strontium experiment.  Includes flow meters and piezo buzzer.

int flowPIN_INLET=3;//2/22/2016
int flowPIN_OUTLET=5;//2/22/2016
int flow_INLET=0;
int flow_OTULET=0;

int tempHigh=50;
int tempLow=15;

const int buzzer = 52;
int S3=53;
int S2=51;
int S1=49;
int S0=47;

unsigned int statusArray[16]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
unsigned int flowArray[8]={0,102,0,0,0,0,0,0};

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
//Adafruit_ADS1115 ads; //Define ads command

//SETUP AND HANDSHAKING**************************************************************
void setup ()
{
  pinMode(S0, OUTPUT);//initialize the digital out pins as outputs
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  Serial.begin(9600);//Hand shakes the bit rate for communication with the computer.  
//  ads.begin();
//  ads.setGain(GAIN_TWOTHIRDS);   
  Serial.flush();  
  stringComplete = false; 
  //printTemps();
  

  pinMode(0,INPUT);
  pinMode(1,INPUT);
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  pinMode(5,INPUT);
  pinMode(6,INPUT);
  pinMode(7,INPUT);
  Serial.println("\rArduino is ready");
}

void serialEvent() 
{
  while (Serial.available()) {
     char inChar = (char)Serial.read(); 
     if (inChar == '\r' || inChar=='\n') 
      stringComplete = true;    
   else 
     inputString += inChar;   
  }
}
//************************************************************************** 
void loop() {
  //printTemps();
  //delay(2000)
  
  if (stringComplete) {    
    inputString = "";
    stringComplete = false;
    Serial.write('\r');
    for (int k=0; k<16; k++){
      Serial.write('0');
      Serial.write('\r');
      Serial.println(statusArray[k]);}
//      Serial.write(lowByte(statusArray[k]));
//    }
//
    for (int k=0; k<8; k++){
      Serial.write('\r');
      Serial.println(flowArray[k]);
//      Serial.write(lowByte(flowArray[k]));
    }
    Serial.write('\n');
    
  }
  fakeUpdate(); 
  
}
//************************************************************************** 


void fakeUpdate()
{
  statusArray[0]=random(20000,20000);
  statusArray[1]=random(15000,17000);
  statusArray[2]=random(10000,20000);
  statusArray[3]=random(25000,26000);
  statusArray[4]=random(27000,28000);
  statusArray[5]=random(29000,30000);
  statusArray[6]=random(31000,32000);
  statusArray[7]=random(33000,34000);  
  statusArray[8]=random(33000,34000);  
  statusArray[9]=random(33000,34000);  
  statusArray[10]=random(33000,34000);  
  statusArray[11]=random(33000,34000);  
  statusArray[12]=random(33000,34000);  
  statusArray[13]=random(33000,34000);  
  statusArray[14]=random(33000,34000);  
  statusArray[15]=random(33000,34000);

  int bit_precision = 10;
  for(int i=0; i<8; i++){
    flowArray[i] = random(0,pow(2,bit_precision)-1);
  }

}
//
////Based upon the 4051BE pin outs.  Set the channels to correspond with the 3 bit input.
//void chooseChannel(int channel)
//{
//  int A=LOW;
//  int B=LOW;
//  int C=LOW;
//  int D=LOW;
//  
//  if (channel==0){
//    A=LOW;
//    B=LOW;
//    C=LOW;
//    D=LOW;}
//    if (channel==1){
//    A=HIGH;
//    B=LOW;
//    C=LOW;
//    D=LOW;}
//  if (channel==2){
//    A=LOW;
//    B=HIGH;
//    C=LOW;
//    D=LOW;}
//  if (channel==3){    
//    A=HIGH;
//    B=HIGH;
//    C=LOW;
//    D=LOW;}
//  if (channel==4){
//     A=LOW;
//     B=LOW;
//     C=HIGH;
//     D=LOW;}
//  if (channel==5){
//    A=HIGH;
//    B=LOW;
//    C=HIGH;
//    D=LOW;}
//  if (channel==6){
//    A=LOW;
//    B=HIGH;
//    C=HIGH;
//    D=LOW;}
//  if (channel==7){
//    A=HIGH;
//    B=HIGH;
//    C=HIGH;
//    D=LOW;}
//   if (channel==8){
//    A=LOW;
//    B=LOW;
//    C=LOW;
//    D=HIGH;}
//    if (channel==9){
//      A=HIGH;
//      B=LOW;
//     C=LOW;
//      D=HIGH;}
//   if (channel==10){
//      A=LOW;
//     B=HIGH;
//     C=LOW;
//     D=HIGH;}
//   if (channel==11){
//     A=HIGH;
//     B=HIGH;
//     C=LOW;
//     D=HIGH;}
//   if (channel==12){
//     A=LOW;
//     B=LOW;
//     C=HIGH;
//     D=HIGH;}
//   if (channel==13){
//     A=HIGH;
//     B=LOW;
//     C=HIGH;
//     D=HIGH;}
//   if (channel==14){
//     A=LOW;
//     B=HIGH;
//     C=HIGH;
//     D=HIGH;}
//   if (channel==15){
//     A=HIGH;
//     B=HIGH;
//     C=HIGH;
//     D=HIGH;}    
//  digitalWrite(S0, A);
//  digitalWrite(S1, B);
//  digitalWrite(S2, C);  
//  digitalWrite(S3, D);
//}

//void updateMe(){
//  for (int i=0;i<16;i++){
//    chooseChannel(i);    
//    statusArray[i] = ads.readADC_Differential_2_3();//*.1875mV
//
//    /*
//    if (i<8) 
//    {        
//       if (!(statusArray[i]<convertToBit(tempHigh) && statusArray[i]>convertToBit(tempLow))){      
//         tone(buzzer, 2050);
//         delay(1000);        // ...for 1 sec
//         noTone(buzzer);     // Stop sound...
//       }
//     
//    }*/
//  }
//
//
//
//  for (int i=0;i<8;i++)
//  {
//    flowArray[i]=analogRead(i);
//  }  
//}
//
//void printTemps(){
//    for (int i=0;i<9;i++){
//        chooseChannel(i);    
//        int value=ads.readADC_Differential_2_3();//*.1875mV
//        Serial.print(i);
//        Serial.print(":");
//        Serial.print(((value*.1875-2.5)/2.5-100)*2.5586);
//        Serial.println();
//      }
//      Serial.println("*******************");
//      
//
//  }
//
//  float convertToBit(float temp)
//  {
//    return (temp/2.5586+100)*2.5/0.1875;
//  }
//  
//  

  
 
