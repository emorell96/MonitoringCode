class VoltUnit:
    V, mV, microV = 1, 1000, 1000000 
    def __init__(self, Type):
        if(type(Type) is int):
            self.value = Type
        elif(type(Type) is str):
            #initialize with V, mV, µV etc
            if(Type == "V"):
                self.value = self.V
            elif(Type == "mV"):
                self.value = self.mV
            elif(Type == u"µV"):
                self.value = self.microV
            else:
                print("Error!! Voltage Unit not recognized, defaulting to volts.")
                self.value = self.V 
    def __str__(self):
        if self.value == VoltUnit.V:
            return 'V'
        if self.value == VoltUnit.mV:
            return 'mV'
        if self.value == VoltUnit.microV:
            return u'µV'
    def __eq__(self,y):
       return self.value==y.value
class Voltage:
    def __init__(self, value, unit : VoltUnit = VoltUnit("V"), time = None):
        self.time = time
        self.value = value
        self.unit = unit
    def transform(self, to_unit : VoltUnit):
        return (to_unit.value/self.unit.value)*self.value
    def __str__(self, time = False):
        return "{0:.3e} {1}".format(self.value, self.unit) if not time else "{0:.3e} {1} at {2}".format(self.value, self.unit, self.time.strftime('%Y-%m-%d %H:%M:%S.%f'))
    def __repr__(self):
        return str(self)
class TempUnit:
    Celsius, Fahrenheit, Kelvin = range(3)
    def __init__(self, Type):
        self.value = Type
    def __str__(self):
        if self.value == TempUnit.Celsius:
            return u"ºC"
        if self.value == TempUnit.Fahrenheit:
            return 'F'
        if self.value == TempUnit.Kelvin:
            return 'K'
        
    def __eq__(self,y):
       return self.value==y.value
class Temperature:
    def __init__(self, value, unit: TempUnit):
        self.value = value
        self.unit = unit
    def __str__(self):
        return "{0:.1f} {1}".format(self.value, self.unit)
    def __repr__(self):
        return str(self)