from subprocess import call
import pyshark
import os

class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
    def convertPCAP(self):
        print("Opening file with PyShark")
        try:
            varSize= os.path.getsize(self.fileLocation)
        except:
            print("File doesnt exist! ")
            return
        if(varSize >= 50e7):
            print("File size is huge,(" + str(varSize/1e6) + " MB) want to proceed?[Y/N]")
            answer = input()
            if(not answer) or (answer.lower()[0] != 'y'):
                return
        self.pcapFile = pyshark.FileCapture(self.fileLocation)
        print("Done")

    def createObjects(self):
        print("Done")

    def printPackets(self):
        i=0
        for pkt in self.pcapFile:
            print("Packet #: " + str(i))
            print(pkt.pretty_print())
            i = i+1
