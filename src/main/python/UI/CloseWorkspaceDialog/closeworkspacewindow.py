# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'closeworkspace.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
'''
Author: Ernesto Vazquez
Dialog to be displayed when close workspace is clicked
'''
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 130)
        Dialog.setMinimumSize(QtCore.QSize(500, 130))
        Dialog.setMaximumSize(QtCore.QSize(500, 130))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 90, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.messageLabel = QtWidgets.QLabel(Dialog)
        self.messageLabel.setGeometry(QtCore.QRect(20, 30, 451, 21))
        self.messageLabel.setText("")
        self.messageLabel.setObjectName("messageLabel")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 451, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Close Workspace"))
        self.label.setText(_translate("Dialog", "[ You can re-open it later in File menu ]"))
