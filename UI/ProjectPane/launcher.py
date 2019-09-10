#
# This will be the main entry point for the GUI
# evazquez 9/9/2019
#
# it is not complete,
# TODO: I need to complete implementation for both
#  push-buttons to create and open workspace
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import ntpath
sys.path.append('../..')
#from UI.MainPane import mainpane
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from UI.MainPane import mainpane
from Backend.Workspace import workspaceloader
from Backend.Workspace import workspace

class Ui_LauncherDialog(object):
    def setupUi(self, LancherForm):
        LancherForm.setObjectName("LancherForm")
        LancherForm.resize(635, 186)
        LancherForm.setMinimumSize(QtCore.QSize(635, 186))
        LancherForm.setMaximumSize(QtCore.QSize(635, 186))
        self.label = QtWidgets.QLabel(LancherForm)
        self.label.setGeometry(QtCore.QRect(110, 10, 421, 51))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.openWorkspaceButton = QtWidgets.QCommandLinkButton(LancherForm)
        self.openWorkspaceButton.setGeometry(QtCore.QRect(210, 110, 221, 41))
        self.openWorkspaceButton.setObjectName("openWorkspaceButton")
        self.openWorkspaceButton.clicked.connect(self.openworkspace)
        self.newWorkspaceButton = QtWidgets.QCommandLinkButton(LancherForm)
        self.newWorkspaceButton.setGeometry(QtCore.QRect(210, 70, 221, 41))
        self.newWorkspaceButton.setObjectName("newWorkspaceButton")

        self.retranslateUi(LancherForm)
        QtCore.QMetaObject.connectSlotsByName(LancherForm)

    def retranslateUi(self, LancherForm):
        _translate = QtCore.QCoreApplication.translate
        LancherForm.setWindowTitle(_translate("LancherForm", "Protocol Dissector Builder"))
        self.label.setText(_translate("LancherForm", "Protocol Dissector Builder"))
        self.openWorkspaceButton.setText(_translate("LancherForm", "Open Workspace"))
        self.newWorkspaceButton.setText(_translate("LancherForm", "Create New Workspace"))

    def openworkspace(self):
        title = "Please select Workspace"
        suggesteddir = "~/"
        type = "XML files (*.xml)"
        dialog = QtWidgets.QFileDialog(None, title, suggesteddir, type)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.file = str(dialog.selectedFiles()[0])
            wsname = ntpath.basename(self.file)
            wspath = ntpath.dirname(self.file)
            wsl = workspaceloader.WorkspaceLoader()
            wspace = wsl.loadworkspace(wsname, wspath)
            main = mainpane.Ui_MainDialog(wspace)


    def loadworkspace(self):
        wsname = "untitled"
        wsprojects = None
        wspace = workspace.Workspace(wsname, wsprojects)
        main = mainpane.Ui_MainDialog(wspace)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    launcher = QtWidgets.QWidget()
    ui = Ui_LauncherDialog()
    ui.setupUi(launcher)
    launcher.show()
    sys.exit(app.exec_())