from PyQt5.QtWidgets import * #QPushButton, QWidget
from PyQt5.QtCore import * #Qt, QMimeData, QRect
from PyQt5.QtGui import *
import sys
class ErrorDialog(QDialog):
    def __init__(self, text):
        super().__init__()

        self.title = "ERROR"
        self.initUI(text)

    def initUI(self, text):
        self.textToDisplay = text
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.textToDisplay)
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.ok_button_clicked)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.show()
    
    def ok_button_clicked(self):
        self.close()