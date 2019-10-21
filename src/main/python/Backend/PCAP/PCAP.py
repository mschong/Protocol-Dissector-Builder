from subprocess import call
import pyshark
import os
import py
import json
class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
        self.pcapDissectedFile=""
        self.colorFlag = False
        self.yellowFlag = False
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
        param = {"-X": 'lua_script:/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/dissector.lua'}
        self.pcapDissectedFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)


    def savePackets(self):
        packets = {}
        protocols = {}
        fields = {}
        output = []
        for pkt in self.pcapFile:
            number = pkt.frame_info.get_field_value("number")
            protocols = {}
            for protocol in (pkt.frame_info.protocols).split(":"):
                fields = {}
                try:
                    for val in pkt[protocol].field_names:
                        fields[val] = pkt[protocol].get_field_value(val)
                except:
                    pass
                protocols[protocol] = fields
            packets[number] = protocols
        if self.colorList:
            writeFile = open("../UI/PacketPreview/dictColor.log","w")
            output = [packets,protocols,self.colorList]
        else:
            writeFile = open("../UI/PacketPreview/dict.log","w")
            output = [packets,protocols]
        json.dump(output,writeFile)
        writeFile.close()

    def printPackets(self):
        i=0
        for pkt in self.pcapFile:
            print("Packet #: " + str(i))
            print(pkt.pretty_print())
            i = i+1

    def colorFilter(self):
        tw = py.io.TerminalWriter()
        i = 0
        j = 0
        if os.listdir('/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/Lua/') == []:
            self.yellowFlag = True
            for x in self.pcapDissectedFile:
                self.colorList[j] = "Yellow"
                j+=1
        for pkt in self.pcapDissectedFile:
            if self.yellowFlag == False:
                self.colorList[i] = "Red"
            for prot in pkt.frame_info.protocols.split(":"):
                if prot=='mydns' and self.yellowFlag == False:
                    self.colorFlag=True
                    self.colorList[i] = "Green"
                    break
            if self.yellowFlag == True:
                tw.write("%s : %s" %( str(i+1), pkt), yellow=True, bold=True)
            elif self.colorFlag == False:
                tw.write("%s : %s" %( str(i+1), pkt), red=True, bold=True)
            else:
                tw.write("%s : %s" %( str(i+1), pkt), green=True, bold=True)
            i+=1
