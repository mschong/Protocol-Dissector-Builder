import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
#from Backend.Workspace import workspaceloader
#from Backend.Workspace import workspace
from UI.OpenWorkspaceDialog import openworkspacedialog
from UI.WorkspaceButton import WorkspaceButton
import Pyro4
import Pyro4.util
from Backend.Workspace import workspace

class UiMainWindow(object):
    workspace_pool = []
    workspace_file = None

    def setupUi(self, MainWindow):
        self.pyro = Pyro4.Proxy("PYRONAME:pyro.service")
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
        ws = workspace.Workspace(name, None)
        self.appendToWorkspacePool(ws)

    def loadWorkspace(self):
        if self.workspace_file == None or self.workspace_file == "":
            errmsg = "Error While loading Workspace: Workspace cannot be None or Empty"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)
            return
        try:
            #wsl = workspaceloader.WorkspaceLoader()
            ws = self.pyro.loadworkspace(self.workspace_file)
            self.moveWorkspaceButtonToBottom()
            self.appendToWorkspacePool(ws)
            self.moveWorkspaceButtonToBottom()
            button = self.createWorspaceGenericButton(ws)
            self.moveGenericWorkspaceButtonToBottom(button)

        except:
            errmsg = "Error While loading Workspace "
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)

    def appendToWorkspacePool(self, wspace):
        if wspace is None or type(wspace) != workspace.Workspace:
            errormsg = "Invalid object type for workspace"
            print("[-] " + errormsg)
            self.showErrorMessage(errormsg)
            return
        for ws in self.workspace_pool:
            if wspace.name == ws.name:
                errormsg = "Workspace " + wspace.name + " already loaded"
                print("[-] " + errormsg)
                self.showErrorMessage(errormsg)
                return
        self.workspace_pool.append(wspace)
        print("[+] Workspace " + wspace.name + " added to Workspace pool")

    def runWithUnsavedWorkspace(self):
        ws = workspace.Workspace("untitled", None)
        self.appendToWorkspacePool(ws)
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
        action = parent.menu.exec_(self.getDefaultContextMenuQPointforButton(parent))

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
        button = WorkspaceButton.WorkspaceButton(wspace.name, self.centralwidget)
        button.workspace = wspace
        button.setGeometry(QtCore.QRect(10, 50, 181, 25))
        #self.addContextMenuToWorskpaceGenericButton(button)
        return button

    def moveGenericWorkspaceButtonToBottom(self, button):
        y = self.treeView.rect().top() + 40
        x = self.workspaceButton.pos().x()
        point = QtCore.QPoint(x, y)
        button.move(point)
        button.show()


if __name__ == "__main__":
    print("[+] Initializing GUI")
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    sys.exit(app.exec_())
    sys.excepthook = Pyro4.util.excepthook