
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
import Pyro4
import Pyro4.util
import os, sys, ntpath
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from UI.OpenWorkspaceDialog import openworkspacedialog
from UI.WorkspaceButton import WorkspaceButton
from UI.WorkspaceConfigDialog import workspaceconfigwindow
from UI.CloseWorkspaceDialog import closeworkspacewindow
from UI.OpenProjectDialog import openprojectwindow
from UI.DBA_FrontEnd import DBA
from UI.PacketPreview import packetpreview
from UI.ProjectConfigDialog import projectconfig

class UiMainWindow(object):

    workspace_file = None
    pyro_proxy = None
    dba_form = None
    packetpreview_form = None


    def setupUi(self, MainWindow):

        ## Pyro
        ns = Pyro4.locateNS()
        uri = ns.lookup("pyro.service")
        self.pyro_proxy = Pyro4.Proxy(uri)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(0, 30, 211, 521))
        self.treeView.setObjectName("treeView")
        self.canvasFrame = QtWidgets.QFrame(self.centralwidget)
        self.canvasFrame.setGeometry(QtCore.QRect(210, 30, 991, 521))
        self.canvasFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvasFrame.setObjectName("canvasFrame")
     

        ## Dissector Builder Area (DBA)
        self.dba_form = QtWidgets.QWidget()
        dba_ui = DBA.Ui_Form()
        dba_ui.setupUi(self.dba_form)
        canvas_layout = QtWidgets.QVBoxLayout()
        canvas_layout.addWidget(self.dba_form)
        self.canvasFrame.setLayout(canvas_layout)

        #Project navigator
        self.workspaceLabel = QtWidgets.QLabel(self.centralwidget)
        self.workspaceLabel.setGeometry(QtCore.QRect(390, 10, 300, 17))
        self.workspaceLabel.setText("")
        self.workspaceLabel.setObjectName("workspaceLabel")
        self.workspaceButton = QtWidgets.QPushButton(self.centralwidget)
        self.workspaceButton.setGeometry(QtCore.QRect(10, 50, 181, 25))
        self.workspaceButton.setObjectName("workspaceButton")
        self.workspaceButton.clicked.connect(self.addContextMenuToSelfWorkspaceOpenButton)
        self.packetPreviewFrame = QtWidgets.QFrame(self.centralwidget)
        self.packetPreviewFrame.setGeometry(QtCore.QRect(0, 560, 1201, 201))
        self.packetPreviewFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.packetPreviewFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        ## Packet Preview Pane
        self.packetpreview_form = QtWidgets.QWidget()
        packetpreview_ui = packetpreview.Ui_PackagePreview()
        packetpreview_ui.setupUi(self.packetpreview_form)
        ppreview_layout = QtWidgets.QVBoxLayout()
        ppreview_layout.addWidget(self.packetpreview_form)
        self.packetPreviewFrame.setLayout(ppreview_layout)
       

        self.packetPreviewFrame.setObjectName("packetPreviewFrame")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
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
        self.workspaceButton.setText(_translate("MainWindow", "Options"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        
    # WORKSPACE FUNCTIONS
    def openworkspace(self):
        dialog = QtWidgets.QDialog()
        openWorkspaceUi = openworkspacedialog.Ui_OpenWorkspaceDialog()
        openWorkspaceUi.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.workspace_file = openWorkspaceUi.filename
            ws_name = self.loadWorkspace()
            self.workspaceLabel.setText(ws_name)

    def saveWorkspace(self, wsname):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Do you want to save your changes to workspace " + wsname + " ?")
        msgBox.setWindowTitle("Save")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QtWidgets.QMessageBox.Cancel:
            return False
        elif result == QtWidgets.QMessageBox.Discard:
            return True
        elif result == QtWidgets.QMessageBox.Save:
            return self.pyro_proxy.save_workspace()

    def closeWorkspace(self):
        self.workspaceLabel.setText("")
        self.workspace_file = None
        self.pyro_proxy.close_workspace()
        

    def loadWorkspace(self):
        if self.workspace_file == None or self.workspace_file == "":
            errmsg = "Error While loading Workspace: Workspace cannot be None or Empty"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)
            return
        try:
            
            JSON = self.pyro_proxy.load_workspace(self.workspace_file)
            self.moveWorkspaceButtonToBottom()
            if JSON['projects'] != None:
                projects = JSON['projects']
                #print(projects[str(0)])
                spacing = 0
                for project in projects:
                    print(project)
                    button = self.createWorspaceGenericButton(projects[str(project)]['name'],spacing)
                    self.moveGenericWorkspaceButtonToBottom(button,spacing)
                    spacing += 30
                    
            return JSON['name']
        except Exception as ex:
            errmsg = "Error while loading Workspace: " + str(ex)
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)


    def closeWorkspaceDialog(self):
        dialog = QtWidgets.QDialog()
        cwUi = closeworkspacewindow.Ui_Dialog()
        cwUi.setupUi(dialog)
        msg = "Are you sure you would like to close Workspace  ?"
        cwUi.messageLabel.setText(msg)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.closeWorkspace()
        
    def moveWorkspaceButtonToBottom(self):
        currentPos = self.workspaceButton.pos()
        x = currentPos.x()
        y = self.treeView.rect().bottom()
        point = QtCore.QPoint(x, y)
        self.workspaceButton.move(point)

    def createWorspaceGenericButton(self, wsname,spacing):
        button = WorkspaceButton.WorkspaceButton(wsname, self.centralwidget)
        button.setGeometry(QtCore.QRect(10, 50+spacing, 181, 25))
        button.clicked.connect(self.displayProject)
        button.workspace_name = wsname
        return button

    def moveGenericWorkspaceButtonToBottom(self, button,spacing):
        y = self.treeView.rect().top() + (20 + spacing)
        x = self.workspaceButton.pos().x()
        point = QtCore.QPoint(x, y)
        button.move(point)
        button.show()

    def displayProject():
        pass

    def openWorkpaceConfigDialog(self, wsName=None, wsStartDate=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), wsEditDate=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")):
        dialog = QtWidgets.QDialog()
        wcUi = workspaceconfigwindow.Ui_Dialog()
        wcUi.setupUi(dialog)
        wcUi.workspaceFileLineEdit.setText(wsName)
        wcUi.startDateLabel.setText(wsStartDate)
        wcUi.editDateLabel.setText(wsEditDate)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if wcUi.workspaceFileLineEdit.text() != wsName:
                wsName = wcUi.workspaceFileLineEdit.text()
                self.pyro_proxy.new_workspace(wsName,wsStartDate,wsEditDate)
                self.workspaceLabel.setText(wsName)
                self.moveWorkspaceButtonToBottom()
                self.workspace_file = "{}.json".format(wsName)
                self.loadWorkspace()
    
    def openProjectConfigDialog(self,pname=None,pauthor = None,pdesc=None,created=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), edited=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")):
        dialog = QtWidgets.QDialog()
        pUi = projectconfig.P_Dialog()
        pUi.setupUi(dialog)
        pUi.lineEdit.setText(pname)
        pUi.lineEdit_2.setText(pauthor)
        pUi.lineEdit_3.setText(pdesc)
        pUi.label_6.setText(created)
        pUi.label_7.setText(edited)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if pUi.lineEdit.text() != pname:
                pname = pUi.lineEdit.text()
                pauthor = pUi.lineEdit_2.text()
                pdesc = pUi.lineEdit_3.text()
                self.pyro_proxy.new_project(pname,pauthor,pdesc,created,edited)
                self.loadWorkspace()
   
    def addContextMenuToSelfWorkspaceOpenButton(self):
        self.workspaceButton.menu = QtWidgets.QMenu()
        newWsAction = self.workspaceButton.menu.addAction("New Workspace")
        openWsAction = self.workspaceButton.menu.addAction("Open Workspace")
        #ADD CONFIGURE
        configureWsAction = self.workspaceButton.menu.addAction("Configure Workspace")
        closeWsAction = self.workspaceButton.menu.addAction("Close Workspace [X]")
        addProject = self.workspaceButton.menu.addAction("Add project")
        importProject = self.workspaceButton.menu.addAction("Import project")
        action = self.workspaceButton.menu.exec_(self.getDefaultContextMenuQPointforButton(self.workspaceButton))
        if action == newWsAction:
            self.openWorkpaceConfigDialog()
        elif action == openWsAction:
            self.openworkspace()
        elif action == configureWsAction:
            try:
                wsdata = self.pyro_proxy.get_current_workspace()
                if (wsdata == None):
                    self.showErrorMessage("Unable to retrieve Worskpace Information. Workspace data returned empty")
                    return
                self.openWorkpaceConfigDialog(wsdata['name'], wsdata['created'], wsdata['edited'])
            except Exception as ex:
                self.showErrorMessage("Unable to retrieve Worskpace Information: " + str(ex))
        
        elif action == closeWsAction:
            try:
                self.closeWorkspaceDialog()
            except Exception as ex:
                self.showErrorMessage("Unable to close Workspace " + str(ex))
        elif action == addProject:
            self.openProjectConfigDialog()
        elif action == importProject:
            self.openProjectDialog()

   

    #PROJECT FUNCTIONS
    def showErrorMessage(self, errostr):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(str(errostr))
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

    
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

    
        

    def openProjectDialog(self):
        dialog = QtWidgets.QDialog()
        opUi = openprojectwindow.Ui_Dialog()
        opUi.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
             self.pyro_proxy.import_project(opUi.filename)
             self.loadWorkspace()

   

   
