import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.OpenWorkspaceDialog import openworkspacedialog
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from Backend.Workspace import workspaceloader
from Backend.Workspace import workspace
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenWorkspaceDialog(object):

    def setupUi(self, OpenWorkspaceDialog):
        OpenWorkspaceDialog.setObjectName("OpenWorkspaceDialog")
        OpenWorkspaceDialog.resize(576, 121)
        OpenWorkspaceDialog.setMinimumSize(QtCore.QSize(576, 121))
        OpenWorkspaceDialog.setWindowTitle("")
        self.label = QtWidgets.QLabel(OpenWorkspaceDialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 411, 17))
        self.label.setObjectName("label")
        self.linePath = QtWidgets.QLineEdit(OpenWorkspaceDialog)
        self.linePath.setGeometry(QtCore.QRect(30, 40, 391, 25))
        self.linePath.setObjectName("linePath")
        self.browseButton = QtWidgets.QPushButton(OpenWorkspaceDialog)
        self.browseButton.setGeometry(QtCore.QRect(440, 40, 83, 25))
        self.browseButton.setObjectName("browseButton")
        self.browseButton.clicked.connect(self.openworkspace)
        self.addButton = QtWidgets.QDialogButtonBox(OpenWorkspaceDialog)
        self.addButton.setGeometry(QtCore.QRect(440, 70, 83, 25))
        self.addButton.setObjectName("addButton")
        self.addButton.accepted.connect(OpenWorkspaceDialog.accept)
        self.retranslateUi(OpenWorkspaceDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenWorkspaceDialog)

    def openworkspace(self):
        title = "Please select Workspace"
        directory = "~/"
        type = "XML files (*.xml)"
        dialog = QtWidgets.QFileDialog(None, title, directory, type)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.file = str(dialog.selectedFiles()[0])
            self.linePath.setText(self.file)
            self.path = self.linePath.text

    def retranslateUi(self, OpenWorkspaceDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("OpenWorkspaceDialog", "Create a New Workspace / Open New Workspace"))
        self.browseButton.setText(_translate("OpenWorkspaceDialog", "Browse"))
        self.addButton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)

