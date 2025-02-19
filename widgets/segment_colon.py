# widgets/segment_colon.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class SegmentColon(QWidget):
    """
    Entspricht deinem JavaFX SegmentColon:
    - Hat eine boolesche Property 'isOn'.
    - Zeichnet zwei Punkte (oben, unten) in grau oder weiß.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isOn = False
        self.setFixedSize(10, 100)  # prefWidth="10", prefHeight="100"

    def setIsOn(self, value: bool):
        self._isOn = value
        self.update()

    def getIsOn(self):
        return self._isOn

    isOn = property(getIsOn, setIsOn)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # DimGray, falls aus, oder White, falls an
        color = QColor("red") if self._isOn else QColor("dimgray")

        # Zeichne oben
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        # In Java-FXML war (layoutX=5, layoutY=20, radius=4)
        # Hier vereinfachen wir: kreiscenter=(5,20), radius=4 => ellipse(1..9,16..24)
        painter.drawEllipse(1, 16, 8, 8)

        # Zeichne unten
        painter.drawEllipse(1, 60, 8, 8)
