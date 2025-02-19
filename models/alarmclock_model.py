# models/alarmclock_model.py
class AlarmclockModel:
    def __init__(self):
        self.raw = ""
        self.hoursTens = "0"
        self.hoursOnes = "0"
        self.minutesTens = "0"
        self.minutesOnes = "0"
        self.alarmActive = False
        self.beepActive = False
        self.colonOn = False

        self.segMap = {
            "3f": "0",
            "06": "1",
            "5b": "2",
            "4f": "3",
            "66": "4",
            "6d": "5",
            "7d": "6",
            "07": "7",
            "7f": "8",
            "6f": "9"
        }

    def setHexString(self, hexData: str):
        try:
            b3 = int(hexData[0:2], 16)
            b2 = int(hexData[2:4], 16)
            b1 = int(hexData[4:6], 16)
            b0 = int(hexData[6:8], 16)
            self.hoursTens = self.decodeDigit(b3)
            self.hoursOnes = self.decodeDigit(b2)
            self.minutesTens = self.decodeDigit(b1)
            self.minutesOnes = self.decodeDigit(b0)
            self.alarmActive = (b2 & 0x80) != 0
            self.beepActive  = (b0 & 0x80) != 0
            self.colonOn     = (b1 & 0x80) != 0
        except Exception as ex:
            self.clearProperties()

    def clearProperties(self):
        self.hoursTens = " "
        self.hoursOnes = " "
        self.minutesTens = " "
        self.minutesOnes = " "
        self.alarmActive = False
        self.beepActive = False
        self.colonOn = False

    def decodeDigit(self, b):
        value = b & 0x7F  # Entferne das MSB
        hexStr = f"{value:02x}".lower()
        return self.segMap.get(hexStr, "?")
