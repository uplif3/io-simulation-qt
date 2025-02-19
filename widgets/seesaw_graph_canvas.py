from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt

class SeesawGraphCanvas(QWidget):
    def __init__(self, width=600, height=150, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

        self.GRAPH_WIDTH      = width
        self.GRAPH_HEIGHT     = height
        self.GRAPH_MAX_POINTS = 200

        self.referenceData    = [float('nan')] * self.GRAPH_MAX_POINTS
        self.ballData         = [float('nan')] * self.GRAPH_MAX_POINTS
        self.angleData        = [float('nan')] * self.GRAPH_MAX_POINTS

        self.currentIndex     = 0
        self.count            = 0

    def updateGraphData(self, reference, ball, angle):
        refScaled   = (reference / 0.6) * (self.GRAPH_HEIGHT / 2.0)
        ballScaled  = (ball / 0.6)      * (self.GRAPH_HEIGHT / 2.0)
        angleScaled = (angle / 15.0)    * (self.GRAPH_HEIGHT / 2.0)

        self.referenceData[self.currentIndex] = refScaled
        self.ballData[self.currentIndex]      = ballScaled
        self.angleData[self.currentIndex]     = angleScaled

        self.currentIndex += 1
        if self.currentIndex >= self.GRAPH_MAX_POINTS:
            self.currentIndex = 0

        if self.count < self.GRAPH_MAX_POINTS:
            self.count += 1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        baseX = 10
        baseY = 10

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.black))
        painter.drawRect(baseX, baseY, self.GRAPH_WIDTH, self.GRAPH_HEIGHT)

        gridPen = QPen(QColor(0x40, 0x40, 0x40), 1)
        painter.setPen(gridPen)
        for x in range(0, self.GRAPH_WIDTH + 1, 50):
            painter.drawLine(baseX + x, baseY, baseX + x, baseY + self.GRAPH_HEIGHT)
        for y in range(0, self.GRAPH_HEIGHT + 1, 30):
            painter.drawLine(baseX, baseY + y, baseX + self.GRAPH_WIDTH, baseY + y)

        refColor   = QColor(0xFC, 0xF8, 0x00)
        ballColor  = QColor(0xF0, 0xF0, 0xF0)
        angleColor = QColor(0x00, 0x4D, 0xE6)

        if self.GRAPH_MAX_POINTS > 1:
            xStep = self.GRAPH_WIDTH / (self.GRAPH_MAX_POINTS - 1)
        else:
            xStep = self.GRAPH_WIDTH

        self._drawRingCurve(painter, self.referenceData, refColor, xStep, baseX, baseY)
        self._drawRingCurve(painter, self.ballData,      ballColor, xStep, baseX, baseY)
        self._drawRingCurve(painter, self.angleData,     angleColor, xStep, baseX, baseY)

        cursorX = baseX + self.currentIndex * xStep
        painter.setPen(QPen(QColor("orange"), 1))
        painter.drawLine(cursorX, baseY, cursorX, baseY + self.GRAPH_HEIGHT)

        painter.end()

    def _drawRingCurve(self, painter, dataList, color, xStep, baseX, baseY):
        pen = QPen(color, 2)
        painter.setPen(pen)

        lastIndex = self.count - 1
        for i in range(lastIndex):
            i2 = i + 1
            if i2 == self.currentIndex:
                continue

            y1 = dataList[i]
            y2 = dataList[i2]
            if (y1 != y1) or (y2 != y2): 
                continue

            x1 = baseX + i  * xStep
            x2 = baseX + i2 * xStep
            midY = baseY + self.GRAPH_HEIGHT / 2.0
            painter.drawLine(x1, midY - y1, x2, midY - y2)
