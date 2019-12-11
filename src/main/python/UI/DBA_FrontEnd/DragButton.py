from PyQt5.QtWidgets import * #QPushButton, QWidget
from PyQt5.QtCore import * #Qt, QMimeData, QRect
from PyQt5.QtGui import *
import sys

class DragButton(QPushButton):
    def __init__(self, title, parent):
        super(DragButton, self).__init__(title, parent)
    def mousePressEvent(self, e):
        # This helps the button to not appear as pressed when a field is being dragged
        self.setCheckable(False)
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return QPushButton.mouseMoveEvent(self, e)

        # The MimeData has the position of the button
        mimeData = QMimeData()
        mimeData.setText(self.text())


        # This makes the button to be transparent when its dragged.
        pixmap = QPixmap(self.grab())
        painter = QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
        painter.end()


        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())

        # This helps execute the dragging move action
        drag.exec_(Qt.MoveAction)
        return QPushButton.mouseMoveEvent(self, e)

    def dragEnterEvent(self, e):
        e.accept()
        return QPushButton.dragEnterEvent(self, e)

    