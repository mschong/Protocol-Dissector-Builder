#
# This will be the main entry point for the GUI
# evazquez 9/9/2019
#
# it is not complete, I need to complete implementation for both
# push-buttons to create and open workspace
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_LancherForm(object):
    def setupUi(self, LancherForm):
        LancherForm.setObjectName("LancherForm")
        LancherForm.resize(645, 213)
        LancherForm.setMinimumSize(QtCore.QSize(0, 0))
        self.label = QtWidgets.QLabel(LancherForm)
        self.label.setGeometry(QtCore.QRect(110, 10, 421, 51))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.openWorkspaceButton = QtWidgets.QCommandLinkButton(LancherForm)
        self.openWorkspaceButton.setGeometry(QtCore.QRect(210, 130, 251, 41))
        self.openWorkspaceButton.setObjectName("openWorkspaceButton")
        self.newWorkspaceButton = QtWidgets.QCommandLinkButton(LancherForm)
        self.newWorkspaceButton.setGeometry(QtCore.QRect(210, 90, 251, 41))
        self.newWorkspaceButton.setObjectName("newWorkspaceButton")

        self.retranslateUi(LancherForm)
        QtCore.QMetaObject.connectSlotsByName(LancherForm)

    def retranslateUi(self, LancherForm):
        _translate = QtCore.QCoreApplication.translate
        LancherForm.setWindowTitle(_translate("LancherForm", "Protocol Dissector Builder"))
        self.label.setText(_translate("LancherForm", "Protocol Dissector Builder"))
        self.openWorkspaceButton.setText(_translate("LancherForm", "Open Workspace"))
        self.newWorkspaceButton.setText(_translate("LancherForm", "Create New Workspace"))

    def openproject(self):
        title = "Please select Project"
        suggesteddir = "~/"
        type = "all files (*.*)"
        dialog = QFileDialog(None, title, suggesteddir, type)
        if dialog.exec_() == QDialog.Accepted:
            self.file = str(dialog.selectedFiles()[0])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = QtWidgets.QWidget()
    ui = Ui_LancherForm()
    ui.setupUi(launcher)
    launcher.show()
    sys.exit(app.exec_())