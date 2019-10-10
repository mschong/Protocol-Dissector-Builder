# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetpreview.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QBrush, QColor
import sys
sys.path.append('../..')
from Backend.PCAP import PCAP
from Backend.PCAP import parsePDML


class Ui_PackagePreview(object):
    def setupUi(self, PackagePreview):
        PackagePreview.setObjectName("PackagePreview")
        PackagePreview.resize(880, 454)
        
        self.treeView = QtWidgets.QTreeView(PackagePreview)
        self.treeView.setGeometry(QtCore.QRect(0, 50, 400, 401))
        self.treeView.setObjectName("treeView")

        self.model = QtGui.QStandardItemModel(0,1)
        self.treeView.setModel(self.model)

        self.treeView2 = QtWidgets.QTreeView(PackagePreview)
        self.treeView2.setGeometry(QtCore.QRect(530, 50, 321, 381))
        self.treeView2.setObjectName("treeView")
        # self.treeView2.setStyleSheet("text-color: green")

        self.model2 = QtGui.QStandardItemModel(0,1)
        self.treeView2.setModel(self.model2)


       # self.listView = QtWidgets.QListView(PackagePreview)
       # self.listView.setEnabled(False)
       # self.listView.setGeometry(QtCore.QRect(530, 50, 321, 381))
       # self.listView.setObjectName("listView")

        self.pushButton = QtWidgets.QPushButton(PackagePreview)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)

        self.pushButton2 = QtWidgets.QPushButton(PackagePreview)
        self.pushButton2.setGeometry(QtCore.QRect(415, 200, 101, 40))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.clicked.connect(self.dissect)
           
        self.label = QtWidgets.QLabel(PackagePreview)
        self.label.setGeometry(QtCore.QRect(530, 30, 131, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PackagePreview)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 101, 17))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(PackagePreview)
        QtCore.QMetaObject.connectSlotsByName(PackagePreview)

    name = ""
    def openFile(self):
        fname = QFileDialog.getOpenFileName()
        global name
        name = fname[0]
        PCAPFile = PCAP.PCap(fname[0])
        PCAPFile.convertPCAP()
        i=0
        for pkt in PCAPFile.pcapFile:
            branch1= QtGui.QStandardItem("Packet #")
            k=0
            number = pkt.frame_info.get_field_value("number")
            for protocol in (pkt.frame_info.protocols).split(":"):
                #ProtocolToAdd = QtGui.QStandardItem("Protocol" + str(k))
                ProtocolToAdd = QtGui.QStandardItem("Protocol:" + protocol)
                try:
                    for val in pkt[protocol].field_names:
                        if(val != "payload" and val !="data"):
                            ProtocolField = QtGui.QStandardItem(val)
                            ProtocolValue = QtGui.QStandardItem(pkt[protocol].get_field_value(val))
                            ProtocolToAdd.appendRow([ProtocolField,ProtocolValue])
                    k= k+1
                    branch1.appendRow(ProtocolToAdd)
                except:
                    pass
            self.model.appendRow([branch1,QtGui.QStandardItem(str(number))])
    
    def dissect(self):
        print("MESSAGE")
        print(name)
        PCAPFileD = PCAP.PCap(name)
        PCAPFileD.dissectPCAP()
        PCAPFileD.colorFilter()
        color = QColor(255,0,0) #red
        i=0
        j=0
        for pkt in PCAPFileD.pcapFile:
            if PCAPFileD.colorList[j] == "Green":
                color = QColor(0,255,0)#green
            elif PCAPFileD.colorList[j] == "Red":
                color = QColor(255,0,0) #red
            else:
                color = QColor(255,255,0) #yellow
            branch2= QtGui.QStandardItem("Packet #")
            k=0
            number = pkt.frame_info.get_field_value("number")
            for protocol in (pkt.frame_info.protocols).split(":"):
                ProtocolToAdd = QtGui.QStandardItem("Protocol: " + protocol)

                ProtocolToAdd.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                try:
                    for val in pkt[protocol].field_names:
                        if(val != "payload" and val !="data"):
                            ProtocolField = QtGui.QStandardItem(val)
                            ProtocolValue = QtGui.QStandardItem(pkt[protocol].get_field_value(val))
                            ProtocolToAdd.appendRow([ProtocolField,ProtocolValue])
                            
                            ProtocolValue.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                            ProtocolField.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                    k= k+1
                    branch2.appendRow(ProtocolToAdd)

                    branch2.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                    
                except:
                    pass
            numberCol = QtGui.QStandardItem(str(number))
            self.model2.appendRow([branch2,numberCol])

            numberCol.setData(QBrush(color), QtCore.Qt.BackgroundRole)
            j+=1
        

       

    def retranslateUi(self, PackagePreview):
        _translate = QtCore.QCoreApplication.translate
        PackagePreview.setWindowTitle(_translate("PackagePreview", "PackagePreview"))
        self.pushButton.setText(_translate("PackagePreview", "File"))
        self.pushButton2.setText(_translate("PackagePreview", "Dissect >"))
        self.label.setText(_translate("PackagePreview", "Dissected Data"))
        self.label_2.setText(_translate("PackagePreview", "Packet Stream"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PackagePreview = QtWidgets.QWidget()
    ui = Ui_PackagePreview()
    ui.setupUi(PackagePreview)
    PackagePreview.show()
    sys.exit(app.exec_())
