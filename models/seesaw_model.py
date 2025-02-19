from math import sin, cos, radians

class SeesawModel:
    def __init__(self):
        self._reference = 0.0
        self._ball = 0.0
        self._angle = 0.0
        self._boing = False

    @property
    def reference(self):
        return self._reference

    @property
    def ball(self):
        return self._ball

    @property
    def angle(self):
        return self._angle

    @property
    def boing(self):
        return self._boing

    def updateFromPacket(self, packet: str):
        """
        Parst einen Packet-String und aktualisiert die Werte.
        Format (mind. 13 Zeichen):
        - Die ersten 4 Zeichen => Hex für reference
        - Die nächsten 4 Zeichen => Hex für ball
        - Die nächsten 4 Zeichen => Hex für angle
        - 1 Zeichen für boing ('t' => true, 'f' => false)
        """
        if not packet or len(packet) < 13:
            return

        try:
            rawReference = self._parseSignedHex(packet[0:4])
            rawBall      = self._parseSignedHex(packet[4:8])
            rawAngle     = self._parseSignedHex(packet[8:12])
            boingChar    = packet[12]

            self._reference = rawReference / 50000.0
            self._ball      = rawBall      / 50000.0
            self._angle     = rawAngle     / 2000.0
            self._boing     = (boingChar == 't')
        except ValueError:
            pass

    def _parseSignedHex(self, hexStr: str) -> int:
        num = int(hexStr, 16)
        if (num & 0x8000) != 0:
            num -= 0x10000
        return num
