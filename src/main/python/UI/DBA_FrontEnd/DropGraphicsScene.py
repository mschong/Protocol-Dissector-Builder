from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsScene, QGraphicsItem, QAction, QMenu
from PyQt5.QtCore import * #Qt, QMimeData, QRect
from PyQt5.QtGui import *
from Field import Field
from Loop import Loop
from Decision import Decision
from GraphicsProxyWidget  import GraphicsProxyWidget
import sys

class DropGraphicsScene(QGraphicsScene):

    def __init__(self, parent = None):
        super(DropGraphicsScene, self).__init__(parent)

    def contextMenuEvent(self, event):
        menu = QMenu()
        deleteAction = QAction()
        deleteAction = menu.addAction("Delete")
        if menu.exec(event.screenPos()) == deleteAction:
            itemToRemove = QGraphicsWidget()
            for item in self.items(event.scenePos()):
                if item.scene():
                    self.removeItem(item)
    # The following two functions are only preparing the scene to accept any drag movements

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    # In this function is where we will drop the field to the canvas
    def dropEvent(self, event):
        proxy = GraphicsProxyWidget()
        if(event.mimeData().text() == "Field"):
            field = Field()
            proxy = self.addWidgetToScene(field, event.scenePos())
        if(event.mimeData().text() == "Loop"):
            loop = Loop()
            proxy = self.addWidgetToScene(loop, event.scenePos())
        if(event.mimeData().text() == "Decision"):
            decision = Decision()
            proxy = self.addWidgetToScene(decision, event.scenePos())

        if ((proxy.scenePos().x() + proxy.size().width()) > self.width()):
            self.updateScene(proxy.size().width(), True)
        if ((proxy.scenePos().y() + proxy.size().height()) > self.height()):
            self.updateScene(proxy.size().height(), False)


        event.accept()
    def addWidgetToScene(self, widget, pos):
        """ A QGraphicsWidget is a QGraphicsItem and A QGraphicsItem is movable. So I will create
        a parent over the field widget so the field can be movable"""
        parent = QGraphicsWidget()
        parent.setCursor(Qt.SizeAllCursor);
        parent.setGeometry((pos.x())-70, (pos.y())-70, 80, 90)
        parent.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)
        """ Here we are 'dropping' the item to the scene.
         We needed to create a parent over the widget because if would add the widget to scene 
         the widget would be be positioned at (0,0) and we wouldn't be able o move it"""
        self.addItem(parent)
        
        # This Proxy will allows us to add the child to the parent and drop the  widget to the canvas
        proxy = GraphicsProxyWidget()
        proxy.setWidget(widget)
        proxy.setParentItem(parent)
        return proxy
        

    def updateScene(self, widgetSize, isX):
        rec = self.sceneRect()
        if(isX):
            self.setSceneRect(rec.x(), rec.y(), (rec.width() + widgetSize), rec.height())
            
        else:
            self.setSceneRect(rec.x(), rec.y(), rec.width(), (rec.height() + widgetSize))