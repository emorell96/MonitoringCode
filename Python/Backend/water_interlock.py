import serial
import io
import datetime
import quantities as q
import time
# class TempSensor:
#     #class to assure compatibility with old 16 bit rtd measurement scheme and the new ina 15C to 45C in 5V.
#     #the new scheme would allow for the use of the normal 10 bit or 12 bit precision adc converter. Hence it needs
#     #to know the adc bit resolution to properly transform an int to a temperature.
#     def __init__(self, adc_precision = 16, vmin = 0, vmax = 5):
#         self.adc_precision = adc_precision
#         self.vmin = vmin
#         self.vmax = vmax
#     def setType(self, type = "old"):
#         f = lambda t: 2.5586*(t*0.1875/2.5-100)
#         if type == "old":
#             self.conversion_function = f
#         if 
#         #2.5586*(temps*0.1875/2.5-100)
#         #0.191895 slope - ‭255.86‬ y intercept
#         #

class SerialData:
    def __init__(self, port, baud_rate = 9600, databits = 8, parity = serial.PARITY_NONE, eol = "\n", sol ="\r", poll_char = "\r",timeout = 1): #parity = "N" equal to None
        self.port = port
        self.baud_rate = baud_rate
        self.parity = parity
        self.eol = eol
        self.sol = sol
        self.timeout = timeout
        self.databits = 8
        self.poll_char = poll_char
        self.loop = 0

    def __open(self):
        self.ser = serial.Serial(self.port, self.baud_rate, parity=self.parity, timeout = self.timeout)
        self.__waitForArduino()
    def __close(self):
        self.ser.close()
    def __waitForArduino(self):

        # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
        # it also ensures that any bytes left over from a previous message are discarded            
        msg = ""
        while msg.find("Arduino is ready"):
            while self.ser.inWaiting() == 0:
                pass
            msg = self.__readData()
            

        print(msg)

    def __readData(self, bytes = 48):
        byteCount = -1     
        
        x = 'z'
        ck = ''
        #time.sleep(1)
        # wait for the start character
        while  x != self.sol: 
            x = self.ser.read().decode("ascii")

        while x != self.eol:
            if x != self.sol:
                ck = ck + x
                byteCount += 1
                
            x = self.ser.read(1).decode("ascii")
        return ck
    def __sendData(self, message):
        self.ser.write(message.encode())
    def readData(self, lines = 1, isint = True):
        """
        reads an int sent from a serial object where the message is first a begin message character
        and an end message charachter.
        """
        self.__open()
        self.__sendData(self.poll_char)
        data = []
        for i in range(lines):
            x = self.__readData()
            if isint:
                try:
                    x = int(x)
                except:
                    print("data is not an ASCII int")
            data.append(x)
        self.__close()
        return data
    def __int_to_temp(self, temp):
        return 2.5586*(temp*0.1875/2.5-100)


    # def readTemp(self):
    #     #data format from arduino is [b0, b1, b2, b3, b4, ... b47]
    #     #the first n bytes are temperature, and the rest are flows out of 48 bytes.
    #     with serial.Serial(self.port, self.baud_rate, parity=self.parity, timeout = self.timeout):
class Sensor:
    def __init__(self, unit, unittype, adc_precision = 10, vmin = 0, vmax = 5):
        self.unit = unit
        self.adc_precision = adc_precision
        self.vmin = vmin
        self.vmax = vmax
        self.conversion_function = lambda t: t
        self.unittype = unittype
        pass
    def value(self, v):
        pass
class TempSensorOld(Sensor):
    """
    Old sensors baser on the multiplexer
    """
    def _f(self, t):
        return 2.5586*(t*0.1875/2.5-100)
    def value(self, v):
        temp = self._f(v)
        return self.unittype(temp, self.unit)
class FlowSensor(Sensor):
    def setConversion(self, lfunc = lambda t: t):
        self.conversion_function = lfunc
    def value(self, dataint):
        flow = self.conversion_function((self.vmax - self.vmin)*dataint/(2**(self.adc_precision)-1))
        return self.unittype(flow, self.unit)

class WaterInterlock(SerialData):
    def setDataStructure(self, structure = ((16, TempSensorOld), (8, FlowSensor))):
        self.sensor_groups = structure
    def check(self):
        lines = 0
        for s in self.sensor_groups:
            lines += s[0]
        data = self.readData(lines)
        counter = 0
        fdata = []
        for s in self.sensor_groups:
            for i in range(s[0]):
                fdata.append(s[1].value(data[counter]))
                counter += 1
        return fdata

# test code:
tsensor = TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
fsensor = FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)

w = WaterInterlock("COM4", 9600, poll_char="a", sol='\x02', eol='\x03')
w.setDataStructure(structure = ((16, tsensor), (8, fsensor)))
print(w.check())