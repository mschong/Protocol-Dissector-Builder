import Pyro4
import logging
import sys, traceback
import time
import os
from subprocess import Popen
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

def main():
    daemon = Pyro4.Daemon()
    
    Popen("pyro4-ns")
    time.sleep(8)
    ns = Pyro4.locateNS()
    uri = daemon.register(Pyro_Run)
    ns.register("pyro.service",uri)
    print("[+] Pyro4 URI: " + str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    main()