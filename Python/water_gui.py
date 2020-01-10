from PyQt5.QtWidgets import QComboBox,QFormLayout, QAction, qApp, QMainWindow, QWidget, QLineEdit, QGridLayout,QLabel, QApplication
import pyqtgraph as pg
import Backend.water_interlock as wl
import Backend.quantities as q
import sys
from PyQt5.QtCore import Qt, QSettings, QVariant, QTimer
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtGui import QIcon, QColor
import enum 
import aenum
from datetime import timedelta
from collections.abc import Iterable

# tsensor = wl.TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
# fsensor = wl.FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)

# w = wl.WaterInterlock("COM4", 9600)
# w.setDataStructure(structure = ((16, tsensor), (8, fsensor)))
class classproperty:

    def __init__(self, func):
        self._func = func

    def __get__(self, obj, owner):
        return self._func(owner)

class Setting:
    default = QVariant()
    qsettings = QSettings('WeldLab', 'Interlock Monitor')
    #key = ""
    # def __new__(cls, value, description):
    #     obj = object.__new__(cls)
    #     obj._value_ = value
    #     obj.description = description
    #     return obj
    def __init__(self, _value, description = "", key = ""):
        #super().__init__()
        self._value = _value
        self.description = description
        self.key = key
    @classmethod
    def get_by_order(cls, index):
        #starts at 0
        i = 0
        for elem in cls:
            if index == i:
                return elem
            i += 1
        raise ValueError("Out of bounds!")

    @classmethod
    def set_key(cls, key):
        cls.key = key
        for elem in cls:
            elem.key = key
    @classmethod
    def set_description(cls, description):
        cls.description = description
        for elem in cls:
            elem.description = description
    # @classmethod
    # def set_value(cls, value):
    #     cls.current_value = value
    @classmethod
    def save(cls, value):
        cls.qsettings.setValue(cls.key, value)
    @classmethod
    def load(cls):
        try:
            v = cls.qsettings.value(cls.key, cls.default)
            return int(v)
        except:
            if v == None:
                return 0
            raise TypeError("Value is not an int")
    @classmethod
    def create_combobox(cls, current = 0):
        cls.combo = QComboBox()
        for elem in cls:
            cls.combo.addItem(str(elem))
        cls.combo.currentIndexChanged.connect(cls.selectionchange)
        cls.combo.setCurrentIndex(current)
        return cls.combo
    @classmethod
    def selectionchange(cls, i):
        text = cls.combo.itemText(i)
        #cls.set_value(i)
        cls.save(i)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)
    # @classproperty
    # def key(cls):
    #     return cls.key

class UpdateTime(Setting, enum.Enum):
    ONE_SECOND = timedelta(seconds=1)
    TWO_SECOND = timedelta(seconds=2)
    FIVE_SECOND = timedelta(seconds=5)
    FIFTEEN_SECOND = timedelta(seconds=15)
    ONE_MINUTE = timedelta(minutes=1)
    TEN_MINUTE = timedelta(minutes=10)
    #constants of class
    key = aenum.constant("update_time")
    description = aenum.constant("Update Time:")
    default = aenum.constant(TWO_SECOND)
    def __str__(self):
        s = self.value.total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{int(hours):02} hours {int(minutes):02} min {int(seconds):02} s"
        if minutes > 0:
            return f"{int(minutes):02} min {int(seconds):02} s"
        return f"{int(seconds):02} s"
class BaudRate(Setting, enum.Enum):
    STD = 9600


class ColorMarker(Setting, enum.Enum):
    RED = QColor(Qt.red)
    BLUE = QColor(Qt.blue)
    #constants
    key = aenum.constant("marker_color")
    description = aenum.constant("Marker Color:")
    default = aenum.constant(RED)
    def __str__(self):
        return str(self.value.name())
class PortsMeta(type):
    def __iter__(self):
        # Wanna iterate over a class? Then ask that class for iterator.
        return self.classiter()
    def __len__(self):
        return self.classlength()
    def __new__(cls, clsname, bases, dct):
        #print("I am here")
        return super(PortsMeta, cls).__new__(cls, clsname, bases, dct)
class Port(QSerialPortInfo):
    def __str__(self):
        return self.portName()
