import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CodeBlock(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Code Block")
        self.setGeometry(20,20,396,307)
        # Setting up the window
        self.layout = QVBoxLayout()

        self.textBox = QPlainTextEdit()
        self.textBox.move(20,20)
        self.textBox.resize(350,270)
        self.layout.addWidget(self.textBox)
        self.setLayout(self.layout)

        self.show()


    def saveMethod(self):
        code_block_properties = dict({'Code':self.textBox.toPlainText()})
        return code_block_properties

if __name__ == '__main__':
    app = QApplication([])
    test = CodeBlock()
    sys.exit(app.exec_())

