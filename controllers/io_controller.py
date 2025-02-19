# io_controller.py
from PySide6.QtCore import QObject
from models.io_model import IOModel
from views.io_view import IOView

class IOViewController(QObject):
    def __init__(self, view: IOView, model: IOModel, serialService=None, parent=None):
        """
        :param view: Die zugehörige UI (IOView)
        :param model: Das Model, das den Zustand hält
        :param serialService: Eine Referenz zum SerialService, um serielle Nachrichten zu versenden
        """
        super().__init__(parent)
        self.view = view
        self.model = model
        self.serialService = serialService  # Referenz auf den SerialService
        self.setupBindings()

    def setupBindings(self):
        # Verbinde jeden Switch (CheckBox) mit dem Model und sende Statusänderungen
        for i, chk in enumerate(self.view.switches):
            chk.stateChanged.connect(lambda state, index=i: self.setSwitch(index, state))
        # Verbinde die Buttons (hier erfolgt ein Umschalten beim Klick)
        for i, btn in enumerate(self.view.buttons):
            btn.clicked.connect(lambda checked, index=i: self.toggleButton(index))
        # Verbinde die Slider
        self.view.slider0.valueChanged.connect(self.setScale0)
        self.view.slider1.valueChanged.connect(self.setScale1)

    def setSwitch(self, index, state):
        # In Qt entspricht Qt.Checked (in stateChanged) dem Wert 2
        self.model.switches[index] = (state == 2)
        self.sendSwitches()

    def toggleButton(self, index):
        self.model.buttons[index] = not self.model.buttons[index]
        self.sendButtons()

    def setScale0(self, value):
        self.model.scale0 = value
        self.sendScale0()

    def setScale1(self, value):
        self.model.scale1 = value
        self.sendScale1()

    def sendSwitches(self):
        hexVal = self.model.getSwitchesAsHex()
        message = "d01" + hexVal
        print("Sending switches:", message)
        if self.serialService is not None:
            self.serialService.write(message)

    def sendButtons(self):
        hexVal = self.model.getButtonsAsHex()
        message = "d02" + hexVal
        print("Sending buttons:", message)
        if self.serialService is not None:
            self.serialService.write(message)

    def sendScale0(self):
        hexVal = self.model.getScale0AsHex()
        message = "d0a" + hexVal
        print("Sending scale0:", message)
        if self.serialService is not None:
            self.serialService.write(message)

    def sendScale1(self):
        hexVal = self.model.getScale1AsHex()
        message = "d0b" + hexVal
        print("Sending scale1:", message)
        if self.serialService is not None:
            self.serialService.write(message)

    def handleIncomingData(self, hexData: str):
        print("IOViewController received:", hexData)
        # Update im Model anhand des Hex-Strings
        self.model.setLedsFromHex(hexData)