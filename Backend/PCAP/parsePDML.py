import xml.etree.ElementTree as ET
from Backend.PCAP.Packet import Packet
from Backend.PCAP.Protocol import Protocol
from Backend.PCAP.Field import Field


def makePackets(fileName): #Creates a Packet Dictionary object, where the keys are Packet objects and the values are Protocol objects. Furthermore, the Protocol Dictionary that is also returned contains the protocols as keys and a list of fields as a value.
    myFile = open(fileName, 'r')
    PacketNumber = {}
    i = 0
    # create element tree object
    tree = ET.parse(myFile)

    # get root element
    root = tree.getroot()

    # create empty list for objects
    Packets = {}
    ProtocolsList = {}
    for item in root.findall('packet'):
        TemporaryPacket = Packet(item.attrib)
        Packets[TemporaryPacket] = None
        PacketNumber[i]= TemporaryPacket
        Protocols = {}
        for child in item:
            TemporaryProtocol = Protocol(child.attrib)
            FieldValues = []
            for fields in child.findall('field'):
                FieldValues.append(Field(fields.attrib))
            Protocols[TemporaryProtocol] = FieldValues
            ProtocolsList[TemporaryProtocol] = FieldValues
        Packets[TemporaryPacket] = Protocols
        i +=1
    ListMe = [PacketNumber,Packets,ProtocolsList]
    return ListMe



def printPackets(Packets,Protocols): #Prints the resulting packet/protocol/field name.
    for key,value in Packets.items():
        print("Packet:")
        print("----Protocol: \n")
        for i in Protocols[value]:
            for ProtocolKeys,ProtocolValues in i:
                    print("--------" + ProtocolKeys + "-----------" + ProtocolValues + "\n")

if __name__ == '__main__':
    tester = makePackets("pcapTest.pdml")
    printPackets(tester[0],tester[1])
