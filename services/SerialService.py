import serial
import threading
from serial.tools import list_ports

class SerialService:
    def __init__(self):
        self.serial_port = None
        self.reading_thread = None
        self.running = False

    def open_port(self, port_name, baud_rate):
        """
        Öffnet den angegebenen seriellen Port mit der angegebenen Baudrate.
        :param port_name: Name des Ports (z.B. "COM3" oder "/dev/ttyUSB0")
        :param baud_rate: Baudrate (z.B. 9600)
        :return: True, wenn erfolgreich geöffnet, sonst False.
        """
        self.close_port()  # Vorherige Verbindung schließen, falls vorhanden.
        try:
            # timeout=0.1 bewirkt, dass readline() nicht ewig blockiert.
            self.serial_port = serial.Serial(port=port_name, baudrate=baud_rate, timeout=0.1)
            print(f"SerialService: Port {port_name} mit Baud {baud_rate} geöffnet.")
            return True
        except Exception as e:
            print(f"SerialService: Konnte Port {port_name} nicht öffnen! Error: {e}")
            self.serial_port = None
            return False

    def start_reading(self, data_callback):
        """
        Startet einen Thread, der kontinuierlich Daten vom seriellen Port liest
        und Zeilen (oder komplette Nachrichten) an die Callback-Funktion übergibt.
        
        :param data_callback: Funktion, die pro empfangener (Text‑)Zeile aufgerufen wird.
                              Falls die Callback Funktion UI-Updates ausführt, muss auf
                              Thread-Sicherheit geachtet werden.
        """
        if self.serial_port is None or not self.serial_port.is_open:
            print("SerialService: Port ist nicht offen – kann nicht lesen!")
            return

        self.running = True

        def read_thread():
            while self.running:
                try:
                    # Lese eine Zeile (bis zum Zeilenumbruch) oder bis timeout
                    line = self.serial_port.readline()
                    if line:
                        # Decodiere die empfangenen Bytes und entferne Zeilenumbrüche
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
        """
        Schließt den Port und stoppt den Lese-Thread.
        """
        self.running = False
        if self.reading_thread:
            self.reading_thread.join(timeout=1)
            self.reading_thread = None
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("SerialService: Port geschlossen.")
        self.serial_port = None

    def write(self, message):
        """
        Sendet einen String an den offenen Port (z.B. ein Kommando + "\n").
        """
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(message.encode('utf-8'))
            except Exception as e:
                print("SerialService: Fehler beim Senden:", e)
        else:
            print("SerialService: Port nicht offen, kann nicht senden!")

    def is_open(self):
        """
        Gibt zurück, ob der serielle Port geöffnet ist.
        """
        return self.serial_port is not None and self.serial_port.is_open
    
    def list_ports(self):
        """
        Gibt eine Liste der verfügbaren seriellen Ports zurück.
        :return: Liste der verfügbaren Ports.
        """
        ports = list_ports.comports()
        return [port.device for port in ports]
