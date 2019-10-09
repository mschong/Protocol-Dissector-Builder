from subprocess import call
import pyshark
import os
import py

class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
        self.colorFlag = False
        self.colorList = {}
    def convertPCAP(self):
        print("Opening file with PyShark")
        try:
            varSize= os.path.getsize(self.fileLocation)
        except Exception as e:
            print(str(e))
            print("File doesnt exist! ")
            return
        if(varSize >= 50e7):
            print("File size is huge,(" + str(varSize/1e6) + " MB) want to proceed?[Y/N]")
            answer = input()
            if(not answer) or (answer.lower()[0] != 'y'):
                return
        # How 2 dissect using MyDNS
        # param = {"-X": 'lua_script:/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/dissector.lua'}
        # self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)

        self.pcapFile = pyshark.FileCapture(self.fileLocation)
        print("Done")

    def dissectPCAP(self):
        param = {"-X": 'lua_script:/root/Documents/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/dissector.lua'}
        self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)
        



    def createObjects(self):
        print("Done")

    def printPackets(self):
        i=0
        for pkt in self.pcapFile:
            print("Packet #: " + str(i))
            print(pkt.pretty_print())
            i = i+1


    def colorFilter(self):
        tw = py.io.TerminalWriter()
        i = 0
        for pkt in self.pcapFile:
            self.colorList[i] = False
            for prot in pkt.frame_info.protocols.split(":"):
                if prot=='mydns':
                    self.colorFlag=True
                    self.colorList[i] = True
                    break
            if self.colorList[i] == False:
                tw.write("%s : %s" %( str(i+1), pkt), red=True, bold=True)
            else:
                tw.write("%s : %s" %( str(i+1), pkt), green=True, bold=True)
            i+=1

