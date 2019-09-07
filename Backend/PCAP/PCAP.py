from subprocess import call

class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation

    def convertPCAP(self):
        fileName = self.obtainFilePath()
        print("Converting")
        print("Arguments: tshark -r "+ self.fileLocation + " -T pdml > " + fileName)
        call("tshark -r "+ self.fileLocation + " -T pdml > " + fileName,shell=True)
        print("Done")

    def obtainFilePath(self):
        filePath = self.fileLocation.split("/")
        fileName = filePath[-1]
        del filePath[-1]
        fileExt = fileName.split(".")
        fileName = fileExt[0] + ".pdml"
        filePath.append(fileName)
        return '/'.join(filePath)
