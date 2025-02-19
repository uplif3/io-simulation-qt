import serial
import threading
from serial.tools import list_ports

class SerialService:
    def __init__(self):
        self.serial_port = None
        self.reading_thread = None
        self.running = False

    def open_port(self, port_name, baud_rate):
        self.close_port() 
        try:
            self.serial_port = serial.Serial(port=port_name, baudrate=baud_rate, timeout=0.1)
            print(f"SerialService: Port {port_name} mit Baud {baud_rate} geöffnet.")
            return True
        except Exception as e:
            print(f"SerialService: Konnte Port {port_name} nicht öffnen! Error: {e}")
            self.serial_port = None
            return False

    def start_reading(self, data_callback):
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
                            data_callback(line_str)
                except Exception as e:
                    print("SerialService: Exception im Lese-Thread:", e)
                    break
            print("SerialService: Lese-Thread beendet.")

        self.reading_thread = threading.Thread(target=read_thread, daemon=True)
        self.reading_thread.start()

    def close_port(self):
        self.running = False
        if self.reading_thread:
            self.reading_thread.join(timeout=1)
            self.reading_thread = None
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("SerialService: Port geschlossen.")
        self.serial_port = None

    def write(self, message):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(message.encode('utf-8'))
            except Exception as e:
                print("SerialService: Fehler beim Senden:", e)
        else:
            print("SerialService: Port nicht offen, kann nicht senden!")

    def is_open(self):
        return self.serial_port is not None and self.serial_port.is_open
    
    def list_ports(self):
        ports = list_ports.comports()
        return [port.device for port in ports]
