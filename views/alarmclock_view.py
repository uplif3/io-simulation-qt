# views/alarmclock_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from widgets.segment_digit import SegmentDigit
from widgets.segment_colon import SegmentColon

class AlarmclockView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter)
        mainLayout.setSpacing(10)

        title = QLabel("Alarm Clock", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        mainLayout.addWidget(title)

        hboxDigits = QHBoxLayout()
        hboxDigits.setAlignment(Qt.AlignCenter)
        hboxDigits.setSpacing(10)
        self.hoursTens = SegmentDigit(self)
        self.hoursOnes = SegmentDigit(self)
        self.colon = SegmentColon(self)
        self.minutesTens = SegmentDigit(self)
        self.minutesOnes = SegmentDigit(self)
        hboxDigits.addWidget(self.hoursTens)
        hboxDigits.addWidget(self.hoursOnes)
        hboxDigits.addWidget(self.colon)
        hboxDigits.addWidget(self.minutesTens)
        hboxDigits.addWidget(self.minutesOnes)
        mainLayout.addLayout(hboxDigits)

        hboxStatus = QHBoxLayout()
        hboxStatus.setAlignment(Qt.AlignCenter)
        hboxStatus.setSpacing(20)
        self.alarmLabel = QLabel("ALARM", self)
        self.alarmLabel.setStyleSheet("color: red; font-weight: bold;")
        self.beepLabel = QLabel("BEEP", self)
        self.beepLabel.setStyleSheet("color: orange; font-weight: bold;")
        hboxStatus.addWidget(self.alarmLabel)
        hboxStatus.addWidget(self.beepLabel)
        mainLayout.addLayout(hboxStatus)

        self.setLayout(mainLayout)
