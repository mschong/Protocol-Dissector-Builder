import Pyro4
import logging
import sys, traceback
import time
import os
from subprocess import Popen
from Project.project import Project
from Workspace.workspace import Workspace
from Workspace.workspaceloader import WorkspaceLoader


@Pyro4.expose
class Pyro_Run():
    def __init__(self):
        self.project = Project()
        self.workspace = Workspace()
        self.workspace_loader = WorkspaceLoader()
    
    def open_project(self,filename):
        self.project.open_project(filename)

    def save_project(self,filename,file_contents=None):
        self.project.save_project(filename)
    
    def save_workspace(self,file,projects):
        self.workspace_loader.saveworkspace(file,projects)

    def parse_XML_to_workspace(self,file):
        self.workspace_loader.parsexmltoworkspace(file)

    def load_workspace(self,file):
        self.workspace_loader.loadworkspace(file)


def main():
    daemon = Pyro4.Daemon()
    
    Popen("pyro4-ns")
    time.sleep(8)
    
    ns = Pyro4.locateNS()
    uri = daemon.register(Pyro_Run)
    ns.register("pyro.service",uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()