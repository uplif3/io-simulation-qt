# log_view.py
from PySide6.QtWidgets import QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class TextView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.autoScroll = True  
        self.setupUi()
        
    def setupUi(self):
        self.logTextArea = QTextEdit(self)
        self.logTextArea.setReadOnly(True)
        self.logTextArea.setLineWrapMode(QTextEdit.WidgetWidth)
        
        self.btnSync = QPushButton("Unsync", self)
        self.btnClear = QPushButton("Clear", self)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(self.logTextArea)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(10)
        buttonLayout.setAlignment(Qt.AlignLeft)
        buttonLayout.addWidget(self.btnSync)
        buttonLayout.addWidget(self.btnClear)
        
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
    
    def scrollToBottom(self):
        """Scrollt das Textfeld an das Ende."""
        scrollbar = self.logTextArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def appendLog(self, text: str):
        """Fügt einen neuen Logeintrag hinzu und scrollt gegebenenfalls nach unten."""
        self.logTextArea.append(text)
        if self.autoScroll:
            self.scrollToBottom()
