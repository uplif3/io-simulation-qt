# widgets/segment_colon.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class SegmentColon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isOn = False
        self.setFixedSize(10, 100)  

    def setIsOn(self, value: bool):
        self._isOn = value
        self.update()

    def getIsOn(self):
        return self._isOn

    isOn = property(getIsOn, setIsOn)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        color = QColor("red") if self._isOn else QColor("dimgray")

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(1, 16, 8, 8)
        painter.drawEllipse(1, 60, 8, 8)
