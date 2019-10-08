from subprocess import call
import pyshark
import os
import py

class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
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
        flag= False
        for pkt in self.pcapFile:
            for prot in pkt.frame_info.protocols.split(":"):
                if prot=='mydns':
                    flag=True
            for prot in pkt:
                if flag:
                    tw.write("%s" % prot, green=True, bold=True )
                else:
                    tw.write("%s" % prot, red=True, bold=True )
