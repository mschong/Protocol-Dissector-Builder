from subprocess import call
import pyshark
import os
import py
import json
import platform
class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
        self.pcapDissectedFile=""
        # self.colorFlag = False
        self.yellowFlag = False
        self.colorList = {}
    def convertPCAP(self):
        print("Opening file with PyShark")

        # How 2 dissect using MyDNS
        # param = {"-X": 'lua_script:/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/dissector.lua'}
        # self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)

        self.pcapFile = pyshark.FileCapture(self.fileLocation)
        print("Done")

    def dissectPCAP(self,workspace,project):
        print(workspace)
        print(project)
        param = {"-X": 'lua_script: '  + '{}/Lua/{}.lua'.format(workspace,project)}
        self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)


    def savePackets(self):
        packets = {}
        protocols = {}
        fields = {}
        output = []
        try:
            os.remove(os.getcwd() + "/src/main/python/UI/MainPane/dictColor.log")
            os.remove(os.getcwd() + "/src/main/python/UI/MainPane/dict.log")
        except:
            pass

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
            # if platform.system() == 'Linux' or platform.system() == 'Windows':
            #     writeFile = open("../UI/MainPane/dictColor.log","w")
            # if platform.system() == 'Darwin':
            writeFile = open(os.getcwd() + "/src/main/python/UI/MainPane/dictColor.log","w")
            output = [packets,protocols,self.colorList]
        else:
            # if platform.system() == 'Linux' or platform.system() == 'Windows':
            #     writeFile = open("../UI/MainPane/dict.log","w")
            # if platform.system() == 'Darwin':
            writeFile = open(os.getcwd() + "/src/main/python/UI/MainPane/dict.log","w")

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
        # path = os.getcwd() + '/Lua/'
        # if platform.system() == 'Darwin':
        path = os.getcwd() + '/src/main/python/Backend/Lua/'
        with open(path + "dissector.json") as f:
            data = json.load(f)
            print(data["protocol"])
        print(data["protocol"])
        if os.listdir(path) == []:
            self.yellowFlag = True
            for x in self.pcapFile:
                self.colorList[j] = "Yellow"
                j+=1
        for pkt in self.pcapFile:
            # if self.yellowFlag == False:
            #     self.colorList[i] = "Red"
            for prot in pkt.frame_info.protocols.split(":"):
                #print(prot)
                print("prot: {}".format(prot))
                print("data[protocol]: {}".format(data['protocol']))
                print("prot==data[protocol]: {}".format(prot==data['protocol']))
                if prot=='mydns':
                    # self.colorFlag=True
                    self.colorList[i] = "Green"
                    break
                elif prot==data['protocol'] or prot=="data":
                    self.colorList[i] = "Yellow"
                else:
                    self.colorList[i] = "Red"
            if (self.yellowFlag == True) or (self.colorList[i] == "Yellow"):
                tw.write("%s : %s" %( str(i+1), pkt), yellow=True, bold=True)
            elif self.colorList[i] == "Red":
                tw.write("%s : %s" %( str(i+1), pkt), red=True, bold=True)
            else:
                tw.write("%s : %s" %( str(i+1), pkt), green=True, bold=True)
            i+=1
