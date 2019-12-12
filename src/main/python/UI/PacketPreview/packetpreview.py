from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QBrush, QColor
import sys
sys.path.append('../..')
import json
import Pyro4
import Pyro4.util
import os
import logging
import subprocess
from UI.PacketPreview.customSort import sortableElement
from UI.PacketPreview.demo import Demo

class Ui_PackagePreview(object):
    def setupUi(self, PackagePreview):
        ns = Pyro4.locateNS()
        uri = ns.lookup("pyro.service")
        self.pyro_proxy = Pyro4.Proxy(uri)
        PackagePreview.setObjectName("PackagePreview")
        PackagePreview.resize(400, 200)
        #PackagePreview.setMinimumSize(QtCore.QSize(100, 454))
        self.treeView = QtWidgets.QTreeView(PackagePreview)
        self.treeView.setGeometry(QtCore.QRect(0, 50, 800, 401))
        self.treeView.setObjectName("treeView")
        self.treeView.setSortingEnabled(True)

        self.model = QtGui.QStandardItemModel(0,1)
        self.treeView.setModel(self.model)

        # self.treeView2 = QtWidgets.QTreeView(PackagePreview)
        # self.treeView2.setGeometry(QtCore.QRect(530, 50, 321, 381))
        # self.treeView2.setObjectName("treeView")
        # self.treeView2.setStyleSheet("text-color: green")

        # self.model = QtGui.QStandardItemModel(0,1)
        # self.treeView2.setModel(self.model)


       # self.listView = QtWidgets.QListView(PackagePreview)
       # self.listView.setEnabled(False)
       # self.listView.setGeometry(QtCore.QRect(530, 50, 321, 381))
       # self.listView.setObjectName("listView")

        self.pushButton = QtWidgets.QPushButton(PackagePreview)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)

        self.label_3 = QtWidgets.QLabel(PackagePreview)
        self.label_3.setGeometry(QtCore.QRect(300, 30, 500, 17))
        self.label_3.setObjectName("label_2")

        self.pushButton2 = QtWidgets.QPushButton(PackagePreview)
        self.pushButton2.setGeometry(QtCore.QRect(100, 0, 83, 25))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.clicked.connect(self.dissect)

        # self.label = QtWidgets.QLabel(PackagePreview)
        # self.label.setGeometry(QtCore.QRect(530, 30, 131, 17))
        # self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PackagePreview)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 101, 17))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(PackagePreview)
        QtCore.QMetaObject.connectSlotsByName(PackagePreview)

    def openFile(self):
        logging.info("Opening PCAP file")
        self.label_3.setText("Status: Opening a file...")
        self.model.removeRows(0,self.model.rowCount())
        self.name = QFileDialog.getOpenFileName()
        p = subprocess.Popen(['python', f'{os.getcwd()}/demo.py'])
        if(self.name[0] and ".pcap" in self.name[0] ):
            self.pyro_proxy.createPackets(self.name[0])
            self.pyro_proxy.savePackets()
            self.label_3.setText(" ")
            self.pyro_proxy.printPackets()
            fileToRead = open(f'{os.getcwd()}/dict.log', "r")

            # fileToRead = open(os.getcwd() + "/src/main/python/UI/MainPane/dict.log","r")
            vars = json.loads(fileToRead.read().strip())
            packetDict = vars[0]
            protocolDict = vars[1]
            for number,packet in packetDict.items():
                branch1 = sortableElement()
                branch1.setData("Packet #" + str(number),QtCore.Qt.EditRole)

                # branch1= QtGui.QStandardItem("Packet #" + str(number))
                for protocol,fields in packet.items():
                    # ProtocolToAdd = QtGui.QStandardItem("Protocol:" + protocol)
                    ProtocolToAdd = sortableElement()
                    ProtocolToAdd.setData("Protocol: " + protocol,QtCore.Qt.EditRole)
                    for name,value in fields.items():

                        # ProtocolField = QtGui.QStandardItem(name)
                        # ProtocolValue = QtGui.QStandardItem(value)

                        ProtocolField = sortableElement()
                        ProtocolField.setData(name,QtCore.Qt.EditRole)

                        ProtocolValue = sortableElement()
                        ProtocolValue.setData(value,QtCore.Qt.EditRole)

                        ProtocolToAdd.appendRow([ProtocolField,ProtocolValue])
                    branch1.appendRow(ProtocolToAdd)
                self.model.appendRow([branch1])
        p.terminate()
        logging.info("File Opened")
        self.pushButton2.setText("Dissect")


    def dissect(self):
        logging.info("Dissecting")
        p = subprocess.Popen(['python', f'{os.getcwd()}/demo.py'])
        try:
            if(self.name[0] and ".pcap" in self.name[0] ):
                self.model.removeRows(0,self.model.rowCount())
                self.pushButton2.setText("ReDissect")
                self.label_3.setText("Status: Dissecting...: ")


                self.pyro_proxy.createPackets(self.name[0])
                self.label_3.setText("")

                self.pyro_proxy.dissectPackets()
                fileToRead = open(f'{os.getcwd()}/dictColor.log', "r")

                # fileToRead = open(os.getcwd() + "/src/main/python/UI/MainPane/dictColor.log","r")
                vars = json.loads(fileToRead.read().strip())
                packetDict = vars[0]
                protocolDict = vars[1]
                colorList = vars[2]
                color = QColor(255,0,0) #red
                i=0
                j=0
                print(colorList)
                for pkt in colorList:

                    j= j+1
                for number,packet in packetDict.items():
                    # branch2= QtGui.QStandardItem("Packet # " + str(number))
                    branch2 = sortableElement()
                    branch2.setData("Packet #" + str(number),QtCore.Qt.EditRole)
                    index = int(number) -1
                    if colorList[str(index)] == "Green":
                        color = QColor(0,255,0)#green
                    elif colorList[str(index)] == "Red":
                        color = QColor(255,0,0) #red
                    else:
                        color = QColor(255,255,0) #yellow
                    for protocol,fields in packet.items():
                        # ProtocolToAdd = QtGui.QStandardItem("Protocol:" + protocol)
                        ProtocolToAdd = sortableElement()
                        ProtocolToAdd.setData("Protocol: " + protocol,QtCore.Qt.EditRole)
                        ProtocolToAdd.setData(QBrush(color), QtCore.Qt.BackgroundRole)

                        for name,value in fields.items():
                            # ProtocolField = QtGui.QStandardItem(name)
                            # ProtocolValue = QtGui.QStandardItem(value)
                            ProtocolField = sortableElement()
                            ProtocolField.setData(name,QtCore.Qt.EditRole)

                            ProtocolValue = sortableElement()
                            ProtocolValue.setData(value,QtCore.Qt.EditRole)

                            ProtocolValue.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                            ProtocolField.setData(QBrush(color), QtCore.Qt.BackgroundRole)

                            ProtocolToAdd.appendRow([ProtocolField,ProtocolValue])
                        branch2.appendRow(ProtocolToAdd)
                        branch2.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                    numberCol = QtGui.QStandardItem(str(colorList[str(index)]))
                    self.model.appendRow([branch2,numberCol])
                    numberCol.setData(QBrush(color), QtCore.Qt.BackgroundRole)
                self.label_3.setText("Status: Package has been dissected.")
        except:
                pass
        p.terminate()
        logging.info("Dissected")


    def retranslateUi(self, PackagePreview):
        _translate = QtCore.QCoreApplication.translate
        PackagePreview.setWindowTitle(_translate("PackagePreview", "PackagePreview"))
        self.pushButton.setText(_translate("PackagePreview", "File"))
        self.pushButton2.setText(_translate("PackagePreview", "Dissect"))
        # self.label.setText(_translate("PackagePreview", "Dissected Data"))
        self.label_2.setText(_translate("PackagePreview", "Packet Stream"))
        self.label_3.setText(_translate("PackagePreview", "Status: Waiting for Input"))

    def set_pyro_workspace(self,workspace,project):
        self.set_ui_workspace(workspace,project)
        self.pyro_proxy.set_workspace(workspace,project)
    def set_ui_workspace(self,workspace,project):
        path = "{}/Lua/{}.lua".format(workspace,project)
        if os.path.exists(path) is False:
            self.label_3.setText("Status: No LUA file found")
            logging.info("Lua file not found for the current project")
        else:
            self.label_3.setText("Status: Waiting for Input")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PackagePreview = QtWidgets.QWidget()
    ui = Ui_PackagePreview()
    ui.setupUi(PackagePreview)
    PackagePreview.show()
    sys.exit(app.exec_())
