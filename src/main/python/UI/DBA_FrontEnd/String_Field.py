import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class String_Field(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Field")
        self.setGeometry(20,20,396,307)
        # Setting up the window
        self.draw_field_table()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.show()
    def draw_field_table(self):
        self.table = QTableWidget(10, 2)
        # Making the indexes of rows and columns invisible to user
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        column_1_text = ["Name","Abbreviation","Description", "Data Type", "Base", "Mask", "Value Constraint", "Var Size", "ID Value", "Required"]
        i = 0
        while i < self.table.rowCount():
            self.table.setItem(i, 0, QTableWidgetItem(column_1_text[i]))
            i += 1

        widgets = []

    # Creating line To get Name

        name_line = QLineEdit()
        widgets.append(name_line)

        # Creating line To get Abbreviation
        abbr_line = QLineEdit()
        widgets.append(abbr_line)

        # Creating line To get Description
        desc_line = QLineEdit()
        widgets.append(desc_line)

        # Creating drop down list of data types
        data_type_com= QComboBox()
        data_types = ["STRING"]
        for data_type in data_types:
            data_type_com.addItem(data_type)
        widgets.append(data_type_com)

        # Creating drop down list of bases
        base_com = QComboBox()
        bases = ["Select base", "NONE", "DEC", "HEX", "OCT", "DEC_HEX", "HEX_DEC"]
        for base in bases:
            base_com.addItem(base)
        widgets.append(base_com)

        # Creating line To get mask
        mask_line = QLineEdit()
        widgets.append(mask_line)

        # Creating line To get Value Constraint
        va_cons_line = QLineEdit()
        widgets.append(va_cons_line)

        # Creating a line edit to add number of size and drop down to identify if it is in bytes or bits
        var_size_row_layout = QHBoxLayout()
        var_choice = QComboBox()
        var_choices = ["BYTES", "BITS"]
        for choice in var_choices:
            var_choice.addItem(choice)
        var_size_line = QLineEdit()
        var_size_row_layout.addWidget(var_size_line)
        var_size_row_layout.addWidget(var_choice)
        var_size_cell = QWidget()
        var_size_cell.setLayout(var_size_row_layout)
        widgets.append(var_size_cell)

        # Creating line To get ID Value
        id_value_line = QLineEdit()
        widgets.append(id_value_line)

        req_check_box = QCheckBox()
        req_cell = QWidget()
        req_cell_layout = QHBoxLayout()
        req_cell_layout.addWidget(req_check_box)
        req_cell_layout.setAlignment(Qt.AlignCenter)
        req_cell.setLayout(req_cell_layout)
        widgets.append(req_cell)

        # Adding Widgets to Table
        j = 0
        while j < len(widgets):
            self.table.setCellWidget(j, 1, widgets[j])
            j += 1
        self.table.setColumnWidth(1, 138)
        self.table.resizeRowsToContents()

    def clickMethod(self):
        dict01 = dict({'Name': self.table.cellWidget(0,1).text(), 'Abbreviation': self.table.cellWidget(1,1).text(), 'Description': self.table.cellWidget(2,1).text(), 'Reference List': self.table.cellWidget(3,1).currentText(), 'Data Type': self.table.cellWidget(4,1).currentText(), 'Base': self.table.cellWidget(5,1).currentText(), 'Mask': self.table.cellWidget(6,1).text(), 'Values Constraint': self.table.cellWidget(7,1).text(), 'Var Size': self.table.cellWidget(8,1).currentText()})
        if self.table.cellWidget(9,1).isTristate():
            dict.update({'Required': 'true'})
        else:
            dict.update({'Required': 'false'})

if __name__ == '__main__':
    app = QApplication([])
    test = String_Field()
    sys.exit(app.exec_())

