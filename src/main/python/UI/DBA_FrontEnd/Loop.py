import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint
from UI.DBA_FrontEnd.DBA_BackEnd import While

class Loop(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("While Loop")
        self.setGeometry(100, 100, 250, 200)

        self.while_label = QLabel(self)
        self.while_label.setText("while")
        self.while_label.resize(63, 32)
        self.while_label.move(110, 25)

        self.part_a = QLineEdit(self)
        self.part_a.resize(60, 30)
        self.part_a.move(30, 68)

        self.logical_ops_box= QComboBox(self)
        self.logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in self.logical_ops:
            self.logical_ops_box.addItem(op)

        self.logical_ops_box.resize(60, 30)
        self.logical_ops_box.move(95, 68)

        self. part_b = QLineEdit(self)
        self.part_b.resize(60, 30)
        self.part_b.move(160, 68)

        applyButton = QPushButton("Apply",self)
        applyButton.resize(63, 32)
        applyButton.move(188, 168)
        applyButton.clicked.connect(self.clickMethod)

        self.show()

    #def paintEvent(self, event):
    #    painter = QPainter()
    #    painter.begin(self)
    #    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
    #    points = [QPoint(125, 0), QPoint(0, 80),QPoint(125, 170),QPoint(250, 80)]
    #    rhombus = QPolygon(points)
    #    painter.drawPolygon(rhombus)
    #    painter.end()

    def clickMethod(self):
        loopDict = dict({'part_a': self.part_a.text(), 'logical': self.logical_ops_box.currentText(), 'part_b': self.part_b.text()})

        whileLoop = While.While(loopDict['part_a'], loopDict['logical'], loopDict['part_b'])
        print(whileLoop.__dict__)

if __name__ == '__main__':
    app = QApplication([])
    test = Loop()
    sys.exit(app.exec_())