from PyQt5.QtWidgets import QGraphicsItem, QGraphicsWidget, QGraphicsProxyWidget, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPointF
import sys
# This will allow to drop the widget
class GraphicsProxyWidget(QGraphicsProxyWidget):

	def __init__(self):
		super().__init__()
		self.connectors = []

	def dragEnterEvent(self, e):
		e.acceptProposedAction()

	def dropEvent(self, e):
		# pass drop event to child widget
		return self.widget().dropEvent(e)

	def dragMoveEvent(self, e):
		e.acceptProposedAction()

	def setPolygon(self):

		tlvX = self.sceneBoundingRect().topLeft().x() - self.sceneBoundingRect().center().x()
		tlvY = self.sceneBoundingRect().topLeft().y() - self.sceneBoundingRect().center().y()

		trvX = self.sceneBoundingRect().topRight().x() - self.sceneBoundingRect().center().x()
		trvY = self.sceneBoundingRect().topRight().y() - self.sceneBoundingRect().center().y()

		blvX = self.sceneBoundingRect().bottomLeft().x() - self.sceneBoundingRect().center().x()
		blvY = self.sceneBoundingRect().bottomLeft().y() - self.sceneBoundingRect().center().y()

		brvX = self.sceneBoundingRect().bottomRight().x() - self.sceneBoundingRect().center().x()
		brvY = self.sceneBoundingRect().bottomRight().y() - self.sceneBoundingRect().center().y()

		polyVector = QPolygonF([QPointF(tlvX, tlvY), QPointF(trvX, trvY), QPointF(brvX, brvY), QPointF(blvX, blvY), QPointF(tlvX, tlvY)])

		self.polygon = QGraphicsPolygonItem()
		self.polygon.setPolygon(polyVector)
		self.polygon.setPos(self.sceneBoundingRect().center())

	def removeConnector(self, connector):
		try:
			self.connectors.remove(connector)
		except ValueError:
			pass


	def removeConnectors(self):
		for connector in self.connectors[:]:
			connector.startItem().removeConnector(connector)
			connector.endItem().remove(connector)
			self.scene().removeConnector(connector)

	def addConnector(self, connector):
		self.connectors.append(connector)

	def itemChange(self, change, value):
		if change == QGraphicsItem.ItemPositionChange:
			for connector in self.connectors:
				connector.updatePosition()
		return value