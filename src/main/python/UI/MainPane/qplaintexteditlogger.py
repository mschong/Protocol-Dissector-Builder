import logging
from PyQt5 import QtCore, QtGui, QtWidgets

"""
Code taken from Stackoverflow
reference: https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt/28794076#28794076
Author: mfitzp
"""

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)