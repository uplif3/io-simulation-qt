import sys
import serial.tools.list_ports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QComboBox, QPushButton, QLabel,
    QGridLayout, QToolBar, QStatusBar, QVBoxLayout
)
from PySide6.QtCore import QObject, Signal, Slot, Qt

from services.SerialService import SerialService
from views.text_view import TextView
from controllers.log_controller import LogViewController

from views.io_view import IOView
from controllers.io_controller import IOViewController
from models.io_model import IOModel

from views.alarmclock_view import AlarmclockView
from controllers.alarmclock_controller import AlarmclockViewController
from models.alarmclock_model import AlarmclockModel

from views.seesaw_view import SeesawView
from controllers.seesaw_controller import SeesawController
from models.seesaw_model import SeesawModel

class QtSerialService(QObject):
    """
    Adapter für den asynchronen SerialService.
    Er stellt Methoden und Signale bereit, um den Service in die Qt-Umgebung einzubinden.
    """
    connected = Signal()
    disconnected = Signal()
    dataReceived = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_service = SerialService()
        self.isConnected = False

    def listComPorts(self):
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]

    @Slot(str)
    def connectPort(self, portName):
        if not self.isConnected:
            if self.serial_service.open_port(portName, 9600):
                self.isConnected = True
                self.connected.emit()
                self.serial_service.start_reading(self._on_data_received)
                print(f"Verbunden mit {portName}")
            else:
                print(f"Fehler beim Verbinden mit {portName}")
        else:
            print("Bereits verbunden")

    @Slot()
    def disconnectPort(self):
        if self.isConnected:
            self.serial_service.close_port()
            self.isConnected = False
            self.disconnected.emit()
            print("Verbindung getrennt")
        else:
            print("Keine Verbindung vorhanden")

    def _on_data_received(self, data):
        self.dataReceived.emit(data)

    def write(self, message):
        """
        Sende eine Nachricht an den seriellen Port, gefolgt von einem Zeilenumbruch.
        """
        self.serial_service.write(message + "\n")


class MainWindow(QMainWindow):
    def __init__(self, serialService):
        super().__init__()
        self.setWindowTitle("GUI mit Serial & Log Service")
        self.serialService = serialService
        self.initUI()

    def initUI(self):
        toolbar = QToolBar("Haupt-Toolbar", self)
        self.addToolBar(toolbar)

        self.comboPorts = QComboBox(self)
        self.comboPorts.addItems(self.serialService.listComPorts())
        toolbar.addWidget(QLabel("COM-Port: "))
        toolbar.addWidget(self.comboPorts)

        self.btnConnect = QPushButton("Verbinden", self)
        self.btnConnect.clicked.connect(self.onConnect)
        toolbar.addWidget(self.btnConnect)

        self.btnDisconnect = QPushButton("Trennen", self)
        self.btnDisconnect.clicked.connect(self.onDisconnect)
        toolbar.addWidget(self.btnDisconnect)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        grid = QGridLayout(centralWidget)

        self.leftContainer = QWidget(self)
        self.leftLayout = QVBoxLayout(self.leftContainer)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(5)

        self.ioView = IOView()
        self.ioModel = IOModel()
        self.ioView.bindModel(self.ioModel)
        self.ioController = IOViewController(self.ioView, self.ioModel, self.serialService)

        self.alarmclockView = AlarmclockView()
        self.alarmclockModel = AlarmclockModel()
        self.alarmclockController = AlarmclockViewController(self.alarmclockView, self.alarmclockModel)

        self.seesawView = SeesawView()
        self.seesawModel = SeesawModel()
        self.seesawController = SeesawController(self.seesawModel, self.seesawView)

        self.left_views = []
        self.setLeftViews([self.ioView])  
        grid.addWidget(self.leftContainer, 0, 0, 2, 1)

        self.rightContainer = QWidget(self)
        self.rightLayout = QVBoxLayout(self.rightContainer)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(5)

        self.logView = TextView(self)
        self.logController = LogViewController(self.logView)

        self.debugView = TextView(self)
        self.debugController = LogViewController(self.debugView)

        right_views = [self.logView, self.debugView]
        for view in right_views:
            self.rightLayout.addWidget(view)
            self.rightLayout.setStretchFactor(view, 1)

        grid.addWidget(self.rightContainer, 0, 1, 2, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)  
        grid.setColumnStretch(1, 2)  

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.serialService.connected.connect(lambda: self.statusBar.showMessage("Verbunden", 3000))
        self.serialService.disconnected.connect(lambda: self.statusBar.showMessage("Getrennt", 3000))
        self.serialService.dataReceived.connect(self.onDataReceived)
        

    def setLeftViews(self, new_views):
        while self.leftLayout.count() > 0:
            item = self.leftLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        for view in new_views:
            self.leftLayout.addWidget(view)
            self.leftLayout.setStretchFactor(view, 1)
        self.left_views = new_views
        self.leftContainer.update()

    @Slot(str)
    def onDataReceived(self, data):
        if data.startswith("dL"):
            msg = data.replace("LOG:", "").strip()
            self.logController.handleIncomingData(msg)
        elif data.startswith("dS"):
            if data.startswith("dS0"):
                self.setLeftViews([self.ioView])
            elif data.startswith("dS1"):
                self.setLeftViews([self.alarmclockView, self.ioView])
            elif data.startswith("dS2"):
                self.setLeftViews([self.seesawView, self.ioView])

        elif data.startswith("dD"):
            self.debugController.handleIncomingData(data)
        elif data.startswith("d0"):
            self.ioController.handleIncomingData(data[2:])
        elif data.startswith("d1"):
            self.alarmclockController.handleIncomingData(data[2:])
        elif data.startswith("d2"):
            self.seesawController.handleIncomingData(data[2:])
        else:
            self.debugController.handleIncomingData(data)

    @Slot()
    def onConnect(self):
        portName = self.comboPorts.currentText()
        self.serialService.connectPort(portName)

    @Slot()
    def onDisconnect(self):
        self.serialService.disconnectPort()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    serialService = QtSerialService()
    window = MainWindow(serialService)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
