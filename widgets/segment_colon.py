# widgets/segment_colon.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import Qt, Property

class SegmentColon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isOn = False
        self.setFixedSize(20, 100)

    def getIsOn(self):
        return self._isOn

    def setIsOn(self, value: bool):
        self._isOn = value
        self.update()

    isOn = Property(bool, getIsOn, setIsOn)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opacity = 1.0 if self._isOn else 0.1
        painter.setOpacity(opacity)
        painter.setBrush(QBrush(QColor("dimgray")))
        # Zeichne oberen Punkt
        radius = 4
        painter.drawEllipse((self.width() - 2*radius) / 2, self.height() * 0.2, 2*radius, 2*radius)
        # Zeichne unteren Punkt
        painter.drawEllipse((self.width() - 2*radius) / 2, self.height() * 0.6, 2*radius, 2*radius)
