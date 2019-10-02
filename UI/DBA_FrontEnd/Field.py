import sys
from PyQt5.QtWidgets import *
from DBA_BackEnd.Field import FieldBackEnd

class Field(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Field")
        self.setGeometry(100,100,288,145)
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
        self.table = QTableWidget(3, 2)
        # Making the indexes of rows and columns invisible to user
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        column_1_text = ["Name","Description","Var Size"]
        i = 0
        while i < 3:
            self.table.setItem(i, 0, QTableWidgetItem(column_1_text[i]))
            i += 1

        widgets = []

        # Creating line To get Name
        name_line = QLineEdit()
        widgets.append(name_line)

        # Creating line To get Abbreviation
        #abbr_line = QLineEdit()
        #widgets.append(abbr_line)

        # Creating line To get Description
        desc_line = QLineEdit()
        widgets.append(desc_line)

        # Creating drop down list of reference lists
        #ref_list = QComboBox()
        #ref_list.addItem("Select from a predefined list of reference lists")
        #widgets.append(ref_list)

        # Creating drop down list of data types
        #data_type_com= QComboBox()
        #data_types = ["Select from a list of data types", "NONE", "Protocol", "Boolean", "UNIT8", "UNIT16", "UNIT24", "UNIT32", "UNIT64", "INT8", "INT16", "INT24", "INT32", "INT64", "Float", "Double", "Absolute Time", "Relative Time", "String", "StringZ", "UNIT String", "Ether", "Bytes"]
        #for data_type in data_types:
        #    data_type_com.addItem(data_type)
        #widgets.append(data_type_com)

        # Creating drop down list of bases
        #base_com = QComboBox()
        #bases = ["Select from a list of bases ", "NONE", "DEC", "HEX", "OCT", "DEC_HEX", "HEX_DEC"]
        #for base in bases:
        #    base_com.addItem(base)
        #widgets.append(base_com)

        # Creating line To get mask
        #mask_line = QLineEdit()
        #widgets.append(mask_line)

        # Creating line To get Value Constraint
        #va_cons_line = QLineEdit()
        #widgets.append(va_cons_line)

        var_size = QComboBox()
        sizes = ["Select number of bytes", "1 byte", "2 bytes", "4 bytes", "8 bytes", "16 bytes", "32 bytes"]
        for size in sizes:
            var_size.addItem(size)
        widgets.append(var_size)

        #req_line = QCheckBox()
        #widgets.append(req_line)

        # Adding Widgets to Table
        j = 0
        while j < len(widgets):
            self.table.setCellWidget(j, 1, widgets[j])
            j += 1
        self.table.resizeColumnsToContents()

    def clickMethod(self):
        fieldDict = dict({'Name': self.table.cellWidget(0,1).text(), 'Description': self.table.cellWidget(1,1).text(), 'Var Size': self.table.cellWidget(2,1).currentText()})
        

        field = FieldBackEnd(fieldDict['Var Size'],
                             fieldDict['Name'],
                             fieldDict['Description'])

        print(field.__dict__)

if __name__ == '__main__':
    app = QApplication([])
    test = Field()
    sys.exit(app.exec_())

