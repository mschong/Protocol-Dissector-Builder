import sys
from PyQt5.QtWidgets import *

class PackInfo(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Packet Information")
        self.setGeometry(100,100,350,294)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)


        self.draw_refList_table()
        self.layout.addWidget(self.table, 2, 0)
        self.setLayout(self.layout)

        addButton = QPushButton("+", self)
        self.layout.addWidget(addButton, 3, 1)
        addButton.clicked.connect(self.clickMethod)

        self.show()

    def draw_refList_table(self):
        self.table = QTableWidget(1, 2)
        #self.model = QStandardItemModel()
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Value", "Text Description "])
        self.table.resizeColumnsToContents()

    def clickMethod(self):
        self.table.insertRow(self.table.rowCount())


if __name__ == '__main__':
    app = QApplication([])
    test = ReferenceList()
    sys.exit(app.exec_())