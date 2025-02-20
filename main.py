import sys
from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Haupt-Controller erzeugen (erstellt intern den MainView usw.)
    mainController = MainController()

    # Hauptfenster anzeigen
    mainController.showMainWindow()

    # (Optional) Event-Filter auf Applikationsebene:
    app.installEventFilter(mainController)

    sys.exit(app.exec())
