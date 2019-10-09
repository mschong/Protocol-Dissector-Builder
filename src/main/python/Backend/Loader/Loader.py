import datetime
import ntpath
import sys
import xml.etree.ElementTree as ET
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
sys.path.insert(1, "../../../../")
from Project import project
from Workspace import workspace
import json


class Loader():

    workspace = None
    project_pool = []

    #WORKSAPCE FUNCTIONS

    '''
    save workspace information
    get JSON from current workspace and update json file
    '''
    def save_workspace(self):
            JSON = self.workspace.get_JSON()
            f = open("{}.json".format(self.workspace.name) ,"w+")
            f.write(json.dumps(JSON))
            f.close()
    '''
    load a workspace already created
    Receives json filename, loads into JSON object and updates the current workspace object
    returns the name of the workspace
    '''
    def loadworkspace(self, filename):
        print("[+] Opening Workspace from {}".format(filename) )
        with open(filename) as f:
            data = json.loads(f.read())
        self.workspace = workspace.Workspace(JSON=data)
        return self.workspace.JSON
    '''
    Creates a new workspace object with the given name. saves the workspace afterwards.
    '''
    def new_workspace(self,ws_name,ws_created,ws_edited):
        self.workspace = workspace.Workspace(ws_name, None)
        self.workspace.startDate = ws_created
        self.workspace.editDate = ws_edited
        self.save_workspace()

    '''
    Close a workspace
    '''
    def close_workspace(self):
        self.workspace = None
        self.project_pool = []
  
       

   
    #Project functions
    def new_project(self,p_name):
        p = project.Project(p_name)
        project_pool['p_name'] = p
        self.workspace.addProjectToWorkspace(p.get_JSON())
        self.save_project(p_name)
    

    def save_project(self,p_name):
        JSON = project_pool['p_name'].get_JSON()
        
        f = open("{}.json".format(self.p_name) ,"w+")
        f.write(json.dumps(JSON))
        f.close()

    def import_project(self,p_name):
        pass
            
    def open_project(self,p_name):
        pass


  



  
