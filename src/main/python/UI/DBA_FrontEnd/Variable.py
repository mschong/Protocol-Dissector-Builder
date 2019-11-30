from PyQt5.QtWidgets import * #QPushButton, QWidget
from PyQt5.QtCore import * #Qt, QMimeData, QRect
from PyQt5.QtGui import *
from UI.DBA_FrontEnd.Dialogs.ErrorDialog import ErrorDialog
import sys

class Variable(QWidget):
    def __init__(self):
        self.toolButton = None
        self.scope = "global"
        self.name = ""
        self.value = ""
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(20, 20, 278, 100)
        self.nameLineEdit = QLineEdit()
        name_line_exp_validator = QRegExp("[a-z0-9_]+\S?[A-za-z0-9_]+")
        name_line_validator = QRegExpValidator(name_line_exp_validator)
        self.nameLineEdit.setValidator(name_line_validator)
        self.nameLineEdit.setFixedWidth(80)
        self.equal_sign = QLabel("=")
        self.valueLineEdit = QLineEdit()
        self.valueLineEdit.setFixedWidth(80)
        self.scope_choice = QComboBox()
        scope_choices = ["global", "local"]
        for choice in scope_choices:
            self.scope_choice.addItem(choice)
        self.data_type_combo = QComboBox()
        data_types = ['string', 'number', 'boolean', 'thread', 'table']
        for data_type in data_types:
            self.data_type_combo.addItem(data_type)
        name_label = QLabel('Name')
        scope_label = QLabel('Scope')
        value_label = QLabel('Value')
        data_type_label = QLabel('Data Type')
        self.widget_layout = QVBoxLayout()
        self.setLayout(self.widget_layout)
        self.variable_layout = QGridLayout()
        self.variable_layout.addWidget(scope_label,0,0)
        self.variable_layout.addWidget(self.scope_choice,1,0)
        self.variable_layout.addWidget(data_type_label, 0, 1)
        self.variable_layout.addWidget(self.data_type_combo,1,1)
        self.variable_layout.addWidget(name_label, 0, 2)
        self.variable_layout.addWidget(self.nameLineEdit,1,2)
        self.variable_layout.addWidget(self.equal_sign,1,3)
        self.variable_layout.addWidget(value_label, 0, 4)
        self.variable_layout.addWidget(self.valueLineEdit,1,4)
        self.widget_layout.addLayout(self.variable_layout)
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.clickOKMethod)
        self.widget_layout.addWidget(self.okButton)
        self.show()

    def getName(self):
        return self.name
    
    def setName(self, name):
        #self.name = name
        self.nameLineEdit.setText(name)
    def setValue(self, value):
        #self.value = value
        self.valueLineEdit.setText(value)
    def setScope(self, scope):
        #self.scope = scope
        scope_combo = self.scope_choice
        index = scope_combo.findText(scope)
        scope_combo.setCurrentIndex(index)
    def setDataType(self, data_type):
        dataType_combo = self.data_type_combo
        index = dataType_combo.findText(data_type)
        dataType_combo.setCurrentIndex(index)
    def setButton(self, toolButton):
        self.toolButton = toolButton
    def saveMethod(self):
        variable_properties = dict(
            {'Scope': self.scope_choice.currentText(), 'Data Type': self.data_type_combo.currentText(), 'Name': self.nameLineEdit.text(), 'Value': self.valueLineEdit.text()})
        return variable_properties
    def setButton(self, toolButton):
        self.toolButton = toolButton

    def clickOKMethod(self):
        if self.nameLineEdit.text() == "":
            text = "No Name declared. Please declare a name for variable"
            dialog = ErrorDialog(text)
            dialog.exec()

        elif self.valueLineEdit.text() == "":
            text = "No declaration declared. Please make a declaration for variable"
            dialog = ErrorDialog(text)
            dialog.exec()
        else:
            self.toolButton.setText(self.nameLineEdit.text())

if __name__ == '__main__':
    app = QApplication([])
    test = Variable()
    sys.exit(app.exec_())
