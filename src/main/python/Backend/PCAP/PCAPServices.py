import PCAP
import sys
global PCAPFile
try:
    while(1):
        print("loop")
        currCommand = input().split(" ")
        if currCommand[0] == "create":
            PCAPFile = PCAP.PCap(currCommand[1])
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
            PCAPFile.dissectPCAP(currCommand[1],currCommand[2])
            PCAPFile.colorFilter(currCommand[1],currCommand[2])
            PCAPFile.savePackets()
            print("dissected")
            sys.exit()
        elif currCommand[0] == "colorcode":
            #PCAPFile.colorFilter()
            print("colored")
        elif currCommand[0] == "debug":
            print(currCommand)
        else:
            pass
        currCommand = ""
except Exception as e:
    writeMe = open("errorFile","w+")
    writeMe.write(str(e))