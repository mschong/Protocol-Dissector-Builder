import sys
import xml.etree.ElementTree as ET
sys.path.append('../..')
from Backend.Workspace import workspace
from Backend.Project import project
#
# The Workspace class has utility methods to load and save workspaces
#
class WorkspaceLoader:

    def saveworkspace(self, name, path, projects):
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
            with open(name + ".txt", "w") as text_file:
                text_file.write(xml)
        except:
            print("[-] Unable to create file")

    def parsexmltoworkspace(self, name, path):
        print("[+] Parsing Workspace")
        try:
            tree = ET.parse(path + "/" + name)
            root = tree.getroot()
            wsname = root.get("name")
            projects = []
            for prj in root.findall("project"):
                p = project.Project(prj.get("name"))
                # TODO:missing implementation to parse the attributes of each project xml
                #  like bytes, multi bytes, etc
                projects.append(p)
            ws = workspace.Workspace(wsname, projects)
            return ws
        except :
            print("[-] Unable to parse Workspace from XML")
            print("[-] Exiting now")
        exit(1)

    def loadworkspace(self, name, path):
        print("[+] Loading Workspace from " + path + "/" + name)
        ws = self.parsexmltoworkspace(name, path)
        return ws
