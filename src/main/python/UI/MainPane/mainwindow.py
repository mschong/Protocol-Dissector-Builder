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

    packetpreview_ui = None

    dba_scrollarea = None
    treeview_model = None
    dba_pool = []
    MAX_PROJECTS = 10

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
        self.treeView.setGeometry(QtCore.QRect(0, 40, 211, 511))
        self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeView.setObjectName("treeView")
        self.treeview_model = self.createProjectTreeViewModel(self.treeView)
        self.treeView.setModel(self.treeview_model)
        self.canvasFrame = QtWidgets.QScrollArea(self.centralwidget)
        self.canvasFrame.setGeometry(QtCore.QRect(210, 40, 981, 511))
        self.canvasFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvasFrame.setObjectName("canvasFrame")
        self.canvasFrame.setWidgetResizable(True)
        ## Dissector Builder Area (DBA)

        dba_form = QtWidgets.QWidget()
        dba_ui = DBA.Ui_Form()
        dba_ui.setupUi(dba_form)
        self.canvasFrame.setWidget(dba_form)
        self.dba_pool.append(dba_ui)

        self.workspaceLabel = QtWidgets.QLabel(self.centralwidget)
        self.workspaceLabel.setGeometry(QtCore.QRect(213, 10, 971, 20))
        self.workspaceLabel.setText("")
        self.workspaceLabel.setObjectName("workspaceLabel")
      
        self.packetPreviewFrame = QtWidgets.QScrollArea(self.centralwidget)
        self.packetPreviewFrame.setGeometry(QtCore.QRect(0, 560, 1191, 211))
        self.packetPreviewFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.packetPreviewFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.packetPreviewFrame.setObjectName("packetPreviewFrame")
        self.packetPreviewFrame.setWidgetResizable(True)

        ## Packet Preview Pane
        packetpreview_form = QtWidgets.QWidget()
        self.packetpreview_ui = packetpreview.Ui_PackagePreview()
        self.packetpreview_ui.setupUi(packetpreview_form)
        self.packetPreviewFrame.setWidget(packetpreview_form)

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

        #Workspace Options
        self.new_ws = QtWidgets.QAction("New Workspace", self.menubar)
        self.open_ws = QtWidgets.QAction("Open Workspace",self.menubar)
        self.close_ws = QtWidgets.QAction("Close Workspace",self.menubar)
        self.config_ws = QtWidgets.QAction("Configure Workspace",self.menubar)
        #Workspace Options functions
      
        self.new_ws.triggered.connect(self.openWorkpaceConfigDialog)
        self.open_ws.triggered.connect(self.openworkspace)
        self.close_ws.triggered.connect(self.closeWorkspaceDialog)
        self.config_ws.triggered.connect(self.openWorkpaceConfigDialog)
        #Project Options
        self.new_proj = QtWidgets.QAction("New Project",self.menubar)
        self.import_proj =  QtWidgets.QAction("Import Project",self.menubar)
        #Project options functions
        self.new_proj.triggered.connect(self.openProjectConfigDialog)
        self.import_proj.triggered.connect(self.openProjectDialog)


        self.options = [self.new_ws,self.open_ws,self.close_ws,self.config_ws,self.new_proj,self.import_proj]
        self.menuFile.addActions(self.options)
      
        MainWindow.setMenuBar(self.menubar)
       

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Protocol Dissector Window"))
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
        self.clearProjectTreview()

    def loadWorkspace(self):
        if self.workspace_file == None or self.workspace_file == "":
            errmsg = "Error While loading Workspace: Workspace cannot be None or Empty"
            print("[-] " + errmsg)
            self.showErrorMessage(errmsg)
            return
        try:

            JSON = self.pyro_proxy.load_workspace(self.workspace_file)
            if JSON['projects'] != None:
                projects = JSON['projects']
                # print(projects[str(0)])
                self.clearProjectTreview()
                for project in projects:
                    print(projects[str(project)])
                    self.addProjectToTreeView(self.treeview_model, projects[str(project)])

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

  


    

    def openProjectConfigDialog(self, pname=None, pauthor=None, pdesc=None,
                                created=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                                edited=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")):
        pass

    def openWorkpaceConfigDialog(self, wsName=None):
        wsStartDate = None
        wsEditDate = None
        try:
            wsdata = self.pyro_proxy.get_current_workspace()
            if (wsdata != None):
                wsName = wsdata['name']
                wsStartDate = wsdata['created']
                wsEditDate = wsdata['edited']
        finally:   
            if wsName is None or wsName is False:
                    wsName = " "
            if wsStartDate is None :
                wsStartDate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            if wsEditDate is None :
                wsEditDate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            dialog = QtWidgets.QDialog()
            wcUi = workspaceconfigwindow.Ui_Dialog()
            wcUi.setupUi(dialog)
            wcUi.workspaceFileLineEdit.setText(str(wsName))
            wcUi.startDateLabel.setText(wsStartDate)
            wcUi.editDateLabel.setText(wsEditDate)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                if wcUi.workspaceFileLineEdit.text() != wsName:
                    wsName = wcUi.workspaceFileLineEdit.text()
                    self.pyro_proxy.new_workspace(wsName,wsStartDate,wsEditDate)
                    self.workspaceLabel.setText(wsName)
                    self.workspace_file = "{}.json".format(wsName)
                    self.loadWorkspace()
 
   
    

   

    #PROJECT FUNCTIONS
       
    def openProjectConfigDialog(self,pname=None,pauthor = None,pdesc=None,created=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), edited=datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")):
        dialog = QtWidgets.QDialog()
        pUi = projectconfig.P_Dialog()
        pUi.setupUi(dialog)
        if pname is False:
            pname = " "
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
                self.pyro_proxy.new_project(pname, pauthor, pdesc, created, edited)
                self.loadWorkspace()

    # PROJECT FUNCTIONS
    def showErrorMessage(self, errostr):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(str(errostr))
        msgBox.setWindowTitle("Error")
        msgBox.exec_()

  
  
    def openProjectDialog(self):
        dialog = QtWidgets.QDialog()
        opUi = openprojectwindow.Ui_Dialog()
        opUi.setupUi(dialog)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.pyro_proxy.import_project(opUi.filename)
            self.loadWorkspace()

    def createProjectTreeViewModel(self, treeView):
        model = QtGui.QStandardItemModel(0, 1, treeView)
        model.setHeaderData(0, QtCore.Qt.Horizontal, "Projects")
        return model

    def addProjectToTreeView(self, model, project_name):
        
        model.insertRow(0)
        model.setData(model.index(0, 0), project_name)

    def clearProjectTreview(self):
        self.treeview_model.removeRows(0, self.treeview_model.rowCount())
