'''
@Authors:
    Ernesto Vazquez
    Daniel Ornelas

This is the main module in charge of kickstarting the application.
'''
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(1, "../")
from UI.MainPane import mainwindow
from Backend import pyro_run
import threading
import time

if __name__ == "__main__":
    '''
    Starts pyro service and UI
    '''
    pyro = pyro_run.Pyro_Run()
    #pyro needs to start in a separate thread
    pyro_thread = threading.Thread(target=pyro.main)
    pyro_thread.start()
    #sleep to allow pyro namespace to register
    time.sleep(10)
    #start UI
    appctxt = ApplicationContext()
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = mainwindow.UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
