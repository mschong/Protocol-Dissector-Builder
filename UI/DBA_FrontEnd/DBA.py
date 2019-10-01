# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dissectorbuilderarea.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from StartField import StartField
from Field import Field
from Loop import Loop
from Decision import Decision


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(619, 300)
        self.dba_label = QtWidgets.QLabel(Form)
        self.dba_label.setGeometry(QtCore.QRect(120, 10, 151, 16))
        self.dba_label.setObjectName("dba_label")
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(35, 31, 321, 251))
        self.graphicsView.setObjectName("graphicsView")
        self.toolbox_label = QtWidgets.QLabel(Form)
        self.toolbox_label.setGeometry(QtCore.QRect(480, 10, 64, 17))
        self.toolbox_label.setObjectName("toolbox_label")
        self.toolBox = QtWidgets.QToolBox(Form)
        self.toolBox.setGeometry(QtCore.QRect(400, 30, 201, 251))
        self.toolBox.setObjectName("toolBox")
        self.field_tab = QtWidgets.QWidget()
        self.field_tab.setGeometry(QtCore.QRect(0, 0, 201, 189))
        self.field_tab.setObjectName("field_tab")
        self.startField_button = QtWidgets.QPushButton(self.field_tab)
        self.startField_button.setGeometry(QtCore.QRect(20, 10, 171, 71))
        self.startField_button.setObjectName("startField_button")
        self.startField_button.clicked.connect(self.open_start_field_window)

        self.field_button = QtWidgets.QPushButton(self.field_tab)
        self.field_button.setGeometry(QtCore.QRect(20, 90, 171, 71))
        self.field_button.setObjectName("field_button")
        self.field_button.clicked.connect(self.open_field_window)

        self.toolBox.addItem(self.field_tab, "")
        self.construct_tab = QtWidgets.QWidget()
        self.construct_tab.setGeometry(QtCore.QRect(0, 0, 201, 189))
        self.construct_tab.setObjectName("construct_tab")
        self.decision_button = QtWidgets.QPushButton(self.construct_tab)
        self.decision_button.setGeometry(QtCore.QRect(0, 0, 83, 25))
        self.decision_button.setObjectName("decision_button")
        self.decision_button.clicked.connect(self.open_decision_window)

        self.loop_button = QtWidgets.QPushButton(self.construct_tab)
        self.loop_button.setGeometry(QtCore.QRect(0, 30, 83, 25))
        self.loop_button.setObjectName("loop_button")
        self.loop_button.clicked.connect(self.open_loop_window)

        self.exp_label = QtWidgets.QLabel(self.construct_tab)
        self.exp_label.setGeometry(QtCore.QRect(0, 70, 81, 17))
        self.exp_label.setObjectName("exp_label")
        self.rel_op_label = QtWidgets.QLabel(self.construct_tab)
        self.rel_op_label.setGeometry(QtCore.QRect(0, 90, 131, 17))
        self.rel_op_label.setObjectName("rel_op_label")
        self.less_button = QtWidgets.QPushButton(self.construct_tab)
        self.less_button.setGeometry(QtCore.QRect(0, 110, 21, 25))
        self.less_button.setObjectName("less_button")
        self.greater_button = QtWidgets.QPushButton(self.construct_tab)
        self.greater_button.setGeometry(QtCore.QRect(30, 110, 21, 25))
        self.greater_button.setObjectName("greater_button")
        self.less_eq_button = QtWidgets.QPushButton(self.construct_tab)
        self.less_eq_button.setGeometry(QtCore.QRect(60, 110, 21, 25))
        self.less_eq_button.setObjectName("less_eq_button")
        self.greater_eq_button = QtWidgets.QPushButton(self.construct_tab)
        self.greater_eq_button.setGeometry(QtCore.QRect(90, 110, 21, 25))
        self.greater_eq_button.setObjectName("greater_eq_button")
        self.eq_button = QtWidgets.QPushButton(self.construct_tab)
        self.eq_button.setGeometry(QtCore.QRect(120, 110, 21, 25))
        self.eq_button.setObjectName("eq_button")
        self.not_eq_button = QtWidgets.QPushButton(self.construct_tab)
        self.not_eq_button.setGeometry(QtCore.QRect(150, 110, 21, 25))
        self.not_eq_button.setObjectName("not_eq_button")
        self.log_op_label = QtWidgets.QLabel(self.construct_tab)
        self.log_op_label.setGeometry(QtCore.QRect(0, 140, 111, 17))
        self.log_op_label.setObjectName("log_op_label")
        self.and_button = QtWidgets.QPushButton(self.construct_tab)
        self.and_button.setGeometry(QtCore.QRect(0, 160, 41, 25))
        self.and_button.setObjectName("and_button")
        self.or_button = QtWidgets.QPushButton(self.construct_tab)
        self.or_button.setGeometry(QtCore.QRect(50, 160, 31, 25))
        self.or_button.setObjectName("or_button")
        self.not_button = QtWidgets.QPushButton(self.construct_tab)
        self.not_button.setGeometry(QtCore.QRect(90, 160, 31, 25))
        self.not_button.setObjectName("not_button")
        self.op_button = QtWidgets.QPushButton(self.construct_tab)
        self.op_button.setGeometry(QtCore.QRect(130, 160, 71, 25))
        self.op_button.setObjectName("op_button")
        self.toolBox.addItem(self.construct_tab, "")

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dba_label.setText(_translate("Form", "Dissector Builder Area"))
        self.toolbox_label.setText(_translate("Form", "Toolbox"))
        self.startField_button.setText(_translate("Form", "Start Field"))
        self.field_button.setText(_translate("Form", "Field"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.field_tab), _translate("Form", "Field"))
        self.decision_button.setText(_translate("Form", "Decision"))
        self.loop_button.setText(_translate("Form", "Loop"))
        self.exp_label.setText(_translate("Form", "Expression"))
        self.rel_op_label.setText(_translate("Form", "Relational Operator"))
        self.less_button.setText(_translate("Form", "<"))
        self.greater_button.setText(_translate("Form", ">"))
        self.less_eq_button.setText(_translate("Form", "<="))
        self.greater_eq_button.setText(_translate("Form", ">="))
        self.eq_button.setText(_translate("Form", "=="))
        self.not_eq_button.setText(_translate("Form", "!="))
        self.log_op_label.setText(_translate("Form", "Logical Operator"))
        self.and_button.setText(_translate("Form", "And"))
        self.or_button.setText(_translate("Form", "Or"))
        self.not_button.setText(_translate("Form", "Not"))
        self.op_button.setText(_translate("Form", "Operand"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.construct_tab), _translate("Form", "Construct"))

    def open_field_window(self):
        self.field_win = Field()
        self.field_win.show()

    def open_start_field_window(self):
        self.start_field_win = StartField()
        self.start_field_win.show()

    def open_loop_window(self):
        self.loop_win = Loop()
        self.loop_win.show()

    def open_decision_window(self):
        self.decision_win = Decision()
        self.decision_win.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
