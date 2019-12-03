import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FieldOKDialog(QDialog):
    def __init__(self, text):
        super().__init__()

        self.title = "ERROR"
        self.initUI(text)

    def initUI(self, text):
        self.textToDisplay = text
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.textToDisplay)
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.ok_button_clicked)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        

    def ok_button_clicked(self):
        self.close()

class Field(QWidget):
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
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.clickOKMethod)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def draw_field_table(self):
        self.table = QTableWidget(11, 2)
        # Making the indexes of rows and columns invisible to user
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        column_1_text = ["Name *","Abbreviation *","Description *", "Data Type *", "Base", "Mask", "Value Constraint", "Var Size *", "ID Value", "Required", "Little Endian"]
        i = 0
        while i < self.table.rowCount():
            item = QTableWidgetItem(column_1_text[i])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 0, item)
            i += 1

        widgets = []

    # Creating line To get Name

        name_line = QLineEdit()
        name_line_exp_validator = QRegExp("[A-za-z0-9_\.]+")
        name_line_validator = QRegExpValidator(name_line_exp_validator)
        name_line.setValidator(name_line_validator)
        widgets.append(name_line)

        # Creating line To get Abbreviation
        abbr_line = QLineEdit()
        abbr_line_exp_validator = QRegExp("[A-za-z0-9\.]+")
        abbr_line_validator = QRegExpValidator(abbr_line_exp_validator)
        abbr_line.setValidator(abbr_line_validator)
        widgets.append(abbr_line)


        # Creating line To get Description
        desc_line = QLineEdit()
        widgets.append(desc_line)

        # Creating drop down list of data types
        data_type_com= QComboBox()
        data_types = ["NONE", "PROTOCOL", "BOOLEAN","FRAMENUM", "UNIT8", "UNIT16", "UNIT24", "UNIT32", "UNIT64", "INT8", "INT16",
                      "INT24", "INT32", "INT64", "FLOAT", "DOUBLE", "ABSOLUTE_TIME", "RELATIVE_TIME", "STRING", "STRINGZ", "UNIT_STRING", "ETHER", "BYTES","UNIT_BYTES", "IPv4","IPv6", "IPXNET", "PROTOCOL", "GUID", "OID"]
        for data_type in data_types:
            data_type_com.addItem(data_type)
        widgets.append(data_type_com)

        # Creating drop down list of bases
        base_com = QComboBox()
        bases = ["NONE", "ASCII", "DEC", "HEX", "OCT", "DEC_HEX", "HEX_DEC"]
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
        var_size_line_exp_validator = QRegExp("[0-9]+")
        var_size_line_validator = QRegExpValidator(var_size_line_exp_validator)
        var_size_line.setValidator(var_size_line_validator)
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

        little_endian_check_box = QCheckBox()
        little_endian_cell = QWidget()
        little_endian_cell_layout = QHBoxLayout()
        little_endian_cell_layout.addWidget(little_endian_check_box)
        little_endian_cell_layout.setAlignment(Qt.AlignCenter)
        little_endian_cell.setLayout(little_endian_cell_layout)
        widgets.append(little_endian_cell)

        # Adding Widgets to Table
        j = 0
        while j < len(widgets):
            self.table.setCellWidget(j, 1, widgets[j])
            j += 1
        self.table.setColumnWidth(1, 138)
        self.table.resizeRowsToContents()

    def clickOKMethod(self):
        if self.table.cellWidget(0, 1).text() == "":
            text = "No name declared. Please declare a name"
            dialog = FieldOKDialog(text)
            dialog.exec()
        elif self.table.cellWidget(1, 1).text() == "":
            text = "No abbreviation declared. Please declare a abbreviation"
            dialog = FieldOKDialog(text)
            dialog.exec()
        elif self.table.cellWidget(2, 1).text() == "":
            text = "No description declared. Please declare a description"
            dialog = FieldOKDialog(text)
            dialog.exec()
        elif self.table.cellWidget(3, 1).currentText() == "Select data type":
            text = "No Data Type selected. If field has no type then select NONE otherwise please select a type"
            dialog = FieldOKDialog(text)
            dialog.exec()

        elif self.table.cellWidget(7, 1).children()[1].text() == "":
            text = "No size declared. Please declare a size"
            dialog = FieldOKDialog(text)
            dialog.exec()

        else:
            self.toolButton.setText(self.table.cellWidget(0, 1).text())
    
    def setName(self, name):
        self.table.cellWidget(0,1).setText(name)

    def setAbbreviation(self, abbr):
        self.table.cellWidget(1,1).setText(abbr)

    def setDescription(self, description):
        self.table.cellWidget(2,1).setText(description)

    def setDataType(self, dataType):
        combo = self.table.cellWidget(3,1)
        index = combo.findText(dataType)
        combo.setCurrentIndex(index)

    def setBase(self, base_value):
        combo = self.table.cellWidget(4,1)
        index = combo.findText(base_value)
        combo.setCurrentIndex(index)

    def setMask(self, mask):
        self.table.cellWidget(5,1).setText(mask)

    def setValueConstraint(self, constraint):
        self.table.cellWidget(6,1).setText(constraint)

    def setSize(self, value, unit):
        # setting lineEdit String
        self.table.cellWidget(7,1).children()[1].setText(value)
        # setting combobox data
        combo = self.table.cellWidget(7,1).children()[2]
        index = combo.findText(unit)
        combo.setCurrentIndex(index)

    def setID(self, id_value):
        self.table.cellWidget(8,1).setText(id_value)

    def setRequired(self, isChecked):
        if(isChecked == "true"):
            self.table.cellWidget(9,1).children()[1].setChecked(True)
        else:
            self.table.cellWidget(9,1).children()[1].setChecked(False)

    def setLittleEndian(self, isChecked):
        if(isChecked == "true"):
            self.table.cellWidget(10,1).children()[1].setChecked(True)
        else:
            self.table.cellWidget(10,1).children()[1].setChecked(False)

    def saveMethod(self):
        field_properties = dict({'Name': self.table.cellWidget(0,1).text(), 'Abbreviation': self.table.cellWidget(1,1).text(), 'Description': self.table.cellWidget(2,1).text(), 'Data Type': self.table.cellWidget(3,1).currentText(), 'Base': self.table.cellWidget(4,1).currentText(), 'Mask': self.table.cellWidget(5,1).text(), 'Value Constraint': self.table.cellWidget(6,1).text(), 'Var Size': {'editText': self.table.cellWidget(7,1).children()[1].text(), 'combobox': self.table.cellWidget(7,1).children()[2].currentText()}, 'ID Value': self.table.cellWidget(8,1).text()})
        if self.table.cellWidget(9,1).children()[1].isChecked():
            field_properties.update({'Required': 'true'})
        else:
            field_properties.update({'Required': 'false'})
        if self.table.cellWidget(10,1).children()[1].isChecked():
            field_properties.update({'LE': 'true'})
        else:
            field_properties.update({'LE': 'false'})

        return field_properties
    
    def setButton(self, toolButton):
        self.toolButton = toolButton
if __name__ == '__main__':
    app = QApplication([])
    test = Field()
    sys.exit(app.exec_())

