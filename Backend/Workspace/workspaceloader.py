import sys, os, ntpath
import xml.etree.ElementTree as ET
sys.path.append('../..')
from Workspace import workspace
from Project import project
#
# The Workspace class has utility methods to load and save workspaces
#
class WorkspaceLoader():

    workspace_pool = []

    def saveworkspace(self, file, projects):
        name = ntpath.basename(file)
        if name is None or name == "":
            print("[-] The name of the workspace cannot be empty")
            exit(1)
        print("[+] Creating Workspace " + name)
        xml = "<?xml version=\"1.0\"?>"
        if projects is not None and len(projects) > 0:
            for prj in projects:
                xml += "<project name=\"" + prj.name + "\">"
                ## TODO: missing project attributes implementation
                xml += "</project>"
        xml += "<workspace name=\"" + name + "\"></workspace>"
        try:
            with open(file, "w") as text_file:
                text_file.write(xml)
        except:
            print("[-] Unable to create file")

    def parsexmltoworkspace(self, file):
        print("[+] Parsing Workspace from " + file)
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            wsname = root.get("name")
            projects = []
            for prj in root.findall("project"):
                p = project.Project(prj.get("name"))
                # TODO:missing implementation to parse the attributes of each project xml
                #  like bytes, multi bytes, etc
                projects.append(p)
                print("[+] Parsed Project " + p.name + " from Workspace")
            ws = workspace.Workspace(wsname, projects)
            ws.startdate = root.get("startdate")
            ws.editDate = root.get("editdate")
            print("[+] Parsing complete")
            return ws
        except :
            print("[-] Unable to parse Workspace from XML")

    def loadworkspace(self, file):
        print("[+] Opening Workspace from " + file)
        ws = self.parsexmltoworkspace(file)
        try:
            self.appendToWorkspacePool(ws)
            return ws.name
        except Exception as ex:
            raise ex

    def appendToWorkspacePool(self, wspace):
        if wspace is None or type(wspace) != workspace.Workspace:
            errormsg = "Invalid object type for workspace"
            print("[-] " + errormsg)
            raise Exception(errormsg)
        for ws in self.workspace_pool:
            if wspace.name == ws.name:
                errormsg = "Workspace " + wspace.name + " already loaded"
                print("[-] " + errormsg)
                raise Exception(errormsg)
        self.workspace_pool.append(wspace)
        print("[+] Workspace " + wspace.name + " added to Workspace pool")

    def runWithUnsavedWorkspace(self):
        ws = workspace.Workspace("untitled", None)
        self.appendToWorkspacePool(ws)
        print("[+] Created generic untitled workspace")
        return ws.name