class Ports(Setting, metaclass = PortsMeta):
    #__metaclass__ = It
    ports = list(map(Port, QSerialPortInfo.availablePorts()))
    key = aenum.constant("serial_port")
    description = aenum.constant("Serial Port:")
    
    def __init__(self, _value = "", description = "", key = ""):
        super(Ports, self).__init__("")
        Ports.value = _value
        Ports.description = description
        Ports.key = key
        self.available_ports = QSerialPortInfo.availablePorts()
        for port in self.available_ports:
            Ports.ports.append(port)
    @classmethod
    def create_combobox(cls, current = 0):
        cls.combo = QComboBox()
        if len(cls) == 0:
            cls.combo.addItem("No COM Port Available")
        else:
            cls.combo.addItem("Select a Port")
        for elem in cls:
            cls.combo.addItem(str(elem))
        cls.combo.currentIndexChanged.connect(cls.selectionchange)
        cls.combo.setCurrentText(current)
        return cls.combo
    @classmethod
    def classiter(cls): # iterate over class by giving all instances which have been instantiated
        return iter(cls.ports)
    @classmethod
    def classlength(cls):
        return len(cls.ports)
    def __str__(self):
        return str(self.value)
    @classmethod
    def load(cls):
        try:
            v = cls.qsettings.value(cls.key, cls.default)
            # if v == None:
            #     return 0
            return str(v)
        except:
            raise TypeError("Value is not a COM port string")
    @classmethod
    def get_by_order(cls, index):
        return super(Ports, cls).get_by_order(int(index)-1)
class Settings(enum.Enum):
    #Enumeration of classes derived from Setting
    ut = UpdateTime
    cm = ColorMarker
    sp = Ports
    @classmethod
    def load_settings(cls):
        for elem in cls:
            elem.load()
    @classmethod
    def initialize(cls, layout):
        for setting in cls:
            layout.addRow(setting.value.description, setting.value.create_combobox(setting.value.load()))


class SettingsWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(100, 100, 1000, 500)
        #initialize any settings you need:
        self.initlayout()
        Settings.initialize(self.layout())
    #form layout
    def initlayout(self):
        layout = QFormLayout()
        
        #layout.addRow(QLabel("Update Time:"), )
        self.setLayout(layout)




class MainWindow(QMainWindow):
    tsensor = wl.TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
    fsensor = wl.FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)
    def __init__(self):   
        QMainWindow.__init__(self)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        #self.edit = QLineEdit('TSLA', self)
        #self.edit.editingFinished.connect(self.setTicker)
        #self.label = QLabel('-', self)
        self.setGeometry(100, 100, 1000, 500)
        self.guiplot = pg.PlotWidget()
        self.guiplot.enableAutoRange()
        self.curve = self.guiplot.plot(pen='r', symbol='o', connect='all')
        self.setWindowTitle('Water Monitoring')
        self.set_exit()
        self.set_connect()
        self.set_settings()
        self.set_menu()
        
        
        #self.setLayout(QGridLayout(self))
        self.setCentralWidget(self.guiplot)
        
        #self.guiplot.plot([1, 3], [2, 4])
        # #layout.addWidget(self.label, 1, 0)
        # layout.addWidget(self.guiplot, 2, 0, 3, 3)

        # self.prevBar = None
        # self.bars = None
        #self.setTicker()
        #ib.setCallback('updated', self.update)
    def set_exit(self):
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.exitAct = exitAct
    def set_connect(self):
        connectAct = QAction(QIcon('connect.png'), '&Connect', self)
        connectAct.setShortcut('Ctrl+C')
        connectAct.setStatusTip(f'Connect to Serial Port {Settings.sp.value.load()}')
        connectAct.triggered.connect(self.connect)
        self.connectAct = connectAct
    def connect(self):
        comport = Settings.sp.value.get_by_order(Settings.sp.value.load())
        print(f"Using {comport} for connection")
        self.w = wl.WaterInterlock(str(comport), 9600, poll_char="a", sol='\x02', eol='\x03')
        self.w.setDataStructure(structure = ((16, MainWindow.tsensor), (8, MainWindow.fsensor)))
        self.timer = QTimer()
        x = Settings.ut.value.load()
        t = Settings.ut.value.get_by_order(x)
        self.t0 = self.w.check()[0].time.timestamp()
        self.timer.timeout.connect(self.update)
        self.timer.start(t.value.total_seconds()*1000)
        
        self.chunksize = 2
        
        print("done")
    def set_settings(self):
        settingsAct = QAction(QIcon('settings.png'), '&Settings', self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.setStatusTip('Open Settings Pane')
        settingsAct.triggered.connect(self.open_settings)
        self.settingsAct = settingsAct
    def set_menu(self):
        
        menubar = self.menuBar()
        #file menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAct)
        fileMenu.addAction(self.connectAct)
        #Option menu
        optionsMenu = menubar.addMenu('&Options')
        optionsMenu.addAction(self.settingsAct)
    
    def open_settings(self):
        self.settings = SettingsWindow()
        self.settings.show()

    # def setTicker(self):
    #     #contract = Stock(self.edit.text(), 'SMART', 'USD')

    #     # self.bars = ib.reqHistoricalData(
    #     #     contract,
    #     #     endDateTime='',
    #     #     durationStr='500 S',
    #     #     barSizeSetting='5 secs',
    #     #     whatToShow='MIDPOINT',
    #     #     useRTH=True,
    #     #     formatDate=1,
    #     #     keepUpToDate=True)
    #     self.update()

    def update(self):
        print("iter")
        d = self.w.check()
        print(d)
        i = 0
        for data in d:
            self.curve.setData([d[0].time.timestamp()-self.t0], [d[0].value])
        # i+=1
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



