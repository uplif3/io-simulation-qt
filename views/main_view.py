from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QLabel, QComboBox, QPushButton, 
    QGridLayout, QWidget, QVBoxLayout, QStatusBar
)
from PySide6.QtCore import Qt
from views.text_view import TextView
from controllers.log_controller import LogViewController

class MainView(QMainWindow):
    """
    Reine View: Stellt ComboBox, Buttons, Layout für leftViews + rightViews bereit.
    Minimalste Logik.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GUI mit Serial & Log Service")

        self._initUI()

    def _initUI(self):
        toolbar = QToolBar("Haupt-Toolbar", self)
        self.addToolBar(toolbar)

        self.comboPorts = QComboBox(self)
        toolbar.addWidget(QLabel("COM-Port: "))
        toolbar.addWidget(self.comboPorts)

        self.btnConnect = QPushButton("Verbinden", self)
        toolbar.addWidget(self.btnConnect)

        self.btnDisconnect = QPushButton("Trennen", self)
        toolbar.addWidget(self.btnDisconnect)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        grid = QGridLayout(centralWidget)

        self.leftContainer = QWidget(self)
        self.leftLayout = QVBoxLayout(self.leftContainer)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(5)
        grid.addWidget(self.leftContainer, 0, 0, 2, 1)

        self.rightContainer = QWidget(self)
        self.rightLayout = QVBoxLayout(self.rightContainer)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(5)

        self.logView = TextView(self)
        self.logController = LogViewController(self.logView)

        self.debugView = TextView(self)
        self.debugController = LogViewController(self.debugView)

        for view in [self.logView, self.debugView]:
            self.rightLayout.addWidget(view)
            self.rightLayout.setStretchFactor(view, 1)

        grid.addWidget(self.rightContainer, 0, 1, 2, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)


    def setPortList(self, ports):
        """Ersetzt alle Einträge in der ComboBox durch 'ports'."""
        self.comboPorts.clear()
        self.comboPorts.addItems(ports)

    def currentPort(self):
        """Gibt das aktuell gewählte COM-Port-Label zurück."""
        return self.comboPorts.currentText()

    def showStatus(self, text, timeout=0):
        """Zeigt eine kurze Meldung in der StatusBar."""
        self.statusBar.showMessage(text, timeout)

    def setLeftViews(self, new_views):
        """
        Entfernt alle Widgets aus leftLayout und fügt new_views ein.
        """
        while self.leftLayout.count() > 0:
            item = self.leftLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for view in new_views:
            self.leftLayout.addWidget(view)
            self.leftLayout.setStretchFactor(view, 1)

        self.leftContainer.update()
