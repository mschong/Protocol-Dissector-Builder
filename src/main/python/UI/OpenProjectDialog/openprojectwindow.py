# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openproject.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
'''
Author: Ernesto Vazquez 
Dialog to browse files to open a project
'''

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Import an existing project")
        Dialog.resize(576, 121)
        Dialog.setMinimumSize(QtCore.QSize(576, 121))
        Dialog.setMaximumSize(QtCore.QSize(576, 121))
        self.browseButton = QtWidgets.QPushButton(Dialog)
        self.browseButton.setGeometry(QtCore.QRect(440, 40, 83, 25))
        self.browseButton.setObjectName("browseButton")
        self.browseButton.clicked.connect(self.openProject)
        self.addButton = QtWidgets.QDialogButtonBox(Dialog)
        self.addButton.setGeometry(QtCore.QRect(440, 70, 83, 25))
        self.addButton.setObjectName("addButton")
        self.addButton.accepted.connect(Dialog.accept)
        self.linePathEdit = QtWidgets.QLineEdit(Dialog)
        self.linePathEdit.setGeometry(QtCore.QRect(30, 40, 391, 25))
        self.linePathEdit.setObjectName("linePathEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 401, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.browseButton.setText(_translate("Dialog", "Browse"))
        self.label.setText(_translate("Dialog", "Open Existing Project"))
        self.addButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)

    def openProject(self):
        '''
        Open the selected project
        '''
        title = "Please select Project"
        directory = "./"
        #Look for files with pdbproj extension only
        ftype = "JSON files (*.pdbproj)"
        dialog = QtWidgets.QFileDialog(None, title, directory, ftype)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.filename = str(dialog.selectedFiles()[0])
            self.linePathEdit.setText(self.filename)