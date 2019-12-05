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
        return "Done"
    
    def dissectPCAP(self,workspace,project):
        # paramPath = os.getcwd() + '/src/main/python/Backend/Lua/dissector.lua'
        # param = {"-X": 'lua_script:'  + paramPath}
        # a = open("logFIle", "w+")
        # a.write(paramPath)
        
        paramPath = '{}/Lua/{}.lua'.format(workspace,project)
        print("Loading lua script from {}".format(paramPath))
        param = {"-X": 'lua_script:'  + paramPath}
       
        self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)
        return "SUCCESSFUL"

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

    def colorFilter(self,workspace,project):
        tw = py.io.TerminalWriter()
        i = 0
        j = 0
        path = '{}/{}.pdbproj'.format(workspace,project)
      
        print("CURR PATH {}".format(path))
        with open(path) as f:
            data = json.load(f)
        if os.listdir(workspace) == []:
            self.yellowFlag = True
            for x in self.pcapFile:
                self.colorList[j] = "Yellow"
                j+=1
        for pkt in self.pcapFile:
            self.colorList[i] = ""
            theProtocols =pkt.frame_info.protocols.split(":")
            for prot in theProtocols:
                expectedVal=""
                try:
                    expectedVal = list(data.keys())[list(data.values()).index(prot)]
                except Exception as e:
                    pass
                if prot in data.values():
                    if prot==data['name']:
                        self.colorList[i] = "Green"
                        break
                    else:
                        try:
                            diff = ""
                            diff = (set(pkt[prot].field_names) ^ set(data.keys()))
                        except Exception as e:
                            pass
                        if  len(diff)-len(data.keys()) > 0:
                            self.colorList[i] = "Yellow"
                if self.colorList[i] == "":
                            self.colorList[i] = "Red"
            if (self.yellowFlag == True) or (self.colorList[i] == "Yellow"):
                tw.write("%s : %s" %( str(i+1), pkt), yellow=True, bold=True)
            elif self.colorList[i] == "Red":
                tw.write("%s : %s" %( str(i+1), pkt), red=True, bold=True)
            else:
                tw.write("%s : %s" %( str(i+1), pkt), green=True, bold=True)
            i+=1
        print("COMPLETE")