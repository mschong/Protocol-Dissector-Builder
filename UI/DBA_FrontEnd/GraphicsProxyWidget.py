from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsProxyWidget
import sys
# This will allow to drop the widget
class GraphicsProxyWidget(QGraphicsProxyWidget):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
         # pass drop event to child widget
        return self.widget().dropEvent(e)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()