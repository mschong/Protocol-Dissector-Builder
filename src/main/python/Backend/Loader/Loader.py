import datetime
import ntpath
import sys
import xml.etree.ElementTree as ET
sys.path.insert(1,"./")
sys.path.insert(1,"../../")
sys.path.insert(1,"../../../")
sys.path.insert(1,"../../../../")
from Project import project
from Workspace import workspace
#from ..UI.DBA_FrontEnd import DBA
import json


class Loader():

    workspace = None

    def __init__(self):
        print("sys.path: ", sys.path)
        self.workspace = workspace.Workspace()


    #WORKSAPCE FUNCTIONS

    '''
    save workspace information
    get JSON from current workspace and update json file
    '''
    def save_workspace(self):
            JSON = self.workspace.get_JSON()
            
            print(JSON)
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
        self.project_pool = self.workspace.JSON['projects']
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
        self.project_pool = {}
  
       

   
    #Project functions
    def new_project(self,p_name,p_author,p_desc,p_created,p_edited,):
        
        p = project.Project(p_name)
        p.description = p_desc
        p.dateCreated = p_created
        p.editDate =p_edited
        p.author = p_author
        self.workspace.addProjectToWorkspace(p.get_JSON())
        self.save_project(p_name)
    

    def save_project(self,p_name):
       
        JSON = self.workspace.projects
        print(JSON)
        for project in JSON:
            print(project)
            if JSON[project]['name'] == p_name:
                JSON = JSON[project]
         
       
        f = open("{}.json".format(p_name) ,"w+")
        f.write(json.dumps(JSON))
        f.close()
        self.save_workspace()

    def import_project(self,filename):
        
     
        with open(filename) as f:
            data = json.loads(f.read())
     
        p = project.Project(JSON = data)
      
        self.workspace.addProjectToWorkspace(p.get_JSON())
        self.save_project(p.name)

            
    def open_project(self,p_name):
        pass

    def get_dissector(self):
        dissector = DBA.Ui_Form()
        json_string = dissector.save_button_clicked()
        f = open("{}.json".format("dissector"), "w+")
        f.write(json_string)
        f.close()

  



  
