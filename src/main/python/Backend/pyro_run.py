import Pyro4
import logging
import sys, traceback
import time
import os
import asyncio
from PCAP.PCAP import PCap
from subprocess import Popen,PIPE
import pexpect
import subprocess
from Workspace.workspaceloader import WorkspaceLoader


@Pyro4.expose
class Pyro_Run():
    def __init__(self):
        self.workspace_loader = WorkspaceLoader()

    def parse_XML_to_workspace(self,file):
        self.workspace_loader.parsexmltoworkspace(file)

    def load_workspace(self, file):
        return self.workspace_loader.loadworkspace(file)

    def load_empty_worspace(self):
        return self.workspace_loader.runWithUnsavedWorkspace()

    def get_workspace_pool_count(self):
        return self.workspace_loader.get_workspace_pool_count()

    def get_workspace_data_from_pool(self, wsname):
        return self.workspace_loader.get_workspace_data_from_pool(wsname)
    def update_workspace_name(self, ws_currentname, ws_newname):
        self.workspace_loader.update_workspace(ws_currentname, ws_newname)

    def createPackets(self,fileName):
        self.child = pexpect.spawn("python3.6 PCAP/PCAPServices.py",encoding='utf-8')
        self.child.expect("loop",timeout=None)
        print("Creating")
        self.child.sendline("create " + fileName)
        self.child.expect("Done",timeout=None)

    def savePackets(self):
        print("saving")
        self.child.sendline("save")
        self.child.expect("saved",timeout=None)

    def dissectPackets(self):
        print("dissecting")
        self.child.sendline("dissect")
        self.child.expect("dissected")

    def colorCode(self):
        print("Coloring")
        self.child.sendline("colorcode")
        self.child.expect("colored")

    def printPackets(self):
        self.child.sendline("print")
        print(self.child.read())


def main():
    daemon = Pyro4.Daemon()

    Popen("pyro4-ns")
    ns = Pyro4.locateNS()
    uri = daemon.register(Pyro_Run)
    ns.register("pyro.service",uri)
    print("[+] Pyro4 URI: " + str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    main()
