from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygonF
from PySide6.QtCore import Qt, QPointF
from math import radians, tan

class SeesawCanvas(QWidget):
    def __init__(self, width=600, height=300, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

        self._reference = 0.0
        self._ball = 0.0
        self._angle = 0.0
        self._boing = False

    def setData(self, reference, ball, angle, boing):
        self._reference = reference
        self._ball = ball
        self._angle = angle
        self._boing = boing
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        canvasWidth  = self.width()
        canvasHeight = self.height()

        bgColor = self.palette().window().color()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bgColor))
        painter.drawRect(0, 0, canvasWidth, canvasHeight)

        colorStand    = QColor(0x60, 0x60, 0x60)
        colorRamp     = QColor(0x00, 0x4D, 0xE6)
        colorBall     = QColor(0xF0, 0xF0, 0xF0)
        colorRef      = QColor(0xFC, 0xF8, 0x00)
        colorBoingOn  = QColor(0xCC, 0x00, 0x00)
        colorBoingOff = QColor(0x60, 0x60, 0x60)

        marginBottom = 10.0
        baseX        = canvasWidth / 2.0
        baseY        = canvasHeight - marginBottom

        seesawWidth  = 420.0
        standWidth   = 36.0
        standHeight  = 70.0
        rBall        = 9.0
        markerWidth  = 6.0
        markerHeight = 11.0

        # --- Stand (Dreieck) ---
        sp1x = baseX - standWidth / 2
        sp1y = baseY
        sp2x = baseX
        sp2y = baseY - standHeight
        sp3x = baseX + standWidth / 2
        sp3y = baseY

        standPolygon = QPolygonF([
            QPointF(sp1x, sp1y),
            QPointF(sp2x, sp2y),
            QPointF(sp3x, sp3y)
        ])

        painter.setBrush(QBrush(colorStand))
        painter.drawPolygon(standPolygon)

        # --- Reference-Marker ---
        markerRawX = self._reference / 0.6 * ((seesawWidth / 2) - 1.5 * rBall)
        markerRawY = 180.0 - 1.0

        m1x = baseX + (markerRawX - markerWidth)
        m1y = baseY - markerRawY
        m2x = baseX + (markerRawX + markerWidth)
        m2y = baseY - markerRawY
        m3x = baseX + markerRawX
        m3y = baseY - (markerRawY - markerHeight)

        refPolygon = QPolygonF([
            QPointF(m1x, m1y),
            QPointF(m2x, m2y),
            QPointF(m3x, m3y)
        ])
        painter.setBrush(colorRef)
        painter.drawPolygon(refPolygon)

        # --- Wippe ---
        angleRad      = radians(self._angle)
        seesawHalfW   = seesawWidth / 2.0
        seesawPivotY  = 90.0
        yOffset       = tan(angleRad) * seesawHalfW
        yLeft         = seesawPivotY + yOffset
        yRight        = seesawPivotY - yOffset

        rampP1x = baseX - seesawHalfW
        rampP1y = baseY - yLeft
        rampP2x = baseX + seesawHalfW
        rampP2y = baseY - yRight

        penRamp = QPen(colorRamp, 3.0)
        painter.setPen(penRamp)
        painter.drawLine(rampP1x, rampP1y, rampP2x, rampP2y)

        # --- Ball ---
        ballX = self._ball / 0.6 * seesawHalfW
        ballY = seesawPivotY - tan(angleRad) * ballX + rBall
        ballCenterX = baseX + ballX
        ballCenterY = baseY - ballY

        painter.setPen(Qt.NoPen)
        painter.setBrush(colorBall)
        painter.drawEllipse(ballCenterX - rBall, ballCenterY - rBall, 2*rBall, 2*rBall)

        # --- Boing! ---
        boingColor = colorBoingOn if self._boing else colorBoingOff
        painter.setPen(boingColor)
        painter.setFont(QFont("Verdana", 14))
        textX = baseX - seesawWidth / 2 - 40
        textY = baseY - 10
        painter.drawText(textX, textY, "Boing!")

        painter.end()
