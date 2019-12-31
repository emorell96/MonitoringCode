from PyQt5.QtWidgets import QComboBox,QFormLayout, QAction, qApp, QMainWindow, QWidget, QLineEdit, QGridLayout,QLabel, QApplication
import pyqtgraph as pg
import Backend.water_interlock as wl
import Backend.quantities as q
import sys
from PyQt5.QtCore import Qt, QSettings, QVariant
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtGui import QIcon, QColor
import enum 
import aenum
from datetime import timedelta
from collections.abc import Iterable

tsensor = wl.TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
fsensor = wl.FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)

w = wl.WaterInterlock("COM4", 9600)
w.setDataStructure(structure = ((16, tsensor), (8, fsensor)))
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
        #if len(cls) == 0:

        for elem in cls:
            cls.combo.addItem(str(elem))
        cls.combo.currentIndexChanged.connect(cls.selectionchange)
        cls.combo.setCurrentIndex(current)
        return cls.combo
    @classmethod
    def classiter(cls): # iterate over class by giving all instances which have been instantiated
        return iter(cls.ports)
    def __str__(self):
        return str(self.value)+" Test "

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
        self.initSettings()
        #Serial ports settings:
        #ports = Ports()
        
        #set layout
        self.initlayout()
        Settings.initialize(self.layout())
        #create combo for update frequency and add to layout:
        # self.layout().addRow(UpdateTime.description, UpdateTime.create_combobox())
        # self.layout().addRow(ColorMarker.description, ColorMarker.create_combobox())
        # self.layout().addRow(Ports.description, Ports.create_combobox())
    def initSettings(self):
        self.settings = QSettings("WeldLab", "Interlock Monitor")
        # UpdateTime.set_key("update_time")
        # UpdateTime.set_description("Update Time:")
        # ColorMarker.set_key("marker_color")
        # ColorMarker.set_description("Marker Color:")
        # Ports.set_key("serial_port")
        # Ports.set_description("Serial Port:")
        # SettingsWindow.settings.append(UpdateTime)
        #SettingsWindow.settings.append()
    #form layout
    def initlayout(self):
        layout = QFormLayout()
        
        #layout.addRow(QLabel("Update Time:"), )
        self.setLayout(layout)
    # def timeCombo(self):
    #     self.combotime = QComboBox()
    #     self.combotime.addItem("1 s")
    #     self.combotime.addItem("5 s")
    #     self.combotime.addItem("20 s")
    #     self.combotime.addItem("40 s")
    #     self.combotime.addItem("200 s")
    #     self.combotime.addItem("3600 s")
    #     self.combotime.currentIndexChanged.connect(lambda index: self.selectionchange(index, "update_time"))
    #     self.layout().addRow(QLabel("Update Time:"),self.combotime)
    # def selectionchange(self, i, key):
    #     text = self.combotime.itemText(i)
    #     self.saveSetting(key, text)

    # def saveSetting(self, key : str, value : str):
    #     settings = QSettings('WeldLab', 'Interlock Monitor')
    #     settings.setValue(key, value)
    #     #settings.setValue('mylist', json.dumps(self.mylist))
    def loadSetting(self, key):
        settings = QSettings('WeldLab', 'Interlock Monitor')
        return settings.value(key)








class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #self.edit = QLineEdit('TSLA', self)
        #self.edit.editingFinished.connect(self.setTicker)
        #self.label = QLabel('-', self)
        
        
        
        self.setGeometry(100, 100, 1000, 500)
        self.guiplot = pg.PlotWidget()
        self.guiplot.enableAutoRange()
        self.setWindowTitle('Water Monitoring')
        self.set_exit()
        self.set_settings()
        self.set_menu()
        
        # layout = QGridLayout(self)
        # #layout.addWidget(self.edit, 0, 0)
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
        #Option menu
        optionsMenu = menubar.addMenu('&Options')
        optionsMenu.addAction(self.settingsAct)
    
    def open_settings(self):
        self.settings = SettingsWindow()
        self.settings.show()

    def setTicker(self):
        #contract = Stock(self.edit.text(), 'SMART', 'USD')

        # self.bars = ib.reqHistoricalData(
        #     contract,
        #     endDateTime='',
        #     durationStr='500 S',
        #     barSizeSetting='5 secs',
        #     whatToShow='MIDPOINT',
        #     useRTH=True,
        #     formatDate=1,
        #     keepUpToDate=True)
        self.update()

    def update(self):
        #currBar = self.bars[-1] if self.bars else None
        # if self.prevBar != currBar:
        #     self.prevBar = currBar
        #     self.label.setText(str(currBar))

        #     # Get only the close values
        #     #bclose =  [b.close for b in self.bars]
        #     # Plot only last 100 items
        #     self.guiplot.plot(bclose[-100:], clear=True, )
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



