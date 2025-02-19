# widgets/segment_digit.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt, Property

class SegmentDigit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._digit = "0"
        self.setFixedSize(60, 100)

    def getDigit(self):
        return self._digit

    def setDigit(self, value: str):
        self._digit = value
        self.update()

    digit = Property(str, getDigit, setDigit)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Farben für an/aus
        colorOn = QColor("dimgray")
        colorOff = QColor("lightgray")
        
        # Bestimme, welche Segmente an sind (A, B, C, D, E, F, G)
        segments = {
            "A": False, "B": False, "C": False, "D": False,
            "E": False, "F": False, "G": False
        }
        d = self._digit
        if d == "0": segments = {"A":True, "B":True, "C":True, "D":True, "E":True, "F":True, "G":False}
        elif d == "1": segments = {"A":False, "B":True, "C":True, "D":False, "E":False, "F":False, "G":False}
        elif d == "2": segments = {"A":True, "B":True, "C":False, "D":True, "E":True, "F":False, "G":True}
        elif d == "3": segments = {"A":True, "B":True, "C":True, "D":True, "E":False, "F":False, "G":True}
        elif d == "4": segments = {"A":False, "B":True, "C":True, "D":False, "E":False, "F":True, "G":True}
        elif d == "5": segments = {"A":True, "B":False, "C":True, "D":True, "E":False, "F":True, "G":True}
        elif d == "6": segments = {"A":True, "B":False, "C":True, "D":True, "E":True, "F":True, "G":True}
        elif d == "7": segments = {"A":True, "B":True, "C":True, "D":False, "E":False, "F":False, "G":False}
        elif d == "8": segments = {"A":True, "B":True, "C":True, "D":True, "E":True, "F":True, "G":True}
        elif d == "9": segments = {"A":True, "B":True, "C":True, "D":True, "E":False, "F":True, "G":True}

        # Zeichne die Segmente als Rechtecke:
        w, h = self.width(), self.height()
        margin = 5
        thickness = 8
        painter.setPen(Qt.NoPen)
        def drawSeg(segOn, x, y, width, height):
            painter.setBrush(QBrush(colorOn if segOn else colorOff))
            painter.drawRect(x, y, width, height)

        # Segment A (oben)
        drawSeg(segments["A"], margin, 0, w - 2*margin, thickness)
        # Segment D (unten)
        drawSeg(segments["D"], margin, h - thickness, w - 2*margin, thickness)
        # Segment G (Mitte)
        drawSeg(segments["G"], margin, (h-thickness)/2, w - 2*margin, thickness)
        # Segment F (oben links)
        drawSeg(segments["F"], 0, margin, thickness, (h - 3*margin) / 2)
        # Segment E (unten links)
        drawSeg(segments["E"], 0, (h+margin)/2, thickness, (h - 3*margin) / 2)
        # Segment B (oben rechts)
        drawSeg(segments["B"], w - thickness, margin, thickness, (h - 3*margin) / 2)
        # Segment C (unten rechts)
        drawSeg(segments["C"], w - thickness, (h+margin)/2, thickness, (h - 3*margin) / 2)
