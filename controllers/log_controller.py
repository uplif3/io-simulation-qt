# log_controller.py
from PySide6.QtCore import QObject

class LogViewController(QObject):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        self.autoScroll = True
        self.connectSignals()
    
    def connectSignals(self):
        self.view.btnClear.clicked.connect(self.clearLog)
        self.view.btnSync.clicked.connect(self.toggleSync)
    
    def clearLog(self):
        self.view.logTextArea.clear()
    
    def toggleSync(self):
        self.autoScroll = not self.autoScroll
        self.view.autoScroll = self.autoScroll
        if self.autoScroll:
            self.view.btnSync.setText("Unsync")
            self.view.scrollToBottom()
        else:
            self.view.btnSync.setText("Sync")
    
    def handleIncomingData(self, data: str):
        self.view.appendLog(data)
