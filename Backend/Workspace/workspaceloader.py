import sys, os, ntpath
import xml.etree.ElementTree as ET
sys.path.append('../..')
from Workspace import workspace
from Project import project
#
# The Workspace class has utility methods to load and save workspaces
#
class WorkspaceLoader:

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
            return ws
        except :
            print("[-] Unable to parse Workspace from XML")

    def loadworkspace(self, file):
        print("[+] Opening Workspace from " + file)
        ws = self.parsexmltoworkspace(file)
        print("[+] Parsing complete")
        return ws
