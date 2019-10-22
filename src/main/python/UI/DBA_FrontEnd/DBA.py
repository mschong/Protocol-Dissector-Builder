# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dissectorbuilderarea.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
#from StartField import StartField

from UI.DBA_FrontEnd.Field import Field
from UI.DBA_FrontEnd.Loop import Loop
from UI.DBA_FrontEnd.Decision import Decision
from UI.DBA_FrontEnd.GraphicsProxyWidget import GraphicsProxyWidget
from UI.DBA_FrontEnd.DropGraphicsScene import DropGraphicsScene
from UI.DBA_FrontEnd.DragButton import DragButton
class QGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(QGraphicsView, self).__init__(parent)
        
    #This helps zoom in and out the canvas 
    #RESOURCE: https://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel
    def wheelEvent(self, event):
        
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        oldPos = self.mapToScene(event.pos())

        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        newPos = self.mapToScene(event.pos())

        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 550)
        self.dba_label = QtWidgets.QLabel(Form)
        self.dba_label.setGeometry(QtCore.QRect(120, 10, 151, 16))
        self.dba_label.setObjectName("dba_label")
        self.graphicsView = QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(35, 31, 600, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = DropGraphicsScene(QtCore.QRectF(0,0,self.graphicsView.width(), self.graphicsView.height()))
        self.graphicsView.setScene(self.scene)
        self.toolbox_label = QtWidgets.QLabel(Form)
        self.toolbox_label.setGeometry(QtCore.QRect(650, 10, 64, 17))
        self.toolbox_label.setObjectName("toolbox_label")
        self.toolBox = QtWidgets.QToolBox(Form)
        self.toolBox.setGeometry(QtCore.QRect(650, 30, 201, 251))
        self.toolBox.setObjectName("toolBox")
        self.field_tab = QtWidgets.QWidget()
        self.field_tab.setGeometry(QtCore.QRect(0, 0, 201, 65))
        self.field_tab.setObjectName("field_tab")
        

        self.field_button = DragButton('Field', self.field_tab)
        self.field_button.setGeometry(QtCore.QRect(20, 30, 171, 65))
        self.field_button.setObjectName("field_button")


        self.toolBox.addItem(self.field_tab, "")
        self.construct_tab = QtWidgets.QWidget()
        self.construct_tab.setGeometry(QtCore.QRect(0, 0, 201, 189))
        self.construct_tab.setObjectName("construct_tab")
        self.decision_button = DragButton("Decision", self.construct_tab)
        self.decision_button.setGeometry(QtCore.QRect(0, 0, 83, 25))
        self.decision_button.setObjectName("decision_button")
        

        self.loop_button =DragButton("Loop", self.construct_tab)
        self.loop_button.setGeometry(QtCore.QRect(0, 30, 83, 25))
        self.loop_button.setObjectName("loop_button")
        #self.loop_button.clicked.connect(self.open_loop_window)

        self.connector_button = QtWidgets.QPushButton('Connector', self.construct_tab)
        self.connector_button.setGeometry(QtCore.QRect(0,60,83,25))
        self.connector_button.setObjectName("connector_button")
        self.connector_button.setCheckable(True)
        self.connector_button.clicked.connect(self.connector_button_clicked)

        self.toolBox.addItem(self.construct_tab, "")

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dba_label.setText(_translate("Form", "Dissector Builder Area"))
        self.toolbox_label.setText(_translate("Form", "Toolbox"))
        #self.startField_button.setText(_translate("Form", "Start Field"))
        #self.field_button.setText(_translate("Form", "Field"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.field_tab), _translate("Form", "Field"))
        #self.decision_button.setText(_translate("Form", "Decision"))
       # self.loop_button.setText(_translate("Form", "Loop"))
        
        self.toolBox.setItemText(self.toolBox.indexOf(self.construct_tab), _translate("Form", "Construct"))

    def open_field_window(self):
        self.field_win = Field()
        self.field_win.show()

    def open_loop_window(self):
        self.loop_win = Loop()
        self.loop_win.show()

    def open_decision_window(self):
        self.decision_win = Decision()
        self.decision_win.show()

    def connector_button_clicked(self):
        if(self.connector_button.isChecked()):
            self.scene.setMode(self.scene.InsertLine_ON)
        else:
            self.scene.setMode(self.scene.InsertLine_OFF)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
