from PySide6.QtCore import QObject

class SeesawController(QObject):
    def __init__(self, model, view, parent=None):
        super().__init__(parent)
        self.model = model
        self.view = view
        self.updateView()

    def handleIncomingData(self, data: str):
        self.model.updateFromPacket(data)
        self.updateView()

    def updateView(self):
        self.view.seesawCanvas.setData(
            reference=self.model.reference,
            ball=self.model.ball,
            angle=self.model.angle,
            boing=self.model.boing
        )
        self.view.graphCanvas.updateGraphData(
            self.model.reference,
            self.model.ball,
            self.model.angle
        )
