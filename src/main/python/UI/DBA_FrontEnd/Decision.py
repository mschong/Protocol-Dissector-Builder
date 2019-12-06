import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint

class Decision(QWidget):
    def __init__(self, name):

        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):

        self.setWindowTitle("if Statement")
        self.layout = QGridLayout()
        self.col = 0
        
        self.if_label = QLabel()
        self.if_label.setText(" if")
        self.layout.addWidget(self.if_label, 0, 0)

        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        logical_ops_box= QComboBox()
        logical_ops = ["",">", "<", "=>", "<=", "==", "!="]

        for op in logical_ops:
            logical_ops_box.addItem(op)
        # self.layout.addWidget(logical_ops_box,1, self.col)
        # self.col+=1

        # self.layout.addWidget(QLineEdit(), 1, self.col)
        # self.col+=1

        self.addButton = QPushButton("+")
        self.layout.addWidget(self.addButton,2,0)
        self.addButton.clicked.connect(self.clickMethod)

        self.setLayout(self.layout)

    def getName(self):
        return self.name

    def setCondition(self, condition):
        colNum = 0
        if(len(condition) > 1):
            for i in range(int(len(condition)/2)):
                self.clickMethod()
        for value in condition:
            conditionWidget = self.layout.itemAtPosition(1, colNum).widget()
            if(isinstance(conditionWidget, QLineEdit)):
                conditionWidget.setText(value)
            elif(isinstance(conditionWidget, QComboBox)):
                index = conditionWidget.findText(value)
                conditionWidget.setCurrentIndex(index)
            colNum += 1


    def clickMethod(self):
        logical_ops_box = QComboBox()
        logical_ops = ["",">", "<", "=>", "<=", "==", "!=", "AND", "OR"]

        for op in logical_ops:
            logical_ops_box.addItem(op)
        self.layout.addWidget(logical_ops_box,1, self.col)
        self.col+=1
        self.layout.setColumnMinimumWidth(self.col, 85) #Added this for menu size change
        self.layout.addWidget(QLineEdit(), 1, self.col)
        self.col+=1
        self.layout.removeWidget(self.if_label)
        self.layout.addWidget(self.if_label, 0, self.col//2)

        self.parent().resize(self.layout.sizeHint()) #Added this for menu size change
        

    def saveMethod(self):
        decision_properties = []
        colCount = self.layout.columnCount()
        for i in range(colCount):
            loopWidget = self.layout.itemAtPosition(1, i).widget()
            if(isinstance(loopWidget, QLineEdit)):
                decision_properties.append(loopWidget.text())
            if(isinstance(loopWidget, QComboBox)):
                decision_properties.append(loopWidget.currentText())
        return decision_properties


if __name__ == '__main__':
    app = QApplication([])
    test = Decision()
    sys.exit(app.exec_())