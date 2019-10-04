import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
import Pyro4
import Pyro4.util
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from UI.OpenWorkspaceDialog import openworkspacedialog
from UI.WorkspaceButton import WorkspaceButton
from UI.WorkspaceConfigDialog import workspaceconfigwindow
from UI.CloseWorkspaceDialog import closeworkspacewindow
from UI.OpenProjectDialog import openprojectwindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext


class UiMainWindow(object):
    workspace_file = None
    pyro_proxy = None

    def setupUi(self, MainWindow):
        ns = Pyro4.locateNS()
        uri = ns.lookup("pyro.service")
        self.pyro_proxy = Pyro4.Proxy(uri)
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
            self.loadWorkspace()
            self.workspaceLabel.setText(self.workspace_file)

    def loadWorkspace(self):
        if self.workspace_file == None or self.workspace_file == "":
            errmsg = "Error While loading Workspace: Workspace cannot be None or Empty"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)
            return
        try:
            wsname = self.pyro_proxy.load_workspace(self.workspace_file)
            self.moveWorkspaceButtonToBottom()
            button = self.createWorspaceGenericButton(wsname)
            self.moveGenericWorkspaceButtonToBottom(button)
        except Exception as ex:
            errmsg = "Error while loading Workspace: " + str(ex)
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)

    def runWithUnsavedWorkspace(self):
        try:
            wsname = self.pyro_proxy.load_empty_worspace()
            self.workspaceLabel.setText("Untitled Workspace*")
            self.moveWorkspaceButtonToBottom()
            button = self.createWorspaceGenericButton(wsname)
            self.moveGenericWorkspaceButtonToBottom(button)
        except Exception as ex:
            self.showErrorMessage(ex)

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
        closeProjectAction = parent.menu.addAction("Close Project [X]")

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

    def createWorspaceGenericButton(self, wsname):
        button = WorkspaceButton.WorkspaceButton(wsname, self.centralwidget)
        button.setGeometry(QtCore.QRect(10, 50, 181, 25))
        button.clicked.connect(self.addContextMenuToWSGenButton)
        button.workspace_name = wsname
        return button

    def moveGenericWorkspaceButtonToBottom(self, button):
        y = self.treeView.rect().top() + (20 * (self.pyro_proxy.get_workspace_pool_count() + 1))
        x = self.workspaceButton.pos().x()
        point = QtCore.QPoint(x, y)
        button.move(point)
        button.show()

    def RunContextMenuToWorskpaceGenericButton(self,parent):
        parent.menu = QtWidgets.QMenu()
        addProjectAction = parent.menu.addAction("Add a Project")
        configureWsAction = parent.menu.addAction("Configure Workspace")
        closeWsAction = parent.menu.addAction("Close Workspace [X]")
        x = parent.x() + 100
        y = parent.y()
        point = QtCore.QPoint(x, y)
        action = parent.menu.exec_(point)
        if action == addProjectAction:
            self.openProjectDialog(parent.workspace_name)
        elif action == configureWsAction:
            try:
                wsdata = self.pyro_proxy.get_workspace_data_from_pool(parent.workspace_name)
                if (wsdata == None):
                    self.showErrorMessage("Unable to retrieve Worskpace Information. Workspace data returned empty")
                    return
                self.openWorkpaceConfigDialog(wsdata[0], wsdata[1], wsdata[2])
            except Exception as ex:
                self.showErrorMessage("Unable to retrieve Worskpace Information: " + str(ex))
        elif action == closeWsAction:
            try:
                self.closeWorkspaceDialog(parent.workspace_name)
            except Exception as ex:
                self.showErrorMessage("Unable to close Workspace " + str(ex))
        else:
            pass

    def openWorkpaceConfigDialog(self, wsName, wsStartDate, wsEditDate):
        dialog = QtWidgets.QDialog()
        wcUi = workspaceconfigwindow.Ui_Dialog()
        wcUi.setupUi(dialog)
        wcUi.workspaceFileLineEdit.setText(wsName)
        wcUi.startDateLabel.setText(wsStartDate)
        wcUi.editDateLabel.setText(wsEditDate)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if wcUi.workspaceFileLineEdit.text() != wsName:
                # TODO: write code to save workspace
                pass

    def openProjectDialog(self, wsname):
        dialog = QtWidgets.QDialog()
        opUi = openprojectwindow.Ui_Dialog()
        opUi.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass

    def closeWorkspaceDialog(self, wsname):
        dialog = QtWidgets.QDialog()
        cwUi = closeworkspacewindow.Ui_Dialog()
        cwUi.setupUi(dialog)
        msg = "Are you sure you would like to close Workspace " + wsname + " ?"
        cwUi.messageLabel.setText(msg)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # TODO: write code to close workspace
            pass

    def addContextMenuToWSGenButton(self):
        self.RunContextMenuToWorskpaceGenericButton(self.centralwidget.sender())

if __name__ == "__main__":
    print("[+] Initializing GUI")
    appctxt = ApplicationContext() #required for fbs
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    exit_code = appctxt.app.exec_()
    sys.exit(app.exec_())