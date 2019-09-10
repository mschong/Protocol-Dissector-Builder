# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainpane.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from Backend.Workspace import workspace
from Backend.Workspace import workspaceloader
from Backend.Project import project

class Ui_MainDialog(object):
    workspace = None

    def __init__(self, wspace):
        self.workspace = wspace

    def setupUi(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.resize(973, 625)

        self.retranslateUi(MainDialog)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        _translate = QtCore.QCoreApplication.translate
        MainDialog.setWindowTitle(_translate("MainDialog", "Protocol Dissector Builder"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QWidget()
    ui = Ui_MainDialog()
    ui.setupUi(mainDialog)
    mainDialog.show()
    sys.exit(app.exec_())