# log_controller.py
from PySide6.QtCore import QObject

class LogViewController(QObject):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        self.autoScroll = True
        self.connectSignals()
    
    def connectSignals(self):
        # Verbinde die UI-Elemente mit den entsprechenden Methoden
        self.view.btnClear.clicked.connect(self.clearLog)
        self.view.btnSync.clicked.connect(self.toggleSync)
    
    def clearLog(self):
        """Löscht den Inhalt der Log-Ansicht."""
        self.view.logTextArea.clear()
    
    def toggleSync(self):
        """Wechselt zwischen automatischem und manuellem Scrollen."""
        self.autoScroll = not self.autoScroll
        self.view.autoScroll = self.autoScroll
        if self.autoScroll:
            self.view.btnSync.setText("Unsync")
            self.view.scrollToBottom()
        else:
            self.view.btnSync.setText("Sync")
    
    def handleIncomingData(self, data: str):
        """Fügt eingehende Daten als Logeintrag hinzu."""
        self.view.appendLog(data)
