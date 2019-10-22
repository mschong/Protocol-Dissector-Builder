from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsScene, QGraphicsItem, QAction, QMenu, QGraphicsLineItem
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from UI.DBA_FrontEnd.Field import Field
from UI.DBA_FrontEnd.Connector import Connector
from UI.DBA_FrontEnd.Loop import Loop
from UI.DBA_FrontEnd.Decision import Decision
from UI.DBA_FrontEnd.GraphicsProxyWidget  import GraphicsProxyWidget
from UI.DBA_FrontEnd.Dialogs.ConnectorTypeDialog import ConnectorTypeDialog
import sys

class DropGraphicsScene(QGraphicsScene):
    InsertLine_ON, InsertLine_OFF, MoveItem = range(3)

    def __init__(self, parent = None):
        super(DropGraphicsScene, self).__init__(parent)
        self.line = None
        self.myMode = self.MoveItem
        self.myLineColor = Qt.black

    def contextMenuEvent(self, event):
        if(len(self.items(event.scenePos()))):
            menu = QMenu()

            deleteAction = QAction()
            

            if isinstance(self.items(event.scenePos())[0], Connector):
                change_type_action = QAction()
                change_type_action = menu.addAction("Change Type")

                deleteAction = menu.addAction("Delete")

                action = menu.exec_(event.screenPos())
                
                if action == deleteAction:
                    itemToRemove = QGraphicsWidget()
                    for item in self.items(event.scenePos()):
                        if item.scene():
                            # Following two if statements remove field's connectors
                            if isinstance(item, GraphicsProxyWidget):
                                item.removeConnectors()
                            elif isinstance(item, Connector):
                                item.startItem().removeConnector(item)
                                item.endItem().removeConnector(item)
                            self.removeItem(item)
                elif action == change_type_action:
                    dialog = ConnectorTypeDialog(self.items(event.scenePos())[0])
                    dialog.setModal(True)
                    dialog.exec()
            else:
                deleteAction = menu.addAction("Delete")

                action = menu.exec_(event.screenPos())
                
                if action == deleteAction:
                    itemToRemove = QGraphicsWidget()
                    for item in self.items(event.scenePos()):
                        if item.scene():
                            # Following two if statements remove field's connectors
                            if isinstance(item, GraphicsProxyWidget):
                                item.removeConnectors()
                            elif isinstance(item, Connector):
                                item.startItem().removeConnector(item)
                                item.endItem().removeConnector(item)
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
            proxy = self.addWidgetToScene(field, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        if(event.mimeData().text() == "Loop"):
            loop = Loop()
            proxy = self.addWidgetToScene(loop, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        if(event.mimeData().text() == "Decision"):
            decision = Decision()
            proxy = self.addWidgetToScene(decision, event.scenePos()), event.mimeData().text()
            proxy.setPolygon()

        if ((proxy.scenePos().x() + proxy.size().width()) > self.width()):
            self.updateScene(proxy.size().width(), True)
        if ((proxy.scenePos().y() + proxy.size().height()) > self.height()):
            self.updateScene(proxy.size().height(), False)


        event.accept()
    def addWidgetToScene(self, widget, pos, text):
        button = QToolButton()
        button.setPopupMode(QToolButton.MenuButtonPopup)
        button.setGeometry(QRect(20, 30, 278, 40))
        button.setText(text)
        menu = QMenu()
        button.setMenu(menu)
        action = QWidgetAction(button)
        action.setDefaultWidget(widget)
        button.menu().addAction(action)
        """ A QGraphicsWidget is a QGraphicsItem and A QGraphicsItem is movable. So I will create
        a parent over the field widget so the field can be movable"""
        parent = QGraphicsWidget()
        parent.setCursor(Qt.SizeAllCursor)
        parent.setGeometry((pos.x())-70, (pos.y())-70, 80, 90)
        parent.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        """ Here we are 'dropping' the item to the scene.
         We needed to create a parent over the widget because if would add the widget to scene 
         the widget would be be positioned at (0,0) and we wouldn't be able o move it"""
        self.addItem(parent)

        # This Proxy will allows us to add the child to the parent and drop the  widget to the canvas
        proxy = GraphicsProxyWidget()
        proxy.setWidget(button)
        proxy.setParentItem(parent)

        return proxy
        

    def updateScene(self, widgetSize, isX):
        rec = self.sceneRect()
        if(isX):
            self.setSceneRect(rec.x(), rec.y(), (rec.width() + widgetSize), rec.height())
            
        else:
            self.setSceneRect(rec.x(), rec.y(), rec.width(), (rec.height() + widgetSize))
	
    def setMode(self, mode):
        self.myMode = mode

    def mousePressEvent(self, event):
        if self.myMode == self.InsertLine_ON and event.button() == Qt.LeftButton:
            self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
            self.line.setPen(QPen(self.myLineColor, 2))
            self.addItem(self.line)

        super(DropGraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.myMode == self.InsertLine_ON and self.line:
            newLine = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(newLine)

        elif self.myMode == self.MoveItem:
            super(DropGraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.line and self.myMode == self.InsertLine_ON:
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(startItems) and len(endItems) and isinstance(startItems[0], GraphicsProxyWidget) and isinstance(endItems[0], GraphicsProxyWidget) and startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                connector = Connector(startItem, endItem)
                connector.setColor(self.myLineColor)
                startItem.addConnector(connector)
                endItem.addConnector(connector)
                connector.setZValue(-1000.0)
                self.addItem(connector)
                connector.updatePosition()


        self.line = None
        self.myMode = self.MoveItem
        super(DropGraphicsScene, self).mouseReleaseEvent(event)

    def setLineColor(self, color):
        self.myLineColor = color
        if self.isItemChange(Connector):
            item = self.selectedItems()[0]
            item.setColor(self.myLineColor)
            self.update()

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False
