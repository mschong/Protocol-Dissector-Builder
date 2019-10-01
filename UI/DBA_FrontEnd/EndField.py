import sys
from PyQt5.QtWidgets import *

class EndField(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("End Field")
        self.setGeometry(100,100,200,100)
        self.show()
if __name__ == '__main__':
    app = QApplication([])
    test = EndField()
    sys.exit(app.exec_())