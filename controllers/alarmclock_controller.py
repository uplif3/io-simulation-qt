# controllers/alarmclock_controller.py
from PySide6.QtCore import QObject

class AlarmclockViewController(QObject):
    def __init__(self, view, model, parent=None):
        super().__init__(parent)
        self.view = view
        self.model = model
        self.updateView()

    def setHexString(self, hexStr: str):
        self.model.setHexString(hexStr)
        self.updateView()

    def handleIncomingData(self, data: str):
        self.setHexString(data)

    def updateView(self):
        self.view.hoursTens.setDigit(self.model.hoursTens)
        self.view.hoursOnes.setDigit(self.model.hoursOnes)
        self.view.minutesTens.setDigit(self.model.minutesTens)
        self.view.minutesOnes.setDigit(self.model.minutesOnes)
        self.view.colon.setIsOn(self.model.colonOn)
        self.view.alarmLabel.setVisible(self.model.alarmActive)
        self.view.beepLabel.setVisible(self.model.beepActive)
