
from PCAP import PCap
import PCAP
import pytest

def test_open_file():
    print("test_open_file")
    pcap = PCap("/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/test150.pcap")
    assert pcap.convertPCAP() == "Done"

def test_open_invalidFile():
    print("testing invalid file")
    pcap2 = PCap("/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/test10.pcap")
    assert pcap2.convertPCAP is not "DONE"

def test_dissect():
    print("test_dissect")
    pcap = PCap("/root/Desktop/Protocol-Dissector-Builder/src/main/python/Backend/PCAP/test150.pcap")
    assert pcap.dissectPCAP("workspace", "project") == "SUCCESSFUL"