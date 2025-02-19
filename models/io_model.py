from PySide6.QtCore import QObject, Signal

class IOModel(QObject):
    ledChanged = Signal(int, bool)

    NUM_LEDS = 8
    NUM_SWITCHES = 8
    NUM_BUTTONS = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.leds = [False] * IOModel.NUM_LEDS
        self.switches = [False] * IOModel.NUM_SWITCHES
        self.buttons = [False] * IOModel.NUM_BUTTONS
        self.scale0 = 0
        self.scale1 = 0

    def setLedsFromHex(self, hexVal: str):
        val = int(hexVal, 16)
        for i in range(IOModel.NUM_LEDS):
            new_state = ((val >> i) & 1) == 1
            if self.leds[i] != new_state:
                self.leds[i] = new_state
                self.ledChanged.emit(i, new_state)
        print("LEDs:", format(val, "08b"))

    def setSwitchesFromHex(self, hexVal: str):
        val = int(hexVal, 16)
        for i in range(IOModel.NUM_SWITCHES):
            self.switches[i] = ((val >> i) & 1) == 1

    def setButtonsFromHex(self, hexVal: str):
        val = int(hexVal, 16)
        for i in range(IOModel.NUM_BUTTONS):
            self.buttons[i] = ((val >> i) & 1) == 1

    def getButtonsAsHex(self) -> str:
        val = 0
        for i in range(IOModel.NUM_BUTTONS):
            if self.buttons[i]:
                val |= (1 << i)
        res = format(val, "02x")
        print("Buttons:", res)
        return res

    def getSwitchesAsHex(self) -> str:
        val = 0
        for i in range(IOModel.NUM_SWITCHES):
            if self.switches[i]:
                val |= (1 << i)
        return format(val, "02x")

    def getScale0AsHex(self) -> str:
        res = format(self.scale0, "04x")
        print("Scale0:", res)
        return res

    def getScale1AsHex(self) -> str:
        return format(self.scale1, "04x")
