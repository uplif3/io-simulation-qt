# io_controller.py
from PySide6.QtCore import QObject
from models.io_model import IOModel
from views.io_view import IOView

class IOViewController(QObject):
    def __init__(self, view: IOView, model: IOModel, serialService=None, parent=None):
        super().__init__(parent)
        self.view = view
        self.model = model
        self.serialService = serialService
        self.setupBindings()

    def setupBindings(self):
        for i, chk in enumerate(self.view.switches):
            chk.stateChanged.connect(lambda state, index=i: self.setSwitch(index, state))
        for i, btn in enumerate(self.view.buttons):
            btn.clicked.connect(lambda checked, index=i: self.toggleButton(index))
        self.view.slider0.valueChanged.connect(self.setScale0)
        self.view.slider1.valueChanged.connect(self.setScale1)
        self.view.buttonKeyChanged.connect(self.setButtonKey)

    def setSwitch(self, index, state):
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

    def setButtonKey(self, index, state):
        self.model.buttons[index] = state
        self.sendButtons()

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
        self.model.setLedsFromHex(hexData)
