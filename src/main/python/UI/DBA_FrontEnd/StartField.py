import sys
from PyQt5.QtWidgets import *
from DBA_BackEnd.StartField import StartFieldBackEnd


class StartField(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Start Field")
        self.setGeometry(100,100,305,100)
        # Setting up the window
        self.draw_field_table()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.applyButton = QPushButton("Apply")
        self.layout.addWidget(self.applyButton)
        self.applyButton.clicked.connect(self.clickMethod)
        self.setLayout(self.layout)

        self.show()

    def draw_field_table(self):
        self.table = QTableWidget(2, 2)
        # Making the indexes of rows and columns invisible to user
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        column_1_text = ["Protocol Name","Protocol Description"]
        i = 0
        while i < 2:
            self.table.setItem(i, 0, QTableWidgetItem(column_1_text[i]))
            i += 1

        widgets = []

        # Creating line To get Protocol Name
        protocol_name = QLineEdit()
        widgets.append(protocol_name)

        # Creating line To get Protocol Description
        protocol_desc = QLineEdit()
        widgets.append(protocol_desc)

        # Adding Widgets to Table
        j = 0
        while j < len(widgets):
            self.table.setCellWidget(j, 1, widgets[j])
            j += 1
        self.table.resizeColumnsToContents()

    def clickMethod(self):
        startFieldDict = dict({'Protocol Name': self.table.cellWidget(0,1).text(), 'Protocol Description': self.table.cellWidget(1,1).text()})
        start = StartFieldBackEnd(startFieldDict['Protocol Name'], startFieldDict['Protocol Description'])
        
        print(start.__dict__)

if __name__ == '__main__':
    app = QApplication([])
    test = StartField()
    sys.exit(app.exec_())

