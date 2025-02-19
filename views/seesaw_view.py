from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from widgets.seesaw_canvas import SeesawCanvas
from widgets.seesaw_graph_canvas import SeesawGraphCanvas

class SeesawView(QWidget):
    """
    Ein "Container"-Widget, das die SeesawCanvas (Wippe) und 
    die SeesawGraphCanvas (Graph) in einem V-Layout kombiniert.
    Entspricht grob dem VBox im Java-FXML.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.seesawCanvas = SeesawCanvas(width=600, height=300)
        self.graphCanvas  = SeesawGraphCanvas(width=600, height=150)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(self.seesawCanvas)
        layout.addWidget(self.graphCanvas)

        self.setLayout(layout)
