# io_view.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QGridLayout, QHBoxLayout,
    QCheckBox, QPushButton, QSlider
)
from PySide6.QtCore import Qt, Signal  

from widgets.led_widget import LEDWidget

class IOView(QWidget):
    buttonKeyChanged = Signal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setupUi()
        self.setFocus()

    def setupUi(self):
        grid = QGridLayout(self)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(5)
        self.setLayout(grid)

        label_leds = QLabel("LEDs:")
        grid.addWidget(label_leds, 0, 0)
        self.ledContainer = QWidget(self)
        self.ledLayout = QHBoxLayout(self.ledContainer)
        self.ledLayout.setSpacing(5)
        self.ledContainer.setLayout(self.ledLayout)
        grid.addWidget(self.ledContainer, 0, 1)

        self.leds = []
        for i in range(8):
            led = LEDWidget(radius=10, parent=self.ledContainer)
            self.leds.insert(0, led)  
            self.ledLayout.addWidget(led)
            label = QLabel(f"LED {7-i}")
            self.ledLayout.addWidget(label)

        label_switches = QLabel("Switches:")
        grid.addWidget(label_switches, 1, 0)
        self.switchContainer = QWidget(self)
        self.switchLayout = QHBoxLayout(self.switchContainer)
        self.switchLayout.setSpacing(5)
        self.switches = []
        for i in range(8):
            chk = QCheckBox(f"SW {7-i}")
            self.switches.insert(0, chk)  
            self.switchLayout.addWidget(chk)
        self.switchContainer.setLayout(self.switchLayout)
        grid.addWidget(self.switchContainer, 1, 1)

        label_buttons = QLabel("Buttons:")
        grid.addWidget(label_buttons, 2, 0)
        self.buttonContainer = QWidget(self)
        self.buttonLayout = QHBoxLayout(self.buttonContainer)
        self.buttonLayout.setSpacing(5)
        self.buttons = []
        for i in range(4):
            btn = QPushButton(f"BTN {3-i}")
            self.buttons.insert(0, btn)  
            self.buttonLayout.addWidget(btn)
        self.buttonContainer.setLayout(self.buttonLayout)
        grid.addWidget(self.buttonContainer, 2, 1)

        label_scale0 = QLabel("Scale0:")
        grid.addWidget(label_scale0, 3, 0)
        self.slider0 = QSlider(Qt.Horizontal)
        self.slider0.setMinimum(0)
        self.slider0.setMaximum(1023)
        self.slider0.setTickInterval(256)
        self.slider0.setTickPosition(QSlider.TicksBelow)
        grid.addWidget(self.slider0, 3, 1)
        self.valueLabel0 = QLabel("0")
        grid.addWidget(self.valueLabel0, 3, 2)
        self.slider0.valueChanged.connect(lambda value: self.valueLabel0.setText(str(value)))

        label_scale1 = QLabel("Scale1:")
        grid.addWidget(label_scale1, 4, 0)
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(1023)
        self.slider1.setTickInterval(256)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        grid.addWidget(self.slider1, 4, 1)
        self.valueLabel1 = QLabel("0")
        grid.addWidget(self.valueLabel1, 4, 2)
        self.slider1.valueChanged.connect(lambda value: self.valueLabel1.setText(str(value)))

    def bindModel(self, model):
        model.ledChanged.connect(self.updateLED)

    def updateLED(self, index, state):
        if 0 <= index < len(self.leds):
            self.leds[index].setOn(state)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key == Qt.Key_1:
            self.handleButtonKey(3, True)
        elif key == Qt.Key_2:
            self.handleButtonKey(2, True)
        elif key == Qt.Key_3:
            self.handleButtonKey(1, True)
        elif key == Qt.Key_4:
            self.handleButtonKey(0, True)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key == Qt.Key_1:
            self.handleButtonKey(3, False)
        elif key == Qt.Key_2:
            self.handleButtonKey(2, False)
        elif key == Qt.Key_3:
            self.handleButtonKey(1, False)
        elif key == Qt.Key_4:
            self.handleButtonKey(0, False)
        else:
            super().keyReleaseEvent(event)

    def handleButtonKey(self, index, state: bool):
        btn = self.buttons[index]
        btn.setDown(state)
        self.buttonKeyChanged.emit(index, state)
