import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from Backend.Workspace import workspaceloader
from Backend.Workspace import workspace
from UI.OpenWorkspaceDialog import openworkspacedialog

class UiMainWindow(object):
    workspace_pool = None
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
        self.workspaceLabel.setGeometry(QtCore.QRect(390, 10, 500, 17))
        self.workspaceLabel.setText("")
        self.workspaceLabel.setObjectName("workspaceLabel")
        self.workspaceButton = QtWidgets.QPushButton(self.centralwidget)
        self.workspaceButton.setGeometry(QtCore.QRect(10, 50, 181, 25))
        self.workspaceButton.setObjectName("workspaceButton")
        self.workspaceButton.clicked.connect(self.addContextMenuToSelfWorkspaceOpenButton)
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
            self.moveWorkspaceButtonToBottom()
        except:
            errmsg = "Error While loading Workspace"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)

    def runWithUnsavedWorkspace(self):
        self.workspace = workspace.Workspace("untitled", None)
        self.workspaceLabel.setText("Untitled Workspace*")
        print("[+] Created generic untitled workspace")
        self.moveWorkspaceButtonToBottom()

    def showErrorMessage(self, errostr):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(str(errostr))
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    def addContextMenuToSelfWorkspaceOpenButton(self):
        self.workspaceButton.menu = QtWidgets.QMenu()
        newWsAction = self.workspaceButton.menu.addAction("New Workspace")
        openWsAction = self.workspaceButton.menu.addAction("Open Workspace ...")
        action = self.workspaceButton.menu.exec_(self.getDefaultContextMenuQPointforButton(self.workspaceButton))
        if action == newWsAction:
            self.runWithUnsavedWorkspace()
        elif action == openWsAction:
            self.openworkspace()

    def addContextMenuToProject(self, parent):
        parent.menu = QtWidgets.QMenu()
        saveProjectAction = parent.menu.addAction("Save Project")
        exportProjectAction = parent.menu.addAction("Export Dissector [ -> ]")
        configureProjectAction = parent.menu.addAction("Configure Project")
        closeProjectAction = parent.menu.addAction("Close Project [ X ]")

    def addContextMenuToWorskpaceGenericButton(self, parent):
        parent.menu = QtWidgets.QMenu()
        addWsAction = parent.menu.addAction("Add a Project")
        configureWsAction = parent.menu.addAction("Configure Workspace")
        closeWsAction = parent.menu.addAction("Close Workspace [ X ]")

    def getDefaultContextMenuQPointforButton(self, button):
        point = QtCore.QPoint()
        point.setX(button.pos().x())
        point.setY(button.pos().y() + 70)
        return point

    def moveWorkspaceButtonToBottom(self):
        currentPos = self.workspaceButton.pos()
        x = currentPos.x()
        y = self.treeView.rect().bottom()
        point = QtCore.QPoint(x, y)
        self.workspaceButton.move(point)

    def createWorspaceGenericButton(self, wspace):
        button = QtWidgets.QPushButton()
        button.setText(wspace.name)
        self.addContextMenuToWorskpaceGenericButton(button)
        return button

if __name__ == "__main__":
    print("[+] Initializing GUI")
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    sys.exit(app.exec_())