from PyQt5.QtWidgets import QComboBox,QFormLayout, QAction, qApp, QMainWindow, QWidget, QLineEdit, QGridLayout,QLabel, QApplication
import pyqtgraph as pg
import Backend.water_interlock as wl
import Backend.quantities as q
import sys
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
import enum 
from datetime import timedelta


tsensor = wl.TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
fsensor = wl.FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)

w = wl.WaterInterlock("COM4", 9600)
w.setDataStructure(structure = ((16, tsensor), (8, fsensor)))

class SettingsWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.settings = QSettings("WeldLab", "Interlock Monitor")
        
        #set layout
        self.initlayout()
        #create combo for update frequency
        self.timeCombo()

    #form layout
    def initlayout(self):
        layout = QFormLayout()
        
        #layout.addRow(QLabel("Update Time:"), )
        self.setLayout(layout)
    def timeCombo(self):
        self.combotime = QComboBox()
        self.combotime.addItem("1 s")
        self.combotime.addItem("5 s")
        self.combotime.addItem("20 s")
        self.combotime.addItem("40 s")
        self.combotime.addItem("200 s")
        self.combotime.addItem("3600 s")
        self.combotime.currentIndexChanged.connect(lambda index: self.selectionchange(index, "update_time"))
        self.layout().addRow(QLabel("Update Time:"),self.combotime)
    def selectionchange(self, i, key):
        text = self.combotime.itemText(i)
        self.saveSetting(key, text)

    def saveSetting(self, key : str, value : str):
        settings = QSettings('WeldLab', 'Interlock Monitor')
        settings.setValue(key, value)
        #settings.setValue('mylist', json.dumps(self.mylist))
    def loadSetting(self, key):
        settings = QSettings('WeldLab', 'Interlock Monitor')
        return settings.value(key)

class SettingUpdateTime(Setting):
    ONE_SECOND = timedelta(seconds=1)
    TWO_SECOND = timedelta(seconds=2)
    FIVE_SECOND = timedelta(seconds=5)
    FIFTEEN_SECOND = timedelta(seconds=15)
    ONE_MINUTE = timedelta(minutes=1)
    TEN_MINUTE = timedelta(minutes=10)

class Setting(enum.Enum):
    def __init__(key :str):
        self.key = key
        self.values = setting_values
    def set_current_value()
    def save(self):
        settings = QSettings('WeldLab', 'Interlock Monitor')
        settings.setValue(self.key, value)







    

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



