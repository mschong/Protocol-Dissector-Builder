import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint
from UI.DBA_FrontEnd.DBA_BackEnd import While


class While_Loop(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("while Loop")
        self.layout = QGridLayout()
        self.col = 0
        
        self.while_label = QLabel()
        self.while_label.setText(" while")
        self.layout.addWidget(self.while_label, 0, 1)

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        logical_ops_box= QComboBox()
        logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in logical_ops:
            logical_ops_box.addItem(op)
        self.layout.addWidget(logical_ops_box,1, self.col)
        self.col+=1

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1

        self.addButton = QPushButton("+")
        self.layout.addWidget(self.addButton,2,0)
        self.addButton.clicked.connect(self.clickMethod)

        self.setLayout(self.layout)
        self.show()

    def clickMethod(self):
        logical_ops_box = QComboBox()
        logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in logical_ops:
            logical_ops_box.addItem(op)
        self.layout.addWidget(logical_ops_box,1, self.col)
        self.col+=1
        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        self.layout.removeWidget(self.while_label)
        self.layout.addWidget(self.while_label, 0, self.col//2)
        
if __name__ == '__main__':
    app = QApplication([])
    test = While_Loop()
    sys.exit(app.exec_())