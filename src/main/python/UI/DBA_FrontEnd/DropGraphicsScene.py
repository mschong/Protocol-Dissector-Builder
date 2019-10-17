from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import * #Qt, QMimeData, QRect
from PyQt5.QtGui import *
from Field import Field
from GraphicsProxyWidget  import GraphicsProxyWidget
import sys

class DropGraphicsScene(QGraphicsScene):

    def __init__(self, parent = None):
        super(DropGraphicsScene, self).__init__(parent)
    # The following two functions are only preparing the scene to accept any drag movements
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    # In this function is where we will drop the field to the canvas
    def dropEvent(self, event):
        # We create a field
        field = Field()
        """ A QGraphicsWidget is a QGraphicsItem and A QGraphicsItem is movable. So I will create
        a parent over the field widget so the field can be movable"""
        parent = QGraphicsWidget()
        parent.setCursor(Qt.SizeAllCursor);
        parent.setGeometry((event.scenePos().x()), (event.scenePos().y()), field.width(), field.height())
        parent.setFlags(QGraphicsItem.ItemIsMovable)
        """ Here we are 'dropping' the item to the scene.
         We needed to create a parent over the widget because if would add the widget to scene 
         the widget would be be positioned at (0,0) and we wouldn't be able o move it"""
        self.addItem(parent)

        # This Proxy will allows us to add the child to the parent and drip the field widget to the
        proxy = GraphicsProxyWidget()
        proxy.setWidget(field)
        proxy.setParentItem(parent)

        event.accept()