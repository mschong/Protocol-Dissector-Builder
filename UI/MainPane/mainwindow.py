import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from Backend.Workspace import workspaceloader
from Backend.Workspace import workspace
from UI.OpenWorkspaceDialog import openworkspacedialog

class UiMainWindow(object):

    workspace_file = None
    workspace = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(0, 30, 211, 521))
        self.treeView.setObjectName("treeView")
        self.toolboxFrame = QtWidgets.QFrame(self.centralwidget)
        self.toolboxFrame.setGeometry(QtCore.QRect(210, 30, 171, 521))
        self.toolboxFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolboxFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolboxFrame.setObjectName("toolboxFrame")
        self.canvasFrame = QtWidgets.QFrame(self.centralwidget)
        self.canvasFrame.setGeometry(QtCore.QRect(380, 30, 611, 521))
        self.canvasFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvasFrame.setObjectName("canvasFrame")
        self.workspaceLabel = QtWidgets.QLabel(self.centralwidget)
        self.workspaceLabel.setGeometry(QtCore.QRect(390, 10, 300, 17))
        self.workspaceLabel.setText("")
        self.workspaceLabel.setObjectName("workspaceLabel")
        self.workspaceButton = QtWidgets.QPushButton(self.centralwidget)
        self.workspaceButton.setGeometry(QtCore.QRect(10, 50, 181, 25))
        self.workspaceButton.setObjectName("workspaceButton")
        #self.workspaceButton.clicked.connect(self.openworkspace)
        self.workspaceButton.clicked.connect(self.addContextMenuToWorkspaceOpenButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Protocol Dissector Window"))
        self.workspaceButton.setText(_translate("MainWindow", "Add Workspace +"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))

    def openworkspace(self):
        dialog = QtWidgets.QDialog()
        openWorkspaceUi = openworkspacedialog.Ui_OpenWorkspaceDialog()
        openWorkspaceUi.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.workspace_file = openWorkspaceUi.linePath.text()
            self.workspaceLabel.setText(self.workspace_file)
            self.loadWorkspace()

    def createemptyworkspace(self, name):
        self.workspace = workspace.Workspace(name, None)

    def loadWorkspace(self):
        if self.workspace_file == None or self.workspace_file == "":
            errmsg = "Error While loading Workspace: Workspace cannot be None or Empty"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)
            return
        wsname = ntpath.basename(self.workspace_file)
        wspath = ntpath.dirname(self.workspace_file)
        try:
            wsl = workspaceloader.WorkspaceLoader()
            self.workspace = wsl.loadworkspace(self.workspace_file)
        except:
            errmsg = "Error While loading Workspace"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)

    def runWithUnsavedWorkspace(self):
        self.workspace = workspace.Workspace("untitled", None)
        self.workspaceLabel.setText("Untitled Workspace*")
        print("[+] Created generic untitled workspace")

    def addContextMenuToWorkspace(self, event):
        cmenu = QtWidgets.QMenu()
        addNewProjectAction = cmenu.addAction("Add Project [+]")
        configureAction = cmenu.addAction("Configure Workspace")
        closeWorkspaceAction = cmenu.addAction("Close Workspace [X]")
        #cmenu.exec_(self.mapToGlobal(event.pos()))

    def showErrorMessage(self, errostr):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(str(errostr))
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    def addContextMenuToWorkspaceOpenButton(self):
        self.workspaceButton.menu = QtWidgets.QMenu()
        newWsAction = self.workspaceButton.menu.addAction("New Workspace")
        openWsAction = self.workspaceButton.menu.addAction("Open Workspace ...")
        action = self.workspaceButton.menu.exec_(self.workspaceButton.mapToGlobal(QtCore.QPoint(self.workspaceButton.pos())))
        if action == newWsAction:
            self.runWithUnsavedWorkspace()
        elif action == openWsAction:
            self.openworkspace()


if __name__ == "__main__":
    print("[+] Initializing GUI")
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    sys.exit(app.exec_())