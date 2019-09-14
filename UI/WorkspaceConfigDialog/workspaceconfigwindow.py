# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspaceconfig.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 280)
        Dialog.setMinimumSize(QtCore.QSize(400, 280))
        Dialog.setMaximumSize(QtCore.QSize(400, 280))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 351, 17))
        self.label.setObjectName("label")
        self.workspaceFileLineEdit = QtWidgets.QLineEdit(Dialog)
        self.workspaceFileLineEdit.setGeometry(QtCore.QRect(20, 40, 351, 25))
        self.workspaceFileLineEdit.setObjectName("workspaceFileLineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 351, 17))
        self.label_2.setObjectName("label_2")
        self.startDateLabel = QtWidgets.QLabel(Dialog)
        self.startDateLabel.setGeometry(QtCore.QRect(20, 100, 351, 17))
        self.startDateLabel.setText("")
        self.startDateLabel.setObjectName("startDateLabel")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 351, 17))
        self.label_3.setObjectName("label_3")
        self.editDateLabel = QtWidgets.QLabel(Dialog)
        self.editDateLabel.setGeometry(QtCore.QRect(20, 170, 351, 17))
        self.editDateLabel.setText("")
        self.editDateLabel.setObjectName("editDateLabel")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Workspace Configuration"))
        self.label.setText(_translate("Dialog", "Workspace Name"))
        self.label_2.setText(_translate("Dialog", "Date Created"))
        self.label_3.setText(_translate("Dialog", "Last Edited"))
