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
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(10)

        title = QLabel("Alarm Clock", self)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        vbox.addWidget(title)

        # Ziffernzeile (Stunden und Minuten)
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
        vbox.addLayout(hboxDigits)

        # Statuszeile
        hboxStatus = QHBoxLayout()
        hboxStatus.setAlignment(Qt.AlignCenter)
        hboxStatus.setSpacing(20)
        self.alarmLabel = QLabel("ALARM", self)
        self.alarmLabel.setStyleSheet("color: red; font-weight: bold;")
        self.beepLabel = QLabel("BEEP", self)
        self.beepLabel.setStyleSheet("color: orange; font-weight: bold;")
        hboxStatus.addWidget(self.alarmLabel)
        hboxStatus.addWidget(self.beepLabel)
        vbox.addLayout(hboxStatus)

        self.setLayout(vbox)
