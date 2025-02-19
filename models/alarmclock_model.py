# models/alarmclock_model.py

class AlarmclockModel:
    """
    Entspricht deinem Java-AlarmclockModel. 
    Kein Signals/Slots – sondern reine Properties und 'setHexString(...)'.
    """
    def __init__(self):
        self.raw = ""
        self.hoursTens = "0"
        self.hoursOnes = "0"
        self.minutesTens = "0"
        self.minutesOnes = "0"
        self.alarmActive = False
        self.beepActive = False
        self.colonOn = False

        # Mapping der 7-Segment-Bitmasken
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
        """
        Genau wie im Java-Code: 
        - Byte 3 => hoursTens
        - Byte 2 => hoursOnes
        - Byte 1 => minutesTens
        - Byte 0 => minutesOnes
        - Flags: alarm=b2&0x80, beep=b0&0x80, colon=b1&0x80
        """
        try:
            b3 = int(hexData[0:2], 16)
            b2 = int(hexData[2:4], 16)
            b1 = int(hexData[4:6], 16)
            b0 = int(hexData[6:8], 16)

            self.hoursTens   = self.decodeDigit(b3)
            self.hoursOnes   = self.decodeDigit(b2)
            self.minutesTens = self.decodeDigit(b1)
            self.minutesOnes = self.decodeDigit(b0)

            self.alarmActive = (b2 & 0x80) != 0
            self.beepActive  = (b0 & 0x80) != 0
            self.colonOn     = (b1 & 0x80) != 0
        except Exception:
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
        value = b & 0x7F  # Entferne Bit 7
        hexStr = f"{value:02x}"
        return self.segMap.get(hexStr, "?")
