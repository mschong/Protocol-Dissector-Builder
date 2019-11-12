from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(1, "../")
from UI.MainPane import mainwindow
from Backend import pyro_run
import threading
import time

#
# Loads GUI
# Pyro service needs to be started before running GUI (run start-pyro service script)
if __name__ == "__main__":
    pyro = pyro_run.Pyro_Run()
    
    pyro_thread = threading.Thread(target=pyro.main)
    pyro_thread.start()
    time.sleep(10)
    appctxt = ApplicationContext()
    app = QtWidgets.QApplication(sys.argv)
    mainDialog = QtWidgets.QMainWindow()
    ui = mainwindow.UiMainWindow()
    ui.setupUi(mainDialog)
    mainDialog.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
