# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projectpane.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_ProjectPane(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(418, 502)
        self.projectPaneTreeView = QtWidgets.QTreeView(Dialog)
        self.projectPaneTreeView.setGeometry(QtCore.QRect(0, 0, 301, 491))
        self.projectPaneTreeView.setObjectName("projectPaneTreeView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prjpane = QtWidgets.QWidget()
    ui = Ui_ProjectPane()
    ui.setupUi(prjpane)
    prjpane.show()
    sys.exit(app.exec_())