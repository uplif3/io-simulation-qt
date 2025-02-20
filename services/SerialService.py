import serial
import threading
from serial.tools import list_ports
from PySide6.QtCore import QObject, Signal, Slot

class SerialService(QObject):
    # Qt-Signale
    connected = Signal()
    disconnected = Signal()
    dataReceived = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_port = None
        self.reading_thread = None
        self.running = False
        self.isConnected = False

    def listComPorts(self):
        ports = list_ports.comports()
        return [port.device for port in ports]

    @Slot(str, int)
    def connectPort(self, port_name, baud_rate=9600):
        self.disconnectPort()

        try:
            self.serial_port = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                timeout=0.1
            )
            self.isConnected = True
            print(f"SerialService: Port {port_name} mit Baud {baud_rate} geöffnet.")
            self.connected.emit()
            self.start_reading()
            return True
        except Exception as e:
            print(f"SerialService: Konnte Port {port_name} nicht öffnen! Error: {e}")
            self.serial_port = None
            self.isConnected = False
            return False

    def start_reading(self):
        if self.serial_port is None or not self.serial_port.is_open:
            print("SerialService: Port ist nicht offen – kann nicht lesen!")
            return

        self.running = True

        def read_thread():
            while self.running:
                try:
                    line = self.serial_port.readline()
                    if line:
                        line_str = line.decode('utf-8', errors='replace').strip()
                        if line_str:
                            self.dataReceived.emit(line_str)
                except Exception as e:
                    print("SerialService: Exception im Lese-Thread:", e)
                    break

            print("SerialService: Lese-Thread beendet.")

        self.reading_thread = threading.Thread(target=read_thread, daemon=True)
        self.reading_thread.start()

    @Slot()
    def disconnectPort(self):
        self.running = False
        if self.reading_thread:
            self.reading_thread.join(timeout=1)
            self.reading_thread = None

        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("SerialService: Port geschlossen.")

        was_connected = self.isConnected
        self.isConnected = False
        self.serial_port = None

        if was_connected:
            self.disconnected.emit()

    def write(self, message):
        if self.serial_port and self.serial_port.is_open:
            try:
                data = message + "\n"
                self.serial_port.write(data.encode('utf-8'))
            except Exception as e:
                print("SerialService: Fehler beim Senden:", e)
        else:
            print("SerialService: Port nicht offen, kann nicht senden!")

    def is_open(self):
        return self.serial_port is not None and self.serial_port.is_open
