import datetime
import ntpath
import sys
import xml.etree.ElementTree as ET
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
sys.path.insert(1, "../../../../")
from Project import project
from Workspace import workspace

#
# The Workspace class has utility methods to load and save workspaces
#
class Loader():

    workspace_pool = []
    project_pool = []

    def save_workspace(self, file, projects):
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
            ws.startDate = root.get("startdate")
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
        ws.startDate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        ws.editDate = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.appendToWorkspacePool(ws)
        print("[+] Created generic untitled workspace")
        return ws.name

    def get_workspace_pool_count(self):
        return len(self.workspace_pool)

    def print_workspace_pool(self):
        print(self.workspace_pool)

    def find_workspace(self, wsname):
        if (wsname == None or wsname == ""):
            errormsg = "Can't retrieve Workspace from pool because wsname is None or Empty"
            print ("[-] " + errormsg)
            raise Exception(errormsg)
        result = None
        for workspace in self.workspace_pool:
            if wsname == workspace.name:
                result = workspace
                break
        return result

    def get_workspace_data_from_pool(self, wsname):
        if (wsname == None or wsname == ""):
            errormsg = "Can't retrieve Workspace from pool because wsname is None or Empty"
            print ("[-] " + errormsg)
            raise Exception(errormsg)
        workspace = self.find_workspace(wsname)
        result = None
        if workspace != None:
            result = []
            result.append(workspace.name)
            result.append(workspace.startDate)
            result.append(workspace.editDate)
        return result

    def update_workspace(self, ws_currentname, ws_newname):
        if ws_currentname == None or ws_currentname == "":
            errormsg = "Unable to update Workpace, please provide a valid workspace name"
            print("[-] " + errormsg)
            raise Exception (errormsg)
        if ws_newname == None or ws_newname == None:
            errormsg = "Unable to update Workpace, please provide a valid NEW workspace name"
            print("[-] " + errormsg)
            raise Exception(errormsg)
        workspace = self.find_workspace(ws_currentname)
        workspace.name = ws_newname
        # TODO: write changes to disk