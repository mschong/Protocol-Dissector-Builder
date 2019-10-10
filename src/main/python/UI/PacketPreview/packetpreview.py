# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetpreview.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
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

        self.model = QtGui.QStandardItemModel(0,2)
        self.treeView.setModel(self.model)

        self.pushButton2 = QtWidgets.QPushButton(PackagePreview)
        self.pushButton2.setGeometry(QtCore.QRect(415, 200, 101, 40))
        self.pushButton2.setObjectName("pushButton_2")
        self.pushButton2.clicked.connect(self.dissect)

        self.listView = QtWidgets.QListView(PackagePreview)
        self.listView.setEnabled(False)
        self.listView.setGeometry(QtCore.QRect(530, 50, 321, 381))
        self.listView.setObjectName("listView")

        self.pushButton = QtWidgets.QPushButton(PackagePreview)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)

        self.label = QtWidgets.QLabel(PackagePreview)
        self.label.setGeometry(QtCore.QRect(530, 30, 131, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PackagePreview)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 101, 17))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(PackagePreview)
        QtCore.QMetaObject.connectSlotsByName(PackagePreview)

    def openFile(self):
        fname = QFileDialog.getOpenFileName()
        PCAPFile = PCAP.PCap(fname[0])
        PCAPFile.convertPCAP()
        i=0
        for pkt in PCAPFile.pcapFile:
            branch1= QtGui.QStandardItem("Package #")
            k=0
            number = pkt.frame_info.get_field_value("number")
            for protocol in (pkt.frame_info.protocols).split(":"):
                ProtocolToAdd = QtGui.QStandardItem("Protocol #" + str(k))
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
        print("Hello")

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
