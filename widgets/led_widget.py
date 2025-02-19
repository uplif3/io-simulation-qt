# led_widget.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt

class LEDWidget(QWidget):
    def __init__(self, radius=20, parent=None):
        """
        Erstellt ein rundes LED-Widget mit dem angegebenen Radius.
        :param radius: Der Radius der LED in Pixeln.
        """
        super().__init__(parent)
        self._isOn = False
        self._radius = radius
        self.setFixedSize(int(self._radius * 2), int(self._radius * 2))

    def setOn(self, state: bool):
        """
        Schaltet die LED an oder aus und zeichnet neu.
        """
        self._isOn = state
        self.update()

    def isOn(self) -> bool:
        return self._isOn

    def paintEvent(self, event):
        """
        Zeichnet die LED als Kreis mit passender Farbe.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.eraseRect(self.rect())

        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        if self._isOn:
            fillColor = QColor("green")
        else:
            fillColor = QColor("darkgreen")
        painter.setBrush(QBrush(fillColor))

        painter.drawEllipse(0, 0, self.width(), self.height())

        if self._isOn:
            glowColor = QColor(50, 255, 50, 128)  
            painter.setBrush(QBrush(glowColor))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                self._radius * 0.2,
                self._radius * 0.2,
                self._radius * 1.6,
                self._radius * 1.6
            )
