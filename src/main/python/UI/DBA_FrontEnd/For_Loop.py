import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint


class For_Loop(QWidget):
    def __init__(self, name):

        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):

        self.setWindowTitle("for Loop")
        self.layout = QGridLayout()
        self.col = 0
        
        self.for_label = QLabel()
        self.for_label.setText(" for")
        self.layout.addWidget(self.for_label, 0, 2, Qt.AlignCenter)

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        

        exp12_separator = QLabel(";")
        self.layout.addWidget(exp12_separator)
        self.col+=1

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1

        exp23_separator = QLabel(";")
        self.layout.addWidget(exp23_separator, 1, self.col)
        self.col += 1

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col += 1

        self.setLayout(self.layout)

    def getName(self):
        return self.name

    def setExpressions(self, expressions):
        self.layout.itemAtPosition(1,0).widget().setText(expressions['exp1'])
        self.layout.itemAtPosition(1,2).widget().setText(expressions['exp2'])
        self.layout.itemAtPosition(1,4).widget().setText(expressions['exp3'])

    def clickMethod(self):
        logical_ops_box = QComboBox()
        logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in logical_ops:
            logical_ops_box.addItem(op)
        self.layout.addWidget(logical_ops_box,1, self.col)
        self.col+=1
        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        self.layout.removeWidget(self.for_label)
        self.layout.addWidget(self.for_label, 0, self.col//2)

    def saveMethod(self):
        exp1 = self.layout.itemAtPosition(1,0).widget().text()
        exp2 = self.layout.itemAtPosition(1,2).widget().text()
        exp3 = self.layout.itemAtPosition(1,4).widget().text()
        for_properties = {'exp1': exp1, 'exp2':exp2, 'exp3':exp3}
        return for_properties
        
if __name__ == '__main__':
    app = QApplication([])
    test = For_Loop()
    sys.exit(app.exec_())