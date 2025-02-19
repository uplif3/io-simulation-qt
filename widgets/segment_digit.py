# widgets/segment_digit.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class SegmentDigit(QWidget):
    """
    Entspricht deinem JavaFX SegmentDigit:
    - Hat eine 'digit'-Property (String).
    - Beim Setzen wird 'updateSegments(digit)' aufgerufen.
    - Jedes Segment wird als Rechteck oder gezeichnetes Element realisiert.
    Hier machen wir es minimal, du kannst es beliebig ausbauen.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._digit = "0"
        self.setFixedSize(60, 100)  # Entspricht dem Java-FXML: prefWidth="60", prefHeight="100"

    def setDigit(self, value: str):
        self._digit = value
        self.update()

    def getDigit(self):
        return self._digit

    digit = property(getDigit, setDigit)

    def paintEvent(self, event):
        """
        Minimalbeispiel: Wir zeichnen 7 Rechtecke.
        Basierend auf self._digit schalten wir die Segmente an/aus.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Segment-Logik
        segAOn = segBOn = segCOn = segDOn = segEOn = segFOn = segGOn = False
        d = self._digit

        if   d == "0": segAOn=segBOn=segCOn=segDOn=segEOn=segFOn=True
        elif d == "1": segBOn=segCOn=True
        elif d == "2": segAOn=segBOn=segDOn=segEOn=segGOn=True
        elif d == "3": segAOn=segBOn=segCOn=segDOn=segGOn=True
        elif d == "4": segBOn=segCOn=segFOn=segGOn=True
        elif d == "5": segAOn=segCOn=segDOn=segFOn=segGOn=True
        elif d == "6": segAOn=segCOn=segDOn=segEOn=segFOn=segGOn=True
        elif d == "7": segAOn=segBOn=segCOn=True
        elif d == "8": segAOn=segBOn=segCOn=segDOn=segEOn=segFOn=segGOn=True
        elif d == "9": segAOn=segBOn=segCOn=segDOn=segFOn=segGOn=True

        # Farben
        colorOn = QColor("red") 
        colorOff = QColor("gray")

        # Koordinaten an Java-FXML anlehnen:
        # A = oben
        painter.fillRect(5, 0, 50, 8, colorOn if segAOn else colorOff)
        # B = oben rechts
        painter.fillRect(55, 8, 8, 40, colorOn if segBOn else colorOff)
        # C = unten rechts
        painter.fillRect(55, 52, 8, 40, colorOn if segCOn else colorOff)
        # D = unten
        painter.fillRect(5, 92, 50, 8, colorOn if segDOn else colorOff)
        # E = unten links
        painter.fillRect(0, 52, 8, 40, colorOn if segEOn else colorOff)
        # F = oben links
        painter.fillRect(0, 8, 8, 40, colorOn if segFOn else colorOff)
        # G = Mitte
        painter.fillRect(5, 46, 50, 8, colorOn if segGOn else colorOff)
