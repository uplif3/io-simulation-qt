from PySide6.QtCore import Qt, QObject, QEvent, Slot
from services.SerialService import SerialService
from views.main_view import MainView

from views.io_view import IOView
from models.io_model import IOModel
from controllers.io_controller import IOViewController

from views.alarmclock_view import AlarmclockView
from controllers.alarmclock_controller import AlarmclockViewController
from models.alarmclock_model import AlarmclockModel

from views.seesaw_view import SeesawView
from controllers.seesaw_controller import SeesawController
from models.seesaw_model import SeesawModel
from datetime import datetime


class MainController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.serialService = SerialService()
        self.mainView = MainView()

        self.ioModel = IOModel()
        self.ioView = IOView()
        self.ioView.bindModel(self.ioModel)
        self.ioController = IOViewController(self.ioView, self.ioModel, self.serialService)

        self.alarmclockModel = AlarmclockModel()
        self.alarmclockView = AlarmclockView()
        self.alarmclockController = AlarmclockViewController(self.alarmclockView, self.alarmclockModel)

        self.seesawModel = SeesawModel()
        self.seesawView = SeesawView()
        self.seesawController = SeesawController(self.seesawModel, self.seesawView)

        self.mainView.setLeftViews([self.ioView])

        ports = self.serialService.listComPorts() 
        self.mainView.setPortList(ports)

        self.mainView.btnConnect.clicked.connect(self.onConnect)
        self.mainView.btnDisconnect.clicked.connect(self.onDisconnect)

        self.serialService.connected.connect(lambda: self.mainView.showStatus("Verbunden", 3000))
        self.serialService.disconnected.connect(lambda: self.mainView.showStatus("Getrennt", 3000))
        self.serialService.dataReceived.connect(self.onDataReceived)

    def showMainWindow(self):
        """Zeigt das Hauptfenster an."""
        self.mainView.resize(800, 600)
        self.mainView.show()
        self.mainView.activateWindow()
        self.mainView.raise_()

    @Slot()
    def onConnect(self):
        """COM-Port aus der ComboBox lesen und verbinden."""
        portName = self.mainView.currentPort()
        if portName:
            self.serialService.connectPort(portName)
        else:
            self.mainView.showStatus("Kein Port ausgewählt!", 2000)

    @Slot()
    def onDisconnect(self):
        """Trennen des COM-Ports."""
        self.serialService.disconnectPort()


    @Slot(str)
    def onDataReceived(self, data):
        """Verarbeitet eingehende Daten vom Seriellen Port."""
        if data.startswith("dL"):
            self.mainView.logController.handleIncomingData(data[2:])

        elif data.startswith("dS"):
            if data.startswith("dS0"):
                self.mainView.setLeftViews([self.ioView])
            elif data.startswith("dS1"):
                self.mainView.setLeftViews([self.alarmclockView, self.ioView])
            elif data.startswith("dS2"):
                self.mainView.setLeftViews([self.seesawView, self.ioView])

        elif data.startswith("d0"):
            self.ioController.handleIncomingData(data[2:])

        elif data.startswith("d1"):
            self.alarmclockController.handleIncomingData(data[2:])

        elif data.startswith("d2"):
            self.seesawController.handleIncomingData(data[2:])

        elif data.startswith("?"):
            if data.startswith("?T"):
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                self.serialService.write(f"dT{current_time}")
            elif data.startswith("?01"):
                self.ioController.sendSwitches()
            elif data.startswith("?02"):
                self.ioController.sendButtons()
            elif data.startswith("?0a"):
                self.ioController.sendScale0()
            elif data.startswith("?0b"):
                self.ioController.sendScale1()
        else:
            self.mainView.debugController.handleIncomingData(data)


    def eventFilter(self, obj, event):
        """Globaler Event-Filter (falls installiert)."""
        if event.type() == QEvent.KeyPress:
            return self.handleGlobalKeyPress(event)
        elif event.type() == QEvent.KeyRelease:
            return self.handleGlobalKeyRelease(event)
        return False

    def handleGlobalKeyPress(self, event):
        if event.isAutoRepeat():
            return False 

        key = event.key()
        if key == Qt.Key_1:
            self.ioController.setButtonKey(3, True)
            return True
        elif key == Qt.Key_2:
            self.ioController.setButtonKey(2, True)
            return True
        elif key == Qt.Key_3:
            self.ioController.setButtonKey(1, True)
            return True
        elif key == Qt.Key_4:
            self.ioController.setButtonKey(0, True)
            return True
        return False

    def handleGlobalKeyRelease(self, event):
        if event.isAutoRepeat():
            return False

        key = event.key()
        if key == Qt.Key_1:
            self.ioController.setButtonKey(3, False)
            return True
        elif key == Qt.Key_2:
            self.ioController.setButtonKey(2, False)
            return True
        elif key == Qt.Key_3:
            self.ioController.setButtonKey(1, False)
            return True
        elif key == Qt.Key_4:
            self.ioController.setButtonKey(0, False)
            return True
        return False
