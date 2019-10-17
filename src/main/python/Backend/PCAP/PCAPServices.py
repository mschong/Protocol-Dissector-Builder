import PCAP
import sys

global PCAPFile
while(1):
    print("loop")
    currCommand = input().split(" ")
    if currCommand[0] == "create":
        PCAPFile = PCAP.PCap("dns_port.pcap")
        PCAPFile.convertPCAP()
    elif currCommand[0] =="print":
        print("Printing")
        PCAPFile.printPackets()
        print("Success!")
        sys.exit()
    elif currCommand[0] == "save":
        PCAPFile.savePackets()
        print("saved")
    elif currCommand[0] == "dissect":
        PCAPFile.dissectPCAP()
        PCAPFile.colorFilter()
    elif currCommand[0] == "debug":
        print(currCommand)
    else:
        pass
    currCommand = ""
