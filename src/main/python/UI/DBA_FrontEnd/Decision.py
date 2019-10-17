import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint
from DBA_BackEnd.Condition import Condition

class Decision(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("IF Statement")
        self.setGeometry(100, 100, 250, 200)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)

        self.if_label = QLabel(self)
        self.if_label.setText("if")
        self.if_label.resize(63, 32)
        self.if_label.move(20, 68)

        self.part_a = QLineEdit(self)
        self.part_a.resize(60, 30)
        self.part_a.move(35, 68)

        #self.logical_op = QLineEdit(self)
        #self.logical_op.resize(60, 30)
        #self.logical_op.move(100, 68)

        self.logical_ops_box= QComboBox(self)
        self.logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in self.logical_ops:
            self.logical_ops_box.addItem(op)

        self.logical_ops_box.resize(60, 30)
        self.logical_ops_box.move(100, 68)

        self. part_b = QLineEdit(self)
        self.part_b.resize(60, 30)
        self.part_b.move(165, 68)

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
        decisionDict = dict({'part_a': self.part_a.text(), 'logical': self.logical_ops_box.currentText(), 'part_b': self.part_b.text()})

        condition = Condition(decisionDict['part_a'], decisionDict['logical'], decisionDict['part_b'])
        print(condition.__dict__)


if __name__ == '__main__':
    app = QApplication([])
    test = Decision()
    sys.exit(app.exec_())