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
        self.treeView.setGeometry(QtCore.QRect(0, 50, 521, 401))
        self.treeView.setObjectName("treeView")

        self.model = QtGui.QStandardItemModel(0,2)
        self.treeView.setModel(self.model)

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
        useMe = PCAPFile.obtainFilePath()
        parsePDMLOut = parsePDML.makePackets(useMe)
        parsePDML.printPackets(parsePDMLOut[0],parsePDMLOut[1])
        for i in parsePDMLOut[0].keys():
            branch1= QtGui.QStandardItem("Package #")
            tempPackage = parsePDMLOut[0][i]
            k=0
            for Protocol in parsePDMLOut[1][tempPackage]:
                ProtocolToAdd = QtGui.QStandardItem("Protocol #" + str(k))
                for ProtocolField,ProtocolValue in Protocol:
                    ProtocolField = QtGui.QStandardItem(ProtocolField)
                    ProtocolValue = QtGui.QStandardItem(ProtocolValue)
                    ProtocolToAdd.appendRow([ProtocolField,ProtocolValue])
                branch1.appendRow(ProtocolToAdd)
                k = k+1

            self.model.appendRow([branch1,QtGui.QStandardItem(str(i))])

    def retranslateUi(self, PackagePreview):
        _translate = QtCore.QCoreApplication.translate
        PackagePreview.setWindowTitle(_translate("PackagePreview", "PackagePreview"))
        self.pushButton.setText(_translate("PackagePreview", "File"))
        self.label.setText(_translate("PackagePreview", "Dissected Data"))
        self.label_2.setText(_translate("PackagePreview", "Packet Stream"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PackagePreview = QtWidgets.QWidget()
    ui = Ui_PackagePreview()
    ui.setupUi(PackagePreview)
    PackagePreview.show()
    sys.exit(app.exec_())
